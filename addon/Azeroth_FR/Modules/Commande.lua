-- ============================================================================
-- Azeroth_FR : la commande /azfr.
--   /azfr on          active l'affichage en francais
--   /azfr off         le coupe (le jeu reste en anglais ; les fenetres deja ouvertes gardent leur
--                     texte jusqu'a leur prochain affichage)
--   /azfr version     version de l'add-on et du paquet d'interface (PTRXML)
--   /azfr stats       familles chargees, memoire, nombre de traductions, erreurs evitees
--   /azfr etiquettes  trois infobulles d'objets reels du serveur portant des etiquettes (Mythic N,
--                     Heroic Raid, Bloodforged) : lignes brutes du jeu dans la discussion, puis traduction
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
    local c = A.Compteurs
    A.Message(format("affichage %s ; %d textes posés en français, %d recherches ; %d messages de discussion, %d infobulles de sorts, %d lignes du suivi rehaussées, %d bulles, %d messages du centre (%s) ; erreurs évitées : %d.",
        A.Actif() and "ACTIF" or "COUPÉ", c.traduits, c.recherches, c.discussion or 0, c.sorts or 0,
        c.suivi_hauteur or 0, c.bulles or 0, c.centre or 0,
        A.CentrePris and (A.CentrePris() and "pris en charge" or (A.CentreEnPanne and "rendus au jeu après une erreur" or "laissés au jeu")) or "?",
        A.Erreurs))
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
            local reste = 0
            for _ in pairs(t.morceaux) do reste = reste + 1 end
            A.Message(format("  table %s.%s : %d seaux compilés sur %d", famille, nom, t.compiles, t.compiles + reste))
        end
    end
    A.Message(format("mémoire : add-ons Azeroth_FR %s ; toute l'interface %s.", Ko(total), Ko(collectgarbage("count"))))
end

-- ----------------------------------------------------------------------------
-- /azfr etiquettes : trois infobulles d'essai (nos propres cadres, nommes AzerothFR_Etiquette1…3).
-- Si un objet n'est pas encore dans le cache du client, le jeu le demande au serveur et
-- l'infobulle reste vide ou incomplete : l'add-on refait l'essai une fois, 2 secondes plus tard ;
-- sinon, retaper la commande (deuxieme essai).
-- ----------------------------------------------------------------------------
local bulles = {}
local minuteur = CreateFrame("Frame")
minuteur:Hide()

local function Brut(t) return (string.gsub(t, "|", "||")) end

-- Quand le jeu remplit une infobulle d'essai (tout de suite si l'objet est dans le cache, sinon a
-- l'arrivee des donnees du serveur), OnTooltipSetItem est declenche : le jeu y a deja fait son
-- propre traitement (GameTooltip_OnSetItem de CoA, accroche par GameTooltipTemplate). On affiche
-- alors, UNE fois par commande, les lignes brutes telles que le jeu les montre, puis on traduit.
local function SurBulleEssai(b)
    if b.azfr_afficher then
        b.azfr_afficher = false
        local nom, lien = b:GetItem()
        local n = b:NumLines()
        A.Message(format("étiquette « %s », objet %s : %d lignes affichées par le jeu (avant traduction) :",
            tostring(b.azfr_quoi), tostring(A.IdDepuisLien(lien, "item") or b.azfr_id), n))
        for k = 1, n do
            local l = _G[b:GetName() .. "TextLeft" .. k]
            local r = _G[b:GetName() .. "TextRight" .. k]
            local t = l and l:GetText()
            local d = r and r:IsShown() and r:GetText()
            if (t and t ~= "") or (d and d ~= "") then
                A.Message(format("   %d : %s%s", k, Brut(t or ""), (d and d ~= "") and ("   [à droite : " .. Brut(d) .. "]") or ""))
            end
        end
    end
    if A.SurObjet then A.SurObjet(b) end
end

local function Bulle(i)
    local b = bulles[i]
    if not b then
        b = CreateFrame("GameTooltip", "AzerothFR_Etiquette" .. i, UIParent, "GameTooltipTemplate")
        b:HookScript("OnTooltipSetItem", A.Proteger("infobulle d'essai", SurBulleEssai))
        bulles[i] = b
    end
    return b
end

local function AfficherEtiquettes(relance)
    local manquants = 0
    for i, o in ipairs(A.OBJETS_ETIQUETTES or {}) do
        local id, quoi = o[1], o[2]
        local b = Bulle(i)
        local enCache = type(GetItemInfo) == "function" and GetItemInfo(id) ~= nil
        if not relance or enCache then
            b.azfr_afficher, b.azfr_quoi, b.azfr_id = true, quoi, id
        end
        b:SetOwner(UIParent, "ANCHOR_NONE")
        b:ClearAllPoints()
        b:SetPoint("TOP", UIParent, "TOP", -280 + (i - 1) * 280, -120)
        b:SetHyperlink(format("item:%d:0:0:0:0:0:0:0", id))
        local n = b:NumLines()
        if not enCache or n == 0 then
            manquants = manquants + 1
            if not relance then
                A.Message(format("étiquette « %s », objet %d : PAS encore dans le cache du jeu.", quoi, id))
            end
        end
        b:Show()
    end
    minuteur.attente, minuteur.relance = 0, (manquants > 0 and not relance)
    minuteur:Show()
    if manquants > 0 and not relance then
        A.Message(format("%d objet(s) pas encore connus du client : nouvel essai dans 2 secondes (sinon retapez /azfr etiquettes).", manquants))
    end
end

minuteur:SetScript("OnUpdate", A.Proteger("etiquettes.minuteur", function(self, ecoule)
    self.attente = (self.attente or 0) + (ecoule or 0)
    if self.relance and self.attente >= 2 then
        self.relance = false
        AfficherEtiquettes(true)
        return
    end
    if self.attente >= 60 then
        for _, b in pairs(bulles) do b:Hide() end
        self:Hide()
    end
end))
A.AfficherEtiquettes = AfficherEtiquettes

local function Activation(actif)
    for _, fn in ipairs(A.QuandActivation or {}) do
        local ok, err = pcall(fn, actif)
        if not ok then A.NoterErreur("/azfr " .. (actif and "on" or "off"), err) end
    end
end

local function Commande(msg)
    local ok, err = pcall(function()
        msg = string.lower(string.match(msg or "", "^%s*(.-)%s*$") or "")
        if msg == "on" then
            if type(AzerothFR_Reglages) ~= "table" then AzerothFR_Reglages = {} end
            AzerothFR_Reglages.inactif = nil
            Activation(true)
            A.Message("affichage en français ACTIVÉ.")
        elseif msg == "off" then
            if type(AzerothFR_Reglages) ~= "table" then AzerothFR_Reglages = {} end
            AzerothFR_Reglages.inactif = true
            Activation(false)
            A.Message("affichage en français COUPÉ (les fenêtres ouvertes changeront à leur prochain affichage ; messages du centre de l'écran rendus au jeu).")
        elseif msg == "version" then
            Version()
        elseif msg == "stats" then
            Stats()
        elseif msg == "etiquettes" or msg == "étiquettes" then
            AfficherEtiquettes(false)
        else
            A.Message("commandes : /azfr on, /azfr off, /azfr version, /azfr stats, /azfr etiquettes")
        end
    end)
    if not ok then A.NoterErreur("/azfr", err) end
end

SLASH_AZFR1 = "/azfr"
SlashCmdList["AZFR"] = Commande
A.Commande = Commande
