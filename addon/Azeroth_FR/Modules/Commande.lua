-- ============================================================================
-- Azeroth_FR : la commande /azfr.
--   /azfr on       active l'affichage en francais
--   /azfr off      le coupe (le jeu reste en anglais ; les fenetres deja ouvertes gardent leur
--                  texte jusqu'a leur prochain affichage)
--   /azfr version  version de l'add-on et du paquet d'interface (PTRXML)
--   /azfr stats    familles chargees, memoire, nombre de traductions, erreurs evitees
-- ============================================================================
local A = AzerothFR
local format = string.format

local function Ko(x) return format("%.0f Ko", x or 0) end

local function Version()
    A.Message(format("version %s (fabriquée le %s).", tostring(A.VERSION), tostring(A.DATE_FABRICATION)))
    local i = AzerothFR_Interface
    if type(i) == "table" then
        if i.erreur then
            A.Message("interface (PTRXML) " .. tostring(i.version) .. " : erreur évitée, " .. tostring(i.erreur))
        else
            A.Message(format("interface (PTRXML) %s : %d textes en français, %d laissés en anglais (absents ou différents dans ce client).",
                tostring(i.version), i.remplaces or 0, i.ignores or 0))
        end
    else
        A.Message("interface (PTRXML) : non chargée (dossier Interface\\PTRXML absent ?).")
    end
end

local function Stats()
    A.Message(format("affichage %s ; %d textes posés en français, %d recherches ; erreurs évitées : %d.",
        A.Actif() and "ACTIF" or "COUPÉ", A.Compteurs.traduits, A.Compteurs.recherches, A.Erreurs))
    if A.DerniereErreur then A.Message("dernière erreur évitée : " .. A.DerniereErreur) end
    if type(UpdateAddOnMemoryUsage) == "function" then pcall(UpdateAddOnMemoryUsage) end
    local total = 0
    local noms = { "Azeroth_FR" }
    for _, f in ipairs(A.FAMILLES or {}) do noms[#noms + 1] = f.addon end
    for _, addon in ipairs(noms) do
        local etat = A.Charges[addon]
        if addon == "Azeroth_FR" or etat ~= nil then
            local mem = 0
            if type(GetAddOnMemoryUsage) == "function" then
                local ok, m = pcall(GetAddOnMemoryUsage, addon)
                if ok and m then mem = m end
            end
            total = total + mem
            local d = A.DureesChargement[addon]
            A.Message(format("  %s : %s%s%s", addon,
                (addon == "Azeroth_FR" or etat) and "chargé" or ("NON chargé (" .. tostring(A.RaisonsEchec[addon]) .. ")"),
                mem > 0 and (", " .. Ko(mem)) or "",
                d and format(", %.0f ms", d) or ""))
        end
    end
    for famille, tables in pairs(A.Tables) do
        for nom, t in pairs(tables) do
            A.Message(format("  table %s.%s : %d seaux compilés sur %d", famille, nom, t.compiles, t.compiles + (function()
                local n = 0
                for _ in pairs(t.morceaux) do n = n + 1 end
                return n
            end)()))
        end
    end
    A.Message(format("mémoire : add-ons Azeroth_FR %s ; toute l'interface %s.", Ko(total), Ko(collectgarbage("count"))))
end

local function Commande(msg)
    local ok, err = pcall(function()
        msg = string.lower(string.match(msg or "", "^%s*(.-)%s*$") or "")
        if msg == "on" then
            if type(AzerothFR_Reglages) ~= "table" then AzerothFR_Reglages = {} end
            AzerothFR_Reglages.inactif = nil
            A.Message("affichage en français ACTIVÉ.")
        elseif msg == "off" then
            if type(AzerothFR_Reglages) ~= "table" then AzerothFR_Reglages = {} end
            AzerothFR_Reglages.inactif = true
            A.Message("affichage en français COUPÉ (les fenêtres ouvertes changeront à leur prochain affichage).")
        elseif msg == "version" then
            Version()
        elseif msg == "stats" then
            Stats()
        else
            A.Message("commandes : /azfr on, /azfr off, /azfr version, /azfr stats")
        end
    end)
    if not ok then A.NoterErreur("/azfr", err) end
end

SLASH_AZFR1 = "/azfr"
SlashCmdList["AZFR"] = Commande
A.Commande = Commande
