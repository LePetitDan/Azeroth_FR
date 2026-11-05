-- ============================================================================
-- Azeroth_FR : fenetres du jeu (version 0.5) : marchand (achat et rachat), fenetre de butin, panneau des
-- quetes de la carte du monde, livre des metiers de CoA ; (0.5) en-tetes des fenetres de PNJ (marchand, banque,
-- maitre de classe, taxi, tabard) et infobulle des points de quete de la carte.
-- Chaque branchement est verifie contre le code que le client CoA charge vraiment (04/11/2026) :
--   - MerchantFrame_Update (patch-B, MerchantFrame.lua) : appelee PAR SON NOM par MerchantFrame_OnEvent,
--     MerchantFrame_OnShow et les boutons de page ; elle appelle MerchantFrame_UpdateMerchantInfo ou
--     MerchantFrame_UpdateBuybackInfo, qui posent MerchantItemNName:SetText(nom) ;
--   - LootFrame_UpdateButton (patch-enUS-3, LootFrame.lua ; patch-B n'a que LootFrame.xml) : appelee par son nom
--     par LootFrame_Update, pose LootButtonNText:SetText(nom) et button.slot ;
--   - WorldMapFrame_UpdateQuests (patch-B, WorldMapFrame.lua) : appelee par son nom (WorldMapFrame_DisplayQuests,
--     OnEvent) ; pose questFrame.title (titre), questFrame.objectives (objectifs « 0/8 X slain », retournes par
--     WorldMapFrame_ReverseQuestObjective, separes par |n) et questFrame.dashes, puis la hauteur du cadre ;
--   - livre des metiers (patch-B, Ascension_Spellbook/Ascension_ProfessionBook.lua) : boutons SECURISES
--     (SecureActionButton_OnLoad) ; le nom vient de ProfessionUtil.GetProfessionByID -> GetSkillInfo ; on ne
--     touche qu'au texte de leur zone de texte (GetFontString) et de leur rang (.Rank), hors combat.
-- (0.5, verifie le 05/11/2026 contre le code charge par le client CoA) :
--   - en-tete du marchand : MerchantFrame_UpdateMerchantInfo (patch-B, MerchantFrame.lua l. 85) pose
--     MerchantNameText:SetText(UnitName("NPC")) ; elle est appelee par son nom par MerchantFrame_Update (notre crochet
--     passe apres). Onglet Rachat : MERCHANT_BUYBACK (texte d'interface, PTRXML) ;
--   - banque : BankFrame_OnEvent (patch-B, BankFrame.lua l. 149 ; liee par <OnEvent function=…> dans BankFrame.xml de
--     patch-enUS-3, donc CAPTUREE) : BankFrame:HookScript("OnEvent"), BANKFRAME_OPENED -> BankFrameTitleText ;
--   - taxi : TaxiFrame_OnEvent (patch-enUS, TaxiFrame.lua l. 30 ; function= dans TaxiFrame.xml de patch-enUS-2) :
--     TaxiFrame:HookScript("OnEvent"), TAXIMAP_OPENED -> TaxiMerchant ;
--   - tabard : TabardFrame_OnEvent (locale-enUS, TabardFrame.lua l. 29 ; function= dans TabardFrame.xml de
--     patch-enUS) : TabardFrame:HookScript("OnEvent"), OPEN_TABARD_FRAME -> TabardFrameNameText ;
--   - maitre de classe : ClassTrainerFrame_Update (patch-B, AddOns/Blizzard_TrainerUI, charge a la demande, l. 81)
--     pose ClassTrainerNameText ; appelee par son nom (ClassTrainerFrame_OnEvent, TRAINER_UPDATE) : crochet pose
--     au chargement de l'add-on Blizzard_TrainerUI ;
--   - infobulle d'un point de quete de la carte : WorldMapQuestPOI_SetTooltip (patch-B, WorldMapFrame.lua l. 2235),
--     appelee par son nom par WorldMapQuestPOI_OnEnter et WorldMapBlobFrame_OnUpdate (a chaque image, souris sur la
--     zone de la quete) : titre (GetQuestLogTitle), puis « - » + objectif retourne ou texte de fin.
-- Nom du PNJ : celui de la creature (numero tire du GUID de l'unite « npc », empreinte du nom anglais), pose
-- seulement si le texte de la zone est EXACTEMENT ce nom anglais (A.TraduireNomPNJ, comme la fenetre de quete).
-- Noms d'objets : par le numero tire du lien (GetMerchantItemLink, GetBuybackItemLink, GetLootSlotLink), le
-- francais n'est pose que si l'anglais affiche a l'empreinte de l'anglais traduit (A.NomObjetAffiche).
-- ============================================================================
local A = AzerothFR
local P = A.Proteger
local gsub, match, find, sub = string.gsub, string.match, string.find, string.sub

-- Nom d'objet dans une zone de texte, verifie par le numero du lien et l'empreinte de l'anglais affiche.
local function NomObjetZone(zone, lien)
    if not zone or type(zone.GetText) ~= "function" then return false end
    local t = zone:GetText()
    if not t or t == "" or A.DejaEcrit(zone, t) then return false end
    local id = A.IdDepuisLien(lien, "item")
    local fr = id and A.NomObjetAffiche(id, t)
    if fr and fr ~= t then
        A.Ecrire(zone, fr)
        return true
    end
    return false
end
A.NomObjetZone = NomObjetZone

-- ----------------------------------------------------------------------------
-- Marchand : achat (page courante) et rachat ; « dernier objet vendu » sous la liste d'achat.
-- ----------------------------------------------------------------------------
local function TraduireMarchand()
    if not A.Actif() or not MerchantFrame or not MerchantFrame:IsShown() then return end
    local achat = MerchantFrame.selectedTab == 1
    if achat and A.TraduireNomPNJ then A.TraduireNomPNJ(MerchantNameText, { "npc" }) end
    local parPage = MERCHANT_ITEMS_PER_PAGE or 10
    local page = MerchantFrame.page or 1
    for i = 1, 12 do
        local zone = _G["MerchantItem" .. i .. "Name"]
        if zone then
            local lien
            if achat then
                if i <= parPage and type(GetMerchantItemLink) == "function" then
                    lien = GetMerchantItemLink((page - 1) * parPage + i)
                end
            elseif type(GetBuybackItemLink) == "function" then
                lien = GetBuybackItemLink(i)
            end
            if lien then NomObjetZone(zone, lien) end
        end
    end
    if achat and MerchantBuyBackItemName and type(GetBuybackItemLink) == "function"
        and type(GetNumBuybackItems) == "function" then
        local n = GetNumBuybackItems()
        if n and n > 0 then NomObjetZone(MerchantBuyBackItemName, GetBuybackItemLink(n)) end
    end
end
A.TraduireMarchand = TraduireMarchand
if type(MerchantFrame_Update) == "function" then
    hooksecurefunc("MerchantFrame_Update", P("MerchantFrame_Update", TraduireMarchand))
end

-- ----------------------------------------------------------------------------
-- (0.5) En-tetes des fenetres de PNJ : banque, taxi, tabard (cadres dont le script OnEvent est capture par le XML :
-- on passe apres lui, HookScript), maitre de classe (add-on du jeu charge a la demande).
-- ----------------------------------------------------------------------------
local ENTETES = {
    { cadre = "BankFrame", evenement = "BANKFRAME_OPENED", zone = "BankFrameTitleText" },
    { cadre = "TaxiFrame", evenement = "TAXIMAP_OPENED", zone = "TaxiMerchant" },
    { cadre = "TabardFrame", evenement = "OPEN_TABARD_FRAME", zone = "TabardFrameNameText" },
}
for _, e in ipairs(ENTETES) do
    local cadre = _G[e.cadre]
    if cadre and type(cadre.HookScript) == "function" then
        cadre:HookScript("OnEvent", P(e.cadre .. ".OnEvent", function(_, evenement)
            if evenement == e.evenement and A.Actif() and A.TraduireNomPNJ then
                A.TraduireNomPNJ(_G[e.zone], { "npc" })
            end
        end))
    end
end
A.ENTETES_PNJ = ENTETES

local function TraduireMaitreDeClasse()
    if A.Actif() and A.TraduireNomPNJ then A.TraduireNomPNJ(ClassTrainerNameText, { "npc" }) end
end
local maitre_branche = false
local function BrancherMaitreDeClasse()
    if maitre_branche or type(ClassTrainerFrame_Update) ~= "function" then return end
    maitre_branche = true
    hooksecurefunc("ClassTrainerFrame_Update", P("ClassTrainerFrame_Update", TraduireMaitreDeClasse))
end
BrancherMaitreDeClasse()
local guetteurTrainer = CreateFrame("Frame")
guetteurTrainer:RegisterEvent("ADDON_LOADED")
guetteurTrainer:SetScript("OnEvent", P("Fenetres.ADDON_LOADED", function(self, _, nom)
    if nom == "Blizzard_TrainerUI" then
        BrancherMaitreDeClasse()
        self:UnregisterEvent("ADDON_LOADED")
    end
end))

-- ----------------------------------------------------------------------------
-- Fenetre de butin
-- ----------------------------------------------------------------------------
local function TraduireButin(index)
    if not A.Actif() then return end
    local bouton = _G["LootButton" .. tostring(index)]
    local zone = _G["LootButton" .. tostring(index) .. "Text"]
    if not bouton or not zone or not bouton:IsShown() or not bouton.slot or type(GetLootSlotLink) ~= "function" then return end
    NomObjetZone(zone, GetLootSlotLink(bouton.slot))
end
A.TraduireButin = TraduireButin
if type(LootFrame_UpdateButton) == "function" then
    hooksecurefunc("LootFrame_UpdateButton", P("LootFrame_UpdateButton", TraduireButin))
end

-- ----------------------------------------------------------------------------
-- Carte du monde : panneau des quetes a droite (code CoA). Titre par le numero de la quete (index du journal
-- -> GetQuestLogTitle, 9e valeur), objectifs ligne par ligne (A.TraduireObjectif : « 0/8 Kobold Vermin tué »
-- -> « 0/8 Vermine kobold tué »), texte de fin (quete terminee) par le texte de la quete. Puis, HORS COMBAT, la
-- mise en page du client refaite avec le francais (tirets et hauteur du cadre, memes calculs que
-- WorldMapFrame_UpdateQuests). En combat : rien (repris a la fin du combat si la carte est ouverte).
-- ----------------------------------------------------------------------------
local carte_a_refaire = false

local function Objectifs(texte, termine)
    if termine then return A.TexteQuete and A.TexteQuete(texte) end
    local morceaux, change = {}, false
    local pos = 1
    while true do
        local d, f = find(texte, "|n", pos, true)
        local ligne = d and sub(texte, pos, d - 1) or sub(texte, pos)
        local fr = ligne ~= "" and A.TraduireObjectif(ligne) or nil
        if fr and fr ~= ligne then change = true end
        morceaux[#morceaux + 1] = fr or ligne
        if not d then break end
        pos = f + 1
    end
    if not change then return nil end
    return table.concat(morceaux, "|n")
end

-- Tirets du client recalcules avec le francais : une ligne de tiret par objectif, puis autant de |n que de
-- lignes occupees (mesurees, comme le client, sur la zone de reference WorldMapQuestFrame0.objectives).
local function Tirets(objectifs)
    local ref = _G.WorldMapQuestFrame0
    if not ref or not ref.objectives or not ref.lineHeight or not ref.lineSpacing then return nil end
    local tiret = QUEST_DASH or "- "
    local out = {}
    local pos = 1
    while true do
        local d, f = find(objectifs, "|n", pos, true)
        local ligne = d and sub(objectifs, pos, d - 1) or sub(objectifs, pos)
        if ligne ~= "" then
            ref.objectives:SetText(ligne)
            local n = math.floor((ref.objectives:GetHeight() + ref.lineSpacing) / ref.lineHeight + 0.5)
            out[#out + 1] = tiret .. string.rep("|n", math.max(1, n))
        end
        if not d then break end
        pos = f + 1
    end
    return table.concat(out)
end

local function TraduireQuetesCarte()
    if not A.Actif() or not WorldMapFrame or not WorldMapFrame:IsShown() then return end
    if A.EnCombat() then carte_a_refaire = true; return end
    local n = WorldMapFrame.numQuests or 0
    for i = 1, n do
        local q = _G["WorldMapQuestFrame" .. i]
        if q and q:IsShown() and q.title and q.objectives then
            local modifie = false
            local t = q.title:GetText()
            if t and t ~= "" and not A.DejaEcrit(q.title, t) then
                local id = q.questLogIndex and A.IdJournal and A.IdJournal(q.questLogIndex)
                local fr = (id and A.TitreParId(id, t)) or (A.TitreQuete and A.TitreQuete(t))
                if fr and fr ~= t then A.Ecrire(q.title, fr); modifie = true end
            end
            local o = q.objectives:GetText()
            if o and o ~= "" and not A.DejaEcrit(q.objectives, o) then
                local fr = Objectifs(o, q.completed)
                if fr and fr ~= o then
                    A.Ecrire(q.objectives, fr)
                    modifie = true
                    if not q.completed and q.dashes then
                        local tirets = Tirets(fr)
                        if tirets then q.dashes:SetText(tirets) end
                    end
                end
            end
            if modifie and not A.EstProtege(q) then
                q:SetHeight(math.max(q.title:GetHeight() + q.objectives:GetHeight() + (QUESTFRAME_PADDING or 0),
                    QUESTFRAME_MINHEIGHT or 0))
            end
        end
    end
end
A.TraduireQuetesCarte = TraduireQuetesCarte
if type(WorldMapFrame_UpdateQuests) == "function" then
    hooksecurefunc("WorldMapFrame_UpdateQuests", P("WorldMapFrame_UpdateQuests", TraduireQuetesCarte))
end
table.insert(A.ApresCombat, function()
    if carte_a_refaire then
        carte_a_refaire = false
        TraduireQuetesCarte()
    end
end)

-- (0.5) Infobulle d'un point de quete (WorldMapTooltip) : refaite par le jeu a chaque image tant que la souris est
-- sur la zone de la quete ; les lignes deja traduites sont gardees en memoire (texte anglais -> francais).
local memo_bulle, n_memo_bulle = {}, 0
local function LigneBulleCarte(t)
    local m = memo_bulle[t]
    if m ~= nil then return m or nil end
    local fr = A.TraduireObjectif(t) or false
    n_memo_bulle = n_memo_bulle + 1
    if n_memo_bulle > 200 then memo_bulle, n_memo_bulle = {}, 0 end
    memo_bulle[t] = fr
    return fr or nil
end

local function TraduireBulleCarte(poi, indexJournal)
    if not A.Actif() then return end
    local bulle = WorldMapTooltip
    if not bulle or type(bulle.GetName) ~= "function" or not bulle:GetName() then return end
    local nom = bulle:GetName()
    local modifie = false
    -- (SetText direct, comme les autres infobulles : le jeu reecrit l'anglais a chaque image)
    local l1 = _G[nom .. "TextLeft1"]
    local t = l1 and l1:GetText()
    if t and t ~= "" then
        local id = indexJournal and A.IdJournal and A.IdJournal(indexJournal)
        local fr = (id and A.TitreParId(id, t)) or (A.TitreQuete and A.TitreQuete(t))
        if fr and fr ~= t then l1:SetText(fr); modifie = true end
    end
    for i = 2, bulle:NumLines() do
        local l = _G[nom .. "TextLeft" .. i]
        local tx = l and l:GetText()
        if tx and tx ~= "" then
            local fr = LigneBulleCarte(tx)
            if fr and fr ~= tx then l:SetText(fr); modifie = true end
        end
    end
    if modifie then
        A.Trace("WorldMapQuestPOI_SetTooltip")
        if bulle:IsShown() and not A.EstProtege(bulle) then pcall(bulle.Show, bulle) end
    end
end
A.TraduireBulleCarte = TraduireBulleCarte
if type(WorldMapQuestPOI_SetTooltip) == "function" then
    -- (appelee a chaque image : pas de fil d'Ariane a chaque appel, seulement quand une ligne change)
    hooksecurefunc("WorldMapQuestPOI_SetTooltip", P("WorldMapQuestPOI_SetTooltip", TraduireBulleCarte, true))
end

-- ----------------------------------------------------------------------------
-- Livre des metiers de CoA (onglet « Métiers » du grimoire) : nom officiel du metier (SkillLine frFR, table des
-- competences par anglais exact ; Menuiserie et Bucheronnage : decisions 15 et 16) et rang (« Apprentice »).
-- Les boutons sont securises : seulement le texte de leurs zones de texte, hors combat. Appele par le guetteur
-- du grimoire (Modules/Sorts.lua), 5 fois par seconde tant que le grimoire est ouvert.
-- ----------------------------------------------------------------------------
local boutons_metiers

local function ChercherMetiers(cadre, profondeur, out)
    if not cadre or profondeur > 6 or type(cadre.GetChildren) ~= "function" then return end
    local enfants = { cadre:GetChildren() }
    for _, e in ipairs(enfants) do
        if type(e) == "table" and e.skillID and e.Rank then out[#out + 1] = e end
        ChercherMetiers(e, profondeur + 1, out)
    end
end

function A.TraduireMetiers(cadre, nouveau)
    if not A.Actif() or A.EnCombat() or not cadre then return end
    if nouveau or not boutons_metiers then
        boutons_metiers = {}
        ChercherMetiers(cadre, 0, boutons_metiers)
    end
    for _, b in ipairs(boutons_metiers) do
        if b:IsShown() then
            local z = type(b.GetFontString) == "function" and b:GetFontString() or nil
            local t = z and z:GetText()
            if t and t ~= "" and not A.DejaEcrit(z, t) then
                local fr = A.Nom("competence", t)
                if fr and fr ~= t then A.Ecrire(z, fr) end
            end
            local r = b.Rank
            local tr = r and type(r.GetText) == "function" and r:GetText()
            if tr and tr ~= "" and not A.DejaEcrit(r, tr) then
                local fr = A.Nom("rang", tr)
                if fr and fr ~= tr then A.Ecrire(r, fr) end
            end
        end
    end
end
