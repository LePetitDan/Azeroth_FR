-- ============================================================================
-- Azeroth_FR : complements de la version 0.8 (essai 7, 07/11/2026). Affichage seulement.
--   - titre des sacs (n° 5) : ContainerFrame_GenerateFrame (patch-B, ContainerFrame.lua l. 404) pose
--     <cadre>Name:SetText(GetBagName(id)) ; le nom vient du lien de l'objet range dans l'emplacement du sac ;
--   - infobulles sans unite ni objet ni sort (n° 18 et 19) : objets du monde (« Elwynn Tree » / « Requires
--     Woodcutting »), points de la minicarte (« Goldshire » / « Lion's Pride Inn ») : GameTooltip OnShow ;
--   - repasse differee (n° 14 et 15) : la fenetre de quete d'un PNJ est retraduite un instant apres son
--     affichage (objets de recompense, nom du PNJ en en-tete), au cas ou le jeu ou les donnees arrivent apres.
-- ============================================================================
local A = AzerothFR
local match, sub, find, gsub = string.match, string.sub, string.find, string.gsub
local P = A.Proteger

-- ----------------------------------------------------------------------------
-- Plus tard : fn() apres « delai » secondes (une seule fois). Pas de C_Timer en 3.3.5.
-- ----------------------------------------------------------------------------
local file = {}
local horloge = CreateFrame("Frame")
horloge:Hide()
horloge:SetScript("OnUpdate", P("Divers.plus_tard", function(self, ecoule)
    local reste = {}
    for _, t in ipairs(file) do
        t.delai = t.delai - (ecoule or 0)
        if t.delai <= 0 then pcall(t.fn) else reste[#reste + 1] = t end
    end
    file = reste
    if #file == 0 then self:Hide() end
end, true))
function A.PlusTard(delai, fn)
    if type(fn) ~= "function" or #file > 50 then return end
    file[#file + 1] = { delai = delai or 0, fn = fn }
    horloge:Show()
end

-- ----------------------------------------------------------------------------
-- Titre des sacs
-- ----------------------------------------------------------------------------
local function TitreSac(cadre, _, id)
    if not A.Actif() or not cadre or type(id) ~= "number" or id <= 0 then return end
    local zone = _G[(cadre:GetName() or "") .. "Name"]
    if not zone or type(ContainerIDToInventoryID) ~= "function" or type(GetInventoryItemLink) ~= "function" then return end
    local ok, emplacement = pcall(ContainerIDToInventoryID, id)
    if not ok or not emplacement then return end
    A.NomObjetZone(zone, GetInventoryItemLink("player", emplacement))
end
if type(ContainerFrame_GenerateFrame) == "function" then
    hooksecurefunc("ContainerFrame_GenerateFrame", P("ContainerFrame_GenerateFrame", TitreSac))
end

-- ----------------------------------------------------------------------------
-- Infobulles sans unite, objet ni sort
-- ----------------------------------------------------------------------------
local function NomLieuOuChose(t)
    return (A.NomZone and A.NomZone(t)) or A.Nom("objet_monde", t) or (A.NomCreature and A.NomCreature(t))
end

-- Une ligne qui peut contenir plusieurs noms separes par des retours a la ligne (minicarte).
local function Lignes(t, fn)
    if not find(t, "\n", 1, true) then return fn(t) end
    local out, change = {}, false
    for morceau in string.gmatch(t .. "\n", "(.-)\n") do
        local fr = morceau ~= "" and fn(morceau)
        if fr then change = true end
        out[#out + 1] = fr or morceau
    end
    return change and table.concat(out, "\n") or nil
end

-- « Requiert Woodcutting », « Requiert Mining (75) » : gabarit ITEM_REQ_SKILL du jeu (« Requires %s », deja en
-- francais par PTRXML) ; seul le nom de metier qui suit est traduit.
local function MetierEnFin(t)
    local g = type(ITEM_REQ_SKILL) == "string" and ITEM_REQ_SKILL or "Requires %s"
    local pre = match(g, "^(.-)%%s")
    if not pre or pre == "" or sub(t, 1, #pre) ~= pre then return nil end
    local reste = sub(t, #pre + 1)
    local metier, rang = match(reste, "^(.-)( %(%d+%))$")
    if not metier then metier, rang = reste, "" end
    -- 0.9 : aussi les objets de focalisation (« Requires Anvil »), outils (« Mining Pick ») et formes (« Cat Form »)
    local fr = A.Nom("competence", metier) or A.Nom("focalisation", metier) or A.Nom("forme", metier)
    return fr and (pre .. fr .. rang)
end
-- « Requires X » ou « Requiert X » (gabarit anglais ou celui du jeu) : X traduit par les tables de noms
function A.LigneRequiert(t)
    if type(t) ~= "string" or t == "" then return nil end
    local fr = MetierEnFin(t)
    if fr then return fr end
    local reste = match(t, "^Requires (.+)$")
    if not reste then return nil end
    local g = type(ITEM_REQ_SKILL) == "string" and ITEM_REQ_SKILL or "Requires %s"
    local pre = match(g, "^(.-)%%s") or "Requires "
    local metier, rang = match(reste, "^(.-)( %(%d+%))$")
    if not metier then metier, rang = reste, "" end
    local nom = A.Nom("competence", metier) or A.Nom("focalisation", metier) or A.Nom("forme", metier)
    return nom and (pre .. nom .. rang)
end

local en_cours = false
local function SurBulle(bulle)
    if en_cours or not A.Actif() or not bulle or not bulle.NumLines then return end
    if bulle.GetUnit and bulle:GetUnit() then return end
    if bulle.GetItem and bulle:GetItem() then return end
    if bulle.GetSpell and bulle:GetSpell() then return end
    local nomBulle = bulle:GetName()
    if not nomBulle then return end
    local proprietaire = bulle.GetOwner and bulle:GetOwner()
    local minicarte = proprietaire and Minimap and proprietaire == Minimap
    local modifie = false
    for i = 1, bulle:NumLines() do
        local l = _G[nomBulle .. "TextLeft" .. i]
        local t = l and l:GetText()
        if t and t ~= "" and not A.DejaEcrit(l, t) then
            local fr
            if minicarte or i == 1 then
                fr = Lignes(t, NomLieuOuChose)
            else
                fr = MetierEnFin(t)
            end
            if fr and fr ~= t then A.Ecrire(l, fr); modifie = true end
        end
    end
    if modifie and bulle:IsShown() and not A.EstProtege(bulle) then
        en_cours = true
        pcall(bulle.Show, bulle)
        en_cours = false
    end
end
A.SurBulleSimple = SurBulle
if GameTooltip and GameTooltip.HookScript then
    GameTooltip:HookScript("OnShow", P("GameTooltip.OnShow", SurBulle))
end

-- ----------------------------------------------------------------------------
-- Repasse differee de la fenetre de quete
-- ----------------------------------------------------------------------------
local function Repasse()
    if not A.Actif() or not A.TraduireFenetreQuete then return end
    local visible = (QuestFrame and QuestFrame:IsShown()) or (QuestLogFrame and QuestLogFrame:IsShown())
    if visible then A.TraduireFenetreQuete() end
end
if type(QuestInfo_Display) == "function" then
    hooksecurefunc("QuestInfo_Display", P("Divers.QuestInfo_Display", function()
        A.PlusTard(0.05, Repasse)
        A.PlusTard(0.6, Repasse)
    end))
end
