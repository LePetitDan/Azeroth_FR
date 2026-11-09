-- ============================================================================
-- Azeroth_FR : « une nouvelle version est disponible » (1.1.0, demande de Dan).
-- Un add-on n'a pas acces a internet. Il peut en revanche echanger un message invisible avec les autres joueurs
-- qui ont Azeroth_FR (canal des add-ons : guilde, groupe, raid). Chacun y annonce sa version ; celui qui decouvre
-- une version plus recente que la sienne l'ecrit une fois dans la discussion et le montre dans le panneau d'options.
-- Le message ne contient QUE le numero de version (« V:1.1.0 »). Rien n'est telecharge par le jeu : pour mettre a
-- jour, le joueur relance l'installateur.
-- Aucune variable du jeu n'est ecrite ; la version vue est gardee dans nos reglages (AzerothFR_Reglages.version_vue).
-- ============================================================================
local A = AzerothFR
local P = A.Proteger
local PREFIXE = "AZFR"

local function Nombres(v)
    if type(v) ~= "string" then return nil end
    local a, b, c = string.match(v, "^(%d+)%.(%d+)%.(%d+)$")
    if not a or #v > 12 then return nil end
    return tonumber(a), tonumber(b), tonumber(c)
end

-- a est-elle plus recente que b ?
local function PlusRecente(a, b)
    local a1, a2, a3 = Nombres(a)
    local b1, b2, b3 = Nombres(b)
    if not a1 or not b1 then return false end
    if a1 ~= b1 then return a1 > b1 end
    if a2 ~= b2 then return a2 > b2 end
    return a3 > b3
end
A.VersionPlusRecente = PlusRecente

-- La version plus recente connue (vue chez un autre joueur), ou nil.
function A.NouvelleVersion()
    local r = AzerothFR_Reglages
    local vue = type(r) == "table" and r.version_vue or nil
    if vue and PlusRecente(vue, A.VERSION) then return vue end
    return nil
end

local annonce = false
local function Annoncer()
    local v = A.NouvelleVersion()
    if not v or annonce then return end
    annonce = true
    A.Message("la version " .. v .. " est disponible (vous avez la " .. tostring(A.VERSION) .. "). Fermez le jeu et relancez l'installateur d'Azeroth_FR pour mettre à jour.")
    if A.RafraichirOptions then A.RafraichirOptions() end
end

local dernier = {}      -- canal -> heure du dernier envoi
local function Envoyer(canal)
    if type(SendAddonMessage) ~= "function" or not Nombres(A.VERSION) then return end
    local maintenant = (type(GetTime) == "function" and GetTime()) or 0
    if dernier[canal] and maintenant - dernier[canal] < 60 then return end
    dernier[canal] = maintenant
    SendAddonMessage(PREFIXE, "V:" .. A.VERSION, canal)
end

local function CanalDeGroupe()
    if type(GetNumRaidMembers) == "function" and GetNumRaidMembers() > 0 then return "RAID" end
    if type(GetNumPartyMembers) == "function" and GetNumPartyMembers() > 0 then return "PARTY" end
    return nil
end

local function Saluer()
    if type(IsInGuild) == "function" and IsInGuild() then Envoyer("GUILD") end
    local g = CanalDeGroupe()
    if g then Envoyer(g) end
end

local cadre = CreateFrame("Frame")
for _, e in ipairs({ "CHAT_MSG_ADDON", "PARTY_MEMBERS_CHANGED", "RAID_ROSTER_UPDATE" }) do cadre:RegisterEvent(e) end
cadre:SetScript("OnEvent", P("Version.OnEvent", function(_, evenement, prefixe, message, canal)
    if evenement ~= "CHAT_MSG_ADDON" then
        local g = CanalDeGroupe()
        if g then Envoyer(g) end
        return
    end
    if prefixe ~= PREFIXE or type(message) ~= "string" then return end
    local v = string.match(message, "^V:(%d+%.%d+%.%d+)$")
    if not v or not Nombres(v) then return end
    if PlusRecente(v, A.VERSION) then
        if type(AzerothFR_Reglages) ~= "table" then return end
        local vue = AzerothFR_Reglages.version_vue
        if not vue or PlusRecente(v, vue) then AzerothFR_Reglages.version_vue = v end
        Annoncer()
    elseif PlusRecente(A.VERSION, v) and (canal == "GUILD" or canal == "PARTY" or canal == "RAID") then
        -- l'autre joueur est en retard : on lui repond notre version (au plus une fois par minute et par canal)
        Envoyer(canal)
    end
end))

-- a l'entree en jeu : rappeler une version deja vue lors d'une session precedente, et s'annoncer
table.insert(A.AEntreeEnJeu, function()
    local r = AzerothFR_Reglages
    -- on a mis a jour depuis : l'ancienne information ne sert plus
    if type(r) == "table" and r.version_vue and not PlusRecente(r.version_vue, A.VERSION) then r.version_vue = nil end
    Annoncer()
    Saluer()
end)
