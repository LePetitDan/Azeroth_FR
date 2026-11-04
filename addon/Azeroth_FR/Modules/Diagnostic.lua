-- ============================================================================
-- Azeroth_FR : diagnostic des actions bloquees (version 0.4).
--
-- Essai 3 : en combat, juste apres une parole de PNJ, le jeu a affiche « Echec d'une action d'interface
-- liee a un programme d'interface personnalisee » (INTERFACE_ACTION_BLOCKED) puis le lien d'erreur de CoA.
-- Le jeu previent par les evenements ADDON_ACTION_BLOCKED (add-on, fonction), ADDON_ACTION_FORBIDDEN,
-- MACRO_ACTION_BLOCKED et MACRO_ACTION_FORBIDDEN. Ce module les ECOUTE SEULEMENT (lecture) et note :
--   - l'evenement, l'add-on accuse, la fonction bloquee ;
--   - l'heure, en combat ou non ;
--   - le fil d'Ariane de l'add-on (Core.lua, A.Fil) : les derniers modules qui ont tourne, avec leur age ;
--   - les premieres lignes de la pile d'appels au moment de l'evenement (si le jeu le livre pendant l'appel
--     bloque, on y voit la fonction du jeu qui a ete arretee).
-- Le premier blocage de la session est annonce une fois dans la discussion ; /azfr stats les montre tous ;
-- les 5 derniers sont gardes dans nos reglages (AzerothFR_Reglages.blocages) pour la session suivante.
--
-- /azfr erreurs lit, SANS RIEN ECRIRE, les dernieres entrees du gestionnaire d'erreurs de CoA
-- (patch-B, Interface\SharedXML\ErrorHandler\ErrorHandler.lua : ERROR_HANDLER_DATABASE.errors.current, puis
-- .previous, la session d'avant) : premiere ligne du message, compte, heure, premieres lignes de la pile.
-- ============================================================================
local A = AzerothFR
local format, gsub, sub, match, find = string.format, string.gsub, string.sub, string.match, string.find

local EVENEMENTS = { "ADDON_ACTION_BLOCKED", "ADDON_ACTION_FORBIDDEN", "MACRO_ACTION_BLOCKED", "MACRO_ACTION_FORBIDDEN" }
local MAX_SESSION, MAX_GARDES, FIL_AGE = 10, 5, 5000        -- FIL_AGE : modules des 5 dernieres secondes
A.Blocages = {}
local annonce = false

local function Brut(t) return (gsub(tostring(t or ""), "|", "||")) end

-- Fil d'Ariane lisible : « Bulles.OnEvent (il y a 0,03 s, en combat) ».
local function FilRecent(maintenant)
    local out = {}
    for _, f in ipairs(A.Fil or {}) do
        local age = (maintenant - (f.t or 0)) / 1000
        if age <= FIL_AGE / 1000 and #out < 6 then
            out[#out + 1] = format("%s (il y a %s s%s%s)", f.nom, gsub(format("%.2f", age), "%.", ","),
                f.n > 1 and format(", %d fois", f.n) or "", f.combat and ", en combat" or "")
        end
    end
    return out
end

local function Pile()
    if type(debugstack) ~= "function" then return {} end
    local ok, p = pcall(debugstack, 2, 12, 0)
    if not ok or type(p) ~= "string" then return {} end
    local out = {}
    for ligne in string.gmatch(p, "[^\n]+") do
        if not find(ligne, "Diagnostic.lua", 1, true) and #out < 8 then out[#out + 1] = sub(ligne, 1, 160) end
    end
    return out
end

local function Decrire(b)
    return format("%s %s : add-on « %s », fonction « %s », %s ; avant : %s", b.heure or "?", b.evenement,
        Brut(b.addon), Brut(b.fonction), b.combat and "EN COMBAT" or "hors combat",
        (#(b.fil or {}) > 0) and table.concat(b.fil, " ; ") or "aucun module de l'add-on dans les 5 s")
end
A.DecrireBlocage = Decrire

local function Noter(evenement, addon, fonction)
    local maintenant = A.Chrono()
    local b = {
        evenement = evenement, addon = tostring(addon or "?"), fonction = tostring(fonction or "?"),
        heure = (type(date) == "function" and date("%H:%M:%S")) or "?", combat = A.EnCombat(),
        fil = FilRecent(maintenant), pile = Pile(),
    }
    table.insert(A.Blocages, b)
    if #A.Blocages > MAX_SESSION then table.remove(A.Blocages, 1) end
    -- gardes pour la session suivante (nos propres reglages)
    if type(AzerothFR_Reglages) == "table" then
        local g = type(AzerothFR_Reglages.blocages) == "table" and AzerothFR_Reglages.blocages or {}
        AzerothFR_Reglages.blocages = g
        table.insert(g, { evenement = b.evenement, addon = b.addon, fonction = b.fonction, heure = b.heure,
            combat = b.combat, fil = b.fil, pile = b.pile })
        while #g > MAX_GARDES do table.remove(g, 1) end
    end
    if not annonce then
        annonce = true
        A.Message("|cffff6060action bloquée|r " .. Decrire(b))
        A.Message("(détails : /azfr stats ; erreurs du jeu : /azfr erreurs ; pour isoler un module : /azfr bulles off, /azfr centre off, /azfr plaques off)")
    end
end
A.NoterBlocage = Noter

local cadre = CreateFrame("Frame")
for _, e in ipairs(EVENEMENTS) do cadre:RegisterEvent(e) end
cadre:SetScript("OnEvent", function(self, evenement, addon, fonction)
    local ok, err = pcall(Noter, evenement, addon, fonction)
    if not ok then A.NoterErreur("diagnostic", err) end
end)

-- Pour /azfr stats (Modules/Commande.lua).
function A.StatsBlocages()
    local n = #A.Blocages
    if n == 0 then
        A.Message("actions bloquées pendant cette session : aucune.")
    else
        A.Message(format("actions bloquées pendant cette session : %d.", n))
        for i, b in ipairs(A.Blocages) do
            A.Message(format("  %d. %s", i, Decrire(b)))
            for _, l in ipairs(b.pile or {}) do A.Message("       pile : " .. Brut(l)) end
        end
    end
    local g = type(AzerothFR_Reglages) == "table" and AzerothFR_Reglages.blocages
    if n == 0 and type(g) == "table" and #g > 0 then
        A.Message(format("actions bloquées gardées des sessions précédentes : %d (la plus récente : %s).", #g,
            Decrire(g[#g])))
    end
end

-- ----------------------------------------------------------------------------
-- /azfr erreurs : lecture seule du gestionnaire d'erreurs de CoA.
-- ----------------------------------------------------------------------------
local function PremiereLigne(t)
    t = tostring(t or "")
    return match(t, "^([^\n]*)") or t
end

local function Lister(liste, titre, max)
    if type(liste) ~= "table" or #liste == 0 then return 0 end
    A.Message(format("%s : %d erreur(s) ; les %d dernières :", titre, #liste, math.min(max, #liste)))
    local debut = math.max(1, #liste - max + 1)
    for i = #liste, debut, -1 do
        local e = liste[i]
        if type(e) == "table" then
            A.Message(format("  %d. [%s] x%s %s", i, Brut(e.time or "?"), tostring(e.counter or "?"),
                Brut(sub(PremiereLigne(e.message), 1, 240))))
            local k = 0
            for ligne in string.gmatch(tostring(e.stack or ""), "[^\n]+") do
                k = k + 1
                if k > 3 then break end
                A.Message("       " .. Brut(sub(ligne, 1, 160)))
            end
        end
    end
    return #liste
end

function A.ListerErreursJeu(max)
    max = max or 5
    local db = ERROR_HANDLER_DATABASE
    local e = type(db) == "table" and type(db.errors) == "table" and db.errors or nil
    if not e then
        A.Message("gestionnaire d'erreurs de CoA introuvable (ERROR_HANDLER_DATABASE absent).")
        return
    end
    local n = Lister(e.current, "erreurs de cette session (gestionnaire de CoA)", max)
    if n == 0 then
        A.Message("erreurs de cette session (gestionnaire de CoA) : aucune.")
        local p = Lister(e.previous, "erreurs de la session précédente", max)
        if p == 0 then A.Message("erreurs de la session précédente : aucune.") end
    end
end
