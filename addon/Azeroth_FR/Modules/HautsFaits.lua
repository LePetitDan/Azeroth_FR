-- ============================================================================
-- Azeroth_FR : fenetre des hauts faits (version 0.9.2, essai 8 au niveau 10 ; 0.9.4 : barres du resume).
-- Verifie le 07/11/2026 contre le code que le client CoA charge (AddOns/Blizzard_AchievementUI, charge a la demande,
-- et FrameXML/AlertFrames.lua) :
--   - AchievementButton_DisplayAchievement (l. 1012) : button.label (nom), button.description et
--     button.hiddenDescription (description), button.reward (« Reward: … ») ; button.id = numero du haut fait ;
--   - AchievementFrameCategories_DisplayButton (l. 367) : button.label (nom de categorie), button.categoryID ;
--     bulle de la categorie : AchievementFrameCategory_StatusBarTooltip (GameTooltip:SetText(self.name)) ;
--   - AchievementObjectives_DisplayCriteria (l. 1423) : criteres textes (AchievementButton_GetCriteria(n).name,
--     « - » devant un critere non rempli), meta-criteres (AchievementButton_GetMeta(n).label = nom d'un haut fait) ;
--   - AchievementFrameSummary_UpdateAchievements (l. 1832) : AchievementFrameSummaryAchievementN (label, description) ;
--   - AchievementFrameStats_SetStat (l. 1705) : button:SetText(nom de la statistique) ;
--   - AchievementFrameComparison_DisplayAchievement (l. 2452) : button.player.label, button.player.description ;
--   - AchievementAlertFrame_ShowAlert (AlertFrames.lua l. 230) : <cadre>Name (nom du haut fait gagne).
-- Donnees (famille hauts_faits, add-on Azeroth_FR_HautsFaits, chargee a la demande) : HF numero -> {nom, empreinte,
-- description, empreinte, recompense, empreinte}, HC categorie -> {nom, empreinte}, HK critere -> {texte, empreinte}.
-- Le francais n'est pose que si le texte affiche est EXACTEMENT l'anglais de la source (empreinte). On n'ecrit que
-- dans des zones de texte de cadres non securises ; aucune variable du jeu n'est touchee.
-- ============================================================================
local A = AzerothFR
local match, select = string.match, select
local P = A.Proteger

local function Table(nom) return A.TableDe("hauts_faits", nom) end

local function Enreg(nom, id)
    if type(id) ~= "number" then return nil end
    local t = Table(nom)
    local r = t and t:ParId(id)
    return type(r) == "table" and r or nil
end
function A.HautFait(id) return Enreg("HF", id) end

local function Actif() return A.Actif() and A.ModuleActif("hauts_faits") end

-- Pose fr dans la zone si son texte (sans enrobage de couleur, sans « - » de tete) a l'empreinte h.
local function Poser(zone, fr, h)
    if not zone or not fr or not h or h == 0 or type(zone.GetText) ~= "function" then return false end
    local t = zone:GetText()
    if type(t) ~= "string" or t == "" or A.DejaEcrit(zone, t) then return false end
    local e1, coeur, e2 = A.Enrobage(t)
    local tiret, reste = match(coeur, "^(%- )(.*)$")
    if tiret then coeur = reste else tiret = "" end
    if A.H1(coeur) ~= h then return false end
    return A.Ecrire(zone, e1 .. tiret .. fr .. e2)
end
A.PoserHautFait = Poser

local function NomEtDescription(label, description, id, cache)
    local r = A.HautFait(id)
    if not r then return end
    if r[1] then Poser(label, r[1], r[2]) end
    if description and r[3] then Poser(description, r[3], r[4]) end
    if cache and r[3] then Poser(cache, r[3], r[4]) end
end

-- Liste des hauts faits : nom, description (et sa copie cachee qui sert a mesurer la hauteur), recompense
local function SurBouton(button)
    if not Actif() or type(button) ~= "table" or type(button.id) ~= "number" then return end
    NomEtDescription(button.label, button.description, button.id, button.hiddenDescription)
    local r = A.HautFait(button.id)
    if r and r[5] then Poser(button.reward, r[5], r[6]) end
end

local function SurCategorie(button, element)
    if not Actif() or not element or type(button) ~= "table" or type(button.categoryID) ~= "number" then return end
    local r = Enreg("HC", button.categoryID)
    if r and r[1] then Poser(button.label, r[1], r[2]) end
end

local function SurBulleCategorie(self)
    if not Actif() or type(self) ~= "table" or type(self.categoryID) ~= "number" then return end
    local r = Enreg("HC", self.categoryID)
    if r and r[1] and Poser(_G["GameTooltipTextLeft1"], r[1], r[2]) and GameTooltip:IsShown() then
        pcall(GameTooltip.Show, GameTooltip)
    end
end

-- Criteres d'un haut fait (fenetre deroulee) : meme ordre que la boucle de Blizzard
local BARRE = ACHIEVEMENT_CRITERIA_PROGRESS_BAR or 1
local function SurCriteres(objectifs, id)
    if not Actif() or type(id) ~= "number" or type(GetAchievementNumCriteria) ~= "function" then return end
    local n = GetAchievementNumCriteria(id) or 0
    local textes, metas = 0, 0
    for i = 1, n do
        local _, typ, _, _, _, _, drapeaux, asset, _, idc = GetAchievementCriteriaInfo(id, i)
        if typ == (CRITERIA_TYPE_ACHIEVEMENT or 8) and asset then
            metas = metas + 1
            local m = _G["AchievementFrameMeta" .. metas]
            if m and m.label then NomEtDescription(m.label, nil, asset) end
        elseif type(drapeaux) == "number" and bit and bit.band(drapeaux, BARRE) == BARRE then
            -- barre de progression : nombres seulement
        else
            textes = textes + 1
            local c = _G["AchievementFrameCriteria" .. textes]
            local r = Enreg("HK", idc)
            if c and c.name and r and r[1] then Poser(c.name, r[1], r[2]) end
        end
    end
end

local function SurResume()
    if not Actif() then return end
    for i = 1, 8 do
        local b = _G["AchievementFrameSummaryAchievement" .. i]
        if not b then break end
        if b:IsShown() and type(b.id) == "number" then NomEtDescription(b.label, b.description, b.id) end
    end
end

-- 0.9.4 (essai 8, captures du 08/11) : barres des categories du resume (« General 1/48 », « Quests »…) : leur nom est
-- pose une fois pour toutes a la creation du cadre (AchievementFrameSummaryCategory_OnLoad, l. 1980 : GetCategoryInfo de
-- self:GetID() dans <cadre>Label), avant nos crochets : on le reprend a chaque affichage (OnShow, et la mise a jour du
-- resume). Numero de categorie = GetID() du cadre (92, 96, 97, 95, 168, 169, 201…).
local function SurBarreCategorie(barre)
    if not Actif() or type(barre) ~= "table" or type(barre.GetID) ~= "function" or type(barre.GetName) ~= "function" then
        return
    end
    local nom = barre:GetName()
    local r = Enreg("HC", barre:GetID())
    if nom and r and r[1] then Poser(_G[nom .. "Label"], r[1], r[2]) end
end

local function SurBarresCategories()
    if not Actif() then return end
    for i = 1, 12 do
        local b = _G["AchievementFrameSummaryCategoriesCategory" .. i]
        if not b then break end
        SurBarreCategorie(b)
    end
end

local function SurStat(button, categorie, index, _, resume)
    if not Actif() or type(button) ~= "table" or type(button.id) ~= "number" then return end
    local r = A.HautFait(button.id)
    if r and r[1] then Poser(button, r[1], r[2]) end
end

local function SurComparaison(button)
    if not Actif() or type(button) ~= "table" or type(button.id) ~= "number" or not button.player then return end
    NomEtDescription(button.player.label, button.player.description, button.id)
end

local function SurAlerte(idHF)
    if not Actif() or type(idHF) ~= "number" then return end
    for i = 1, 4 do
        local f = _G["AchievementAlertFrame" .. i]
        if f and f.id == idHF then
            local r = A.HautFait(idHF)
            if r and r[1] then Poser(_G[f:GetName() .. "Name"], r[1], r[2]) end
        end
    end
end

-- Bulle d'un lien de haut fait (resume, discussion) : nom, description, criteres (texte exact d'un critere)
local function SurBulleLien(bulle, lien)
    if not Actif() or type(lien) ~= "string" then return end
    local id = tonumber(match(lien, "achievement:(%d+)"))
    if not id or type(bulle.NumLines) ~= "function" then return end
    local nom = bulle:GetName()
    local r = A.HautFait(id)
    local par_empreinte = {}
    if r then
        if r[1] then par_empreinte[r[2]] = r[1] end
        if r[3] then par_empreinte[r[4]] = r[3] end
    end
    local n = (type(GetAchievementNumCriteria) == "function" and GetAchievementNumCriteria(id)) or 0
    for i = 1, n do
        local idc = select(10, GetAchievementCriteriaInfo(id, i))
        local k = Enreg("HK", idc)
        if k and k[1] then par_empreinte[k[2]] = k[1] end
    end
    local modifie = false
    for i = 1, bulle:NumLines() do
        for _, cote in ipairs({ "TextLeft", "TextRight" }) do
            local z = nom and _G[nom .. cote .. i]
            local t = z and z:GetText()
            if t and t ~= "" and not A.DejaEcrit(z, t) then
                local e1, coeur, e2 = A.Enrobage(t)
                local fr = par_empreinte[A.H1(coeur)]
                if fr then A.Ecrire(z, e1 .. fr .. e2); modifie = true end
            end
        end
    end
    if modifie and bulle:IsShown() and not A.EstProtege(bulle) then pcall(bulle.Show, bulle) end
