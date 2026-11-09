-- ============================================================================
-- Azeroth_FR : fenetre des maitres (version 0.8, essai 7 n° 1 et 17) : maitres de classe, de metier, de monte.
-- Verifie le 07/11/2026 contre le code que le client CoA charge (patch-B, AddOns/Blizzard_TrainerUI, charge a
-- la demande) :
--   - ClassTrainerFrame_Update (l. 79) : appelee par son nom (OnEvent TRAINER_UPDATE, defilement) ; pour chaque
--     ligne, ClassTrainerSkillN:SetText(nom) (« nom » pour une categorie, « "  "..nom » pour un sort) et
--     ClassTrainerSkillNSubText:SetFormattedText(PARENS_TEMPLATE, rang) ;
--   - ClassTrainer_SetSelection (l. 243) : appelee par son nom ; ClassTrainerSkillName (nom),
--     ClassTrainerSubSkillName (« (Rank 1) »), ClassTrainerSkillDescription (description du sort, nombres deja
--     calcules, passee par C_Format.Format de CoA).
-- Le client ne donne pas le numero du sort, seulement son nom : l'index NS (nom anglais -> numeros, add-on
-- Azeroth_FR_SortsIndex) donne les sorts candidats ; le nom francais n'est pose que si TOUS les sorts de ce nom
-- qui ont un francais donnent le meme, et la description que si l'alignement sur l'un d'eux reussit.
-- On n'ecrit que dans des zones de texte (FontString) de cadres non securises.
-- ============================================================================
local A = AzerothFR
local match, sub = string.match, string.sub
local P = A.Proteger

-- Numeros des sorts portant ce nom anglais (au plus 12).
function A.IdsSortsParNom(nomEN)
    if type(nomEN) ~= "string" or nomEN == "" then return nil end
    local t = A.TableDe("sorts_index", "NS")
    local v = t and t:ParTexte(nomEN)
    if type(v) == "table" and #v > 0 then return v end
    return nil
end

function A.NomSortParNom(nomEN)
    local ids = A.IdsSortsParNom(nomEN)
    if not ids then return nil end
    local fr
    for _, id in ipairs(ids) do
        local f = A.NomSort and A.NomSort(id, nomEN)
        if f then
            if fr and fr ~= f then return nil end
            fr = f
        end
    end
    return fr
end

function A.DescriptionSortParNom(nomEN, affiche)
    local ids = A.IdsSortsParNom(nomEN)
    if not ids or not A.DescriptionSort then return nil end
    for _, id in ipairs(ids) do
        local fr = A.DescriptionSort(id, affiche)
        if fr then return fr end
    end
    return nil
end

-- « (Rank 1) » -> « (Rang 1) » ; « Rank 1 » -> « Rang 1 ».
local function Rang(t)
    if type(t) ~= "string" or t == "" or not A.RangSort then return nil end
    local coeur = match(t, "^%((.*)%)$")
    if coeur then
        local fr = A.RangSort(nil, coeur)
        return fr and ("(" .. fr .. ")")
    end
    return A.RangSort(nil, t)
end

-- Categorie de la liste : ligne de competence (« Riding »), classe, ou nom divers.
local function Categorie(t)
    return A.Nom("competence", t) or A.Nom("classe", t) or A.Nom("divers", t) or A.NomZone and A.NomZone(t)
end

local function Ecrire(zone, fn)
    if not zone or type(zone.GetText) ~= "function" then return end
    local t = zone:GetText()
    if not t or t == "" or A.DejaEcrit(zone, t) then return end
    local fr = fn(t)
    if fr and fr ~= t then A.Ecrire(zone, fr) end
end

local function NomService(t)
    local blancs, nom = match(t, "^(%s*)(.-)$")
    if not nom or nom == "" then return nil end
    local fr = A.NomSortParNom(nom) or (blancs == "" and Categorie(nom))
    return fr and (blancs .. fr)
end

local function TraduireListe()
    if not A.Actif() then return end
    for i = 1, (CLASS_TRAINER_SKILLS_DISPLAYED or 11) do
        local bouton = _G["ClassTrainerSkill" .. i]
        if bouton and bouton:IsShown() then
            Ecrire(_G["ClassTrainerSkill" .. i .. "Text"] or (bouton.GetFontString and bouton:GetFontString()), NomService)
            local st = _G["ClassTrainerSkill" .. i .. "SubText"]
            if st and st:IsShown() then Ecrire(st, Rang) end
        end
    end
end
A.TraduireListeMaitre = TraduireListe

local function TraduireDetail()
    if not A.Actif() then return end
    local zNom = ClassTrainerSkillName
    local nomEN = A.TexteAnglais(zNom)
    Ecrire(zNom, function(t) return A.NomSortParNom(t) end)
    Ecrire(ClassTrainerSubSkillName, Rang)
    if nomEN and nomEN ~= "" then
        Ecrire(ClassTrainerSkillDescription, function(t) return A.DescriptionSortParNom(nomEN, t) end)
    end
end
A.TraduireDetailMaitre = TraduireDetail

local branche = false
local function Brancher()
    if branche or type(ClassTrainerFrame_Update) ~= "function" then return end
    branche = true
    hooksecurefunc("ClassTrainerFrame_Update", P("Maitres.liste", TraduireListe))
    if type(ClassTrainer_SetSelection) == "function" then
        hooksecurefunc("ClassTrainer_SetSelection", P("Maitres.detail", TraduireDetail))
    end
end
Brancher()
local guetteur = CreateFrame("Frame")
guetteur:RegisterEvent("ADDON_LOADED")
guetteur:SetScript("OnEvent", P("Maitres.ADDON_LOADED", function(self, _, nom)
    if nom == "Blizzard_TrainerUI" then
        Brancher()
        self:UnregisterEvent("ADDON_LOADED")
    end
end))
