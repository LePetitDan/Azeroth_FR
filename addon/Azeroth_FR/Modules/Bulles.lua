-- ============================================================================
-- Azeroth_FR : bulles de dialogue au-dessus des PNJ (version 0.4 : jamais en combat, bulles reconnues plus
-- strictement, interrupteur /azfr bulles on|off).
-- En 3.3.5, une bulle est un cadre SANS NOM, enfant de WorldFrame, dont une zone de texte porte la
-- replique. Sur CHAT_MSG_MONSTER_SAY / _YELL / _PARTY, on note l'anglais recu et son francais (memes
-- tables que la discussion : Modules/Cris.lua) ; pendant les images suivantes, on cherche la bulle dont
-- le texte est EXACTEMENT cet anglais et on y pose le francais.
-- Affichage seulement : on ne touche qu'au texte d'une zone de texte. Un cadre est pris pour une bulle
-- seulement s'il n'a pas de nom, n'est pas protege, n'a aucun cadre enfant et ne recoit pas la souris : les
-- plaques de nom (classiques ou celles d'Ascension, C_NamePlateManager) ont des enfants et ne sont donc
-- jamais regardees de pres.
-- 0.4 : l'action bloquee de l'essai 3 est arrivee en combat, juste apres une parole de PNJ. Rien dans ce
-- module n'appelle de fonction protegee (lecture des cadres, SetText d'une zone de texte), mais par prudence
-- il ne fait plus RIEN pendant un combat (InCombatLockdown) : la replique reste en francais dans la
-- discussion, la bulle reste en anglais. /azfr bulles off le coupe entierement.
-- Bornes : au plus 8 repliques en attente, 1,5 s de recherche par replique, une recherche toutes les
-- 0,05 s, au plus 300 enfants de WorldFrame regardes par recherche (les plus recents d'abord). Tout passe
-- sous pcall.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger

local MAX_ATTENTE, DUREE, PAS, MAX_ENFANTS = 8, 1.5, 0.05, 300
local attente = {}            -- { en = anglais, fr = francais, reste = secondes }
local cadre = CreateFrame("Frame")
cadre:Hide()
A.Compteurs.bulles = 0
A.Compteurs.bulles_combat = 0

local function Actif()
    return A.ModuleActif("bulles") and not A.EnCombat()
end

-- Un enfant de WorldFrame qui peut etre une bulle : sans nom, non protege, sans cadre enfant, sans souris.
local function PeutEtreBulle(enfant)
    if not enfant or type(enfant.GetRegions) ~= "function" then return false end
    if type(enfant.GetName) == "function" and enfant:GetName() ~= nil then return false end
    if type(enfant.GetNumChildren) == "function" and (enfant:GetNumChildren() or 0) > 0 then return false end
    if type(enfant.IsMouseEnabled) == "function" and enfant:IsMouseEnabled() then return false end
    if A.EstProtege(enfant) then return false end
    return true
end

-- Pose le francais dans la bulle dont le texte est l'anglais attendu. Renvoie true si trouvee.
local function Poser(enfant, en, fr)
    if not PeutEtreBulle(enfant) then return false end
    local regions = { enfant:GetRegions() }
    for i = 1, #regions do
        local r = regions[i]
        if r and type(r.GetObjectType) == "function" and r:GetObjectType() == "FontString" then
            local t = r:GetText()
            if t == en then
                A.Ecrire(r, fr)
                A.Compteurs.bulles = A.Compteurs.bulles + 1
                return true
            end
        end
    end
    return false
end

local function Chercher()
    if not WorldFrame or type(WorldFrame.GetChildren) ~= "function" then return end
    local enfants = { WorldFrame:GetChildren() }
    local bas = math.max(1, #enfants - MAX_ENFANTS + 1)
    for k = #attente, 1, -1 do
        local a = attente[k]
        local trouve = false
        for i = #enfants, bas, -1 do
            if Poser(enfants[i], a.en, a.fr) then trouve = true; break end
        end
        if trouve then table.remove(attente, k) end
    end
end
A.ChercherBulles = Chercher

local cumul = 0
cadre:SetScript("OnUpdate", P("Bulles.OnUpdate", function(self, ecoule)
    ecoule = ecoule or 0
    cumul = cumul + ecoule
    -- un combat commence, ou le module est coupe : on abandonne tout
    if not Actif() then
        for k = #attente, 1, -1 do attente[k] = nil end
        self:Hide(); cumul = 0
        return
    end
    for k = #attente, 1, -1 do
        attente[k].reste = attente[k].reste - ecoule
        if attente[k].reste <= 0 then table.remove(attente, k) end
    end
    if #attente == 0 then self:Hide(); cumul = 0; return end
    if cumul < PAS then return end
    cumul = 0
    A.Trace("Bulles.recherche")
    Chercher()
end, true))

-- Arguments : texte, emetteur, langue, canal, cible ($n) (3.3.5)
cadre:RegisterEvent("CHAT_MSG_MONSTER_SAY")
cadre:RegisterEvent("CHAT_MSG_MONSTER_YELL")
cadre:RegisterEvent("CHAT_MSG_MONSTER_PARTY")
cadre:SetScript("OnEvent", P("Bulles.OnEvent", function(self, evenement, message, emetteur, langue, canal, cible)
    if not A.ModuleActif("bulles") or type(message) ~= "string" or message == "" or not A.TraduireCri then return end
    if A.EnCombat() then
        A.Compteurs.bulles_combat = A.Compteurs.bulles_combat + 1      -- (laissee en anglais : combat)
        return
    end
    local fr = A.TraduireCri(message, emetteur, cible)
    if not fr or fr == message then return end
    if #attente >= MAX_ATTENTE then table.remove(attente, 1) end
    attente[#attente + 1] = { en = message, fr = fr, reste = DUREE }
    Chercher()                      -- la bulle peut deja exister
    if #attente > 0 then self:Show() end
end))
