-- ============================================================================
-- Azeroth_FR : panneau d'options (0.9.6, demande de Dan : « une petite interface pour desactiver les choses »).
-- Menu du jeu > Interface > onglet AddOns > Azeroth_FR, ou /azfr tout seul.
-- Les memes reglages que les commandes (/azfr on|off, /azfr bulles|centre|plaques on|off) : chaque case appelle
-- A.Commande, rien d'autre. Cadres SANS NOM et sans modele XML (les modeles creent des enfants nommes « $parent… ») :
-- aucune variable globale creee ; enregistrement par la fonction officielle InterfaceOptions_AddCategory.
-- ============================================================================
local A = AzerothFR

local MODULES = {
    { "bulles", "Bulles des PNJ" },
    { "centre", "Messages au centre de l'écran" },
    { "plaques", "Plaques de nom" },
}

local panneau

local function Texte(parent, modele, texte)
    local fs = parent:CreateFontString(nil, "ARTWORK", modele)
    fs:SetJustifyH("LEFT")
    fs:SetText(texte)
    return fs
end

-- case a cocher sans modele XML : les textures du jeu, comme InterfaceOptionsCheckButtonTemplate
local function Case(parent, libelle)
    local c = CreateFrame("CheckButton", nil, parent)
    c:SetWidth(26)
    c:SetHeight(26)
    c:SetNormalTexture("Interface\\Buttons\\UI-CheckBox-Up")
    c:SetPushedTexture("Interface\\Buttons\\UI-CheckBox-Down")
    c:SetHighlightTexture("Interface\\Buttons\\UI-CheckBox-Highlight", "ADD")
    c:SetCheckedTexture("Interface\\Buttons\\UI-CheckBox-Check")
    c:SetDisabledCheckedTexture("Interface\\Buttons\\UI-CheckBox-Check-Disabled")
    c.libelle = Texte(parent, "GameFontHighlight", libelle)
    c.libelle:SetPoint("LEFT", c, "RIGHT", 2, 1)
    return c
end

local function Coupe(module)
    local r = AzerothFR_Reglages
    return type(r) == "table" and type(r.coupes) == "table" and r.coupes[module] and true or false
end

local function Rafraichir()
    if not panneau then return end
    local actif = A.Actif()
    panneau.francais:SetChecked(actif)
    for _, m in ipairs(MODULES) do
        local c = panneau.cases[m[1]]
        c:SetChecked(not Coupe(m[1]))
        if actif then
            c:Enable()
            c.libelle:SetFontObject(GameFontHighlight)
        else
            c:Disable()
            c.libelle:SetFontObject(GameFontDisable)
        end
    end
end

local function Construire()
    if panneau or type(InterfaceOptions_AddCategory) ~= "function" then return end
    local p = CreateFrame("Frame")
    p:Hide()
    p.name = "Azeroth_FR"

    local logo = p:CreateTexture(nil, "ARTWORK")
    logo:SetTexture("Interface\\AddOns\\Azeroth_FR\\Logo")
    logo:SetWidth(72)
    logo:SetHeight(72)
    logo:SetPoint("TOPLEFT", p, "TOPLEFT", 16, -16)

    local titre = Texte(p, "GameFontNormalLarge", "Azeroth_FR")
    titre:SetPoint("TOPLEFT", logo, "TOPRIGHT", 14, -10)
    local version = GetAddOnMetadata and GetAddOnMetadata("Azeroth_FR", "Version") or ""
    local sous = Texte(p, "GameFontHighlightSmall", "Conquest of Azeroth en français · version " .. tostring(version))
    sous:SetPoint("TOPLEFT", titre, "BOTTOMLEFT", 0, -6)

    p.francais = Case(p, "Jeu en français")
    p.francais:SetPoint("TOPLEFT", logo, "BOTTOMLEFT", -2, -18)
    local aide = Texte(p, "GameFontDisableSmall", "Décochez pour revoir le jeu en anglais. Les fenêtres déjà ouvertes changent à leur prochain affichage.")
    aide:SetPoint("TOPLEFT", p.francais.libelle, "BOTTOMLEFT", 0, -4)
    aide:SetWidth(520)
    p.francais:SetScript("OnClick", function(self)
        A.Commande(self:GetChecked() and "on" or "off")
        Rafraichir()
    end)

    local groupe = Texte(p, "GameFontNormal", "Parties de la traduction")
    groupe:SetPoint("TOPLEFT", p.francais, "BOTTOMLEFT", 2, -34)
    local aide2 = Texte(p, "GameFontDisableSmall", "À couper seulement en cas de souci, par exemple une action bloquée en combat.")
    aide2:SetPoint("TOPLEFT", groupe, "BOTTOMLEFT", 0, -4)
    aide2:SetWidth(520)

    p.cases = {}
    local precedent = aide2
    for i, m in ipairs(MODULES) do
        local c = Case(p, m[2])
        c:SetPoint("TOPLEFT", precedent, "BOTTOMLEFT", i == 1 and 0 or 0, i == 1 and -8 or -2)
        c:SetScript("OnClick", function(self)
            A.Commande(m[1] .. (self:GetChecked() and " on" or " off"))
            Rafraichir()
        end)
        p.cases[m[1]] = c
        precedent = c
    end

    local signaler = Texte(p, "GameFontHighlightSmall", "Une erreur de traduction ? Survolez le texte, tapez /azfr bulle, puis envoyez une capture d'écran sur le Discord Azeroth_FR.")
    signaler:SetPoint("TOPLEFT", precedent, "BOTTOMLEFT", 2, -28)
    signaler:SetWidth(520)
    local commandes = Texte(p, "GameFontDisableSmall", "Commandes : /azfr on, /azfr off, /azfr version, /azfr stats, /azfr bulle, /azfr aide.")
    commandes:SetPoint("TOPLEFT", signaler, "BOTTOMLEFT", 0, -8)
    commandes:SetWidth(520)
    local mention = Texte(p, "GameFontDisableSmall", "Projet de joueurs, sans lien avec Blizzard Entertainment ni avec l'équipe de Conquest of Azeroth.")
    mention:SetPoint("BOTTOMLEFT", p, "BOTTOMLEFT", 16, 16)

    p.refresh = Rafraichir
    p.default = function()
        A.Commande("on")
        for _, m in ipairs(MODULES) do A.Commande(m[1] .. " on") end
        Rafraichir()
    end
    p.okay = function() end
    p.cancel = function() end
    p:SetScript("OnShow", Rafraichir)
    panneau = p
    InterfaceOptions_AddCategory(p)
end

-- /azfr tout seul : ouvre le panneau (deux appels : le premier ne deroule pas toujours la liste des add-ons)
function A.OuvrirOptions()
    if not panneau or type(InterfaceOptionsFrame_OpenToCategory) ~= "function" then return false end
    InterfaceOptionsFrame_OpenToCategory(panneau)
    InterfaceOptionsFrame_OpenToCategory(panneau)
    return true
end

A.Options = function() return panneau end
A.RafraichirOptions = Rafraichir
local ok, err = pcall(Construire)
if not ok and A.NoterErreur then A.NoterErreur("panneau d'options", err) end
