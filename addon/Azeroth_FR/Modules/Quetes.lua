-- ============================================================================
-- Azeroth_FR : quetes (version 0.2).
-- Fenetre de quete (detail, progression, recompense), journal des quetes, suivi des
-- objectifs, accueil des donneurs de quetes. Affichage seulement.
--
-- Reconnaissance d'une quete :
-- - journal : par NUMERO (9e valeur de GetQuestLogTitle, ou lien GetQuestLink) ;
-- - fenetre d'un PNJ (le client 3.3.5 ne donne pas de numero) : par le TITRE, puis, si
--   plusieurs quetes portent ce titre, celle dont un texte anglais correspond au texte
--   affiche (description, objectifs, recompense) ;
-- - textes : par texte anglais exact, variables $n $r $c $g $b reconstituees ($c = classe
--   en minuscules dans le client anglais : « young stormbringer »).
-- Un texte dont le francais n'est pas affichable (a_revoir, a_traduire…) reste en anglais.
-- ============================================================================
local A = AzerothFR
local match, find, sub, gsub, format = string.match, string.find, string.sub, string.gsub, string.format
local P = A.Proteger

local function QT() return A.TableDe("quetes", "QT") end
local function QI() return A.TableDe("quetes", "QI") end
local function QN() return A.TableDe("quetes", "QN") end

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

