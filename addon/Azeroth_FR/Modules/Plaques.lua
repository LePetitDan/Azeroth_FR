-- ============================================================================
-- Azeroth_FR : plaques de nom (version 0.4). Interrupteur : /azfr plaques on|off.
--
-- Ce que fait le client CoA (lu le 04/11/2026) :
--   - le moteur envoie NAME_PLATE_UNIT_ADDED / NAME_PLATE_UNIT_REMOVED (unite « nameplateN ») et donne la plaque
--     par GetNamePlateForUnit(unite) (patch-B, Util/C_NamePlateManager.lua : SecureNamePlateDriver) ;
--   - plaque classique 3.3.5 : la plaque est un enfant sans nom de WorldFrame, son nom est une zone de texte du
--     cadre ; plaque d'Ascension (Ascension_NamePlates, chargee si l'option « nouvelles plaques » est active) :
--     plaque.UnitFrame.name (CompactUnitFrame), remise a jour par le client (CompactUnitFrame_UpdateName) ;
--   - les plaques sont REUTILISEES d'une unite a l'autre.
-- Ce que fait l'add-on : a l'arrivee d'une plaque (et toutes les 0,3 s pour les plaques visibles, au plus 40),
-- il cherche, parmi les zones de texte du nom, celle dont le texte est EXACTEMENT le nom anglais de l'unite
-- (UnitName) et y pose le nom francais prouve : numero de la creature tire du GUID et empreinte du nom anglais
-- (A.NomUnite), jamais pour un joueur. Une zone dont le cadre est protege n'est pas touchee. Un texte remis en
-- anglais par le client (plaque reutilisee, mise a jour) est repris au passage suivant.
-- Si le client n'a pas GetNamePlateForUnit, repli borne : enfants sans nom de WorldFrame (au plus 300), zone de
-- texte qui porte un nom de creature connu SANS AMBIGUITE (table des creatures par nom anglais).
-- Affichage seulement : SetText d'une zone de texte, rien d'autre ; tout sous pcall.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger

local MAX_PLAQUES, PAS, MAX_ENFANTS = 40, 0.3, 300
local unites = {}              -- unite « nameplateN » -> true
local nb_unites = 0
A.Compteurs.plaques = 0

local function Actif()
    return A.ModuleActif("plaques")
end

-- Zones de texte candidates d'une plaque : nom de la plaque d'Ascension, puis zones de texte du cadre.
local function Zones(plaque)
    local out = {}
    local uf = type(plaque.UnitFrame) == "table" and plaque.UnitFrame or nil
    if uf and type(uf.name) == "table" and type(uf.name.GetText) == "function" then out[#out + 1] = uf.name end
    if type(plaque.GetRegions) == "function" then
        local regions = { plaque:GetRegions() }
        for i = 1, #regions do
            local r = regions[i]
            if r and type(r.GetObjectType) == "function" and r:GetObjectType() == "FontString" then out[#out + 1] = r end
        end
    end
    return out
end

local function ZoneTouchable(z)
    local parent = type(z.GetParent) == "function" and z:GetParent() or nil
    return not (parent and A.EstProtege(parent))
end

-- Traduit la plaque d'une unite ; renvoie true si un nom francais est en place.
local function TraduireUnite(unite)
    if type(GetNamePlateForUnit) ~= "function" then return false end
    local ok, plaque = pcall(GetNamePlateForUnit, unite)
    if not ok or type(plaque) ~= "table" then return false end
    local fr, en = A.NomUnite(unite)
    if not fr or not en or fr == en then return false end
    for _, z in ipairs(Zones(plaque)) do
        local t = z:GetText()
        if t == fr and A.DejaEcrit(z, t) then return true end
        if t == en and ZoneTouchable(z) then
            A.Ecrire(z, fr)
            A.Compteurs.plaques = A.Compteurs.plaques + 1
            return true
        end
    end
    return false
end
A.TraduirePlaque = TraduireUnite

-- Repli sans GetNamePlateForUnit : enfants sans nom de WorldFrame, nom de creature sans ambiguite.
local function Repli()
    if not WorldFrame or type(WorldFrame.GetChildren) ~= "function" then return end
    local enfants = { WorldFrame:GetChildren() }
    local bas = math.max(1, #enfants - MAX_ENFANTS + 1)
    for i = #enfants, bas, -1 do
        local c = enfants[i]
        if c and type(c.GetName) == "function" and c:GetName() == nil and type(c.GetNumChildren) == "function"
            and (c:GetNumChildren() or 0) > 0 and type(c.IsShown) == "function" and c:IsShown() and not A.EstProtege(c) then
            for _, z in ipairs(Zones(c)) do
                local t = z:GetText()
                if t and t ~= "" and not A.DejaEcrit(z, t) then
                    local fr = A.NomCreature(t)
                    if fr and fr ~= t and ZoneTouchable(z) then
                        A.Ecrire(z, fr)
                        A.Compteurs.plaques = A.Compteurs.plaques + 1
                    end
                end
            end
        end
    end
end
A.PlaquesRepli = Repli

local cadre = CreateFrame("Frame")
cadre:RegisterEvent("NAME_PLATE_UNIT_ADDED")
cadre:RegisterEvent("NAME_PLATE_UNIT_REMOVED")
cadre:RegisterEvent("PLAYER_ENTERING_WORLD")
cadre:SetScript("OnEvent", P("Plaques.OnEvent", function(self, evenement, unite)
    if evenement == "PLAYER_ENTERING_WORLD" then
        for u in pairs(unites) do unites[u] = nil end
        nb_unites = 0
        return
    end
    if type(unite) ~= "string" then return end
    if evenement == "NAME_PLATE_UNIT_REMOVED" then
        if unites[unite] then unites[unite] = nil; nb_unites = nb_unites - 1 end
        return
    end
    if not unites[unite] and nb_unites < MAX_PLAQUES then unites[unite] = true; nb_unites = nb_unites + 1 end
    if Actif() then TraduireUnite(unite) end
end))

local cumul = 0
cadre:Show()
cadre:SetScript("OnUpdate", P("Plaques.OnUpdate", function(self, ecoule)
    cumul = cumul + (ecoule or 0)
    if cumul < PAS then return end
    cumul = 0
    if not Actif() then return end
    if type(GetNamePlateForUnit) == "function" then
        if nb_unites > 0 then A.Trace("Plaques.passage") end
        for u in pairs(unites) do
            if type(UnitExists) == "function" and not UnitExists(u) then
                unites[u] = nil; nb_unites = nb_unites - 1
            else
                TraduireUnite(u)
            end
        end
    else
        A.Trace("Plaques.repli")
        Repli()
    end
end, true))
