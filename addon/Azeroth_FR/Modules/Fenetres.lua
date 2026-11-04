-- ============================================================================
-- Azeroth_FR : fenetres du jeu (version 0.4) : marchand (achat et rachat), fenetre de butin, panneau des
-- quetes de la carte du monde, livre des metiers de CoA.
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
