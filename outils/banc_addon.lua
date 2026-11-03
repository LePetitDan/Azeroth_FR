-- ============================================================================
-- Banc d'essai HORS JEU de l'add-on Azeroth_FR (Lua 5.1, comme le client 3.3.5).
-- Usage : lua5.1 outils/banc_addon.lua <dossier dist/Interface> <fichier de cas>
-- (lance par outils/tester_addon.py, qui choisit les cas dans textes/).
--
-- De fausses fonctions WoW, minimales : cadres, crochets, infobulles, unites, filtres de
-- discussion, LoadAddOn (lit le .toc et charge ses fichiers). Le coeur et les modules sont
-- charges tels quels, puis chaque cas est verifie.
-- ============================================================================
local RACINE, CAS = arg[1], arg[2]
local resultats = { ok = 0, ko = 0 }
local function noter(ok, nom, detail)
    if ok then resultats.ok = resultats.ok + 1 else resultats.ko = resultats.ko + 1 end
    print((ok and "OK  " or "KO  ") .. nom .. (detail and ("  " .. detail) or ""))
end

-- ----------------------------------------------------------------------------
-- Faux environnement WoW
-- ----------------------------------------------------------------------------
local horloge = 0
function debugprofilestop() return os.clock() * 1000 end
function InCombatLockdown() return false end
function GetLocale() return "enUS" end
function strtrim(s) return (string.match(s, "^%s*(.-)%s*$")) end

local JOUEUR = { nom = "Thalwyn", race = "Night Elf", classe = "Warrior", sexe = 2 }
function UnitName(u) if u == "player" then return JOUEUR.nom end return UNITES and UNITES[u] and UNITES[u].nom end
function UnitRace(u) return JOUEUR.race end
function UnitClass(u) return JOUEUR.classe end
function UnitSex(u) return JOUEUR.sexe end
function UnitIsPlayer(u) return u == "player" end
function UnitGUID(u) return UNITES and UNITES[u] and UNITES[u].guid end
function GetItemInfo(nom) return nil end

-- Zones de texte et cadres
local function NouvelleZone(texte)
    local z = { texte = texte, visible = true }
    function z:GetText() return self.texte end
    function z:SetText(t) self.texte = t end
    function z:IsShown() return self.visible end
    function z:GetObjectType() return "FontString" end
    function z:GetTextHeight() return 12 end
    function z:SetHeight() end
    return z
end

local evenements = {}       -- evenement -> liste de cadres
local function NouveauCadre(nom)
    local c = { scripts = {}, crochets = {}, visible = false, regions = {}, enfants = {} }
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
    if nom then _G[nom] = c end
    return c
end
function CreateFrame(_, nom, parent) return NouveauCadre(nom) end

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

-- Infobulles
local function NouvelleBulle(nom)
    local b = NouveauCadre(nom)
    b.lignes = {}
    function b:Effacer(lignes, objet, unite)
        self.lignes = {}
        for i, t in ipairs(lignes) do
            local z = NouvelleZone(t)
            _G[nom .. "TextLeft" .. i] = z
            self.lignes[i] = z
        end
        self.objet, self.unite = objet, unite
        self.visible = true
    end
    function b:NumLines() return #self.lignes end
    function b:GetItem() if self.objet then return self.objet[1], self.objet[2] end end
    function b:GetUnit() if self.unite then return UNITES[self.unite].nom, self.unite end end
    function b:Declencher(script) for _, f in ipairs(self.crochets[script] or {}) do f(self) end end
    return b
end
GameTooltip = NouvelleBulle("GameTooltip")
ItemRefTooltip = NouvelleBulle("ItemRefTooltip")
UNITES = {}

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
function GossipFrameUpdate() end
function GossipResize(b) end
QuestInfoTitleText = NouvelleZone(nil)
QuestInfoDescriptionText = NouvelleZone(nil)
QuestInfoObjectivesText = NouvelleZone(nil)
QuestInfoRewardText = NouvelleZone(nil)
QuestProgressTitleText = NouvelleZone(nil)
QuestProgressText = NouvelleZone(nil)
QuestInfoObjective1 = NouvelleZone(nil)
QuestInfoFrame = { questLog = false }
function QuestInfo_Display() end
WatchFrameLine1 = { text = NouvelleZone(nil) }
function WatchFrame_Update() end
function GetNumQuestLogEntries() return 0 end
function ItemTextGetText() return ITEM_TEXT end
ItemTextPageText = NouvelleZone(nil)

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
-- Chargement du coeur (comme le jeu : fichiers du .toc), connexion
-- ----------------------------------------------------------------------------
collectgarbage("collect")
local mem0 = collectgarbage("count")
assert(LoadAddOn("Azeroth_FR"))
local A = AzerothFR
noter(type(A) == "table" and A.VERSION ~= nil, "coeur charge", "version " .. tostring(A and A.VERSION))
noter(type(SlashCmdList.AZFR) == "function" and SLASH_AZFR1 == "/azfr", "commande /azfr enregistree")

local t0 = os.clock()
Declencher("PLAYER_LOGIN")
local duree = (os.clock() - t0) * 1000
collectgarbage("collect")
local mem1 = collectgarbage("count")
print(string.format("MESURE  connexion : familles auto chargees en %.0f ms ; memoire Lua %.1f Mo (avant : %.1f Mo)",
    duree, mem1 / 1024, mem0 / 1024))
for _, f in ipairs(A.FAMILLES) do
    if f.auto then noter(A.Charges[f.addon] == true, "famille chargee : " .. f.addon) end