end

-- ----------------------------------------------------------------------------
local branche_ui, branche_alerte, branche_lien = false, false, false
local function Brancher()
    if not branche_alerte and type(AchievementAlertFrame_ShowAlert) == "function" then
        hooksecurefunc("AchievementAlertFrame_ShowAlert", P("HautsFaits.alerte", SurAlerte))
        branche_alerte = true
    end
    if not branche_lien and GameTooltip and type(GameTooltip.SetHyperlink) == "function" then
        hooksecurefunc(GameTooltip, "SetHyperlink", P("HautsFaits.lien", SurBulleLien))
        branche_lien = true
    end
    if branche_ui or type(AchievementButton_DisplayAchievement) ~= "function" then return end
    hooksecurefunc("AchievementButton_DisplayAchievement", P("HautsFaits.bouton", SurBouton))
    if type(AchievementFrameCategories_DisplayButton) == "function" then
        hooksecurefunc("AchievementFrameCategories_DisplayButton", P("HautsFaits.categorie", SurCategorie))
    end
    if type(AchievementFrameCategory_StatusBarTooltip) == "function" then
        hooksecurefunc("AchievementFrameCategory_StatusBarTooltip", P("HautsFaits.bulle_categorie", SurBulleCategorie))
    end
    if type(AchievementObjectives_DisplayCriteria) == "function" then
        hooksecurefunc("AchievementObjectives_DisplayCriteria", P("HautsFaits.criteres", SurCriteres))
    end
    if type(AchievementFrameSummary_UpdateAchievements) == "function" then
        hooksecurefunc("AchievementFrameSummary_UpdateAchievements", P("HautsFaits.resume", SurResume))
        hooksecurefunc("AchievementFrameSummary_UpdateAchievements", P("HautsFaits.resume_barres", SurBarresCategories))
    end
    if type(AchievementFrameSummaryCategory_OnShow) == "function" then
        hooksecurefunc("AchievementFrameSummaryCategory_OnShow", P("HautsFaits.barre_categorie", SurBarreCategorie))
    end
    if type(AchievementFrameStats_SetStat) == "function" then
        hooksecurefunc("AchievementFrameStats_SetStat", P("HautsFaits.stat", SurStat))
    end
    if type(AchievementFrameComparison_DisplayAchievement) == "function" then
        hooksecurefunc("AchievementFrameComparison_DisplayAchievement", P("HautsFaits.comparaison", SurComparaison))
    end
    branche_ui = true
    SurBarresCategories()
end

local ev = CreateFrame("Frame")
ev:RegisterEvent("ADDON_LOADED")
ev:RegisterEvent("PLAYER_LOGIN")
ev:SetScript("OnEvent", P("HautsFaits.OnEvent", function(self, evenement, nom)
    if evenement == "ADDON_LOADED" and nom ~= "Blizzard_AchievementUI" and nom ~= "Azeroth_FR" then return end
    Brancher()
end, true))
Brancher()
