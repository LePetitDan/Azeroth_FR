-- ============================================================================
-- Azeroth_FR : fenetres ou des objets changent de mains (version 1.2, 17/11/2026). Affichage seulement.
-- Reste du § 1 de l'inventaire du 07/11 : hotel des ventes, echange entre joueurs, jets de butin de groupe,
-- montures et familiers. Le nom francais vient du LIEN de l'objet (son numero), jamais du texte seul : il n'est
-- pose que si le nom anglais affiche est bien celui qu'on a traduit (A.NomObjetZone, comme le marchand).
-- Chaque branchement est verifie contre le code que le client CoA charge vraiment (copie du 07/11/2026) :
--   - hotel des ventes (patch-B, AddOns/Blizzard_AuctionUI/Blizzard_AuctionUI.lua, charge a la demande) :
--       AuctionFrameBrowse_Update (l. 787)   pose BrowseButtonNName   <- GetAuctionItemInfo("list", offset + i)
--       AuctionFrameBid_Update (l. 994)      pose BidButtonNName      <- GetAuctionItemInfo("bidder", offset + i)
--       AuctionFrameAuctions_Update (l. 1205) pose AuctionsButtonNName <- GetAuctionItemInfo("owner", offset + i)
--     (offset = FauxScrollFrame_GetOffset de Browse/Bid/AuctionsScrollFrame ; 8, 9 et 9 lignes). Les trois fonctions
--     sont appelees par leur nom (evenements, defilement) : crochets poses au chargement de Blizzard_AuctionUI ;
--   - echange (patch-enUS-3, FrameXML/TradeFrame.lua) : TradeFrame_UpdatePlayerItem(id) (l. 67) pose
--     TradePlayerItemNName, TradeFrame_UpdateTargetItem(id) (l. 95) pose TradeRecipientItemNName ; appelees par leur
--     nom par TradeFrame_Update et TradeFrame_OnEvent. L'emplacement « ne sera pas echange » (enchantement) est
--     laisse tel quel ;
--   - jets de butin (patch-enUS-3, FrameXML/LootFrame.lua l. 339) : GroupLootFrame_OnShow pose GroupLootFrameNName ;
--     elle est liee par <OnShow function="GroupLootFrame_OnShow"/> (patch-B, LootFrame.xml l. 509), donc CAPTUREE :
--     GroupLootFrameN:HookScript("OnShow") ; le lien vient de GetLootRollItemLink(cadre.rollID) ;
--   - montures et familiers (patch-B, FrameXML/Ascension_CharacterFrame/SidePanels/CompanionPanel.lua) : chaque
--     ligne de la liste (CompanionScrollItemMixin) garde sa monture dans .companion (name, spellID) et ecrit
--     self:SetText(name) ; la fiche (AscensionPetPaperDollPanel.CompanionTab.CompanionModel.Overlay) a .Title.
--     Tant que le panneau AscensionCharacterCompanionPanel est visible, ses lignes sont relues toutes les 0,4 s :
--     le francais est celui du sort de la monture si son nom anglais est le meme (A.NomSort), sinon celui de la
--     creature de meme nom (A.NomCreature).
-- Rien n'est ecrit dans les tables du jeu : hooksecurefunc, HookScript et SetText sur des zones de texte.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger

-- ----------------------------------------------------------------------------
-- Hotel des ventes
-- ----------------------------------------------------------------------------
local function ListeEncheres(prefixe, nombre, sorte, defilement)
    return function()
        if not A.Actif() or type(GetAuctionItemLink) ~= "function" then return end
        local cadre = _G[defilement]
        local decalage = (cadre and type(FauxScrollFrame_GetOffset) == "function" and FauxScrollFrame_GetOffset(cadre)) or 0
        for i = 1, (_G[nombre] or 9) do
            local bouton, zone = _G[prefixe .. i], _G[prefixe .. i .. "Name"]
            if bouton and zone and (type(bouton.IsShown) ~= "function" or bouton:IsShown()) then
                A.NomObjetZone(zone, GetAuctionItemLink(sorte, decalage + i))
            end
        end
    end
end
local ENCHERES = {
    { "AuctionFrameBrowse_Update", ListeEncheres("BrowseButton", "NUM_BROWSE_TO_DISPLAY", "list", "BrowseScrollFrame") },
    { "AuctionFrameBid_Update", ListeEncheres("BidButton", "NUM_BIDS_TO_DISPLAY", "bidder", "BidScrollFrame") },
    { "AuctionFrameAuctions_Update", ListeEncheres("AuctionsButton", "NUM_AUCTIONS_TO_DISPLAY", "owner", "AuctionsScrollFrame") },
}
A.TraduireEncheres = function() for _, e in ipairs(ENCHERES) do e[2]() end end

