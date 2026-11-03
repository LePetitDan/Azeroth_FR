-- ============================================================================
-- Azeroth_FR : quetes.
-- Fenetre de quete (detail, progression, recompense), journal des quetes, suivi des
-- objectifs, accueil des donneurs de quetes. Par numero quand le jeu le donne (journal),
-- sinon par texte anglais exact. Affichage seulement.
-- ============================================================================
local A = AzerothFR
local match, find, sub, format = string.match, string.find, string.sub, string.format
local P = A.Proteger

local function QT() return A.TableDe("quetes", "QT") end
local function QI() return A.TableDe("quetes", "QI") end

-- Texte de quete (titre, description, objectifs, progression, recompense…) par texte anglais.
function A.TexteQuete(texte)
    return A.Traduire(QT(), texte)
end

-- Titre par numero de quete, verifie : l'anglais affiche doit etre celui qu'on a traduit.
function A.TitreParId(id, titreEN)
    local qi = QI()
    if not qi or not id then return nil end
    local r = qi:ParId(id)
    if type(r) ~= "table" or not r[1] then return nil end
    if titreEN and A.H1(titreEN) ~= r[2] then return nil end
    return A.Rendre(r[1])
end

-- Numero de la quete proposee par un PNJ, si le client le donne (GetQuestID n'existait
-- pas sur le client d'Ascension).
local function IdQueteOfferte()
    if type(GetQuestID) == "function" then
        local ok, id = pcall(GetQuestID)
        if ok and type(id) == "number" and id > 0 then return id end
    end
    return nil
end

-- Titre (avec ou sans habillage « [12] » ou couleur) : par la table du journal, par numero,
-- puis par texte.
local function Titre(texte, corr, id)
    if not texte or texte == "" then return nil end
    local fr = corr and corr[texte]
    if fr then return fr end
    if id then
        fr = A.TitreParId(id, texte)
        if fr then return fr end
    end
    fr = A.TexteQuete(texte)
    if fr then return fr end
    local couleur, nu = match(texte, "^(|c%x%x%x%x%x%x%x%x)(.-)|r$")
    if nu and nu ~= "" then
        fr = (corr and corr[nu]) or A.TexteQuete(nu)
        if fr then return couleur .. fr .. "|r" end
    end
    local pre, corps = match(texte, "^(%s*%[[^%]]*%]%s*)(.+)$")
    if not pre then pre, corps = match(texte, "^(%s+)(.+)$") end
    if corps then
        fr = (corr and corr[corps]) or A.TexteQuete(corps)
        if fr then return pre .. fr end
    end
    return nil
end
A.TitreQuete = Titre

-- ----------------------------------------------------------------------------
-- Lignes d'objectifs : « Kobold Vermin slain: 3/8 », « Linen Cloth: 2/10 »,
-- « Remember your talents ». Le nom passe par : le texte d'objectif de la quete, le nom
-- de creature, le nom d'objet (cache du client -> numero -> table des objets).
-- ----------------------------------------------------------------------------
local function NomObjectif(nom)
    local fr = A.TexteQuete(nom)
    if fr then return fr end
    fr = A.NomCreature(nom)
    if fr then return fr end
    if type(GetItemInfo) == "function" then
        local ok, _, lien = pcall(GetItemInfo, nom)
        local id = ok and A.IdDepuisLien(lien, "item")
        local o = id and A.Objet(id)
        if type(o) == "table" and o[1] and A.H1(nom) == o[2] then return o[1] end
    end
    return nil
end

function A.TraduireObjectif(texte)
    if type(texte) ~= "string" or texte == "" then return nil end
    local pre, nom, x, y, reste = match(texte, "^([%s%-]*)(.-) slain: (%d+)/(%d+)(.*)$")
    if nom and nom ~= "" then
        local fr = NomObjectif(nom)
        if fr then return pre .. fr .. " tué(s) : " .. x .. "/" .. y .. reste end
        return nil
    end
    pre, nom, x, y, reste = match(texte, "^([%s%-]*)(.-):%s*(%d+)%s*/%s*(%d+)(.*)$")
    if nom and nom ~= "" then
        local fr = NomObjectif(nom)
        if fr then return pre .. fr .. " : " .. x .. "/" .. y .. reste end
        return nil
    end
    pre, nom = match(texte, "^([%s%-]*)(.+)$")
    if nom then
        local fr = A.TexteQuete(nom)
        if fr then return pre .. fr end
    end
    return nil
end

-- ----------------------------------------------------------------------------
-- Correspondances du journal : titre anglais -> titre francais, par numero de quete
-- (GetQuestLink). Reconstruites a chaque mise a jour du journal.
-- ----------------------------------------------------------------------------
local corr_journal, corr_a_refaire = {}, true

local function CorrespondancesJournal()
    if not corr_a_refaire then return corr_journal end
    corr_a_refaire = false
    local corr = {}
    if type(GetNumQuestLogEntries) == "function" then
        for i = 1, (GetNumQuestLogEntries() or 0) do
            local titre, _, _, _, entete = GetQuestLogTitle(i)
            if titre and titre ~= "" and not entete then
                local id = A.IdDepuisLien(GetQuestLink(i), "quest")
                local fr = (id and A.TitreParId(id, titre)) or A.TexteQuete(titre)
                if fr then corr[titre] = fr end
            end
        end
    end
    corr_journal = corr
    return corr
end
A.CorrespondancesJournal = CorrespondancesJournal

-- Une zone de texte de quete : titre, texte long ou objectif.
local function TraduireZone(zone, corr)
    if not zone or not zone.GetText then return end
    local texte = zone:GetText()
    if not texte or texte == "" or A.DejaEcrit(zone, texte) then return end
    local fr = Titre(texte, corr) or A.TraduireObjectif(texte)
    if fr and fr ~= texte then A.Ecrire(zone, fr) end
end

-- Parcourt un cadre (non protege) et traduit toutes ses zones de texte reconnues : le
-- client de CoA (herite d'Ascension) a reecrit certaines fenetres, on ne nomme donc pas
-- tous les cadres.
local function Parcourir(cadre, corr, profondeur)
    if not cadre or profondeur > 7 or A.EstProtege(cadre) then return end
    if cadre.GetRegions then
        local regions = { cadre:GetRegions() }
        for i = 1, #regions do
            local r = regions[i]
            if r and r.GetObjectType and r:GetObjectType() == "FontString" then TraduireZone(r, corr) end
        end
    end
    if cadre.GetChildren then
        local enfants = { cadre:GetChildren() }
        for i = 1, #enfants do Parcourir(enfants[i], corr, profondeur + 1) end
    end
end

-- ----------------------------------------------------------------------------
-- Fenetre de quete (PNJ) et detail du journal : QuestInfo_Display est partage.
-- ----------------------------------------------------------------------------
local ZONES_QUETE = { "QuestInfoTitleText", "QuestInfoDescriptionText", "QuestInfoObjectivesText",
    "QuestInfoRewardText", "QuestProgressTitleText", "QuestProgressText" }

local function NomsRecompenses(journal)
    for i = 1, 12 do
        local bouton = _G["QuestInfoItem" .. i]
        if not bouton then break end
        local zone = _G["QuestInfoItem" .. i .. "Name"]
        if zone and bouton:IsShown() and bouton.type and bouton.rewardType ~= "spell" then
            local lien
            if journal then lien = GetQuestLogItemLink(bouton.type, bouton:GetID())
            else lien = GetQuestItemLink(bouton.type, bouton:GetID()) end
            local id = A.IdDepuisLien(lien, "item")
            local o = id and A.Objet(id)
            local texte = zone:GetText()
            if type(o) == "table" and o[1] and texte and A.H1(texte) == o[2] then A.Ecrire(zone, o[1]) end
        end
    end
end

local function TraduireFenetreQuete()
    if not A.Actif() then return end
    local journal = QuestInfoFrame and QuestInfoFrame.questLog
    local corr = CorrespondancesJournal()
    if not journal then
        -- fenetre d'un PNJ : le titre par numero si le client le donne
        local id = IdQueteOfferte()
        local zone = QuestInfoTitleText
        local texte = zone and zone:GetText()
        if id and texte and not A.DejaEcrit(zone, texte) then
            local fr = A.TitreParId(id, texte)
            if fr then A.Ecrire(zone, fr) end
        end
    end
    for _, nom in ipairs(ZONES_QUETE) do TraduireZone(_G[nom], corr) end
    for i = 1, 10 do
        local ligne = _G["QuestInfoObjective" .. i]
        if ligne and ligne:IsShown() then TraduireZone(ligne, corr) end
    end
    NomsRecompenses(journal)
    if QuestFrame and QuestFrame:IsShown() then Parcourir(QuestFrame, corr, 0) end
end

if type(QuestInfo_Display) == "function" then
    hooksecurefunc("QuestInfo_Display", P("QuestInfo_Display", TraduireFenetreQuete))
end

-- Progression (« Avez-vous les objets ? ») et accueil des donneurs de plusieurs quetes.
local function TraduireAccueil()
    if not A.Actif() then return end
    TraduireZone(GreetingText, nil)
    for i = 1, 32 do
        local bouton = _G["QuestTitleButton" .. i]
        if not bouton then break end
        if bouton:IsShown() then
            local texte = bouton:GetText()
            if texte and texte ~= "" and not A.DejaEcrit(bouton, texte) then
                local fr = Titre(texte, nil)
                if fr then A.Ecrire(bouton, fr) end
            end
        end
    end
end

local f = CreateFrame("Frame")
f:RegisterEvent("QUEST_PROGRESS")
f:RegisterEvent("QUEST_GREETING")
f:RegisterEvent("QUEST_LOG_UPDATE")
f:SetScript("OnEvent", P("Quetes.OnEvent", function(self, evenement)
    if evenement == "QUEST_LOG_UPDATE" then corr_a_refaire = true; return end
    if not A.Actif() then return end
    if evenement == "QUEST_PROGRESS" then
        TraduireZone(QuestProgressTitleText, CorrespondancesJournal())
        TraduireZone(QuestProgressText, nil)
    elseif evenement == "QUEST_GREETING" then
        TraduireAccueil()
    end
end))

-- ----------------------------------------------------------------------------
-- Journal des quetes : la liste est redessinee sans toujours passer par QuestLog_Update
-- (lecon d'AscensionFR) : on repasse 5 fois par seconde, seulement journal ouvert.
-- ----------------------------------------------------------------------------
local function TraduireJournal()
    if not A.Actif() or not QuestLogFrame or not QuestLogFrame:IsShown() then return end
    Parcourir(QuestLogFrame, CorrespondancesJournal(), 0)
end

if type(QuestLog_Update) == "function" then
    hooksecurefunc("QuestLog_Update", P("QuestLog_Update", TraduireJournal))
end

local arme = false
local function ArmerPulsation()
    if arme or not QuestLogFrame then return end
    arme = true
    local guetteur = CreateFrame("Frame", nil, QuestLogFrame)
    local cumul = 0
    guetteur:SetScript("OnUpdate", P("Quetes.pulsation", function(_, ecoule)
        cumul = cumul + (ecoule or 0)
        if cumul < 0.2 then return end
        cumul = 0
        TraduireJournal()
    end))
end
ArmerPulsation()

-- ----------------------------------------------------------------------------
-- Suivi des objectifs (a droite de l'ecran) : on n'atteint que les lignes par leur nom
-- (WatchFrameLineN.text), sans jamais parcourir le cadre : ses boutons d'objets sont
-- securises. Valable aussi en combat.
-- ----------------------------------------------------------------------------
local function TraduireSuivi()
    if not A.Actif() then return end
    local corr = CorrespondancesJournal()
    local i = 1
    while true do
        local ligne = _G["WatchFrameLine" .. i]
        if not ligne then break end
        local zone = ligne.text
        if zone and zone.GetText then
            local texte = zone:GetText()
            if texte and texte ~= "" and not A.DejaEcrit(zone, texte) then
                local fr = corr[texte] or A.TraduireObjectif(texte)
                if fr and fr ~= texte then A.Ecrire(zone, fr) end
            end
        end
        i = i + 1
    end
end

if type(WatchFrame_Update) == "function" then
    hooksecurefunc("WatchFrame_Update", P("WatchFrame_Update", TraduireSuivi))
end