-- Numero de la quete proposee par un PNJ, si le client le donne (GetQuestID n'existe pas en
-- 3.3.5 ; certains clients l'ajoutent).
local function IdQueteOfferte()
    if type(GetQuestID) == "function" then
        local ok, id = pcall(GetQuestID)
        if ok and type(id) == "number" and id > 0 then return id end
    end
    return nil
end

-- Fenetre de quete : le numero par le titre affiche. textes = autres textes affiches (description,
-- objectifs…) servant a departager les quetes de meme titre. Renvoie le numero, ou nil.
function A.QueteParTitre(titreEN, textes)
    local qn = QN()
    if not qn or type(titreEN) ~= "string" or titreEN == "" then return nil end
    local ids = qn:ParTexte(A.Canon(titreEN))
    if type(ids) ~= "table" or #ids == 0 then return nil end
    if #ids == 1 then return ids[1] end
    local cles = {}
    for _, t in ipairs(textes or {}) do
        for _, c in ipairs(A.ClesCandidates(t)) do cles[c[1]] = true end
    end
    local qi, trouve = QI(), nil
    for _, id in ipairs(ids) do
        local r = qi and qi:ParId(id)
        if type(r) == "table" and type(r[3]) == "table" then
            for _, k in ipairs(r[3]) do
                if cles[k] then
                    if trouve and trouve ~= id then return nil end      -- deux quetes conviennent : ambigu
                    trouve = id
                    break
                end
            end
        end
    end
    return trouve
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
-- Lignes d'objectifs. Deux formes :
-- - Blizzard : « Kobold Vermin slain: 3/8 », « Linen Cloth: 2/10 » (fenetre, journal) ;
-- - ce client, dans le suivi : le compte d'abord, « 0/8 Kobold Vermin slain »
--   (WatchFrame_ReverseQuestObjective), parfois sans « slain » (QuestInfo_GetObjectivesText).
-- Le nom passe par : le texte d'objectif de la quete, le nom de creature, le nom d'objet
-- (cache du client -> numero -> table des objets). On rend la meme forme que l'anglais.
-- Gabarit francais : celui de la source (QUEST_MONSTERS_KILLED…) s'il est affichable, sinon
-- la formule de l'essai 1 « %s tué(s) : %d/%d ».
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
A.NomObjectif = NomObjectif

local GABARITS_OBJ = { "QUEST_MONSTERS_KILLED", "QUEST_ITEMS_NEEDED", "QUEST_OBJECTS_FOUND" }
local REPLI_FR = { QUEST_MONSTERS_KILLED = "%s tué(s) : %d/%d", QUEST_ITEMS_NEEDED = "%s : %d/%d",
    QUEST_OBJECTS_FOUND = "%s : %d/%d" }

local function Gabarit(cle)
    for _, g in ipairs(A.GABARITS or {}) do
        if g.cle == cle then return g end
    end
end
A.Gabarit = Gabarit

-- « %s slain: %d/%d » -> « %1$s slain: %2$d/%3$d » (pour pouvoir le retourner).
local function Positionnel(g)
    local n = 0
    return (gsub(g, "%%(%%?)(%d*%$?)([%-%+ #0]*%d*%.?%d*[sdiufgxc])", function(pct, pos, spec)
        if pct == "%" then return "%%" .. pos .. spec end
        if pos ~= "" then return "%" .. pos .. spec end
        n = n + 1
        return "%" .. n .. "$" .. spec
    end))
end

-- Exactement WatchFrame_ReverseQuestObjective du client (le compte passe devant).
local function Inverser(texte)
    local _, _, a1, a2 = find(texte, "(.*):%s(.*)")
    if a1 and a2 then return a2 .. " " .. a1 end
    return texte
end
A.InverserObjectif = Inverser

local function Nettoyer(s) return (match(s, "^%s*(.-)%s*$")) end

local function FormesAnglaises(cle)
    local out, g = {}, Gabarit(cle)
    if g and g.en then out[#out + 1] = g.en end
    local cur = _G[cle]
    if type(cur) == "string" and cur ~= "" and (not g or cur ~= g.en) then out[#out + 1] = cur end
    return out
end

local function GabaritFR(cle)
    local g = Gabarit(cle)
    if g and type(g.fr) == "string" then return g.fr end
    return REPLI_FR[cle]
end

-- Suffixe « (Complete) » ajoute par la fenetre de quete aux objectifs remplis.
local function Suffixe(texte)
    local fins = { " (Complete)" }
    local c = _G.COMPLETE
    if type(c) == "string" and c ~= "" and c ~= "Complete" then fins[2] = " (" .. c .. ")" end
    for _, f in ipairs(fins) do
        if sub(texte, -#f) == f then
            local cur = (type(c) == "string" and c ~= "") and (" (" .. c .. ")") or f
            return sub(texte, 1, -#f - 1), cur
        end
    end
    return texte, ""
end

function A.TraduireObjectif(texte)
    if type(texte) ~= "string" or texte == "" then return nil end
    local corps, fin = Suffixe(texte)
    local pre, reste = match(corps, "^([%s%-]*)(.-)$")
    if not reste or reste == "" then return nil end
    for _, cle in ipairs(GABARITS_OBJ) do
        for _, g in ipairs(FormesAnglaises(cle)) do
            local gp = Positionnel(g)
            for inverse = 0, 1 do
                local forme = (inverse == 1) and Inverser(gp) or gp
                local args = A.LireGabarit(forme, reste)
                if args and args[1] and args[1] ~= "" and args[2] then
                    local fr = NomObjectif(args[1])
                    if not fr then return nil end
                    local sortie = A.Formater(Positionnel(GabaritFR(cle)), { fr, args[2], args[3] })
                    if inverse == 1 then sortie = Nettoyer(Inverser(sortie)) end
                    return pre .. sortie .. fin
                end
            end
        end
    end
    local fr = A.TexteQuete(reste)
    if fr then return pre .. fr .. fin end
    return nil
end

-- ----------------------------------------------------------------------------
-- Correspondances du journal : titre anglais -> titre francais, par numero de quete ; en-tetes
-- (zones, categories) -> nom francais. Reconstruites a chaque mise a jour du journal.
-- ----------------------------------------------------------------------------
local corr_journal, corr_a_refaire = {}, true

local function IdJournal(i)
    local id = select(9, GetQuestLogTitle(i))
    if type(id) == "number" and id > 0 then return id end
    return A.IdDepuisLien(GetQuestLink and GetQuestLink(i), "quest")
end

local function CorrespondancesJournal()
    if not corr_a_refaire then return corr_journal end
    corr_a_refaire = false
    local corr = {}
    if type(GetNumQuestLogEntries) == "function" then
        for i = 1, (GetNumQuestLogEntries() or 0) do
            local titre, _, _, _, entete = GetQuestLogTitle(i)
            if titre and titre ~= "" then
                local fr
                if entete then
                    fr = A.Nom("zone", titre) or A.Nom("divers", titre)
                else
                    local id = IdJournal(i)
                    fr = (id and A.TitreParId(id, titre)) or A.TexteQuete(titre)
                end
                if fr then corr[titre] = fr end
            end
        end
    end
    corr_journal = corr
    return corr
end
A.CorrespondancesJournal = CorrespondancesJournal
function A.JournalAChange() corr_a_refaire = true end

-- Une zone de texte de quete : titre, texte long ou objectif.
local function TraduireZone(zone, corr, id)
    if not zone or not zone.GetText then return end
    local texte = zone:GetText()
    if not texte or texte == "" or A.DejaEcrit(zone, texte) then return end
    local fr = Titre(texte, corr, id) or A.TraduireObjectif(texte)
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
local ZONES_QUETE = { "QuestInfoDescriptionText", "QuestInfoObjectivesText", "QuestInfoRewardText",
    "QuestProgressTitleText", "QuestProgressText" }
local ZONES_TITRE = { "QuestInfoTitleHeader", "QuestInfoTitleText" }

local function Texte(nom)
    local z = _G[nom]
    return z and z.GetText and z:GetText()
end

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

-- En-tete de la fenetre de quete : le nom du PNJ (UnitName("questnpc")).
function A.TraduireNomPNJ(zone, unites)
    if not zone or not zone.GetText then return end
    local texte = zone:GetText()
    if not texte or texte == "" or A.DejaEcrit(zone, texte) then return end
    for _, u in ipairs(unites) do
        local fr, en = A.NomUnite(u)
        if fr and en == texte then A.Ecrire(zone, fr); return end
    end
end

-- Numero de la quete affichee (journal : par numero ; PNJ : par le titre).
function A.QueteAffichee()
    local journal = QuestInfoFrame and QuestInfoFrame.questLog
    local titre = Texte("QuestInfoTitleHeader") or Texte("QuestInfoTitleText")
    if journal and type(GetQuestLogSelection) == "function" then
        local sel = GetQuestLogSelection()
        if sel and sel > 0 then return IdJournal(sel), titre end
    end
    local id = IdQueteOfferte()
    if id then return id, titre end
    if not titre or titre == "" then titre = Texte("QuestProgressTitleText") end
    return A.QueteParTitre(titre, { Texte("QuestInfoDescriptionText"), Texte("QuestInfoObjectivesText"),
        Texte("QuestInfoRewardText"), Texte("QuestProgressText") }), titre
end

local function TraduireFenetreQuete()
    if not A.Actif() then return end
    local journal = QuestInfoFrame and QuestInfoFrame.questLog
    local corr = CorrespondancesJournal()
    local id = A.QueteAffichee()
    for _, nom in ipairs(ZONES_TITRE) do TraduireZone(_G[nom], corr, id) end
    for _, nom in ipairs(ZONES_QUETE) do TraduireZone(_G[nom], corr, (nom == "QuestProgressTitleText") and id or nil) end
    for i = 1, 10 do
        local ligne = _G["QuestInfoObjective" .. i]
        if ligne and ligne:IsShown() then TraduireZone(ligne, corr) end
    end
    NomsRecompenses(journal)
    if QuestFrame and QuestFrame:IsShown() then
        A.TraduireNomPNJ(QuestFrameNpcNameText, { "questnpc", "npc" })
        Parcourir(QuestFrame, corr, 0)
    end
end
A.TraduireFenetreQuete = TraduireFenetreQuete

if type(QuestInfo_Display) == "function" then
    hooksecurefunc("QuestInfo_Display", P("QuestInfo_Display", TraduireFenetreQuete))
end
if QuestFrame and QuestFrame.HookScript then
    QuestFrame:HookScript("OnShow", P("QuestFrame.OnShow", function()
        if A.Actif() then A.TraduireNomPNJ(QuestFrameNpcNameText, { "questnpc", "npc" }) end
    end))
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
    A.TraduireNomPNJ(QuestFrameNpcNameText, { "questnpc", "npc" })
end

local f = CreateFrame("Frame")
f:RegisterEvent("QUEST_PROGRESS")
f:RegisterEvent("QUEST_GREETING")
f:RegisterEvent("QUEST_LOG_UPDATE")
f:SetScript("OnEvent", P("Quetes.OnEvent", function(self, evenement)
    if evenement == "QUEST_LOG_UPDATE" then corr_a_refaire = true; return end
    if not A.Actif() then return end
    if evenement == "QUEST_PROGRESS" then
        local id = A.QueteAffichee()
        TraduireZone(QuestProgressTitleText, CorrespondancesJournal(), id)
        TraduireZone(QuestProgressText, nil)
        A.TraduireNomPNJ(QuestFrameNpcNameText, { "questnpc", "npc" })
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
-- Suivi des objectifs (a droite de l'ecran).
-- Le client pose chaque ligne par WatchFrame_SetLine(ligne, ancre, decalage, estTitre, texte,
-- tiret, objet, terminee) et fixe ALORS sa hauteur d'apres le texte anglais : 16 px pour une
-- ligne, 29 px (WATCHFRAME_MULTIPLE_LINEHEIGHT) si le texte en fait deux. Un titre francais
-- plus long, pose apres coup, passait sur deux lignes dans une ligne de 16 px : il debordait
-- sur la ligne d'objectif (retour de l'essai 1). On passe donc juste apres SetLine
-- (hooksecurefunc : le jeu n'est pas modifie), on pose le francais, puis on refait le calcul
-- de hauteur du jeu avec le texte francais. Les lignes suivantes sont ancrees au bas de
-- celle-ci : elles descendent d'elles-memes. Ces lignes sont de simples cadres (non proteges) ;
-- le bouton d'objet de quete n'est pas un bouton securise dans ce client. Valable en combat.
-- ----------------------------------------------------------------------------
local function AjusterHauteur(ligne, terminee)
    local t = ligne.text
    if not t or type(t.GetHeight) ~= "function" or type(ligne.SetHeight) ~= "function" then return end
    local LH = WATCHFRAME_LINEHEIGHT or 16
    local MLH = WATCHFRAME_MULTIPLE_LINEHEIGHT or 29
    t:SetHeight(0)                               -- hauteur automatique (comme WatchFrameLineTemplate_Reset)
    local h = t:GetHeight() or 0
    local cible
    if h > LH then
        cible = terminee and (h + 4) or math.max(MLH, h + 3)
    else
        cible = LH
    end
    local actuelle = ligne:GetHeight() or 0
    if math.abs(actuelle - cible) > 0.5 then
        ligne:SetHeight(cible)
        A.Compteurs.suivi_hauteur = A.Compteurs.suivi_hauteur + 1
    end
end
A.AjusterHauteurSuivi = AjusterHauteur

local function TraduireLigneSuivi(ligne, estTitre, terminee)
    local zone = ligne and ligne.text
    if not zone or not zone.GetText then return end
    local texte = zone:GetText()
    if not texte or texte == "" or A.DejaEcrit(zone, texte) then return end
    local corr = CorrespondancesJournal()
    local fr = corr[texte]
    if not fr then
        if estTitre then fr = Titre(texte, corr) else fr = A.TraduireObjectif(texte) end
    end
    if fr and fr ~= texte then
        A.Ecrire(zone, fr)
        AjusterHauteur(ligne, terminee)
    end
end

if type(WatchFrame_SetLine) == "function" then
    hooksecurefunc("WatchFrame_SetLine", P("WatchFrame_SetLine", function(ligne, ancre, decalage, estTitre, texte,
                                                                          tiret, objet, terminee)
        if A.Actif() then TraduireLigneSuivi(ligne, estTitre, terminee) end
    end))
end

-- Repasse apres la mise a jour complete (lignes posees sans WatchFrame_SetLine : minuteurs…).
local function TraduireSuivi()
    if not A.Actif() then return end
    local lignes = type(WATCHFRAME_QUESTLINES) == "table" and WATCHFRAME_QUESTLINES or nil
    if lignes then
        for _, ligne in ipairs(lignes) do TraduireLigneSuivi(ligne, nil, nil) end
    end
    local i = 1
    while true do
        local ligne = _G["WatchFrameLine" .. i]
        if not ligne then break end
        TraduireLigneSuivi(ligne, nil, nil)
        i = i + 1
    end
end
A.TraduireSuivi = TraduireSuivi

if type(WatchFrame_Update) == "function" then
    hooksecurefunc("WatchFrame_Update", P("WatchFrame_Update", TraduireSuivi))
end
