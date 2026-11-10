-- ============================================================================
-- Azeroth_FR : signaler une erreur de traduction, par une fenetre (1.2.0, demande de Dan : « une interface pour
-- que le joueur voie ce qu'il fait, pas juste une commande », et « que ca marche aussi sur un menu »).
--
-- Entrees : le bouton Azeroth_FR de la minicarte, le bouton du panneau d'options, ou /azfr signaler.
-- La fenetre guide en trois etapes :
--   1. « Viser un texte » : la fenetre se retire, un bandeau compte 4 secondes pendant que le joueur pose sa
--      souris sur le texte en cause ; ce qui est sous la souris est releve : l'infobulle affichee (objet, sort),
--      ou l'element d'interface (bouton, ligne de menu, texte d'une fenetre) et le nom de sa fenetre ;
--   2. le joueur coche ce qui ne va pas ;
--   3. le compte rendu, pret a copier (Ctrl+C) et a coller sur le Discord.
-- Le jeu ne peut rien envoyer sur internet : c'est le joueur qui colle. Le compte rendu ne contient ni nom de
-- personnage ni nom de joueur. Cadres sans nom global ni modele XML ; aucune variable du jeu n'est ecrite ; on ne
-- fait que LIRE les cadres du jeu.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger
local UI = A.UI
local MAX_LIGNES, MAX_LONGUEUR, DELAI = 14, 220, 4
local PROBLEMES = {
    { "anglais", "Le texte est resté en anglais" },
    { "faux", "La traduction est fausse ou maladroite" },
    { "affichage", "Le texte est coupé ou mal placé" },
    { "autre", "Autre chose" },
}

-- Texte lisible hors du jeu : sans codes de couleur ni images.
local function Propre(t)
    if type(t) ~= "string" then return "" end
    t = string.gsub(t, "|c%x%x%x%x%x%x%x%x", "")
    t = string.gsub(t, "|r", "")
    t = string.gsub(t, "|T.-|t", "")
    t = string.gsub(t, "|H.-|h(.-)|h", "%1")
    t = string.gsub(t, "[\r\n]+", " / ")
    t = string.gsub(t, "`", "'")
    if #t > MAX_LONGUEUR then t = string.sub(t, 1, MAX_LONGUEUR) .. "…" end
    return t
end

local function Zone()
    local z = (type(GetRealZoneText) == "function" and GetRealZoneText()) or ""
    local s = (type(GetSubZoneText) == "function" and GetSubZoneText()) or ""
    if s ~= "" and s ~= z then return z .. " / " .. s end
    return z
end

-- ---------------------------------------------------------------------------
-- Releve de ce qui est sous la souris
-- ---------------------------------------------------------------------------
local function Appel(objet, methode, ...)
    if objet and type(objet[methode]) == "function" then
        local ok, a, b, c = pcall(objet[methode], objet, ...)
        if ok then return a, b, c end
    end
    return nil
end

-- Le texte (FontString) d'un cadre qui se trouve sous le curseur ; on descend dans ses enfants.
local function TexteSousCurseur(cadre, x, y, profondeur)
    if not cadre or profondeur < 0 or Appel(cadre, "IsVisible") == false then return nil end
    local e = Appel(cadre, "GetEffectiveScale") or 1
    if e <= 0 then e = 1 end
    local cx, cy = x / e, y / e
    if type(cadre.GetRegions) == "function" then
        for _, r in ipairs({ cadre:GetRegions() }) do
            if Appel(r, "GetObjectType") == "FontString" and Appel(r, "IsVisible") ~= false then
                local t = Appel(r, "GetText")
                local g, d, h, b = Appel(r, "GetLeft"), Appel(r, "GetRight"), Appel(r, "GetTop"), Appel(r, "GetBottom")
                if t and t ~= "" and g and d and h and b and cx >= g and cx <= d and cy >= b and cy <= h then
                    return t, r
                end
            end
        end
    end
    if type(cadre.GetChildren) == "function" then
        for _, enfant in ipairs({ cadre:GetChildren() }) do
            local t, r = TexteSousCurseur(enfant, x, y, profondeur - 1)
            if t then return t, r end
        end
    end
    return nil
end

-- Le nom de la fenetre qui contient le cadre (le dernier parent nomme avant l'ecran).
local function Fenetre(cadre)
    local nom
    local c, garde = cadre, 0
    while c and garde < 30 do
        local n = Appel(c, "GetName")
        if n and n ~= "UIParent" and n ~= "WorldFrame" then nom = n end
        c = Appel(c, "GetParent")
        if c == UIParent then break end
        garde = garde + 1
    end
    return nom
end

-- Ce que le joueur montre : { objet, sort, lignes = { {texte, anglais} }, element, fenetre, resume }
local function Relever(ignorer)
    local r = { lignes = {}, zone = Zone() }
    local b = GameTooltip
    if b and Appel(b, "IsShown") then
        local _, lien = Appel(b, "GetItem")
        r.objet = lien and A.IdDepuisLien and A.IdDepuisLien(lien, "item") or nil
        local _, _, idSort = Appel(b, "GetSpell")
        r.sort = idSort
        local n = Appel(b, "NumLines") or 0
        for i = 1, math.min(n, MAX_LIGNES) do
            local g = _G["GameTooltipTextLeft" .. i]
            local t = g and g:GetText()
            if t and t ~= "" then
                local anglais = A.Originaux and A.Originaux[g] and A.DejaEcrit and A.DejaEcrit(g, t) and A.Originaux[g] or nil
                r.lignes[#r.lignes + 1] = { t, anglais }
            end
        end
        r.en_plus = n > MAX_LIGNES and (n - MAX_LIGNES) or nil
    end
    -- l'element d'interface sous la souris : bouton, ligne de menu, texte d'une fenetre
    local c = type(GetMouseFocus) == "function" and GetMouseFocus() or nil
    if c and c ~= WorldFrame and c ~= ignorer then
        r.element = Appel(c, "GetName")
        r.fenetre = Fenetre(c)
        if #r.lignes == 0 then
            local x, y = 0, 0
            if type(GetCursorPosition) == "function" then x, y = GetCursorPosition() end
            local t, region = TexteSousCurseur(c, x, y, 3)
            if not t then t = Appel(c, "GetText") end
            if t and t ~= "" then
                local anglais = region and A.Originaux and A.Originaux[region] and A.DejaEcrit and A.DejaEcrit(region, t)
                    and A.Originaux[region] or nil
                r.lignes[1] = { t, anglais }
                r.texte_interface = true
            end
        end
    end
    -- une ligne pour dire au joueur ce qui a ete releve
    local premier = r.lignes[1] and Propre(r.lignes[1][1]) or nil
    if r.objet then r.resume = "Objet n° " .. tostring(r.objet) .. (premier and (" : « " .. premier .. " »") or "")
    elseif r.sort then r.resume = "Sort n° " .. tostring(r.sort) .. (premier and (" : « " .. premier .. " »") or "")
    elseif premier and r.texte_interface then r.resume = "Texte d'interface : « " .. premier .. " »" .. (r.fenetre and (" (fenêtre " .. r.fenetre .. ")") or "")
    elseif premier then r.resume = "Infobulle : « " .. premier .. " »"
    elseif r.fenetre then r.resume = "Fenêtre " .. r.fenetre .. " (aucun texte trouvé sous la souris)"
    end
    return r
end

-- Le compte rendu, en texte simple.
local function Rediger(r, probleme)
    local l = {}
    l[#l + 1] = "[Azeroth_FR " .. tostring(A.VERSION) .. "] Signalement"
    for _, p in ipairs(PROBLEMES) do
        if p[1] == probleme then l[#l + 1] = "Problème : " .. p[2] end
    end
    if r.zone and r.zone ~= "" then l[#l + 1] = "Zone : " .. Propre(r.zone) end
    if r.objet then l[#l + 1] = "Objet : " .. tostring(r.objet) end
    if r.sort then l[#l + 1] = "Sort : " .. tostring(r.sort) end
    if r.fenetre then l[#l + 1] = "Fenêtre : " .. Propre(r.fenetre) end
    if r.element and r.element ~= r.fenetre then l[#l + 1] = "Élément : " .. Propre(r.element) end
    if #r.lignes > 0 then
        l[#l + 1] = "Texte affiché :"
        for _, x in ipairs(r.lignes) do
            l[#l + 1] = "  " .. Propre(x[1])
            if x[2] then l[#l + 1] = "    (anglais : " .. Propre(x[2]) .. ")" end
        end
        if r.en_plus then l[#l + 1] = "  (" .. r.en_plus .. " lignes de plus)" end
    else
        l[#l + 1] = "Texte affiché : (rien de relevé : décrivez l'endroit ci-dessous ou joignez une capture d'écran)"
    end
    l[#l + 1] = "Précision : "
    return table.concat(l, "\n")
end

-- pour les essais et /azfr signaler direct
function A.TexteSignalement(probleme) return Rediger(Relever(), probleme) end

-- ---------------------------------------------------------------------------
-- La fenetre
-- ---------------------------------------------------------------------------
local fenetre, bandeau
local releve, probleme = nil, nil

local function Decor(f)
    f:SetBackdrop({
        bgFile = "Interface\\ChatFrame\\ChatFrameBackground",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border", edgeSize = 16,
        insets = { left = 4, right = 4, top = 4, bottom = 4 },
    })
    f:SetBackdropColor(0.02, 0.06, 0.18, 0.96)
    f:SetBackdropBorderColor(0.91, 0.71, 0.37, 1)
end

local function Actualiser()
    local f = fenetre
    if not f then return end
    f.vise:SetText(releve and releve.resume or "Rien n'est encore visé.")
    for _, p in ipairs(PROBLEMES) do f.cases[p[1]]:SetChecked(probleme == p[1]) end
    if releve then
        f.texte = "```\n" .. Rediger(releve, probleme) .. "\n```"
    else
        f.texte = ""
    end
    f.zone:SetText(f.texte)
    if releve then
        f.zone:SetFocus()
        f.zone:HighlightText()
    end
end

local function CreerFenetre()
    if fenetre then return fenetre end
    local f = CreateFrame("Frame", nil, UIParent)
    f:SetWidth(540)
    f:SetHeight(470)
    f:SetPoint("CENTER", UIParent, "CENTER", 0, 30)
    f:SetFrameStrata("DIALOG")
    Decor(f)
    f:EnableMouse(true)

    local logo = f:CreateTexture(nil, "ARTWORK")
    logo:SetWidth(36)
    logo:SetHeight(36)
    logo:SetPoint("TOPLEFT", f, "TOPLEFT", 14, -12)
    logo:SetTexture("Interface\\AddOns\\Azeroth_FR\\Logo")
    local titre = UI.Texte(f, "GameFontNormalLarge", "Signaler une erreur de traduction")
    titre:SetPoint("LEFT", logo, "RIGHT", 10, 0)

    -- etape 1
    local e1 = UI.Texte(f, "GameFontNormal", "1. Montrez le texte en cause")
    e1:SetPoint("TOPLEFT", logo, "BOTTOMLEFT", 2, -12)
    local a1 = UI.Texte(f, "GameFontHighlightSmall", "Cliquez sur « Viser un texte », puis posez la souris sur le texte : un objet, un sort, un bouton, une ligne de menu, un texte de fenêtre. Il est relevé au bout de " .. DELAI .. " secondes.")
    a1:SetPoint("TOPLEFT", e1, "BOTTOMLEFT", 0, -4)
    a1:SetWidth(508)
    f.viser = UI.Bouton(f, "Viser un texte", 150)
    f.viser:SetPoint("TOPLEFT", a1, "BOTTOMLEFT", 0, -8)
    f.viser:SetScript("OnClick", function() A.ViserSignalement() end)
    f.vise = UI.Texte(f, "GameFontGreen", "")
    f.vise:SetPoint("LEFT", f.viser, "RIGHT", 10, 0)
    f.vise:SetWidth(340)

    -- etape 2
    local e2 = UI.Texte(f, "GameFontNormal", "2. Qu'est-ce qui ne va pas ?")
    e2:SetPoint("TOPLEFT", f.viser, "BOTTOMLEFT", 0, -14)
    f.cases = {}
    local precedent = e2
    for i, p in ipairs(PROBLEMES) do
        local c = UI.Case(f, p[2])
        c:SetPoint("TOPLEFT", precedent, "BOTTOMLEFT", 0, i == 1 and -4 or 2)
        c:SetScript("OnClick", function()
            probleme = p[1]
            Actualiser()
        end)
        f.cases[p[1]] = c
        precedent = c
    end

    -- etape 3
    local e3 = UI.Texte(f, "GameFontNormal", "3. Copiez (Ctrl+C) et collez sur le Discord Azeroth_FR")
    e3:SetPoint("TOPLEFT", precedent, "BOTTOMLEFT", 0, -10)
    local a3 = UI.Texte(f, "GameFontHighlightSmall", "Salon des signalements : " .. tostring(A.LIEN_DISCORD) .. ". Vous pourrez y ajouter une précision ou une capture d'écran.")
    a3:SetPoint("TOPLEFT", e3, "BOTTOMLEFT", 0, -4)
    a3:SetWidth(508)

    local cadre = CreateFrame("Frame", nil, f)
    cadre:SetPoint("TOPLEFT", a3, "BOTTOMLEFT", 0, -6)
    cadre:SetWidth(508)
    cadre:SetHeight(118)
    cadre:SetBackdrop({
        bgFile = "Interface\\ChatFrame\\ChatFrameBackground",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border", edgeSize = 10,
        insets = { left = 2, right = 2, top = 2, bottom = 2 },
    })
    cadre:SetBackdropColor(0, 0, 0, 0.5)
    cadre:SetBackdropBorderColor(0.6, 0.6, 0.6, 0.8)
    local zone = CreateFrame("EditBox", nil, cadre)
    zone:SetMultiLine(true)
    zone:SetAutoFocus(false)
    zone:SetFontObject(GameFontHighlightSmall)
    zone:SetWidth(494)
    zone:SetHeight(108)
    zone:SetPoint("TOPLEFT", cadre, "TOPLEFT", 7, -6)
    zone:SetScript("OnEscapePressed", function() f:Hide() end)
    -- le texte ne se modifie pas ici : il revient toujours au compte rendu
    zone:SetScript("OnTextChanged", function(self)
        if f.texte and self:GetText() ~= f.texte then
            self:SetText(f.texte)
            self:HighlightText()
        end
    end)
    zone:SetScript("OnEditFocusGained", function(self) self:HighlightText() end)
    f.zone = zone

    f.fermer = UI.Bouton(f, "Fermer", 100)
    f.fermer:SetPoint("BOTTOMRIGHT", f, "BOTTOMRIGHT", -14, 12)
    f.fermer:SetScript("OnClick", function() f:Hide() end)

    f:Hide()
    fenetre = f
    return f
end

-- Le bandeau de visee : un compte a rebours en haut de l'ecran, et ce qui est sous la souris.
local function CreerBandeau()
    if bandeau then return bandeau end
    local b = CreateFrame("Frame", nil, UIParent)
    b:SetWidth(560)
    b:SetHeight(64)
    b:SetPoint("TOP", UIParent, "TOP", 0, -90)
    b:SetFrameStrata("TOOLTIP")
    Decor(b)
    b.titre = UI.Texte(b, "GameFontNormalLarge", "")
    b.titre:SetPoint("TOP", b, "TOP", 0, -10)
    b.apercu = UI.Texte(b, "GameFontHighlightSmall", "")
    b.apercu:SetPoint("TOP", b.titre, "BOTTOM", 0, -6)
    b.apercu:SetWidth(530)
    b.apercu:SetJustifyH("CENTER")
    b.reste = 0
    b:SetScript("OnUpdate", P("Signaler.visee", function(self, ecoule)
        A.TicVisee(ecoule)
    end, true))
    b:Hide()
    bandeau = b
    return b
end

-- Un pas du compte a rebours (appele par le bandeau ; expose pour les essais).
function A.TicVisee(ecoule)
    local b = bandeau
    if not b or not b.actif then return end
    b.reste = b.reste - (ecoule or 0)
    local vu = Relever(b)
    b.titre:SetText("Posez la souris sur le texte à signaler… " .. math.max(0, math.ceil(b.reste)))
    b.apercu:SetText(vu.resume or "(rien sous la souris pour l'instant)")
    if b.reste <= 0 then
        b.actif = false
        b:Hide()
        releve = vu
        local f = CreerFenetre()
        f:Show()
        Actualiser()
    end
end

-- Etape 1 : la fenetre se retire, le compte a rebours commence.
function A.ViserSignalement()
    local f = CreerFenetre()
    local b = CreerBandeau()
    f:Hide()
    b.reste = DELAI
    b.actif = true
    b.titre:SetText("Posez la souris sur le texte à signaler… " .. DELAI)
    b.apercu:SetText("")
    b:Show()
end
A.ViserSignalement = P("Signaler.viser", A.ViserSignalement)

-- Ouvre la fenetre. Si le joueur survole deja quelque chose (commande tapee la souris sur un objet), c'est releve.
function A.OuvrirSignalement()
    local f = CreerFenetre()
    local vu = Relever(f)
    if vu.resume and (#vu.lignes > 0) then releve = vu end
    f:Show()
    Actualiser()
end
A.OuvrirSignalement = P("Signaler.ouvrir", A.OuvrirSignalement)
A.Signaler = A.OuvrirSignalement
function A.FenetreSignalement() return fenetre, bandeau end

-- ---------------------------------------------------------------------------
-- Le bouton de la minicarte : clic gauche = signaler, clic droit = options
-- ---------------------------------------------------------------------------
local bouton
local function CreerBouton()
    if bouton or not Minimap then return bouton end
    local b = CreateFrame("Button", nil, Minimap)
    b:SetWidth(31)
    b:SetHeight(31)
    b:SetFrameStrata("MEDIUM")
    b:SetFrameLevel(8)
    b:SetPoint("TOPLEFT", Minimap, "TOPLEFT", -14, -72)
    b:RegisterForClicks("LeftButtonUp", "RightButtonUp")
    local icone = b:CreateTexture(nil, "BACKGROUND")
    icone:SetWidth(20)
    icone:SetHeight(20)
    icone:SetPoint("CENTER", b, "CENTER", 0, 0)
    icone:SetTexture("Interface\\AddOns\\Azeroth_FR\\Logo")
    local bord = b:CreateTexture(nil, "OVERLAY")
    bord:SetWidth(53)
    bord:SetHeight(53)
    bord:SetPoint("TOPLEFT", b, "TOPLEFT", 0, 0)
    bord:SetTexture("Interface\\Minimap\\MiniMap-TrackingBorder")
    b:SetHighlightTexture("Interface\\Minimap\\UI-Minimap-ZoomButton-Highlight")
    b:SetScript("OnClick", P("Signaler.bouton", function(_, clic)
        if clic == "RightButton" then
            if A.OuvrirOptions then A.OuvrirOptions() end
        else
            A.OuvrirSignalement()
        end
    end))
    b:SetScript("OnEnter", P("Signaler.bouton.entree", function(self)
        if not GameTooltip then return end
        GameTooltip:SetOwner(self, "ANCHOR_LEFT")
        GameTooltip:AddLine("Azeroth_FR " .. tostring(A.VERSION))
        GameTooltip:AddLine("Clic gauche : signaler une erreur de traduction", 1, 1, 1)
        GameTooltip:AddLine("Clic droit : options", 1, 1, 1)
        local n = A.NouvelleVersion and A.NouvelleVersion()
        if n then GameTooltip:AddLine("Nouvelle version " .. n .. " disponible : relancez l'installateur", 0.2, 1, 0.2) end
        GameTooltip:Show()
    end, true))
    b:SetScript("OnLeave", function() if GameTooltip then GameTooltip:Hide() end end)
    bouton = b
    return b
end

function A.MontrerBoutonMinicarte(visible)
    if type(AzerothFR_Reglages) == "table" then AzerothFR_Reglages.sans_bouton = (not visible) or nil end
    local b = CreerBouton()
    if not b then return end
    if visible then b:Show() else b:Hide() end
end
function A.BoutonMinicarte() return bouton end

table.insert(A.AEntreeEnJeu, function()
    local r = AzerothFR_Reglages
    local b = CreerBouton()
    if b then
        if type(r) == "table" and r.sans_bouton then b:Hide() else b:Show() end
    end
end)
