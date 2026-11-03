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
function InCombatLockdown() return false end
function GetLocale() return "enUS" end
function strtrim(s) return (string.match(s, "^%s*(.-)%s*$")) end

JOUEUR = { nom = "Thalwyn", race = "Night Elf", classe = "Warrior", sexe = 2 }
UNITES = {}
function UnitName(u) if u == "player" then return JOUEUR.nom end return UNITES[u] and UNITES[u].nom end
function GetUnitName(u) return UnitName(u) end
function UnitRace(u) return JOUEUR.race end
function UnitClass(u) return JOUEUR.classe end
function UnitSex(u) return JOUEUR.sexe end
function UnitIsPlayer(u) return u == "player" or (UNITES[u] and UNITES[u].joueur) or false end
function UnitExists(u) return u == "player" or UNITES[u] ~= nil end
function UnitGUID(u) return UNITES[u] and UNITES[u].guid end

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
    function z:SetTextColor() end
    function z:SetFontFlags() end
    function z:SetFontObject() end
    function z:ClearAndSetPoint() end
    function z:SetPoint() end
    function z:ClearAllPoints() end
    function z:SetAlphaGradient() end
    return z
end

local evenements = {}       -- evenement -> liste de cadres
local function NouveauCadre(nom)
    local c = { scripts = {}, crochets = {}, visible = false, regions = {}, enfants = {}, hauteur = 16 }
    function c:RegisterEvent(e) evenements[e] = evenements[e] or {}; table.insert(evenements[e], self) end
    function c:UnregisterEvent() end
    function c:UnregisterAllEvents() end
    function c:SetScript(k, f) self.scripts[k] = f end
    function c:GetScript(k) return self.scripts[k] end
    function c:HookScript(k, f) self.crochets[k] = self.crochets[k] or {}; table.insert(self.crochets[k], f) end
    function c:IsShown() return self.visible end
    function c:Show() self.visible = true end
    function c:Hide() self.visible = false end
    function c:IsProtected() return false end
    function c:GetRegions() return unpack(self.regions) end
    function c:GetChildren() return unpack(self.enfants) end
    function c:GetName() return nom end
    function c:SetHeight(h) self.hauteur = h end
    function c:GetHeight() return self.hauteur end
    function c:SetPoint() end
    function c:ClearAllPoints() end
    function c:SetOwner(o) self.proprio = o end
    function c:IsOwned(o) return self.proprio == o end
    if nom then _G[nom] = c end
    return c
end

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
        if o then self:Effacer(o.lignes, { o.nom, LienObjet(id, o.nom) }) else self:Effacer({}) end
    end
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
GameTooltip = NouvelleBulle("GameTooltip")
ItemRefTooltip = NouvelleBulle("ItemRefTooltip")
UIParent = NouveauCadre("UIParent")
function CreateFrame(genre, nom, parent, modele)
    if genre == "GameTooltip" then return NouvelleBulle(nom) end
    return NouveauCadre(nom)
end

local function Declencher(e, ...)
    for _, c in ipairs(evenements[e] or {}) do
        if c.scripts.OnEvent then c.scripts.OnEvent(c, e, ...) end
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
function Minimap_Update() MinimapZoneText:SetText(GetMinimapZoneText()) end
function Minimap_SetTooltip() end
ZoneTextFrame, SubZoneTextFrame = NouveauCadre("ZoneTextFrame"), NouveauCadre("SubZoneTextFrame")
ZoneTextString, SubZoneTextString = NouvelleZone(""), NouvelleZone("")
WorldMapButton, WorldMapFrameAreaLabel = NouveauCadre("WorldMapButton"), NouvelleZone("")

-- Grimoire d'Ascension : un bouton (securise dans le jeu ; ici un simple cadre)
AscensionSpellbookFrame = NouveauCadre("AscensionSpellbookFrame")
local boutonGrimoire = NouveauCadre("AscensionSpellbookFrameSpellButton1")
boutonGrimoire.SpellName, boutonGrimoire.SubSpellName = NouvelleZone(""), NouvelleZone("")
boutonGrimoire.visible = true
AscensionSpellbookFrame.enfants = { boutonGrimoire }

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
        GameTooltip:Effacer(c.lignes, { c.anglais, LienObjet(c.id, c.anglais) })
        if c.sort_objet then ITEM_SPELLS[c.id] = { "x", c.sort_objet } else ITEM_SPELLS[c.id] = nil end
        GameTooltip:Declencher("OnTooltipSetItem")
        egal(c.nom .. " (nom)", GameTooltip.lignes[1]:GetText(), c.attendu)
        if c.description_attendue then
            egal(c.nom .. " (ligne " .. c.ligne_description .. ")", GameTooltip.lignes[c.ligne_description]:GetText(),
                c.description_attendue)
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
        local args = { c.message, c.emetteur or "", "", c.arg4 or "", "", "", 0, 0, "", 0, 0, nil }
        local r = Filtrer(c.evenement, args)
        egal(c.nom, r and r[c.champ or 1], c.attendu)
    elseif c.quoi == "journal_entete" then
        JOURNAL = { { titre = c.anglais, entete = 1 } }
        A.JournalAChange()
        egal(c.nom, A.CorrespondancesJournal()[c.anglais], c.attendu)
        JOURNAL = {}
        A.JournalAChange()
    elseif c.quoi == "minicarte" then
        ZONE_MINICARTE = c.anglais
        Minimap_Update()
        egal(c.nom, MinimapZoneText:GetText(), c.attendu)
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
        SlashCmdList.AZFR("etiquettes")
        for i, attendu in ipairs(c.attendus) do
            local b = _G["AzerothFR_Etiquette" .. i]
            egal(c.nom .. " (objet " .. i .. ", nom)", b and b.lignes[1] and b.lignes[1]:GetText(), attendu[1])
            egal(c.nom .. " (objet " .. i .. ", étiquette)", b and b.lignes[2] and b.lignes[2]:GetText(), attendu[2])
        end
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