-- Categories de l'hotel des ventes (essai de Dan du 18/11 : « Weapon », « One-Handed Axes »… restaient en anglais).
-- AuctionFrameFilters_Update (l. 629) remplit AuctionFilterButton1..15 par FilterButton_SetType (l. 720) :
-- button:SetText(nom) pour une categorie, « |cffffffff » .. nom .. « |r » pour une sous-categorie ou un emplacement.
-- ATTENTION : AuctionFrameFilter_OnClick (l. 748) relit le texte du bouton (self:GetText()) et le compare au nom
-- ANGLAIS de la categorie pour savoir laquelle ouvrir. On remet donc l'anglais sur le bouton juste avant le clic
-- (PreClick, qui passe avant OnClick) ; le jeu redessine ensuite la liste et notre crochet la retraduit.
-- Le francais : sous-classes officielles (ItemSubClass.dbc frFR), sinon les autres noms connus par leur anglais.
local function NomCategorie(en)
    return A.Nom("sous_classe", en) or A.Nom("divers", en) or (A.TexteClient and A.TexteClient(en))
end
A.NomCategorieEncheres = NomCategorie

local function ZoneFiltre(i)
    return _G["AuctionFilterButton" .. i .. "NormalText"]
end

local function TraduireFiltres()
    if not A.Actif() then return end
    for i = 1, (NUM_FILTERS_TO_DISPLAY or 15) do
        local bouton, zone = _G["AuctionFilterButton" .. i], ZoneFiltre(i)
        if bouton and zone and (type(bouton.IsShown) ~= "function" or bouton:IsShown()) then
            local t = zone:GetText()
            if t and t ~= "" and not A.DejaEcrit(zone, t) then
                local debut, coeur, fin = string.match(t, "^(|c%x%x%x%x%x%x%x%x)(.-)(|r)$")
                if not coeur then debut, coeur, fin = "", t, "" end
                local fr = NomCategorie(coeur)
                if fr and fr ~= coeur then A.Ecrire(zone, debut .. fr .. fin) end
            end
        end
    end
end
A.TraduireFiltresEncheres = TraduireFiltres

-- Avant le clic : le bouton retrouve le texte anglais que le jeu va relire.
local function RendreAnglais(bouton)
    local nom = bouton and type(bouton.GetName) == "function" and bouton:GetName()
    local zone = nom and _G[nom .. "NormalText"]
    if not zone then return end
    local t = zone:GetText()
    local en = t and A.DejaEcrit(zone, t) and A.Originaux[zone]
    if en then zone:SetText(en) end
end
A.RendreAnglaisFiltre = RendreAnglais

local encheres_branchees = false
local function BrancherEncheres()
    if encheres_branchees or type(AuctionFrameBrowse_Update) ~= "function" then return end
    encheres_branchees = true
    for _, e in ipairs(ENCHERES) do
        if type(_G[e[1]]) == "function" then hooksecurefunc(e[1], P(e[1], e[2])) end
    end
    if type(AuctionFrameFilters_Update) == "function" then
        hooksecurefunc("AuctionFrameFilters_Update", P("AuctionFrameFilters_Update", TraduireFiltres))
        for i = 1, (NUM_FILTERS_TO_DISPLAY or 15) do
            local bouton = _G["AuctionFilterButton" .. i]
            if bouton and bouton.HookScript then bouton:HookScript("PreClick", P("AuctionFilterButton.PreClick", RendreAnglais)) end
        end
        TraduireFiltres()
    end
end

-- ----------------------------------------------------------------------------
-- Echange entre joueurs
-- ----------------------------------------------------------------------------
local function ObjetEchange(prefixe, lienDe)
    return function(id)
        if not A.Actif() or type(id) ~= "number" or id == (TRADE_ENCHANT_SLOT or 7) then return end
        local zone = _G[prefixe .. id .. "Name"]
        local lien = type(_G[lienDe]) == "function" and _G[lienDe](id)
        if zone and lien then A.NomObjetZone(zone, lien) end
    end
