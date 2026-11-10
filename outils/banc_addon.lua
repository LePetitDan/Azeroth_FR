-- ============================================================================
-- Banc d'essai HORS JEU de l'add-on Azeroth_FR (Lua 5.1, comme le client 3.3.5).
-- Usage : lua5.1 outils/banc_addon.lua <dossier dist/Interface> <fichier de cas>
-- (lance par outils/tester_addon.py, qui choisit les cas dans textes/).
--
-- De fausses fonctions WoW, minimales : cadres, zones de texte (avec une hauteur qui depend de
-- la largeur, pour le suivi des objectifs), crochets, infobulles (objets, unites, sorts, auras,
-- barre d'action, grimoire), unites, filtres de discussion, journal des quetes, cadres d'unite,
-- minicarte, LoadAddOn (lit le .toc et charge ses fichiers). Le coeur et les modules sont
-- charges tels quels, puis chaque cas est verifie. Les fonctions du jeu que l'add-on accroche
-- (WatchFrame_SetLine, UnitFrame_Update…) imitent ce que fait le client de CoA.
-- ============================================================================
local RACINE, CAS = arg[1], arg[2]
local resultats = { ok = 0, ko = 0, exemples = 0 }
local function noter(ok, nom, detail)
    if ok then resultats.ok = resultats.ok + 1 else resultats.ko = resultats.ko + 1 end
    print((ok and "OK  " or "KO  ") .. nom .. (detail and ("  " .. detail) or ""))
end

-- ----------------------------------------------------------------------------
-- Faux environnement WoW
-- ----------------------------------------------------------------------------
function debugprofilestop() return os.clock() * 1000 end
EN_COMBAT = false
function InCombatLockdown() return EN_COMBAT end
function GetTime() return os.clock() end
date = os.date
function debugstack(debut, n1, n2) return "Interface\\FrameXML\\Banc.lua:1: in function <Banc>\n[C]: ?\n" end
function GetLocale() return "enUS" end
function strtrim(s) return (string.match(s, "^%s*(.-)%s*$")) end

JOUEUR = { nom = "Thalwyn", race = "Night Elf", classe = "Warrior", sexe = 2 }
UNITES = {}
-- (les unites du jeu ne tiennent pas compte de la casse : UnitName("NPC") = UnitName("npc"))
function UnitName(u) u = u and string.lower(u); if u == "player" then return JOUEUR.nom end return UNITES[u] and UNITES[u].nom end
function GetUnitName(u) return UnitName(u) end
function UnitRace(u) return JOUEUR.race end
function UnitClass(u) return JOUEUR.classe end
function UnitSex(u) return JOUEUR.sexe end
function UnitIsPlayer(u) u = u and string.lower(u); return u == "player" or (UNITES[u] and UNITES[u].joueur) or false end
function UnitExists(u) u = u and string.lower(u); return u == "player" or UNITES[u] ~= nil end
function UnitGUID(u) u = u and string.lower(u); return UNITES[u] and UNITES[u].guid end

OBJETS_BANC, ITEM_SPELLS, ACTIONS, GRIMOIRE, AURAS = {}, {}, {}, {}, {}
local function LienObjet(id, nom) return "|cffffffff|Hitem:" .. id .. ":0:0:0:0:0:0:0:0|h[" .. nom .. "]|h|r" end
function GetItemInfo(x)
    for id, o in pairs(OBJETS_BANC) do
        if x == id or x == o.nom then return o.nom, LienObjet(id, o.nom) end
    end
    return nil
end
function GetItemSpell(id)
    local s = ITEM_SPELLS[id]
    if s then return s[1], s[2] end
end
function GetActionInfo(case)
    local a = ACTIONS[case]
    if a then return "spell", 3, "spell", a.id end
end
function GetSpellLink(case, livre)
    if type(case) == "string" then
        local id = SORTS_PAR_NOM[case]
        if id then return "|cff71d5ff|Hspell:" .. id .. "|h[" .. case .. "]|h|r" end
        return nil
    end
    local g = GRIMOIRE[case]
    if g then return "|cff71d5ff|Hspell:" .. g.id .. "|h[" .. g.nom .. "]|h|r" end
end
function UnitAura(unite, index, filtre)
    local a = AURAS[index]
    if a then return a.nom, "", "icone", 0, nil, 0, 0, "player", nil, nil, a.id end
end

-- Zones de texte : la hauteur suit le nombre de lignes (6,5 px par caractere, 13 px par ligne).
local function Longueur(t)
    t = string.gsub(t or "", "|c%x%x%x%x%x%x%x%x", "")
    t = string.gsub(t, "|r", "")
    return #(string.gsub(t, "[\128-\191]", ""))
end
local function NouvelleZone(texte)
    local z = { texte = texte, visible = true, hauteur = 0 }
    function z:GetText() return self.texte end
    function z:SetText(t) self.texte = t end
    function z:IsShown() return self.visible end
    function z:IsVisible() return self.visible end
    function z:Show() self.visible = true end
    function z:Hide() self.visible = false end
    function z:GetObjectType() return "FontString" end
    function z:SetWidth(w) self.largeur = w end
    function z:GetWidth() return self.largeur or Longueur(self.texte) * 6.5 end
    function z:SetHeight(h) self.hauteur = h or 0 end
    function z:GetHeight()
        if self.hauteur and self.hauteur > 0 then return self.hauteur end
        local n = 1
        if self.largeur and self.largeur > 0 then n = math.max(1, math.ceil(Longueur(self.texte) * 6.5 / self.largeur)) end
        return n * 13
    end
    function z:GetTextHeight() return 12 end
    function z:GetStringWidth() return Longueur(self.texte) * 6.5 end
    function z:SetTextColor() end
    function z:SetFontFlags() end
    function z:SetFontObject() end
    function z:ClearAndSetPoint() end
    function z:SetPoint() end
    function z:ClearAllPoints() end
    function z:SetAlphaGradient() end
    function z:GetParent() return self.parent end
    return z
end

local evenements = {}       -- evenement -> liste de cadres
TOUS_CADRES = {}
local function NouveauCadre(nom)
    local c = { scripts = {}, crochets = {}, visible = false, regions = {}, enfants = {}, hauteur = 16 }
    table.insert(TOUS_CADRES, c)
    function c:RegisterEvent(e)
        evenements[e] = evenements[e] or {}
        for _, x in ipairs(evenements[e]) do if x == self then return end end
        table.insert(evenements[e], self)
    end
    function c:UnregisterEvent(e)
        for i, x in ipairs(evenements[e] or {}) do if x == self then table.remove(evenements[e], i); return end end
    end
    function c:IsEventRegistered(e)
        for _, x in ipairs(evenements[e] or {}) do if x == self then return true end end
        return false
    end
    function c:UnregisterAllEvents() end
    function c:SetScript(k, f) self.scripts[k] = f end
    function c:GetScript(k) return self.scripts[k] end
    function c:HookScript(k, f) self.crochets[k] = self.crochets[k] or {}; table.insert(self.crochets[k], f) end
    function c:IsShown() return self.visible end
    function c:IsVisible() return self.visible end
    function c:Show() self.visible = true end
    function c:Hide() self.visible = false end
    function c:IsProtected() return self.protege or false end
    function c:GetFontString() return self.fs end
    function c:GetRegions() return unpack(self.regions) end
    function c:GetChildren() return unpack(self.enfants) end
    function c:GetName() return nom end
    function c:GetNumChildren() return #self.enfants end
    function c:SetHeight(h)
        if EN_COMBAT and SUIVI_GARDE then SUIVI_GARDE.hauteurs_en_combat = SUIVI_GARDE.hauteurs_en_combat + 1 end
        self.hauteur = h
    end
    function c:IsMouseEnabled() return self.souris or false end
    function c:GetHeight() return self.hauteur end
    function c:SetPoint() end
    function c:ClearAllPoints() end
    function c:SetOwner(o) self.proprio = o end
    function c:IsOwned(o) return self.proprio == o end
    -- 0.9.6 : panneau d'options (cases a cocher, textes, logo)
    if not c.SetWidth then function c:SetWidth(w) self.largeur = w end end
    function c:CreateFontString()
        local z = NouvelleZone(nil)
        if not z.SetJustifyH then function z:SetJustifyH() end end
        return z
    end
    function c:CreateTexture()
        local t = {}
        function t:SetTexture(x) self.chemin = x end
        function t:SetWidth() end
        function t:SetHeight() end
        function t:SetPoint() end
        return t
    end
    function c:SetNormalTexture() end
    function c:SetPushedTexture() end
    function c:SetHighlightTexture() end
    function c:SetCheckedTexture() end
    function c:SetDisabledCheckedTexture() end
    function c:SetChecked(v) self.coche = (v and v ~= 0) and true or false end
    function c:GetChecked() return self.coche and 1 or nil end
    function c:Enable() self.desactive = false end
    function c:Disable() self.desactive = true end
    function c:Click()
        if self.desactive then return end
        self.coche = not self.coche
        if self.scripts.OnClick then self.scripts.OnClick(self) end
    end
    -- 1.0.1 : zone de saisie (lien « Soutenir le createur ») ; on ne remplace pas une methode deja simulee
    for _, m in ipairs({ "SetAutoFocus", "SetFontObject", "SetBackdrop", "SetBackdropColor", "SetBackdropBorderColor",
                         "SetTextInsets", "HighlightText", "ClearFocus", "SetMultiLine", "SetFocus", "SetFrameStrata",
                         "EnableMouse", "SetNormalFontObject", "SetHighlightFontObject", "SetJustifyH" }) do
        if not c[m] then c[m] = function() end end
    end
    if not c.SetText then
        function c:SetText(v)
            self.texte = v
            if self.scripts and self.scripts.OnTextChanged then self.scripts.OnTextChanged(self) end
        end
        function c:GetText() return self.texte end
    end
    if nom then _G[nom] = c end
    return c
end
-- 0.9.6 : menu Interface du jeu (onglet AddOns)
PANNEAUX_OPTIONS = {}
function InterfaceOptions_AddCategory(p) table.insert(PANNEAUX_OPTIONS, p) end
function InterfaceOptionsFrame_OpenToCategory(p) PANNEAU_OUVERT = p end

-- Infobulles
local function NouvelleBulle(nom)
    local b = NouveauCadre(nom)
    b.lignes = {}
    function b:Effacer(lignes, objet, unite, sort, droites)
        self.lignes = {}
        for i = 1, 30 do _G[nom .. "TextLeft" .. i] = nil; _G[nom .. "TextRight" .. i] = nil end
        for i, t in ipairs(lignes) do
            local z = NouvelleZone(t)
            _G[nom .. "TextLeft" .. i] = z
            self.lignes[i] = z
            local d = NouvelleZone((droites and droites[i]) or "")
            if not (droites and droites[i]) then d.visible = false end
            _G[nom .. "TextRight" .. i] = d
        end
        self.objet, self.unite, self.sort = objet, unite, sort
        self.visible = true
    end
    function b:NumLines() return #self.lignes end
    function b:GetItem() if self.objet then return self.objet[1], self.objet[2] end end
    function b:GetUnit() if self.unite then return UNITES[self.unite].nom, self.unite end end
    function b:GetSpell() if self.sort then return self.sort[1], self.sort[2], self.sort[3] end end
    function b:Declencher(script) for _, f in ipairs(self.crochets[script] or {}) do f(self) end end
    function b:AddLine(t) local i = #self.lignes + 1; local z = NouvelleZone(t); _G[nom .. "TextLeft" .. i] = z; self.lignes[i] = z end
    function b:SetHyperlink(lien)
        local id = tonumber(string.match(lien, "item:(%d+)"))
        local o = id and OBJETS_BANC[id]
        if o then
            self:Effacer(o.lignes, { o.nom, LienObjet(id, o.nom) }, nil, nil, o.droites)
            self:Declencher("OnTooltipSetItem")
        else self:Effacer({}) end
    end
    -- GameTooltip_OnLoad du client CoA accroche OnTooltipSetItem AVANT tout add-on
    b:HookScript("OnTooltipSetItem", function(self) GameTooltip_ItemVersionReplacer(self) end)
    local function DepuisSort(self, s)
        if s then
            self:Effacer(s.lignes, nil, nil, { s.nom, s.rang or "", s.id }, s.droites)
            self:Declencher("OnTooltipSetSpell")
        end
    end
    function b:SetAction(case) DepuisSort(self, ACTIONS[case]) end
    function b:SetSpell(case, livre) DepuisSort(self, GRIMOIRE[case]) end
    function b:SetUnitAura(unite, index, filtre)        -- comme le jeu : pas de GetSpell sur une aura
        local a = AURAS[index]
        if a then self:Effacer(a.lignes) end
    end
    function b:SetUnitBuff(unite, index) self:SetUnitAura(unite, index, "HELPFUL") end
    function b:SetUnitDebuff(unite, index) self:SetUnitAura(unite, index, "HARMFUL") end
    return b
end
-- Copie de GameTooltip_ItemVersionReplacer du client CoA (patch-B, Interface\FrameXML\GameTooltip.lua) :
-- la ligne « "@X@reste" » devient « "reste" » (ou vide), X remplace la ligne qui commence par ITEM_HEROIC.
function GameTooltip_ItemVersionReplacer(tooltip)
    local numLines = tooltip:NumLines()
    local name = tooltip:GetName()
    if not name or numLines < 2 then return end
    local version, replaceLocation
    for i = numLines, 1, -1 do
        local line = _G[name .. "TextLeft" .. i]
        local text = line and line:GetText()
        if text and string.len(text) > 0 then
            if string.sub(text, 1, 2) == "\"@" then
                local desc
                version, desc = string.match(text, "@(.+)@(.-)\"")
                desc = desc and string.len(desc) > 0 and "\"" .. desc .. "\"" or ""
                line:SetText(desc)
            elseif string.sub(text, 1, string.len(ITEM_HEROIC or "Heroic")) == (ITEM_HEROIC or "Heroic") then
                replaceLocation = i
            end
        end
    end
    if version and replaceLocation then _G[name .. "TextLeft" .. replaceLocation]:SetText(version) end
end
GameTooltip = NouvelleBulle("GameTooltip")
ItemRefTooltip = NouvelleBulle("ItemRefTooltip")
UIParent = NouveauCadre("UIParent")
function CreateFrame(genre, nom, parent, modele)
    if genre == "GameTooltip" then return NouvelleBulle(nom) end
    return NouveauCadre(nom)
end

-- Comme le jeu : chaque cadre inscrit recoit l'evenement (dans l'ordre d'inscription) ; son script, puis
-- les crochets HookScript("OnEvent").
function Declencher(e, ...)
    local liste = {}
    for i, c in ipairs(evenements[e] or {}) do liste[i] = c end
    for _, c in ipairs(liste) do
        if c.scripts.OnEvent then c.scripts.OnEvent(c, e, ...) end
        for _, f in ipairs(c.crochets.OnEvent or {}) do f(c, e, ...) end
    end
end
-- n images de dt secondes : OnUpdate de chaque cadre visible
function Images(n, dt)
    for _ = 1, n do
        for _, c in ipairs(TOUS_CADRES) do
            if c.visible and c.scripts.OnUpdate then c.scripts.OnUpdate(c, dt) end
        end
    end
end

-- hooksecurefunc : fonction globale ou methode d'un objet ; le crochet passe APRES.
function hooksecurefunc(a, b, c)
    local obj, nom, fn = _G, a, b
    if type(a) == "table" then obj, nom, fn = a, b, c end
    local orig = obj[nom]
    obj[nom] = function(...)
        local r = { orig(...) }
        fn(...)
        return unpack(r)
    end
end

-- Discussion
local filtres = {}
function ChatFrame_AddMessageEventFilter(e, f) filtres[e] = filtres[e] or {}; table.insert(filtres[e], f) end
local messages = {}
DEFAULT_CHAT_FRAME = { AddMessage = function(self, t) table.insert(messages, t) end }
SlashCmdList = {}

-- Fenetres du jeu utilisees par les modules (versions minimales)
GossipGreetingText = NouvelleZone(nil)
GossipTitleButton1 = NouvelleZone(nil)
GossipTitleButton2 = NouvelleZone(nil)
GossipFrameNpcNameText = NouvelleZone(nil)
function GossipFrameUpdate() GossipFrameNpcNameText:SetText(UnitName("npc")) end
function GossipResize(b) end
QuestFrame = NouveauCadre("QuestFrame")
QuestFrameNpcNameText = NouvelleZone(nil)
for _, n in ipairs({ "QuestInfoTitleHeader", "QuestInfoDescriptionText", "QuestInfoObjectivesText",
    "QuestInfoRewardText", "QuestProgressTitleText", "QuestProgressText", "QuestInfoObjective1",
    "QuestInfoObjective2" }) do _G[n] = NouvelleZone(nil) end
QuestInfoFrame = { questLog = false }
function QuestInfo_Display() end
JOURNAL, JOURNAL_SELECTION = {}, 0
function GetNumQuestLogEntries() return #JOURNAL end
function GetQuestLogTitle(i)
    local q = JOURNAL[i]
    if q then return q.titre, 1, nil, nil, q.entete, nil, nil, nil, q.id end
end
function GetQuestLink(i) local q = JOURNAL[i]; if q and q.id then return "|Hquest:" .. q.id .. ":1|h[" .. q.titre .. "]|h" end end
function GetQuestLogSelection() return JOURNAL_SELECTION end
function ItemTextGetText() return ITEM_TEXT end
ItemTextPageText = NouvelleZone(nil)

-- Suivi des objectifs : imite WatchFrame_SetLine du client de CoA (hauteur fixee d'apres le texte).
WATCHFRAME_LINEHEIGHT, WATCHFRAME_MULTIPLE_LINEHEIGHT, WATCHFRAME_MAXLINEWIDTH = 16, 29, 192
WATCHFRAME_QUESTLINES = {}
local function NouvelleLigneSuivi(i)
    local l = NouveauCadre("WatchFrameLine" .. i)
    l.text, l.dash = NouvelleZone(""), NouvelleZone("")
    function l:Reset() self.hauteur = WATCHFRAME_LINEHEIGHT; self.text:SetHeight(0); self.text:SetText("") end
    return l
end
WatchFrameLine1, WatchFrameLine2 = NouvelleLigneSuivi(1), NouvelleLigneSuivi(2)
function WatchFrame_SetLine(line, anchor, verticalOffset, isHeader, text, dash, hasItem, isComplete)
    local garde = SUIVI_GARDE; SUIVI_GARDE = nil          -- (les hauteurs posees par le JEU ne comptent pas)
    WatchFrame_SetLine_Jeu(line, text, dash, isComplete)
    SUIVI_GARDE = garde
end
function WatchFrame_SetLine_Jeu(line, text, dash, isComplete)
    line.text:SetText(text)
    line.text:SetWidth(WATCHFRAME_MAXLINEWIDTH - (dash == 1 and 12 or 0))
    if line.text:GetHeight() > WATCHFRAME_LINEHEIGHT then
        if isComplete then line:SetHeight(line.text:GetHeight() + 4)
        else line:SetHeight(WATCHFRAME_MULTIPLE_LINEHEIGHT); line.text:SetHeight(WATCHFRAME_MULTIPLE_LINEHEIGHT) end
    end
end
function WatchFrame_Update() end
function WatchFrame_ReverseQuestObjective(text)
    local _, _, a1, a2 = string.find(text, "(.*):%s(.*)")
    if a1 and a2 then return a2 .. " " .. a1 end
    return text
end

-- Cadres d'unite, minicarte, texte de zone, carte du monde
TargetFrame = NouveauCadre("TargetFrame")
TargetFrame.unit, TargetFrame.name = "target", NouvelleZone("")
function UnitFrame_Update(self) self.name:SetText(GetUnitName(self.unit)) end
function UnitFrame_OnEvent(self, event) end
MinimapZoneText, MinimapZoneTextButton = NouvelleZone(""), NouveauCadre("MinimapZoneTextButton")
function GetMinimapZoneText() return ZONE_MINICARTE end
-- Comme le client CoA (patch-B, Minimap.lua/.xml) : Minimap_Update appelle Minimap_SetTooltip par son nom
-- global ; MinimapCluster a <OnEvent function="Minimap_Update"/> : la fonction est CAPTUREE au chargement
-- (le crochet pose sur le nom global ne la voit pas).
function Minimap_Update() MinimapZoneText:SetText(GetMinimapZoneText()); Minimap_SetTooltip(nil, nil) end
function Minimap_SetTooltip(pvpType, factionName) end
MinimapCluster = NouveauCadre("MinimapCluster")
MinimapCluster.scripts.OnEvent = Minimap_Update
for _, e in ipairs({ "ZONE_CHANGED", "ZONE_CHANGED_INDOORS", "ZONE_CHANGED_NEW_AREA" }) do MinimapCluster:RegisterEvent(e) end
-- Comme le client CoA (patch-B, UIErrorsFrame.lua) : UI_INFO_MESSAGE jaune, UI_ERROR_MESSAGE rouge.
UIErrorsFrame = NouveauCadre("UIErrorsFrame")
MESSAGES_CENTRE = {}
function UIErrorsFrame:AddMessage(t, r, g, b, id) table.insert(MESSAGES_CENTRE, { t, r, g, b, id }) end
function UIErrorsFrame_OnEvent(self, event, ...)
    local arg1, arg2, arg3, arg4 = ...
    if event == "SYSMSG" then self:AddMessage(arg1, arg2, arg3, arg4, 1.0)
    elseif event == "UI_INFO_MESSAGE" then self:AddMessage(arg1, 1.0, 1.0, 0.0, 1.0)
    elseif event == "UI_ERROR_MESSAGE" then self:AddMessage(arg1, 1.0, 0.1, 0.1, 1.0) end
end
UIErrorsFrame.scripts.OnEvent = function(self, event, ...) UIErrorsFrame_OnEvent(self, event, ...) end
for _, e in ipairs({ "SYSMSG", "UI_INFO_MESSAGE", "UI_ERROR_MESSAGE" }) do UIErrorsFrame:RegisterEvent(e) end
-- Bulles : enfants sans nom de WorldFrame (une plaque de nom, puis les bulles creees par les cas)
WorldFrame = NouveauCadre("WorldFrame")
local plaque = NouveauCadre(nil)
plaque.regions = { NouvelleZone("Kobold Vermin") }
plaque.enfants = { NouveauCadre(nil) }           -- une plaque de nom a des enfants (barre de vie…)
WorldFrame.enfants = { plaque }
function NouvelleBulleDeDialogue(texte)
    local b = NouveauCadre(nil)
    b.visible = true
    b.regions = { NouvelleZone(texte) }
    table.insert(WorldFrame.enfants, b)
    return b
end
ZoneTextFrame, SubZoneTextFrame = NouveauCadre("ZoneTextFrame"), NouveauCadre("SubZoneTextFrame")
ZoneTextString, SubZoneTextString = NouvelleZone(""), NouvelleZone("")
WorldMapButton, WorldMapFrameAreaLabel = NouveauCadre("WorldMapButton"), NouvelleZone("")

-- Grimoire d'Ascension : un bouton (securise dans le jeu ; ici un simple cadre)
AscensionSpellbookFrame = NouveauCadre("AscensionSpellbookFrame")
local boutonGrimoire = NouveauCadre("AscensionSpellbookFrameSpellButton1")
boutonGrimoire.SpellName, boutonGrimoire.SubSpellName = NouvelleZone(""), NouvelleZone("")
boutonGrimoire.visible = true
local boutonMetier = NouveauCadre(nil)            -- livre des metiers (Ascension_ProfessionBook.lua, bouton securise)
boutonMetier.fs, boutonMetier.Rank, boutonMetier.skillID, boutonMetier.visible = NouvelleZone(""), NouvelleZone(""), 164, true
BOUTON_METIER = boutonMetier
AscensionSpellbookFrame.enfants = { boutonGrimoire, boutonMetier }

-- ---- add-on 0.4 : fenetres imitant le client CoA (patch-B / patch-enUS-3) ----
-- Marchand (MerchantFrame.lua) : MerchantFrame_Update -> noms anglais des objets de la page ou du rachat.
MERCHANT_ITEMS_PER_PAGE, MARCHAND, RACHAT = 10, {}, {}
MerchantFrame = NouveauCadre("MerchantFrame")
MerchantFrame.selectedTab, MerchantFrame.page = 1, 1
for i = 1, 12 do _G["MerchantItem" .. i .. "Name"] = NouvelleZone("") end
MerchantBuyBackItemName = NouvelleZone("")
MerchantNameText = NouvelleZone("Merchant Name")
function GetMerchantItemLink(index) local o = MARCHAND[index]; return o and LienObjet(o.id, o.nom) end
function GetBuybackItemLink(index) local o = RACHAT[index]; return o and LienObjet(o.id, o.nom) end
function GetNumBuybackItems() return #RACHAT end
-- (0.5) comme patch-B : MerchantFrame_UpdateMerchantInfo pose l'en-tete MerchantNameText:SetText(UnitName("NPC")),
-- MerchantFrame_UpdateBuybackInfo pose MERCHANT_BUYBACK
function MerchantFrame_Update()
    if MerchantFrame.selectedTab == 1 then
        MerchantNameText:SetText(UnitName("NPC"))
        for i = 1, MERCHANT_ITEMS_PER_PAGE do
            local o = MARCHAND[(MerchantFrame.page - 1) * MERCHANT_ITEMS_PER_PAGE + i]
            _G["MerchantItem" .. i .. "Name"]:SetText(o and o.nom or "")
        end
        local d = RACHAT[#RACHAT]
        MerchantBuyBackItemName:SetText(d and d.nom or "")
    else
        MerchantNameText:SetText(MERCHANT_BUYBACK or "Merchant Buyback")
        for i = 1, 12 do local o = RACHAT[i]; _G["MerchantItem" .. i .. "Name"]:SetText(o and o.nom or "") end
    end
end
-- (0.5) Banque, taxi, tabard : script OnEvent lie par function= dans le XML (capture), qui pose le nom du PNJ.
for _, x in ipairs({ { "BankFrame", "BANKFRAME_OPENED", "BankFrameTitleText" }, { "TaxiFrame", "TAXIMAP_OPENED", "TaxiMerchant" },
    { "TabardFrame", "OPEN_TABARD_FRAME", "TabardFrameNameText" } }) do
    local cadre = NouveauCadre(x[1])
    _G[x[3]] = NouvelleZone("")
    cadre.scripts.OnEvent = function(self, event) if event == x[2] then _G[x[3]]:SetText(UnitName("npc")) end end
    cadre:RegisterEvent(x[2])
end
-- (0.5) Carte du monde, infobulle d'un point de quete (patch-B, WorldMapFrame.lua : WorldMapQuestPOI_SetTooltip)
WorldMapTooltip = NouvelleBulle("WorldMapTooltip")
function WorldMapTooltip:SetText(t) self:Effacer({ t }) end
function WorldMapFrame_ReverseQuestObjective(text)
    local _, _, a1, a2 = string.find(text, "(.*):%s(.*)")
    if a1 and a2 then return a2 .. " " .. a1 end
    return text
end
POI_OBJECTIFS = {}
function GetNumQuestLeaderBoards(i) return #POI_OBJECTIFS end
function GetQuestLogLeaderBoard(k, i) return POI_OBJECTIFS[k], "item", false end
function GetNumQuestItemDrops(i) return 0 end
function WorldMapQuestPOI_SetTooltip(poiButton, questLogIndex, numObjectives)
    local title = GetQuestLogTitle(questLogIndex)
    WorldMapTooltip:SetText(title)
    for k = 1, GetNumQuestLeaderBoards(questLogIndex) do
        local text, _, finished = GetQuestLogLeaderBoard(k, questLogIndex)
        if text and not finished then WorldMapTooltip:AddLine("- " .. WorldMapFrame_ReverseQuestObjective(text), 1, 1, 1, 1) end
    end
    WorldMapTooltip:Show()
end
-- Butin (LootFrame.lua de patch-enUS-3) : LootFrame_UpdateButton(index) pose le nom et button.slot.
BUTIN = {}
for i = 1, 4 do
    local b = NouveauCadre("LootButton" .. i)
    _G["LootButton" .. i .. "Text"] = NouvelleZone("")
end
function GetLootSlotLink(slot) local o = BUTIN[slot]; return o and LienObjet(o.id, o.nom) end
function LootFrame_UpdateButton(index)
    local b, o = _G["LootButton" .. index], BUTIN[index]
    if o then _G["LootButton" .. index .. "Text"]:SetText(o.nom); b.slot = index; b:Show() else b:Hide() end
end
-- Carte du monde (WorldMapFrame.lua de patch-B) : panneau des quetes, objectifs retournes, separes par |n.
WorldMapFrame = NouveauCadre("WorldMapFrame")
QUESTFRAME_PADDING, QUESTFRAME_MINHEIGHT, QUEST_DASH = 19, 34, "- "
local function CadreQueteCarte(nom)
    local q = NouveauCadre(nom)
    q.title, q.objectives, q.dashes = NouvelleZone(""), NouvelleZone(""), NouvelleZone("")
    q.title:SetWidth(240); q.objectives:SetWidth(230)
    q.lineHeight, q.lineSpacing = 13, 0
    return q
end
WorldMapQuestFrame0, WorldMapQuestFrame1 = CadreQueteCarte("WorldMapQuestFrame0"), CadreQueteCarte("WorldMapQuestFrame1")
CARTE_QUETE = nil
function WorldMapFrame_UpdateQuests()
    local c = CARTE_QUETE
    if not c then WorldMapFrame.numQuests = 0; return 0 end
    local q = WorldMapQuestFrame1
    q.questLogIndex, q.completed = c.index, c.termine
    q.title:SetText(c.titre)
    if c.termine then q.objectives:SetText(c.texte_fin) else
        local t = ""
        for _, o in ipairs(c.objectifs) do t = t .. WatchFrame_ReverseQuestObjective(o) .. "|n" end
        q.objectives:SetText(t)
    end
    q:SetHeight(math.max(q.title:GetHeight() + q.objectives:GetHeight() + QUESTFRAME_PADDING, QUESTFRAME_MINHEIGHT))
    q:Show()
    WorldMapFrame.numQuests = 1
    return 1
end
-- Barre d'incantation (CastingBarFrame.lua de patch-B) : barText:SetText(nom anglais) au debut du sort.
CastingBarFrame, CastingBarFrameText = NouveauCadre("CastingBarFrame"), NouvelleZone("")
CastingBarFrame.unit = "player"
SORT_EN_COURS = nil
function CastingBarFrame_OnEvent(self, event, unit)
    if unit ~= self.unit then return end
    if event == "UNIT_SPELLCAST_START" then CastingBarFrameText:SetText(SORT_EN_COURS) end
end
SORTS_PAR_NOM = {}
-- Pierre de foyer : lieu du foyer ($z)
function GetBindLocation() return LIEU_FOYER end
-- Types de creatures : UnitCreatureType (anglais, client enUS)
function UnitCreatureType(u) return UNITES[u] and UNITES[u].type end
-- Plaques de nom (C_NamePlateManager.lua de patch-B) : GetNamePlateForUnit(unite) -> plaque ; nom en zone de texte.
PLAQUES = {}
function GetNamePlateForUnit(u) return PLAQUES[u] end

-- LoadAddOn : lit le .toc de l'add-on et charge ses fichiers dans l'ordre.
local charges = {}
function LoadAddOn(nom)
    if charges[nom] then return 1 end
    local toc = io.open(RACINE .. "/AddOns/" .. nom .. "/" .. nom .. ".toc", "rb")
    if not toc then return nil, "MISSING" end
    for ligne in toc:lines() do
        ligne = string.gsub(ligne, "\r", "")
        if ligne ~= "" and not string.find(ligne, "^##") then
            local f = assert(loadfile(RACINE .. "/AddOns/" .. nom .. "/" .. string.gsub(ligne, "\\", "/")))
            f()
        end
    end
    toc:close()
    charges[nom] = true
    return 1
end

-- ----------------------------------------------------------------------------
-- Cas (fichier ecrit par tester_addon.py) : GLOBALES (GlobalStrings anglais du client),
-- OBJETS_BANC, CAS_LISTE…, lus AVANT l'add-on (comme le client pose ses textes avant).
-- ----------------------------------------------------------------------------
dofile(CAS)
for k, v in pairs(GLOBALES or {}) do _G[k] = v end

-- ----------------------------------------------------------------------------
-- Chargement du coeur (comme le jeu : fichiers du .toc), connexion
-- ----------------------------------------------------------------------------
collectgarbage("collect")
local mem0 = collectgarbage("count")
assert(LoadAddOn("Azeroth_FR"))
local A = AzerothFR
noter(type(A) == "table" and A.VERSION ~= nil, "coeur charge", "version " .. tostring(A and A.VERSION))
noter(type(SlashCmdList.AZFR) == "function" and SLASH_AZFR1 == "/azfr", "commande /azfr enregistree")

MESURES_FAMILLES = {}
for _, f in ipairs(A.FAMILLES) do
    if f.auto then
        collectgarbage("collect")
        local m, c0 = collectgarbage("count"), os.clock()
        LoadAddOn(f.addon)
        local d = (os.clock() - c0) * 1000
        collectgarbage("collect")
        MESURES_FAMILLES[f.addon] = { famille = f.famille, charge = (collectgarbage("count") - m) / 1024, ms = d }
    end
end
local t0 = os.clock()
Declencher("PLAYER_LOGIN")
local duree = (os.clock() - t0) * 1000
collectgarbage("collect")
local mem1 = collectgarbage("count")
local total_ms = 0
for _, m in pairs(MESURES_FAMILLES) do total_ms = total_ms + m.ms end
print(string.format("MESURE  connexion : familles auto chargees en %.0f ms au total ; memoire Lua %.1f Mo (avant : %.1f Mo)",
    total_ms + duree, mem1 / 1024, mem0 / 1024))
for _, f in ipairs(A.FAMILLES) do
    if f.auto then noter(A.Charges[f.addon] == true, "famille chargee : " .. f.addon) end
end

-- Sorts et index des sorts : charges a la demande en jeu (premiere infobulle de sort, premiere ligne
-- « Use: ») ; ici mesures a part, avant les cas, par A.ChargerAddon comme dans le jeu.
for _, f in ipairs(A.FAMILLES) do
    if f.famille == "sorts" or f.famille == "sorts_index" then
        collectgarbage("collect")
        local m0, c0 = collectgarbage("count"), os.clock()
        A.ChargerAddon(f.addon)
        local d = (os.clock() - c0) * 1000
        collectgarbage("collect")
        print(string.format("MESURE  %s (%s%s) : chargee a la demande +%.1f Mo en %.0f ms", f.addon, f.famille,
            f.debut and string.format(" %d a %d", f.debut, f.fin) or "", (collectgarbage("count") - m0) / 1024, d))
    end
end

-- Donnees d'essai injectees par le banc (jamais embarquees) : voir tester_addon.py.
local function Injecter(inj)
    local fam = A.Tables[inj.famille]
    local t = fam and fam[inj.nom]
    if not t then
        A.Recevoir(inj.famille, inj.nom, inj.sorte, inj.nb, {})
        t = A.Tables[inj.famille][inj.nom]
    end
    local seau
    if inj.sorte == "id" then seau = math.floor(inj.cle / t.nb) else seau = inj.h2 % t.nb end
    local s = t:Seau(seau)
    if not s then s = {}; t.seaux[seau] = s end
    s[inj.cle] = assert(loadstring("return " .. inj.valeur))()
end
for _, inj in ipairs(INJECTIONS or {}) do Injecter(inj) end

local function egal(nom, obtenu, attendu)
    local ok = obtenu == attendu
    if ok then noter(true, nom) else
        noter(false, nom, "\n      obtenu  : " .. tostring(obtenu) .. "\n      attendu : " .. tostring(attendu))
    end
end

local function Filtrer(evenement, args)
    local r = { false, unpack(args, 1, 12) }
    for _, f in ipairs(filtres[evenement] or {}) do
        local nouveau = { f(nil, evenement, unpack(args, 1, 12)) }
        if nouveau[1] then return nil end
        if nouveau[2] ~= nil then r = nouveau; args = { unpack(nouveau, 2, 13) } end
    end
    return args
end


-- 0.8 : fenetre du maitre (patch-B, Blizzard_TrainerUI) : ClassTrainerFrame_Update pose l'en-tete et la liste
-- (« "  "..nom » pour un sort, rang par PARENS_TEMPLATE), ClassTrainer_SetSelection pose le detail.
MAITRE = {}
function DefinirMaitre()
    if ClassTrainerNameText then return end
    ClassTrainerNameText = NouvelleZone("")
    CLASS_TRAINER_SKILLS_DISPLAYED = 3
    for i = 1, 3 do
        _G["ClassTrainerSkill" .. i] = NouvelleZone("")
        _G["ClassTrainerSkill" .. i .. "Text"] = NouvelleZone("")
        _G["ClassTrainerSkill" .. i .. "SubText"] = NouvelleZone("")
    end
    ClassTrainerSkillName, ClassTrainerSubSkillName, ClassTrainerSkillDescription = NouvelleZone(""), NouvelleZone(""), NouvelleZone("")
    function ClassTrainerFrame_Update()
        ClassTrainerNameText:SetText(UnitName("npc"))
        for i = 1, 3 do
            local s = MAITRE[i]
            _G["ClassTrainerSkill" .. i].visible = s and true or false
            if s then
                _G["ClassTrainerSkill" .. i .. "Text"]:SetText(s.categorie and s.nom or ("  " .. s.nom))
                _G["ClassTrainerSkill" .. i .. "SubText"]:SetText(s.rang and ("(" .. s.rang .. ")") or "")
            end
        end
    end
    function ClassTrainer_SetSelection(id)
        local s = MAITRE[id]
        if not s then return end
        ClassTrainerSkillName:SetText(s.nom)
        ClassTrainerSubSkillName:SetText(s.rang and ("(" .. s.rang .. ")") or "")
        ClassTrainerSkillDescription:SetText(s.description or "")
    end
    Declencher("ADDON_LOADED", "Blizzard_TrainerUI")
end

-- 0.9.5 : audit des sorts des classes (outils/audit_sorts.py) : chaque texte rendu passe par le vrai add-on
if AUDIT_SORTS then
    local A = AzerothFR
    local f = io.open(AUDIT_SORTIE, "w")
    for _, a in ipairs(AUDIT_SORTS) do
        local ok, fr = pcall(function()
            if a.champ == "Name" then return A.NomSort(a.id, a.affiche) end
            return A.DescriptionSort(a.id, a.affiche)
        end)
        fr = ok and fr or nil
        f:write(a.k, "\t", (fr and fr ~= a.affiche) and "OK" or "KO", "\t", (string.gsub(fr or "", "[\t\r\n]", " ")), "\n")
    end
    f:close()
    print("AUDIT : " .. #AUDIT_SORTS .. " textes passés")
    os.exit(0)
end

for _, c in ipairs(CAS_LISTE) do
    resultats.exemples = resultats.exemples + 1
    JOUEUR.sexe = c.sexe or 2
    JOUEUR.classe = c.classe or "Warrior"
    A.LireJoueur()
    A.Memo = setmetatable({}, { __mode = "k" })
    A.Ecrits = setmetatable({}, { __mode = "k" })
    local sauve = {}
    for k, v in pairs(c.globales or {}) do sauve[k] = _G[k]; _G[k] = v end
    if c.quoi == "texte" then
        local fn = ({ quetes = A.TexteQuete, dialogues = A.TexteDialogue, pages = A.TextePage })[c.famille]
        egal(c.nom, fn(c.anglais), c.attendu)
    elseif c.quoi == "cri" then
        local r = { false }
        for _, f in ipairs(filtres[c.evenement] or {}) do
            r = { f(nil, c.evenement, c.anglais, c.emetteur, "", "", c.cible or "") }
        end
        egal(c.nom, r[2], c.attendu)
        if c.emetteur_attendu then egal(c.nom .. " (nom du PNJ)", r[3], c.emetteur_attendu) end
    elseif c.quoi == "titre_id" then
        egal(c.nom, A.TitreParId(c.id, c.anglais), c.attendu)
    elseif c.quoi == "objectif" then
        if c.objet_cache then OBJETS_BANC[c.objet_cache[1]] = { nom = c.objet_cache[2], lignes = {} } end
        egal(c.nom, A.TraduireObjectif(c.anglais), c.attendu)
    elseif c.quoi == "objet" then
        GameTooltip:Effacer(c.lignes, { c.anglais, LienObjet(c.id, c.anglais) }, nil, nil, c.droites)
        if c.sort_objet then ITEM_SPELLS[c.id] = { "x", c.sort_objet } else ITEM_SPELLS[c.id] = nil end
        GameTooltip:Declencher("OnTooltipSetItem")
        egal(c.nom .. " (nom)", GameTooltip.lignes[1]:GetText(), c.attendu)
        if c.description_attendue then
            egal(c.nom .. " (ligne " .. c.ligne_description .. ")", GameTooltip.lignes[c.ligne_description]:GetText(),
                c.description_attendue)
        end
        for _, x in ipairs(c.lignes_attendues or {}) do
            egal(c.nom .. " (ligne " .. x[1] .. ", " .. x[3] .. ")", GameTooltip.lignes[x[1]]:GetText(), x[2])
        end
        for _, x in ipairs(c.droites_attendues or {}) do
            egal(c.nom .. " (à droite, ligne " .. x[1] .. ")", _G["GameTooltipTextRight" .. x[1]]:GetText(), x[2])
        end
    elseif c.quoi == "creature" then
        UNITES.mouseover = { nom = c.anglais, guid = c.guid }
        GameTooltip:Effacer(c.lignes, nil, "mouseover")
        GameTooltip:Declencher("OnTooltipSetUnit")
        egal(c.nom .. " (nom)", GameTooltip.lignes[1]:GetText(), c.attendu)
        if c.sous_titre_attendu then egal(c.nom .. " (sous-titre)", GameTooltip.lignes[2]:GetText(), c.sous_titre_attendu) end
        if c.faction_attendue then
            egal(c.nom .. " (faction)", GameTooltip.lignes[c.ligne_faction]:GetText(), c.faction_attendue)
        end
    elseif c.quoi == "gossip" then
        UNITES.npc = c.pnj and { nom = c.pnj, guid = c.guid } or nil
        GossipGreetingText:SetText(c.accueil)
        GossipTitleButton1:SetText(c.option)
        GossipFrameUpdate()
        egal(c.nom .. " (accueil)", GossipGreetingText:GetText(), c.accueil_attendu)
        egal(c.nom .. " (option)", GossipTitleButton1:GetText(), c.option_attendue)
        if c.pnj_attendu then egal(c.nom .. " (nom du PNJ en tête)", GossipFrameNpcNameText:GetText(), c.pnj_attendu) end
    elseif c.quoi == "fenetre_quete" then
        QuestInfoFrame.questLog = false
        QuestInfoTitleHeader:SetText(c.titre); QuestInfoDescriptionText:SetText(c.description)
        QuestInfoObjectivesText:SetText(c.objectifs or "")
        QuestInfo_Display()
        egal(c.nom .. " (titre)", QuestInfoTitleHeader:GetText(), c.titre_attendu)
        egal(c.nom .. " (description)", QuestInfoDescriptionText:GetText(), c.description_attendue)
        if c.objectifs_attendus then egal(c.nom .. " (objectifs)", QuestInfoObjectivesText:GetText(), c.objectifs_attendus) end
    elseif c.quoi == "suivi" then
        WatchFrameLine1.text:SetText(c.anglais)
        WatchFrame_Update()
        egal(c.nom, WatchFrameLine1.text:GetText(), c.attendu)
    elseif c.quoi == "suivi_hauteur" then
        JOURNAL = { { titre = c.titre_en, id = c.id } }
        A.JournalAChange()
        local l1, l2 = WatchFrameLine1, WatchFrameLine2
        l1:Reset(); l2:Reset()
        local avant = NouvelleZone(c.titre_fr); avant:SetWidth(WATCHFRAME_MAXLINEWIDTH)
        WatchFrame_SetLine(l1, nil, -10, true, c.titre_en, 0, nil, false)
        WatchFrame_SetLine(l2, l1, 0, false, WatchFrame_ReverseQuestObjective(c.objectif_en), 1, nil, false)
        egal(c.nom .. " (titre)", l1.text:GetText(), c.titre_fr)
        egal(c.nom .. " (objectif, compte d'abord)", l2.text:GetText(), c.objectif_fr)
        local h_texte, h_ligne = l1.text:GetHeight(), l1:GetHeight()
        noter(h_ligne >= h_texte and h_texte > WATCHFRAME_LINEHEIGHT, c.nom .. " (pas de chevauchement)",
            string.format("titre francais sur %d px, ligne reservee %d px (le client avait reserve %d px pour l'anglais)",
                h_texte, h_ligne, WATCHFRAME_LINEHEIGHT))
        JOURNAL = {}
        A.JournalAChange()
    elseif c.quoi == "livre" then
        ITEM_TEXT = c.anglais
        Declencher("ITEM_TEXT_READY")
        egal(c.nom, ItemTextPageText:GetText(), c.attendu)
    elseif c.quoi == "discussion" then
        if c.journal then JOURNAL = c.journal; A.JournalAChange() end
        local args = { c.message, c.emetteur or "", "", c.arg4 or "", "", "", 0, 0, "", 0, 0, nil }
        local r = Filtrer(c.evenement, args)
        egal(c.nom, r and r[c.champ or 1], c.attendu)
        if c.journal then JOURNAL = {}; A.JournalAChange() end
    elseif c.quoi == "journal_entete" then
        JOURNAL = { { titre = c.anglais, entete = 1 } }
        A.JournalAChange()
        egal(c.nom, A.CorrespondancesJournal()[c.anglais], c.attendu)
        JOURNAL = {}
        A.JournalAChange()
    elseif c.quoi == "minicarte" then
        -- evenement de zone : le script CAPTURE de MinimapCluster pose l'anglais, nos branchements passent apres
        ZONE_MINICARTE = c.anglais
        MinimapZoneText:SetText("")
        Declencher("ZONE_CHANGED")
        egal(c.nom .. " (ZONE_CHANGED, Minimap_Update capturée par MinimapCluster)", MinimapZoneText:GetText(), c.attendu)
        -- texte pose au chargement de l'interface, avant les donnees : traduit a l'entree en jeu
        A.Ecrits = setmetatable({}, { __mode = "k" })
        MinimapZoneText:SetText(c.anglais)
        Declencher("PLAYER_ENTERING_WORLD")
        egal(c.nom .. " (PLAYER_ENTERING_WORLD)", MinimapZoneText:GetText(), c.attendu)
    elseif c.quoi == "cible" then
        UNITES.target = { nom = c.anglais, guid = c.guid }
        UnitFrame_Update(TargetFrame)
        egal(c.nom, TargetFrame.name:GetText(), c.attendu)
    elseif c.quoi == "sort_barre" or c.quoi == "sort_bulle" or c.quoi == "sort_grimoire_bulle" then
        local s = { id = c.id, nom = c.anglais, rang = c.rang, lignes = c.lignes, droites = c.droites }
        if c.quoi == "sort_barre" then ACTIONS[7] = s; GameTooltip:SetAction(7)
        elseif c.quoi == "sort_grimoire_bulle" then GRIMOIRE[4] = s; GameTooltip:SetSpell(4, "spell")
        else GameTooltip:Effacer(c.lignes, nil, nil, { c.anglais, c.rang or "", c.id }, c.droites); GameTooltip:Declencher("OnTooltipSetSpell") end
        egal(c.nom .. " (nom)", GameTooltip.lignes[1]:GetText(), c.attendu)
        if c.rang_attendu then egal(c.nom .. " (rang)", GameTooltipTextRight1:GetText(), c.rang_attendu) end
        if c.description_attendue then
            egal(c.nom .. " (description)", GameTooltip.lignes[c.ligne_description]:GetText(), c.description_attendue)
        end
    elseif c.quoi == "aura" then
        AURAS[2] = { id = c.id, nom = c.anglais, lignes = c.lignes }
        GameTooltip:SetUnitAura("player", 2, "HELPFUL")
        egal(c.nom .. " (nom)", GameTooltip.lignes[1]:GetText(), c.attendu)
        if c.description_attendue then
            egal(c.nom .. " (description)", GameTooltip.lignes[c.ligne_description]:GetText(), c.description_attendue)
        end
    elseif c.quoi == "grimoire" then
        GRIMOIRE[11] = { id = c.id, nom = c.anglais }
        boutonGrimoire.spell, boutonGrimoire.bookType = 11, "spell"
        boutonGrimoire.SpellName:SetText(c.anglais); boutonGrimoire.SubSpellName:SetText(c.rang or "")
        AscensionSpellbookFrame.visible = true
        A.TraduireGrimoire()
        AscensionSpellbookFrame.visible = false
        egal(c.nom .. " (nom)", boutonGrimoire.SpellName:GetText(), c.attendu)
        if c.rang_attendu then egal(c.nom .. " (rang)", boutonGrimoire.SubSpellName:GetText(), c.rang_attendu) end
    elseif c.quoi == "squelette" then
        local ok = true
        for i, t in ipairs(c.textes) do
            if A.Squelette(t) ~= c.attendus[i] then
                ok = false
                print("      Lua : " .. A.Squelette(t) .. "\n      Python : " .. c.attendus[i])
            end
        end
        noter(ok, c.nom)
    elseif c.quoi == "etiquettes" then
        for id, o in pairs(c.objets) do OBJETS_BANC[tonumber(id)] = o end
        local avant = #messages
        SlashCmdList.AZFR("etiquettes")
        for i, attendu in ipairs(c.attendus) do
            local b = _G["AzerothFR_Etiquette" .. i]
            egal(c.nom .. " (objet " .. i .. ", nom)", b and b.lignes[1] and b.lignes[1]:GetText(), attendu[1])
            egal(c.nom .. " (objet " .. i .. ", ligne d'étiquette)", b and b.lignes[2] and b.lignes[2]:GetText(), attendu[2])
        end
        local brutes = 0
        for k = avant + 1, #messages do
            if string.find(messages[k], "lignes affichées par le jeu", 1, true) then brutes = brutes + 1 end
        end
        noter(brutes == #c.attendus, c.nom .. " (lignes brutes affichées une fois par objet, après le remplissage)",
            brutes .. " annonces")
        -- l'objet arrive plus tard du serveur : le jeu remplit l'infobulle et declenche OnTooltipSetItem
        local b = _G["AzerothFR_Etiquette1"]
        b:Effacer(c.objets[c.premier].lignes, { c.objets[c.premier].nom, LienObjet(c.premier, c.objets[c.premier].nom) })
        b:Declencher("OnTooltipSetItem")
        egal(c.nom .. " (objet arrivé plus tard : OnTooltipSetItem accroché)", b.lignes[2]:GetText(), c.attendus[1][2])
    elseif c.quoi == "bulle" then
        local avant = WorldFrame.enfants[1].regions[1]:GetText()
        Declencher(c.evenement, c.anglais, c.emetteur, "", "", c.cible or "")
        local bulle = NouvelleBulleDeDialogue(c.anglais)       -- le moteur cree la bulle a l'image suivante
        Images(4, 0.05)
        egal(c.nom, bulle.regions[1]:GetText(), c.attendu)
        egal(c.nom .. " (plaque de nom intacte)", WorldFrame.enfants[1].regions[1]:GetText(), avant)
        local autre = NouvelleBulleDeDialogue("Some other words.")
        Images(40, 0.05)
        egal(c.nom .. " (autre bulle intacte, recherche bornée)", autre.regions[1]:GetText(), "Some other words.")
    elseif c.quoi == "centre" then
        MESSAGES_CENTRE = {}
        Declencher(c.evenement, c.anglais)
        local m = MESSAGES_CENTRE[1]
        egal(c.nom .. " (un seul message)", #MESSAGES_CENTRE, 1)
        egal(c.nom, m and m[1], c.attendu)
        egal(c.nom .. " (couleur et argument comme UIErrorsFrame_OnEvent)", m and table.concat({ m[2], m[3], m[4], m[5] }, ","),
            table.concat(c.couleur, ","))
        if c.essai_off then
            SlashCmdList.AZFR("off")
            MESSAGES_CENTRE = {}
            Declencher(c.evenement, c.anglais)
            egal(c.nom .. " (/azfr off : le jeu reprend la main, anglais)", MESSAGES_CENTRE[1] and MESSAGES_CENTRE[1][1], c.anglais)
            egal(c.nom .. " (/azfr off : un seul message)", #MESSAGES_CENTRE, 1)
            SlashCmdList.AZFR("on")
            MESSAGES_CENTRE = {}
            Declencher(c.evenement, c.anglais)
            egal(c.nom .. " (/azfr on : de nouveau en français)", MESSAGES_CENTRE[1] and MESSAGES_CENTRE[1][1], c.attendu)
        end
    elseif c.quoi == "bulle_combat" then
        EN_COMBAT = true
        local n0 = A.Compteurs.bulles
        Declencher(c.evenement, c.anglais, c.emetteur, "", "", "")
        local bulle = NouvelleBulleDeDialogue(c.anglais)
        Images(4, 0.05)
        egal(c.nom, bulle.regions[1]:GetText(), c.anglais)
        egal(c.nom .. " (aucune bulle posée)", A.Compteurs.bulles, n0)
        EN_COMBAT = false
        -- hors combat, /azfr bulles off : rien ; /azfr bulles on : en francais
        SlashCmdList.AZFR("bulles off")
        Declencher(c.evenement, c.anglais, c.emetteur, "", "", "")
        local b2 = NouvelleBulleDeDialogue(c.anglais)
        Images(4, 0.05)
        egal(c.nom .. " (/azfr bulles off : anglais)", b2.regions[1]:GetText(), c.anglais)
        SlashCmdList.AZFR("bulles on")
        -- (les bulles precedentes ont disparu, comme en jeu)
        for k = #WorldFrame.enfants, 1, -1 do
            if WorldFrame.enfants[k] == bulle or WorldFrame.enfants[k] == b2 then table.remove(WorldFrame.enfants, k) end
        end
        Declencher(c.evenement, c.anglais, c.emetteur, "", "", "")
        local b3 = NouvelleBulleDeDialogue(c.anglais)
        Images(4, 0.05)
        egal(c.nom .. " (/azfr bulles on : français)", b3.regions[1]:GetText(), c.attendu)
    elseif c.quoi == "blocage" then
        local avant = #messages
        EN_COMBAT = true
        for _, f in ipairs(filtres.CHAT_MSG_MONSTER_SAY or {}) do f(nil, "CHAT_MSG_MONSTER_SAY", c.anglais, c.emetteur, "", "", "") end
        Declencher("CHAT_MSG_MONSTER_SAY", c.anglais, c.emetteur, "", "", "")
        Declencher("ADDON_ACTION_BLOCKED", c.addon, c.fonction)
        EN_COMBAT = false
        local annonce
        for k = avant + 1, #messages do
            if string.find(messages[k], "action bloquée", 1, true) then annonce = messages[k] end
        end
        noter(annonce ~= nil, c.nom .. " (annoncé dans la discussion)", annonce)
        noter(annonce and string.find(annonce, c.addon, 1, true) and string.find(annonce, c.fonction, 1, true)
            and string.find(annonce, "EN COMBAT", 1, true) and true or false, c.nom .. " (add-on, fonction, combat)")
        noter(annonce and string.find(annonce, "filtre cris", 1, true) and string.find(annonce, "Bulles.OnEvent", 1, true)
            and true or false, c.nom .. " (fil d'Ariane : derniers modules de l'add-on)")
        egal(c.nom .. " (gardé pour la session suivante)", type(AzerothFR_Reglages.blocages) == "table"
            and #AzerothFR_Reglages.blocages, 1)
        local n1 = #messages
        Declencher("ADDON_ACTION_FORBIDDEN", c.addon, "CastSpellByName()")
        local deux = 0
        for k = n1 + 1, #messages do if string.find(messages[k], "action bloquée", 1, true) then deux = deux + 1 end end
        egal(c.nom .. " (annoncé une seule fois par session)", deux, 0)
        egal(c.nom .. " (deux blocages notés)", #A.Blocages, 2)
        local n2 = #messages
        SlashCmdList.AZFR("stats")
        local vus = 0
        for k = n2 + 1, #messages do
            if string.find(messages[k], "ADDON_ACTION_BLOCKED", 1, true) or string.find(messages[k], "ADDON_ACTION_FORBIDDEN", 1, true) then vus = vus + 1 end
        end
        egal(c.nom .. " (/azfr stats les montre)", vus, 2)
    elseif c.quoi == "erreurs_jeu" then
        ERROR_HANDLER_DATABASE = { errors = { current = {
            { message = "AddOn 'Azeroth_FR' prevented the call of the secure function 'UNKNOWN()'.", stack = "Interface\\SharedXML\\ErrorHandler\\ErrorHandler.lua:350: in function <x>", time = "2026/11/04 21:12:03", counter = 1 },
            { message = "Interface\\FrameXML\\Truc.lua:12: attempt to index a nil value\nsuite", stack = "a\nb\nc\nd", time = "2026/11/04 21:13:00", counter = 3 },
        }, previous = {} } }
        local function Copie(t) if type(t) ~= "table" then return t end local r = {} for k, v in pairs(t) do r[k] = Copie(v) end return r end
        local function Pareil(a, b)
            if type(a) ~= type(b) then return false end
            if type(a) ~= "table" then return a == b end
            for k, v in pairs(a) do if not Pareil(v, b[k]) then return false end end
            for k in pairs(b) do if a[k] == nil then return false end end
            return true
        end
        local avant_db = Copie(ERROR_HANDLER_DATABASE)
        local avant = #messages
        SlashCmdList.AZFR("erreurs")
        local vu1, vu2 = false, false
        for k = avant + 1, #messages do
            if string.find(messages[k], "prevented the call of the secure function", 1, true) then vu1 = true end
            if string.find(messages[k], "x3", 1, true) and string.find(messages[k], "attempt to index", 1, true) then vu2 = true end
        end
        noter(vu1 and vu2, c.nom .. " (dernières entrées affichées)")
        noter(Pareil(avant_db, ERROR_HANDLER_DATABASE), c.nom .. " (rien d'écrit dans la base du jeu)")
        ERROR_HANDLER_DATABASE = { errors = { current = {}, previous = { { message = "ancienne", time = "x", counter = 1 } } } }
        avant = #messages
        SlashCmdList.AZFR("erreurs")
        local vu3 = false
        for k = avant + 1, #messages do if string.find(messages[k], "session précédente", 1, true) then vu3 = true end end
        noter(vu3, c.nom .. " (session précédente si la session en cours n'en a pas)")
        ERROR_HANDLER_DATABASE = nil
    elseif c.quoi == "suivi_combat" then
        JOURNAL = { { titre = c.titre_en, id = c.id } }
        A.JournalAChange()
        local l1 = WatchFrameLine1
        l1:Reset()
        WATCHFRAME_QUESTLINES = { l1 }
        SUIVI_GARDE = { hauteurs_en_combat = 0 }
        EN_COMBAT = true
        WatchFrame_SetLine(l1, nil, -10, true, c.titre_en, 0, nil, false)
        egal(c.nom .. " (en combat : anglais gardé)", l1.text:GetText(), c.titre_en)
        egal(c.nom .. " (en combat : aucune hauteur changée par l'add-on)", SUIVI_GARDE.hauteurs_en_combat, 0)
        EN_COMBAT = false
        Declencher("PLAYER_REGEN_ENABLED")
        egal(c.nom .. " (après le combat : français)", l1.text:GetText(), c.titre_fr)
        noter(l1:GetHeight() >= l1.text:GetHeight(), c.nom .. " (après le combat : ligne rehaussée)",
            string.format("%d px pour %d px de texte", l1:GetHeight(), l1.text:GetHeight()))
        SUIVI_GARDE = nil
        WATCHFRAME_QUESTLINES = {}
        JOURNAL = {}
        A.JournalAChange()
    elseif c.quoi == "centre_interrupteur" then
        SlashCmdList.AZFR("centre off")
        MESSAGES_CENTRE = {}
        Declencher(c.evenement, c.anglais)
        egal(c.nom .. " (off : le jeu affiche l'anglais, une fois)", MESSAGES_CENTRE[1] and MESSAGES_CENTRE[1][1], c.anglais)
        egal(c.nom .. " (off : un seul message)", #MESSAGES_CENTRE, 1)
        SlashCmdList.AZFR("centre on")
        MESSAGES_CENTRE = {}
        Declencher(c.evenement, c.anglais)
        egal(c.nom .. " (on : français)", MESSAGES_CENTRE[1] and MESSAGES_CENTRE[1][1], c.attendu)
        egal(c.nom .. " (on : un seul message)", #MESSAGES_CENTRE, 1)
    elseif c.quoi == "marchand" then
        UNITES.npc = c.pnj and { nom = c.pnj.nom, guid = c.pnj.guid } or nil
        MARCHAND, RACHAT = {}, {}
        for i, o in ipairs(c.achat) do MARCHAND[i] = o end
        for i, o in ipairs(c.rachat) do RACHAT[i] = o end
        MerchantFrame.visible, MerchantFrame.selectedTab, MerchantFrame.page = true, 1, 1
        MerchantFrame_Update()
        for i, o in ipairs(c.achat) do
            egal(c.nom .. " (achat " .. i .. ")", _G["MerchantItem" .. i .. "Name"]:GetText(), o.attendu)
        end
        egal(c.nom .. " (dernier objet vendu)", MerchantBuyBackItemName:GetText(), c.rachat[#c.rachat].attendu)
        if c.pnj then egal(c.nom .. " (en-tête : nom du PNJ)", MerchantNameText:GetText(), c.pnj.attendu) end
        MerchantFrame.selectedTab = 2
        MerchantFrame_Update()
        for i, o in ipairs(c.rachat) do
            egal(c.nom .. " (rachat " .. i .. ")", _G["MerchantItem" .. i .. "Name"]:GetText(), o.attendu)
        end
        if c.pnj then egal(c.nom .. " (en-tête de l'onglet Rachat : texte d'interface intact)", MerchantNameText:GetText(),
            MERCHANT_BUYBACK or "Merchant Buyback") end
        MerchantFrame.visible = false
        UNITES.npc = nil
    elseif c.quoi == "butin" then
        BUTIN = {}
        for i, o in ipairs(c.objets) do BUTIN[i] = o end
        for i = 1, 4 do LootFrame_UpdateButton(i) end
        for i, o in ipairs(c.objets) do egal(c.nom .. " (emplacement " .. i .. ")", _G["LootButton" .. i .. "Text"]:GetText(), o.attendu) end
    elseif c.quoi == "carte" then
        JOURNAL = { { titre = c.titre_en, id = c.id } }
        A.JournalAChange()
        WorldMapFrame.visible = true
        CARTE_QUETE = { index = 1, titre = c.titre_en, objectifs = c.objectifs, termine = c.termine, texte_fin = c.texte_fin }
        WorldMapFrame_UpdateQuests()
        egal(c.nom .. " (titre)", WorldMapQuestFrame1.title:GetText(), c.titre_attendu)
        egal(c.nom .. " (objectifs)", WorldMapQuestFrame1.objectives:GetText(), c.objectifs_attendus)
        if not c.termine then
            noter(string.find(WorldMapQuestFrame1.dashes:GetText() or "", QUEST_DASH or "-", 1, true) == 1, c.nom .. " (tirets recalculés)",
                WorldMapQuestFrame1.dashes:GetText())
        end
        noter(WorldMapQuestFrame1:GetHeight() >= WorldMapQuestFrame1.title:GetHeight() + WorldMapQuestFrame1.objectives:GetHeight(),
            c.nom .. " (hauteur du cadre refaite avec le français)")
        -- en combat : rien n'est fait ; repris a la fin du combat
        EN_COMBAT = true
        WorldMapFrame_UpdateQuests()
        egal(c.nom .. " (en combat : laissé en anglais)", WorldMapQuestFrame1.title:GetText(), c.titre_en)
        EN_COMBAT = false
        Declencher("PLAYER_REGEN_ENABLED")
        egal(c.nom .. " (après le combat : français)", WorldMapQuestFrame1.title:GetText(), c.titre_attendu)
        WorldMapFrame.visible = false
        CARTE_QUETE = nil
        JOURNAL = {}
        A.JournalAChange()
    elseif c.quoi == "progression" then
        QuestProgressTitleText:SetText(""); QuestProgressText:SetText(c.anglais)
        Declencher("QUEST_PROGRESS")
        egal(c.nom, QuestProgressText:GetText(), c.attendu)
    elseif c.quoi == "barre" then
        SORTS_PAR_NOM[c.anglais] = c.id
        SORT_EN_COURS = c.anglais
        CastingBarFrame_OnEvent(CastingBarFrame, "UNIT_SPELLCAST_START", "player")
        egal(c.nom, CastingBarFrameText:GetText(), c.attendu)
        SORT_EN_COURS = c.inconnu
        CastingBarFrame_OnEvent(CastingBarFrame, "UNIT_SPELLCAST_START", "player")
        egal(c.nom .. " (sort hors du grimoire : anglais)", CastingBarFrameText:GetText(), c.inconnu)
    elseif c.quoi == "barre_nom" then
        SORT_EN_COURS = c.anglais
        CastingBarFrame_OnEvent(CastingBarFrame, "UNIT_SPELLCAST_START", "player")
        egal(c.nom, CastingBarFrameText:GetText(), c.attendu)
    elseif c.quoi == "pierre_de_foyer" then
        LIEU_FOYER = c.lieu
        GameTooltip:Effacer(c.lignes, { c.anglais, LienObjet(c.id, c.anglais) })
        ITEM_SPELLS[c.id] = c.item_spell           -- (0.5) 3.3.5 : GetItemSpell rend nom et rang, pas le numero
        GameTooltip:Declencher("OnTooltipSetItem")
        egal(c.nom .. " (nom)", GameTooltip.lignes[1]:GetText(), c.attendu)
        egal(c.nom .. " (ligne Utiliser)", GameTooltip.lignes[c.ligne]:GetText(), c.ligne_attendue)
        LIEU_FOYER = nil
    elseif c.quoi == "type_creature" then
        UNITES.mouseover = { nom = c.anglais, guid = c.guid, type = c.type_en }
        GameTooltip:Effacer(c.lignes, nil, "mouseover")
        GameTooltip:Declencher("OnTooltipSetUnit")
        egal(c.nom, GameTooltip.lignes[2]:GetText(), c.attendu)
    elseif c.quoi == "plaques" then
        local function Plaque(nom_affiche, protege)
            local p = NouveauCadre(nil)
            local z = NouvelleZone(nom_affiche)
            p.regions, p.enfants, p.protege, p.visible = { z }, { NouveauCadre(nil) }, protege, true
            z.parent = p
            return p, z
        end
        UNITES.nameplate1 = { nom = c.anglais, guid = c.guid }
        local p1, z1 = Plaque(c.anglais)
        PLAQUES.nameplate1 = p1
        Declencher("NAME_PLATE_UNIT_ADDED", "nameplate1")
        egal(c.nom .. " (arrivée de la plaque)", z1:GetText(), c.attendu)
        -- plaque reutilisee : le client remet l'anglais d'une autre creature, puis de la premiere
        UNITES.nameplate1 = { nom = c.autre_en, guid = c.autre_guid }
        z1:SetText(c.autre_en)
        Declencher("NAME_PLATE_UNIT_REMOVED", "nameplate1")
        Declencher("NAME_PLATE_UNIT_ADDED", "nameplate1")
        egal(c.nom .. " (plaque réutilisée : autre créature)", z1:GetText(), c.autre_attendu)
        z1:SetText(c.autre_en)                         -- le client remet l'anglais (mise a jour du nom)
        Images(8, 0.05)
        egal(c.nom .. " (anglais remis par le client : repris au passage suivant)", z1:GetText(), c.autre_attendu)
        -- cadre protege : jamais touche
        UNITES.nameplate2 = { nom = c.anglais, guid = c.guid }
        local p2, z2 = Plaque(c.anglais, true)
        PLAQUES.nameplate2 = p2
        Declencher("NAME_PLATE_UNIT_ADDED", "nameplate2")
        egal(c.nom .. " (cadre protégé : intact)", z2:GetText(), c.anglais)
        -- un joueur : jamais
        UNITES.nameplate3 = { nom = "Thalwyn", guid = "0x0000000000000042", joueur = true }
        local p3, z3 = Plaque("Thalwyn")
        PLAQUES.nameplate3 = p3
        Declencher("NAME_PLATE_UNIT_ADDED", "nameplate3")
        egal(c.nom .. " (joueur : intact)", z3:GetText(), "Thalwyn")
        -- /azfr plaques off : rien
        SlashCmdList.AZFR("plaques off")
        UNITES.nameplate4 = { nom = c.anglais, guid = c.guid }
        local p4, z4 = Plaque(c.anglais)
        PLAQUES.nameplate4 = p4
        Declencher("NAME_PLATE_UNIT_ADDED", "nameplate4")
        egal(c.nom .. " (/azfr plaques off : anglais)", z4:GetText(), c.anglais)
        SlashCmdList.AZFR("plaques on")
        Images(8, 0.05)
        egal(c.nom .. " (/azfr plaques on : repris)", z4:GetText(), c.attendu)
        for k in pairs(PLAQUES) do PLAQUES[k] = nil end
        for _, u in ipairs({ "nameplate1", "nameplate2", "nameplate3", "nameplate4" }) do
            UNITES[u] = nil; Declencher("NAME_PLATE_UNIT_REMOVED", u)
        end
    elseif c.quoi == "metier" then
        BOUTON_METIER.fs:SetText(c.anglais); BOUTON_METIER.Rank:SetText(c.rang or "")
        AscensionSpellbookFrame.visible = true
        A.TraduireGrimoire()
        AscensionSpellbookFrame.visible = false
        egal(c.nom .. " (nom)", BOUTON_METIER.fs:GetText(), c.attendu)
        if c.rang_attendu then egal(c.nom .. " (rang)", BOUTON_METIER.Rank:GetText(), c.rang_attendu) end
    elseif c.quoi == "fenetre_quete_detail" then
        -- comme QuestFrameDetailPanel_OnShow : QuestInfo_Display deux fois (DETAIL1 : titre et description ;
        -- DETAIL2 : objectifs), la description est deja en francais au second appel
        QuestInfoFrame.questLog = false
        QuestInfoTitleHeader:SetText(c.titre); QuestInfoDescriptionText:SetText(c.description)
        QuestInfoObjectivesText:SetText("")
        QuestInfo_Display()
        QuestInfoObjectivesText:SetText(c.objectifs or "")
        QuestInfo_Display()
        egal(c.nom .. " (en-tête)", QuestInfoTitleHeader:GetText(), c.titre_attendu)
        egal(c.nom .. " (description)", QuestInfoDescriptionText:GetText(), c.description_attendue)
    elseif c.quoi == "entete_pnj" then
        UNITES.npc = { nom = c.anglais, guid = c.guid }
        if c.fenetre == "maitre" then
            DefinirMaitre()
            ClassTrainerFrame_Update()
            egal(c.nom, ClassTrainerNameText:GetText(), c.attendu)
        else
            Declencher(c.evenement)
            egal(c.nom, _G[c.zone]:GetText(), c.attendu)
        end
        UNITES.npc = { nom = c.anglais .. " Jr.", guid = c.guid }
        if c.fenetre == "maitre" then ClassTrainerFrame_Update() else Declencher(c.evenement) end
        egal(c.nom .. " (nom changé par le serveur : anglais)", c.fenetre == "maitre" and ClassTrainerNameText:GetText()
            or _G[c.zone]:GetText(), c.anglais .. " Jr.")
        UNITES.npc = nil
    elseif c.quoi == "client_fenetre" then
        -- 0.9 : une fenetre CoA visible, une zone de texte en anglais ; balayage
        local f = _G[c.cadre] or NouveauCadre(c.cadre)
        local z = NouvelleZone(c.anglais)
        f.regions, f.enfants, f.visible = { z }, {}, true
        A.BalayerFenetre(f, c.domaines)
        egal(c.nom, z:GetText(), c.attendu)
        f.visible = false
    elseif c.quoi == "hauts_faits" then
        -- 0.9.2 : fenetre des hauts faits (Blizzard_AchievementUI chargee a la demande) : versions minimales des
        -- fonctions de Blizzard (memes ecritures que le client), puis ADDON_LOADED
        local en = c.anglais
        function GetAchievementInfo(a, b)
            local i = b and c.id or a
            if i ~= c.id then return nil end
            return i, en.nom, 10, false, nil, nil, nil, en.description, 0, "", en.recompense
        end
        function GetCategoryInfo(id) if id == c.cat then return en.categorie, -1, 0 end end
        function GetAchievementNumCriteria(id) return id == c.id and #en.criteres or 0 end
        function GetAchievementCriteriaInfo(id, i)
            local k = en.criteres[i]
            return k.texte, 0, false, 0, 1, "", 0, 0, "0/1", k.id
        end
        function AchievementObjectives_DisplayCriteria(objectifs, id)
            for i = 1, GetAchievementNumCriteria(id) do
                local s = GetAchievementCriteriaInfo(id, i)
                local f = _G["AchievementFrameCriteria" .. i] or { name = NouvelleZone("") }
                _G["AchievementFrameCriteria" .. i] = f
                f.name:SetText("- " .. s)
            end
        end
        function AchievementButton_DisplayAchievement(button, categorie, index)
            local id, nom, _, _, _, _, _, desc, _, _, rec = GetAchievementInfo(categorie, index)
            button.id = id
            button.label:SetText(nom); button.description:SetText(desc); button.hiddenDescription:SetText(desc)
            if rec ~= "" then button.reward:SetText(rec) end
            AchievementObjectives_DisplayCriteria(nil, id)
            return id
        end
        function AchievementFrameCategories_DisplayButton(button, element)
            button.label:SetText((GetCategoryInfo(element.id))); button.categoryID = element.id
        end
        AchievementAlertFrame1 = AchievementAlertFrame1 or NouveauCadre("AchievementAlertFrame1")
        AchievementAlertFrame1Name = AchievementAlertFrame1Name or NouvelleZone("")
        function AchievementAlertFrame_ShowAlert(id)
            AchievementAlertFrame1.id = id
            AchievementAlertFrame1Name:SetText((select(2, GetAchievementInfo(id))))
        end
        -- 0.9.4 : barre d'une categorie du resume (nom pose a la creation du cadre, OnLoad)
        local barre = AchievementFrameSummaryCategoriesCategory1 or NouveauCadre("AchievementFrameSummaryCategoriesCategory1")
        AchievementFrameSummaryCategoriesCategory1 = barre
        function barre:GetID() return c.cat end
        AchievementFrameSummaryCategoriesCategory1Label = AchievementFrameSummaryCategoriesCategory1Label or NouvelleZone("")
        AchievementFrameSummaryCategoriesCategory1Label:SetText(en.categorie)
        if not AchievementFrameSummaryCategory_OnShow then function AchievementFrameSummaryCategory_OnShow(self) end end
        Declencher("ADDON_LOADED", "Blizzard_AchievementUI")
        AchievementFrameSummaryCategoriesCategory1Label:SetText(en.categorie)
        AchievementFrameSummaryCategory_OnShow(barre)
        egal(c.nom .. " (barre de catégorie du résumé)", AchievementFrameSummaryCategoriesCategory1Label:GetText(), c.attendu.categorie)
        local b = { label = NouvelleZone(""), description = NouvelleZone(""), hiddenDescription = NouvelleZone(""), reward = NouvelleZone("") }
        AchievementButton_DisplayAchievement(b, 1, 1)
        egal(c.nom .. " (nom)", b.label:GetText(), c.attendu.nom)
        egal(c.nom .. " (description)", b.description:GetText(), c.attendu.description)
        egal(c.nom .. " (description cachée, mesure de la hauteur)", b.hiddenDescription:GetText(), c.attendu.description)
        egal(c.nom .. " (récompense)", b.reward:GetText(), c.attendu.recompense)
        for i = 1, #c.attendu.criteres do
            egal(c.nom .. " (critère " .. i .. ")", _G["AchievementFrameCriteria" .. i].name:GetText(), c.attendu.criteres[i])
        end
        local bc = { label = NouvelleZone("") }
        AchievementFrameCategories_DisplayButton(bc, { id = c.cat })
        egal(c.nom .. " (catégorie)", bc.label:GetText(), c.attendu.categorie)
        AchievementAlertFrame_ShowAlert(c.id)
        egal(c.nom .. " (alerte « haut fait obtenu »)", AchievementAlertFrame1Name:GetText(), c.attendu.nom)
    elseif c.quoi == "bulle_sort_citee" then
        GameTooltip:Effacer(c.lignes, nil, nil, { "Talent du banc", "", 999999991 })
        GameTooltip:Declencher("OnTooltipSetSpell")
        egal(c.nom .. " (nom)", GameTooltip.lignes[3]:GetText(), c.attendu_nom)
        egal(c.nom .. " (description)", GameTooltip.lignes[4]:GetText(), c.attendu_desc)
        GameTooltip.visible = false
    elseif c.quoi == "bulle_show" then
        GameTooltip:Effacer({ "Titre de règle" })
        GameTooltip:AddLine(c.anglais)
        GameTooltip:Show()
        egal(c.nom, GameTooltipTextLeft2 and GameTooltipTextLeft2:GetText(), c.attendu)
        GameTooltip.visible = false
    elseif c.quoi == "tutoriel" then
        -- 0.9 : PathObjectiveDisplayMixin (Ascension_PathToAscension) : SetTutorial -> GetTutorialDisplay, SplitPages
        C_Tutorial = C_Tutorial or {}
        function C_Tutorial.GetTutorialDisplay(id) return "Titre", c.anglais, 0 end
        if not (PathToAscensionFrame and PathToAscensionFrame.Display) then
            local d = { affiches = 0 }
            function d:SplitPages(t)
                local pages = {}
                for morceau in string.gmatch(t .. "{page}", "(.-){page}") do pages[#pages + 1] = morceau end
                return pages
            end
            function d:RefreshDisplay() self.affiches = self.affiches + 1; self.affiche = self.pages[self.page] end
            function d:SetTutorial(id)
                self.name, self.description, self.questID = C_Tutorial.GetTutorialDisplay(id)
                self.page = 1
                self.pages = self:SplitPages(self.description)
                self:RefreshDisplay()
            end
            PathToAscensionFrame = PathToAscensionFrame or NouveauCadre("PathToAscensionFrame")
            PathToAscensionFrame.Display = d
            Declencher("ADDON_LOADED", "Ascension_PathToAscension")
        end
        local d = PathToAscensionFrame.Display
        d:SetTutorial(42)
        egal(c.nom .. " (description)", d.description, c.attendu)
        egal(c.nom .. " (pages)", #d.pages, c.pages)
        egal(c.nom .. " (page affichée)", d.affiche, d.pages[1])
    elseif c.quoi == "annexe" then
        C_Tutorial = C_Tutorial or {}
        function C_Tutorial.GetKeywordAtIndex(i) return "Mot", c.anglais, "icone", "" end
        if not PathToAscensionFrame then PathToAscensionFrame = NouveauCadre("PathToAscensionFrame") end
        if not PathToAscensionFrame.AppendixPanel then
            local a = { Display = { Title = NouvelleZone(""), Description = NouvelleZone("") } }
            function a:OnKeywordSelected(index)
                local k, d = C_Tutorial.GetKeywordAtIndex(index)
                d = d:gsub("{[^}]+}", ""):gsub("^\n+", "")
                self.Display.Title:SetText(k)
                self.Display.Description:SetText(d)
            end
            PathToAscensionFrame.AppendixPanel = a
            Declencher("ADDON_LOADED", "Ascension_PathToAscension")
        end
        PathToAscensionFrame.AppendixPanel:OnKeywordSelected(3)
        egal(c.nom, PathToAscensionFrame.AppendixPanel.Display.Description:GetText(), c.attendu)
    elseif c.quoi == "mot_cle" then
        -- 0.9 : KeywordTooltipMixin (SharedXML/KeywordTooltip.lua), bulle creee avec le mixin APRES le crochet
        C_Tutorial = C_Tutorial or {}
        function C_Tutorial.GetKeywordInfo(k) return c.nom_en, c.anglais end
        if not KeywordTooltipMixin then
            KeywordTooltipMixin = {}
            function KeywordTooltipMixin:FormatLine(t) self.lignes_posees = (self.lignes_posees or 0) + 1; self.texte = t end
            function KeywordTooltipMixin:SetKeyword(k)
                self.keyword = k
                local n, t = C_Tutorial.GetKeywordInfo(k)
                self.Title:SetText(n)
                self:FormatLine(t)
            end
            Declencher("ADDON_LOADED", "Banc_MotsCles")
        end
        local b = { Title = NouvelleZone(""), TextPool = { ReleaseAll = function() end },
                    ImagePool = { ReleaseAll = function() end }, SetHeight = function() end }
        for k, v in pairs(KeywordTooltipMixin) do b[k] = v end
        b:SetKeyword(7)
        egal(c.nom .. " (titre)", b.Title:GetText(), c.nom_attendu)
        egal(c.nom .. " (texte)", b.texte, c.attendu)
    elseif c.quoi == "ligne_objet" then
        egal(c.nom, A.LigneObjet(c.ligne), c.attendu)
    elseif c.quoi == "nom_domaine" then
        egal(c.nom, A.Nom(c.domaine, c.anglais), c.attendu)
    elseif c.quoi == "maitre_liste" then
        DefinirMaitre()
        MAITRE = c.services
        ClassTrainerFrame_Update()
        for k, att in ipairs(c.attendus) do
            egal(c.nom .. " (ligne " .. k .. ")", _G["ClassTrainerSkill" .. k .. "Text"]:GetText(), att[1])
            if att[2] then egal(c.nom .. " (rang " .. k .. ")", _G["ClassTrainerSkill" .. k .. "SubText"]:GetText(), att[2]) end
        end
        if c.detail then
            ClassTrainer_SetSelection(c.detail)
            egal(c.nom .. " (détail : nom)", ClassTrainerSkillName:GetText(), c.detail_nom)
            if c.detail_description then
                egal(c.nom .. " (détail : description)", ClassTrainerSkillDescription:GetText(), c.detail_description)
            end
        end
        MAITRE = {}
    elseif c.quoi == "bulle_carte" then
        JOURNAL = { { titre = c.titre_en, id = c.id } }
        A.JournalAChange()
        POI_OBJECTIFS = c.objectifs
        for k = 1, 3 do                                   -- le jeu refait l'infobulle a chaque image
            WorldMapQuestPOI_SetTooltip(nil, 1)
        end
        egal(c.nom .. " (titre)", WorldMapTooltip.lignes[1]:GetText(), c.titre_attendu)
        for k, att in ipairs(c.lignes_attendues) do
            egal(c.nom .. " (ligne " .. (k + 1) .. ")", WorldMapTooltip.lignes[k + 1] and WorldMapTooltip.lignes[k + 1]:GetText(), att)
        end
        POI_OBJECTIFS = {}
        JOURNAL = {}
        A.JournalAChange()
    elseif c.quoi == "memoire" then
        -- comme le client CoA (GarbageCollectionUtil.lua) : UpdateAddOnMemoryUsage ne fait rien tant que
        -- allowAddonMemoryUsage vaut 0, et GetAddOnMemoryUsage rend alors 0
        local CVAR = "0"
        local MEM = {}
        function GetCVar(n) if n == "allowAddonMemoryUsage" then return CVAR end end
        function UpdateAddOnMemoryUsage() if CVAR == "1" then MEM.Azeroth_FR = 2048 end end
        function GetAddOnMemoryUsage(n) return MEM[n] or 0 end
        local function Stats()
            local avant = #messages
            SlashCmdList.AZFR("stats")
            for k = avant + 1, #messages do
                if string.find(messages[k], "mémoire : add-ons Azeroth_FR", 1, true) then return messages[k] end
            end
        end
        local m1 = Stats()
        noter(m1 and string.find(m1, "MESURE APPROCHÉE", 1, true) and not string.find(m1, "Azeroth_FR 0 Ko", 1, true) and true or false,
            c.nom .. " (option du client à 0 : repli sur collectgarbage, dit comme tel)", m1)
        local n = m1 and tonumber(string.match(m1, "≈ (%d+) Ko"))
        noter(n ~= nil and n > 0, c.nom .. " (estimation non nulle)", n and (n .. " Ko") or nil)
        CVAR = "1"
        local m2 = Stats()
        noter(m2 and string.find(m2, "2048 Ko (mesure du jeu", 1, true) and true or false,
            c.nom .. " (option du client à 1 : UpdateAddOnMemoryUsage puis GetAddOnMemoryUsage)", m2)
        GetCVar, UpdateAddOnMemoryUsage, GetAddOnMemoryUsage = nil, nil, nil
    elseif c.quoi == "gossip_quete" then
        UNITES.npc = nil
        GossipGreetingText:SetText("")
        GossipTitleButton1:SetText(c.anglais)
        GossipFrameUpdate()
        egal(c.nom, GossipTitleButton1:GetText(), c.attendu)
    end
    for k, v in pairs(sauve) do _G[k] = v end
end

-- Coupure : /azfr off -> plus rien n'est traduit ; /azfr on -> de nouveau.
JOUEUR.sexe = 2; JOUEUR.classe = "Warrior"; A.LireJoueur()
SlashCmdList.AZFR("off")
noter(A.Actif() == false, "/azfr off coupe l'affichage")
local r = { false }
for _, f in ipairs(filtres.CHAT_MSG_MONSTER_SAY or {}) do r = { f(nil, "CHAT_MSG_MONSTER_SAY", "x", "y") } end
noter(r[1] == false and r[2] == nil, "filtre inactif quand coupe")
SlashCmdList.AZFR("on")
noter(A.Actif() == true, "/azfr on reactive l'affichage")
SlashCmdList.AZFR("version")
SlashCmdList.AZFR("stats")
SlashCmdList.AZFR("n'importe quoi")
noter(A.Erreurs == 0, "aucune erreur evitee pendant les cas", A.DerniereErreur)

-- 0.9.6 : panneau d'options (menu Interface > AddOns > Azeroth_FR), memes reglages que les commandes
local P = A.Options and A.Options()
noter(P ~= nil and PANNEAUX_OPTIONS[1] == P and P.name == "Azeroth_FR", "panneau d'options inscrit dans le menu Interface")
if P then
    SlashCmdList.AZFR("")
    noter(PANNEAU_OUVERT == P, "/azfr tout seul ouvre le panneau d'options")
    P.refresh()
    noter(P.francais:GetChecked() == 1 and P.cases.bulles:GetChecked() == 1, "panneau : cases cochées au départ")
    P.francais:Click()
    noter(A.Actif() == false and P.cases.bulles.desactive == true, "panneau : décocher « Jeu en français » coupe la traduction et grise les parties")
    P.francais:Click()
    noter(A.Actif() == true and P.cases.bulles.desactive == false, "panneau : recocher la remet")
    P.cases.plaques:Click()
    noter(A.ModuleActif("plaques") == false and A.ModuleActif("bulles") == true, "panneau : case « Plaques de nom » coupe ce module seul")
    P.cases.plaques:Click()
    noter(A.ModuleActif("plaques") == true, "panneau : case « Plaques de nom » le remet")
    -- 1.1.1 : adresse du Discord
    noter(P.discord ~= nil and P.discord:GetText() == "discord.gg/kFJGDJbeay", "panneau : adresse du Discord affichée")
    -- 1.0.1 : encart « Soutenir le createur »
    noter(P.lien ~= nil and P.lien:GetText() == A.LIEN_SOUTIEN and A.LIEN_SOUTIEN == "buymeacoffee.com/LePetitDan", "panneau : adresse de soutien affichée")
    if P.lien then
        P.lien:SetText("autre chose")
        noter(P.lien:GetText() == A.LIEN_SOUTIEN, "panneau : l'adresse de soutien ne peut pas être modifiée")
    end
end
-- 1.2.0 : /azfr signaler, compte rendu prêt à copier
do
    local avant = { GetRealZoneText, GetSubZoneText, GetMouseFocus, A.VERSION }
    GetRealZoneText = function() return "Forêt d'Elwynn" end
    GetSubZoneText = function() return "Comté-de-l'Or" end
    GetMouseFocus = function() return nil end
    A.VERSION = "1.2.0"
    GameTooltip:Effacer({ "|cffffffffNom affiché|r", "Deuxième `ligne`" }, nil, nil, nil, nil)
    GameTooltip.visible = true
    if not GameTooltip.IsShown or not GameTooltip:IsShown() then function GameTooltip:IsShown() return true end end
    local t = A.TexteSignalement()
    noter(string.find(t, "[Azeroth_FR 1.2.0] Signalement", 1, true) ~= nil, "signaler : la version est dans le compte rendu")
    noter(string.find(t, "Zone : Forêt d'Elwynn / Comté-de-l'Or", 1, true) ~= nil, "signaler : la zone est dans le compte rendu")
    noter(string.find(t, "  Nom affiché", 1, true) ~= nil and string.find(t, "|c", 1, true) == nil, "signaler : texte de l'infobulle, sans codes de couleur")
    noter(string.find(t, "`", 1, true) == nil, "signaler : pas d'accent grave (il casserait le bloc Discord)")
    noter(string.find(t, "Ce qui ne va pas", 1, true) ~= nil, "signaler : une ligne à compléter")
    SlashCmdList["AZFR"]("signaler")
    local f = A.FenetreSignalement()
    noter(f ~= nil and f.zone ~= nil and string.sub(f.zone:GetText() or "", 1, 4) == "```\n", "signaler : /azfr signaler ouvre la fenêtre avec le bloc à copier")
    if f then
        f.zone:SetText("autre chose")
        noter(f.zone:GetText() == f.texte, "signaler : le compte rendu ne se modifie pas dans la fenêtre")
    end
    GetRealZoneText, GetSubZoneText, GetMouseFocus, A.VERSION = avant[1], avant[2], avant[3], avant[4]
end
-- 1.1.0 : « une nouvelle version est disponible » (messages entre add-ons : guilde, groupe)
do
    noter(A.VersionPlusRecente("1.10.0", "1.9.9") and not A.VersionPlusRecente("1.0.0", "1.0.0") and not A.VersionPlusRecente("abc", "1.0.0") and not A.VersionPlusRecente("999999999999999.0.0", "1.0.0"), "version : comparaison des numéros")
    local envois, messages = {}, {}
    local avant = { SendAddonMessage, IsInGuild, GetTime, GetNumRaidMembers, GetNumPartyMembers, DEFAULT_CHAT_FRAME, A.VERSION }
    local heure = 1000
    SendAddonMessage = function(p, m, c) table.insert(envois, p .. "|" .. m .. "|" .. c) end
    IsInGuild = function() return true end
    GetTime = function() return heure end
    GetNumRaidMembers = function() return 0 end
    GetNumPartyMembers = function() return 0 end
    DEFAULT_CHAT_FRAME = { AddMessage = function(_, m) table.insert(messages, m) end }
    A.VERSION = "1.1.0"
    AzerothFR_Reglages.version_vue = nil
    Declencher("PLAYER_ENTERING_WORLD")
    egal("version : annonce à la guilde à l'entrée en jeu", envois[1], "AZFR|V:1.1.0|GUILD")
    noter(#messages == 0 and A.NouvelleVersion() == nil, "version : rien à signaler tant qu'aucune version plus récente n'est vue")
    Declencher("CHAT_MSG_ADDON", "AUTRE", "V:9.0.0", "GUILD", "Quelquun")
    Declencher("CHAT_MSG_ADDON", "AZFR", "V:9.0.0; os.exit()", "GUILD", "Quelquun")
    Declencher("CHAT_MSG_ADDON", "AZFR", "n'importe quoi", "GUILD", "Quelquun")
    noter(A.NouvelleVersion() == nil and #messages == 0, "version : préfixe étranger et messages mal formés ignorés")
    Declencher("CHAT_MSG_ADDON", "AZFR", "V:1.2.0", "GUILD", "Quelquun")
    egal("version : une version plus récente est retenue", A.NouvelleVersion(), "1.2.0")
    noter(#messages == 1 and string.find(messages[1], "1.2.0", 1, true) ~= nil and string.find(messages[1], "installateur", 1, true) ~= nil, "version : le joueur est prévenu dans la discussion")
    Declencher("CHAT_MSG_ADDON", "AZFR", "V:1.2.0", "GUILD", "Quelquun")
    Declencher("CHAT_MSG_ADDON", "AZFR", "V:1.3.0", "GUILD", "Quelquun")
    noter(#messages == 1 and A.NouvelleVersion() == "1.3.0", "version : prévenu une seule fois par session, la plus récente retenue")
    local Pm = A.Options and A.Options()
    if Pm and Pm.maj then
        Pm.refresh()
        noter(string.find(Pm.maj:GetText() or "", "1.3.0", 1, true) ~= nil, "version : affichée dans le panneau d'options")
    end
    local n = #envois
    heure = heure + 120
    Declencher("CHAT_MSG_ADDON", "AZFR", "V:1.0.0", "PARTY", "Quelquun")
    egal("version : réponse à un joueur en retard", envois[n + 1], "AZFR|V:1.1.0|PARTY")
    Declencher("CHAT_MSG_ADDON", "AZFR", "V:1.0.0", "PARTY", "Quelquun")
    noter(#envois == n + 1, "version : au plus un envoi par minute et par canal")
    Declencher("CHAT_MSG_ADDON", "AZFR", "V:1.0.0", "WHISPER", "Quelquun")
    noter(#envois == n + 1, "version : pas de réponse en message privé")
    A.VERSION = "1.3.0"
    Declencher("PLAYER_ENTERING_WORLD")
    noter(AzerothFR_Reglages.version_vue == nil and A.NouvelleVersion() == nil, "version : après la mise à jour, l'information est oubliée")
    SendAddonMessage, IsInGuild, GetTime, GetNumRaidMembers, GetNumPartyMembers, DEFAULT_CHAT_FRAME, A.VERSION = avant[1], avant[2], avant[3], avant[4], avant[5], avant[6], avant[7]
    if Pm then Pm.refresh() end
end
-- 1.0.1 : carte du monde, zone survolee avec ses niveaux (ajout du client CoA) et listes deroulantes
do
    local fr = A.NomZone("Western Plaguelands")
    noter(fr ~= nil and fr ~= "Western Plaguelands", "carte : « Western Plaguelands » a un nom français (" .. tostring(fr) .. ")")
    if fr then
        egal("carte : zone survolée avec niveaux colorés", A.NomZoneAvecNiveaux("Western Plaguelands |cffff2020(51-60)|r"), fr .. " |cffff2020(51-60)|r")
        egal("carte : zone survolée avec niveaux sans couleur", A.NomZoneAvecNiveaux("Western Plaguelands (51-60)"), fr .. " (51-60)")
        egal("carte : nom inconnu avec niveaux, laissé", A.NomZoneAvecNiveaux("Zzz Inconnue (1-5)"), nil)
        local avant = { UIDROPDOWNMENU_OPEN_MENU, DropDownList1, DropDownList1Button1, DropDownList1Button2 }
        DropDownList1 = NouveauCadre(nil); DropDownList1.visible = true
        if not DropDownList1.IsShown then function DropDownList1:IsShown() return true end end
        local b1, b2 = NouvelleZone("Western Plaguelands"), NouvelleZone("Zzz Inconnue")
        DropDownList1Button1, DropDownList1Button2 = b1, b2
        UIDROPDOWNMENU_OPEN_MENU = "AutreListe"
        A.TraduireListeCarte()
        egal("carte : une autre liste déroulante n'est pas touchée", b1:GetText(), "Western Plaguelands")
        UIDROPDOWNMENU_OPEN_MENU = "WorldMapZoneDropDown"
        A.TraduireListeCarte()
        egal("carte : ligne de la liste « Zone » en français", b1:GetText(), fr)
        egal("carte : ligne inconnue de la liste laissée", b2:GetText(), "Zzz Inconnue")
        UIDROPDOWNMENU_OPEN_MENU, DropDownList1, DropDownList1Button1, DropDownList1Button2 = avant[1], avant[2], avant[3], avant[4]
    end
end

-- Aucune variable globale du jeu ecrite : seules les globales de l'add-on sont nouvelles.
local permises = { AzerothFR = true, AzerothFR_Reglages = true, SLASH_AZFR1 = true, AzerothFR_Interface = true,
    AzerothFR_Etiquette1 = true, AzerothFR_Etiquette2 = true, AzerothFR_Etiquette3 = true }
local intrus = {}
for k, v in pairs(_G) do
    -- (les lignes AzerothFR_EtiquetteNTextLeftM appartiennent a nos propres infobulles d'essai)
    if type(k) == "string" and string.find(k, "^Azeroth") and not permises[k]
        and not string.find(k, "^AzerothFR_Etiquette%dText") then intrus[#intrus + 1] = k end
end
for k in pairs(GLOBALES or {}) do
    if _G[k] ~= GLOBALES[k] then intrus[#intrus + 1] = k .. " (modifiee)" end
end
noter(#intrus == 0, "aucune globale du jeu ecrite par l'add-on", #intrus > 0 and table.concat(intrus, ", ") or nil)

-- Une erreur dans un crochet ne doit jamais remonter au joueur.
local ok = pcall(A.Proteger("essai", function() error("boum") end))
noter(ok and A.Erreurs == 1, "erreur dans un crochet : comptee, jamais visible")

-- Memoire par famille : chargee (morceaux non compiles) puis tout compile (pire cas : le joueur
-- aurait vu tous les textes de la famille).
local function ToutCompiler(tables)
    local n = 0
    for nom, t in pairs(tables) do
        local seaux = {}
        for s in pairs(t.morceaux) do seaux[#seaux + 1] = s end
        for _, s in ipairs(seaux) do t:Seau(s); n = n + 1 end
    end
    return n
end
local familles_vues = {}
for addon, m in pairs(MESURES_FAMILLES) do
    if not familles_vues[m.famille] and A.Tables[m.famille] then
        familles_vues[m.famille] = true
        collectgarbage("collect")
        local avant = collectgarbage("count")
        local n = ToutCompiler(A.Tables[m.famille])
        collectgarbage("collect")
        print(string.format("MESURE  famille %-10s : chargee +%.1f Mo en %.0f ms ; tout compile : +%.1f Mo de plus (%d seaux)",
            m.famille, m.charge, m.ms, (collectgarbage("count") - avant) / 1024, n))
    end
end
collectgarbage("collect")
print(string.format("MESURE  familles de la connexion entierement compilees : memoire Lua %.1f Mo", collectgarbage("count") / 1024))

-- Tranches (objets, sorts) et index : chacun charge seul, memoire et duree.
for _, f in ipairs(A.FAMILLES) do
    if not f.auto and not charges[f.addon] then
        collectgarbage("collect")
        local m0, c0 = collectgarbage("count"), os.clock()
        LoadAddOn(f.addon)
        local d = (os.clock() - c0) * 1000
        collectgarbage("collect")
        local m1 = collectgarbage("count")
        print(string.format("MESURE  %s (%s%s) : chargee +%.1f Mo en %.0f ms", f.addon, f.famille,
            f.debut and string.format(" %d a %d", f.debut, f.fin) or "", (m1 - m0) / 1024, d))
    end
end
for fam, tables in pairs(A.Tables) do ToutCompiler(tables) end
collectgarbage("collect")
print(string.format("MESURE  pire cas, tout charge et tout compile : memoire Lua %.1f Mo", collectgarbage("count") / 1024))

print(string.format("\nBANC : %d exemples, %d verifications OK, %d KO", resultats.exemples, resultats.ok, resultats.ko))
os.exit(resultats.ko == 0 and 0 or 1)