end

-- ----------------------------------------------------------------------------
-- Cas (fichier ecrit par tester_addon.py) : CAS = { {quoi=…, …}, … }
-- ----------------------------------------------------------------------------
dofile(CAS)

local function egal(nom, obtenu, attendu)
    local ok = obtenu == attendu
    if ok then noter(true, nom) else
        noter(false, nom, "\n      obtenu  : " .. tostring(obtenu) .. "\n      attendu : " .. tostring(attendu))
    end
end

for _, c in ipairs(CAS_LISTE) do
    JOUEUR.sexe = c.sexe or 2
    A.LireJoueur()
    A.Memo = setmetatable({}, { __mode = "k" })
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
        egal(c.nom, A.TraduireObjectif(c.anglais), c.attendu)
    elseif c.quoi == "objet" then
        GameTooltip:Effacer(c.lignes, { c.anglais, "|cffffffff|Hitem:" .. c.id .. ":0:0:0:0:0:0:0:0|h[" .. c.anglais .. "]|h|r" })
        GameTooltip:Declencher("OnTooltipSetItem")
        egal(c.nom .. " (nom)", GameTooltip.lignes[1]:GetText(), c.attendu)
        if c.description_attendue then
            egal(c.nom .. " (description)", GameTooltip.lignes[c.ligne_description]:GetText(), c.description_attendue)
        end
    elseif c.quoi == "creature" then
        UNITES.mouseover = { nom = c.anglais, guid = c.guid }
        GameTooltip:Effacer(c.lignes, nil, "mouseover")
        GameTooltip:Declencher("OnTooltipSetUnit")
        egal(c.nom .. " (nom)", GameTooltip.lignes[1]:GetText(), c.attendu)
        if c.sous_titre_attendu then egal(c.nom .. " (sous-titre)", GameTooltip.lignes[2]:GetText(), c.sous_titre_attendu) end
    elseif c.quoi == "gossip" then
        GossipGreetingText:SetText(c.accueil)
        GossipTitleButton1:SetText(c.option)
        A.Ecrits = setmetatable({}, { __mode = "k" })
        GossipFrameUpdate()
        egal(c.nom .. " (accueil)", GossipGreetingText:GetText(), c.accueil_attendu)
        egal(c.nom .. " (option)", GossipTitleButton1:GetText(), c.option_attendue)
    elseif c.quoi == "fenetre_quete" then
        QuestInfoTitleText:SetText(c.titre); QuestInfoDescriptionText:SetText(c.description)
        QuestInfoObjectivesText:SetText(c.objectifs)
        A.Ecrits = setmetatable({}, { __mode = "k" })
        QuestInfo_Display()
        egal(c.nom .. " (titre)", QuestInfoTitleText:GetText(), c.titre_attendu)
        egal(c.nom .. " (description)", QuestInfoDescriptionText:GetText(), c.description_attendue)
        egal(c.nom .. " (objectifs)", QuestInfoObjectivesText:GetText(), c.objectifs_attendus)
    elseif c.quoi == "suivi" then
        WatchFrameLine1.text:SetText(c.anglais)
        A.Ecrits = setmetatable({}, { __mode = "k" })
        WatchFrame_Update()
        egal(c.nom, WatchFrameLine1.text:GetText(), c.attendu)
    elseif c.quoi == "livre" then
        ITEM_TEXT = c.anglais
        Declencher("ITEM_TEXT_READY")
        egal(c.nom, ItemTextPageText:GetText(), c.attendu)
    end
end

-- Coupure : /azfr off -> plus rien n'est traduit ; /azfr on -> de nouveau.
local premier = CAS_LISTE[1]
JOUEUR.sexe = 2; A.LireJoueur()
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

-- Une erreur dans un crochet ne doit jamais remonter au joueur.
local ok = pcall(A.Proteger("essai", function() error("boum") end))
noter(ok and A.Erreurs == 1, "erreur dans un crochet : comptee, jamais visible")

-- Memoire : tout compile (pire cas) pour les familles chargees a la connexion.
collectgarbage("collect")
local avant = collectgarbage("count")
local n = 0
for famille, tables in pairs(A.Tables) do
    for nom, t in pairs(tables) do
        local seaux = {}
        for s in pairs(t.morceaux) do seaux[#seaux + 1] = s end
        for _, s in ipairs(seaux) do t:Seau(s); n = n + 1 end
    end
end
collectgarbage("collect")
print(string.format("MESURE  pire cas : %d seaux compiles en plus ; memoire Lua %.1f Mo (au lieu de %.1f Mo)",
    n, collectgarbage("count") / 1024, avant / 1024))

-- Tranches d'objets : chacune chargee seule, memoire et duree.
for _, f in ipairs(A.FAMILLES) do
    if f.famille == "objets" and not charges[f.addon] then
        collectgarbage("collect")
        local m0, c0 = collectgarbage("count"), os.clock()
        LoadAddOn(f.addon)
        collectgarbage("collect")
        print(string.format("MESURE  %s (objets %d a %d) : +%.1f Mo, %.0f ms", f.addon, f.debut, f.fin,
            (collectgarbage("count") - m0) / 1024, (os.clock() - c0) * 1000))
    end
end
collectgarbage("collect")
print(string.format("MESURE  tout charge (sans compilation des objets) : memoire Lua %.1f Mo", collectgarbage("count") / 1024))

print(string.format("\nBANC : %d OK, %d KO", resultats.ok, resultats.ko))
os.exit(resultats.ko == 0 and 0 or 1)