end
local EchangeJoueur = ObjetEchange("TradePlayerItem", "GetTradePlayerItemLink")
local EchangeAutre = ObjetEchange("TradeRecipientItem", "GetTradeTargetItemLink")
A.TraduireEchange = function() for id = 1, 6 do EchangeJoueur(id); EchangeAutre(id) end end
if type(TradeFrame_UpdatePlayerItem) == "function" then
    hooksecurefunc("TradeFrame_UpdatePlayerItem", P("TradeFrame_UpdatePlayerItem", EchangeJoueur))
end
if type(TradeFrame_UpdateTargetItem) == "function" then
    hooksecurefunc("TradeFrame_UpdateTargetItem", P("TradeFrame_UpdateTargetItem", EchangeAutre))
end

-- ----------------------------------------------------------------------------
-- Jets de butin de groupe
-- ----------------------------------------------------------------------------
local function JetDeButin(cadre)
    if not A.Actif() or not cadre or not cadre.rollID or type(GetLootRollItemLink) ~= "function" then return end
    local zone = _G[(cadre.GetName and cadre:GetName() or "") .. "Name"]
    if zone then A.NomObjetZone(zone, GetLootRollItemLink(cadre.rollID)) end
end
A.TraduireJetDeButin = JetDeButin
for i = 1, (NUM_GROUP_LOOT_FRAMES or 4) do
    local cadre = _G["GroupLootFrame" .. i]
    if cadre and cadre.HookScript then cadre:HookScript("OnShow", P("GroupLootFrame.OnShow", JetDeButin)) end
end

-- ----------------------------------------------------------------------------
-- Montures et familiers (panneau de CoA)
-- ----------------------------------------------------------------------------
local function NomCompagnon(c)
    if type(c) ~= "table" or type(c.name) ~= "string" then return nil end
    local fr = (c.spellID and A.NomSort and A.NomSort(c.spellID, c.name)) or (A.NomCreature and A.NomCreature(c.name))
    if fr and fr ~= c.name then return fr end
    return nil
end
A.NomCompagnon = NomCompagnon

local function ZoneDuBouton(b)
    if type(b.GetFontString) == "function" then
        local z = b:GetFontString()
        if z then return z end
    end
    return b.Text
end

local function Compagnons(cadre, profondeur)
    if not cadre or profondeur > 8 or type(cadre.GetChildren) ~= "function" then return end
    local enfants = { cadre:GetChildren() }
    for i = 1, #enfants do
        local e = enfants[i]
        if type(e) == "table" and type(e.IsVisible) == "function" and e:IsVisible() then
            local c = rawget(e, "companion")
            if type(c) == "table" then
                local zone, fr = ZoneDuBouton(e), NomCompagnon(c)
                if zone and fr and type(zone.GetText) == "function" and zone:GetText() == c.name then A.Ecrire(zone, fr) end
            else
                Compagnons(e, profondeur + 1)
            end
        end
    end
end

local function FicheCompagnon()
    local p = AscensionPetPaperDollPanel
    local o = p and p.CompanionTab and p.CompanionTab.CompanionModel and p.CompanionTab.CompanionModel.Overlay
    local titre = o and o.Title
    if not titre or type(titre.GetText) ~= "function" or type(titre.IsVisible) ~= "function" or not titre:IsVisible() then return end
    local t = titre:GetText()
    if not t or t == "" or A.DejaEcrit(titre, t) then return end
    local fr = (A.NomSortParNom and A.NomSortParNom(t)) or (A.NomCreature and A.NomCreature(t))
    if fr and fr ~= t then A.Ecrire(titre, fr) end
end

function A.TraduireCompagnons()
    if not A.Actif() then return end
    local panneau = AscensionCharacterCompanionPanel
    if panneau and type(panneau.IsVisible) == "function" and panneau:IsVisible() then Compagnons(panneau, 0) end
    FicheCompagnon()
end

-- ----------------------------------------------------------------------------
-- Infobulles du tableau d'appel (signalement de Dan du 18/11). CallBoardWidgets.lua (l. 385) et CallBoardRender.lua
-- (l. 70) composent leurs lignes a la main : « 0 |Ticone|t |cff..|Hitem:975001:..|h[Bazaar Token]|h|r » et
-- « - Rune of Descension ». Tant que l'infobulle appartient a un bouton du tableau d'appel, on y remplace le nom
-- de l'objet : par son lien (numero, anglais verifie) ou, pour « - Nom », par le nom connu sans ambiguite.
-- ----------------------------------------------------------------------------
local function DansTableauAppel(cadre)
    local racine = CallBoardUI
    if type(racine) ~= "table" then return false end
    for _ = 1, 20 do
        if not cadre or type(cadre) ~= "table" then return false end
        if cadre == racine then return true end
        if type(cadre.GetParent) ~= "function" then return false end
        cadre = cadre:GetParent()
    end
    return false
