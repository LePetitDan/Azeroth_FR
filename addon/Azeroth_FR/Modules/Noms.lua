-- ============================================================================
-- Azeroth_FR : noms affiches dans l'interface (version 0.2).
-- - cadres d'unite : cible, focalisation, cible de la cible, boss (nom de la creature par le
--   numero tire de son GUID, verifie par l'empreinte du nom anglais) ;
-- - zones : minicarte (texte et infobulle), grand texte de zone a l'arrivee, carte du monde
--   (nom de la zone survolee, titre, listes deroulantes), en-tetes du journal (Quetes.lua),
--   noms de canaux « General - Zone » (Discussion.lua).
-- Affichage seulement : on passe APRES le jeu (hooksecurefunc, HookScript) et on ne change
-- que le texte d'une zone de texte. Les cadres d'unite sont securises : on ne touche ni a leurs
-- variables ni a leurs methodes, seulement au texte de leur zone « name » (permis par le jeu,
-- meme en combat).
-- LIMITE : les noms AU-DESSUS DES TETES (personnages, PNJ) sont dessines par le moteur du jeu,
-- hors de l'interface Lua : un add-on ne peut pas les changer. Ils restent en anglais.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger

-- Petite memoire des noms de zone (la carte du monde redemande le meme nom a chaque image).
local memo, taille = {}, 0
local function NomZone(t)
    if type(t) ~= "string" or t == "" then return nil end
    local m = memo[t]
    if m ~= nil then return m or nil end
    local fr = A.Nom("zone", t) or false
    taille = taille + 1
    if taille > 500 then memo, taille = {}, 0 end
    memo[t] = fr
    return fr or nil
end
A.NomZone = NomZone

local function TraduireZoneTexte(zone, fn)
    if not zone or type(zone.GetText) ~= "function" then return end
    local t = zone:GetText()
    if not t or t == "" or A.DejaEcrit(zone, t) then return end
    local fr = (fn or NomZone)(t)
    if fr and fr ~= t then A.Ecrire(zone, fr) end
end
A.TraduireZoneTexte = TraduireZoneTexte

-- ----------------------------------------------------------------------------
-- Cadres d'unite (UnitFrame_Update est appele par la cible, la focalisation, la cible de la
-- cible et les cadres de boss ; UnitFrame_OnEvent pour UNIT_NAME_UPDATE).
-- ----------------------------------------------------------------------------
local function TraduireCadreUnite(cadre)
    if not A.Actif() or type(cadre) ~= "table" then return end
    local unite = cadre.overrideName or cadre.unit
    local zone = cadre.name
    if not unite or type(zone) ~= "table" or type(zone.GetText) ~= "function" then return end
    local t = zone:GetText()
    if not t or t == "" or A.DejaEcrit(zone, t) then return end
    local fr, en = A.NomUnite(unite)
    if fr and t == en then A.Ecrire(zone, fr) end
end
A.TraduireCadreUnite = TraduireCadreUnite

if type(UnitFrame_Update) == "function" then
    hooksecurefunc("UnitFrame_Update", P("UnitFrame_Update", TraduireCadreUnite))
end
if type(UnitFrame_OnEvent) == "function" then
    hooksecurefunc("UnitFrame_OnEvent", P("UnitFrame_OnEvent", function(cadre, evenement)
        if evenement == "UNIT_NAME_UPDATE" then TraduireCadreUnite(cadre) end
    end))
end

-- ----------------------------------------------------------------------------
-- Minicarte : nom de la zone et son infobulle.
-- ----------------------------------------------------------------------------
if type(Minimap_Update) == "function" then
    hooksecurefunc("Minimap_Update", P("Minimap_Update", function()
        if A.Actif() then TraduireZoneTexte(MinimapZoneText) end
    end))
end
if type(Minimap_SetTooltip) == "function" then
    hooksecurefunc("Minimap_SetTooltip", P("Minimap_SetTooltip", function()
        if not A.Actif() or not GameTooltip or not MinimapZoneTextButton then return end
        if not GameTooltip:IsOwned(MinimapZoneTextButton) then return end
        local modifie = false
        for i = 1, GameTooltip:NumLines() do
            local l = _G["GameTooltipTextLeft" .. i]
            local t = l and l:GetText()
            local fr = t and NomZone(t)
            if fr and fr ~= t then l:SetText(fr); modifie = true end
        end
        if modifie then GameTooltip:Show() end
    end))
end

-- ----------------------------------------------------------------------------
-- Grand texte de zone (a l'arrivee dans une zone ou une sous-zone).
-- ----------------------------------------------------------------------------
local function TraduireTexteDeZone()
    if not A.Actif() then return end
    TraduireZoneTexte(ZoneTextString)
    TraduireZoneTexte(SubZoneTextString)
end
if ZoneTextFrame and ZoneTextFrame.HookScript then
    ZoneTextFrame:HookScript("OnEvent", P("ZoneText", TraduireTexteDeZone))
end
if SubZoneTextFrame and SubZoneTextFrame.HookScript then
    SubZoneTextFrame:HookScript("OnEvent", P("SubZoneText", TraduireTexteDeZone))
end

-- ----------------------------------------------------------------------------
-- Carte du monde : nom de la zone survolee (pose a chaque image par WorldMapButton_OnUpdate),
-- titre de la fenetre, texte des listes deroulantes (continent, zone).
-- ----------------------------------------------------------------------------
local function TraduireCarte()
    if not A.Actif() then return end
    TraduireZoneTexte(WorldMapFrameAreaLabel)
    TraduireZoneTexte(WorldMapFrameTitle)
    TraduireZoneTexte(WorldMapZoneDropDownText)
    TraduireZoneTexte(WorldMapContinentDropDownText)
end
A.TraduireCarte = TraduireCarte
if WorldMapButton and WorldMapButton.HookScript then
    WorldMapButton:HookScript("OnUpdate", P("WorldMapButton.OnUpdate", function() TraduireZoneTexte(WorldMapFrameAreaLabel) end))
end
for _, fn in ipairs({ "WorldMapFrame_SetMapName", "WorldMapZoneDropDown_Update", "WorldMapContinentsDropDown_Update" }) do
    if type(_G[fn]) == "function" then hooksecurefunc(fn, P(fn, TraduireCarte)) end
end
if WorldMapFrame and WorldMapFrame.HookScript then
    WorldMapFrame:HookScript("OnShow", P("WorldMapFrame.OnShow", TraduireCarte))
end