end

local function LigneTableau(t)
    local avant, id, nom, apres = string.match(t, "^(.*|Hitem:(%d+)[^|]*|h%[)(.-)(%]|h.*)$")
    if id then
        local fr = A.NomObjetAffiche(tonumber(id), nom)
        return fr and fr ~= nom and (avant .. fr .. apres) or nil
    end
    local tiret, nu = string.match(t, "^(%s*%-%s+)(.+)$")
    if nu then
        local fr = A.Nom("objet_quete", nu)
        return fr and fr ~= nu and (tiret .. fr) or nil
    end
    return nil
end
A.LigneTableauAppel = LigneTableau

function A.TraduireBulleTableauAppel()
    if not A.Actif() or not GameTooltip or type(GameTooltip.IsVisible) ~= "function" or not GameTooltip:IsVisible() then return end
    if type(GameTooltip.GetOwner) ~= "function" or not DansTableauAppel(GameTooltip:GetOwner()) then return end
    local change = false
    for i = 1, GameTooltip:NumLines() do
        local zone = _G["GameTooltipTextLeft" .. i]
        local t = zone and zone:GetText()
        if t and t ~= "" and not A.DejaEcrit(zone, t) then
            local fr = LigneTableau(t)
            if fr then A.Ecrire(zone, fr); change = true end
        end
    end
    if change then GameTooltip:Show() end
end

local veille, ecoule = CreateFrame("Frame"), 0
veille:SetScript("OnUpdate", P("Echanges.veille", function(_, dt)
    ecoule = ecoule + (dt or 0)
    if ecoule < 0.4 then return end
    ecoule = 0
    A.TraduireCompagnons()
    A.TraduireBulleTableauAppel()
end, true))

-- ----------------------------------------------------------------------------
-- Fenetre de metier (1.2.1, signalement d'un joueur du 26/11 : composants restes en anglais). Blizzard_TradeSkillUI
-- (charge a la demande) : TradeSkillFrame_SetSelection(id) pose TradeSkillReagentNName (l. 313-315, nom tire de
-- GetTradeSkillReagentInfo) et TradeSkillSkillName (l. 283). Nom par le lien (GetTradeSkillReagentItemLink,
-- GetTradeSkillItemLink) : pose seulement si l'anglais affiche est celui qu'on a traduit.
-- ----------------------------------------------------------------------------
local function Metier(id)
    if not A.Actif() or type(id) ~= "number" then return end
    if type(GetTradeSkillReagentItemLink) == "function" then
        for i = 1, (MAX_TRADE_SKILL_REAGENTS or 8) do
            local zone = _G["TradeSkillReagent" .. i .. "Name"]
            local lien = zone and GetTradeSkillReagentItemLink(id, i)
            if lien then A.NomObjetZone(zone, lien) end
        end
    end
    if TradeSkillSkillName and type(GetTradeSkillItemLink) == "function" then
        local lien = GetTradeSkillItemLink(id)
        if lien and string.find(lien, "|Hitem:", 1, true) then A.NomObjetZone(TradeSkillSkillName, lien) end
    end
end
A.TraduireMetier = Metier

local metier_branche = false
local function BrancherMetier()
    if metier_branche or type(TradeSkillFrame_SetSelection) ~= "function" then return end
    metier_branche = true
    hooksecurefunc("TradeSkillFrame_SetSelection", P("TradeSkillFrame_SetSelection", Metier))
end

-- ----------------------------------------------------------------------------
-- Branchements des fenetres chargees a la demande
-- ----------------------------------------------------------------------------
BrancherEncheres()
BrancherMetier()
local guetteur = CreateFrame("Frame")
guetteur:RegisterEvent("ADDON_LOADED")
guetteur:SetScript("OnEvent", P("Echanges.ADDON_LOADED", function(self, _, nom)
    if nom == "Blizzard_AuctionUI" then BrancherEncheres() end
    if nom == "Blizzard_TradeSkillUI" then BrancherMetier() end
    if encheres_branchees and metier_branche then self:UnregisterEvent("ADDON_LOADED") end
end))
