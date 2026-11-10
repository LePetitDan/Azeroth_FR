-- ============================================================================
-- Azeroth_FR : signaler une erreur de traduction, simplement (1.2.0, demande de Dan).
-- Le joueur survole le texte en cause (objet, sort, bouton…) et tape /azfr signaler : une petite fenetre montre
-- un compte rendu tout pret (version, zone, numero de l'objet ou du sort, texte affiche et anglais d'origine quand
-- l'add-on l'a traduit). Il le copie (Ctrl+C) et le colle dans le salon des signalements du Discord.
-- Le jeu ne peut rien envoyer sur internet : c'est le joueur qui colle. Le compte rendu ne contient ni nom de
-- personnage ni nom de joueur. Fenetre sans nom global ni modele XML ; aucune variable du jeu n'est ecrite.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger
local MAX_LIGNES, MAX_LONGUEUR = 14, 220

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

-- Le compte rendu, en texte simple.
local function Texte()
    local l = {}
    l[#l + 1] = "[Azeroth_FR " .. tostring(A.VERSION) .. "] Signalement"
    local z = Zone()
    if z ~= "" then l[#l + 1] = "Zone : " .. Propre(z) end
    local b = GameTooltip
    if b and type(b.IsShown) == "function" and b:IsShown() then
        local nomEN, lien
        if type(b.GetItem) == "function" then nomEN, lien = b:GetItem() end
        local idObjet = lien and A.IdDepuisLien and A.IdDepuisLien(lien, "item")
        if idObjet then l[#l + 1] = "Objet : " .. tostring(idObjet) end
        if type(b.GetSpell) == "function" then
            local _, _, idSort = b:GetSpell()
            if idSort then l[#l + 1] = "Sort : " .. tostring(idSort) end
        end
        l[#l + 1] = "Texte affiché :"
        local n = (type(b.NumLines) == "function" and b:NumLines()) or 0
        for i = 1, math.min(n, MAX_LIGNES) do
            local g = _G["GameTooltipTextLeft" .. i]
            local t = g and g:GetText()
            if t and t ~= "" then
                l[#l + 1] = "  " .. Propre(t)
                -- l'anglais d'origine, quand cette ligne a ete traduite par l'add-on
                if A.Originaux and A.Originaux[g] and A.DejaEcrit and A.DejaEcrit(g, t) then
                    l[#l + 1] = "    (anglais : " .. Propre(A.Originaux[g]) .. ")"
                end
            end
        end
        if n > MAX_LIGNES then l[#l + 1] = "  (" .. (n - MAX_LIGNES) .. " lignes de plus)" end
    else
        -- pas d'infobulle : le cadre sous la souris (bouton, texte de fenetre)
        local c = type(GetMouseFocus) == "function" and GetMouseFocus() or nil
        local nom = c and type(c.GetName) == "function" and c:GetName() or nil
        if nom and nom ~= "WorldFrame" then l[#l + 1] = "Élément : " .. Propre(nom) end
        local t = c and type(c.GetText) == "function" and c:GetText() or nil
        if t and t ~= "" then l[#l + 1] = "Texte affiché : " .. Propre(t) end
    end
    l[#l + 1] = "Ce qui ne va pas : "
    return table.concat(l, "\n")
end
A.TexteSignalement = Texte

local fenetre
local function Fenetre()
    if fenetre then return fenetre end
    local f = CreateFrame("Frame", nil, UIParent)
    f:SetWidth(520)
    f:SetHeight(330)
    f:SetPoint("CENTER", UIParent, "CENTER", 0, 40)
    f:SetFrameStrata("DIALOG")
    f:SetBackdrop({
        bgFile = "Interface\\ChatFrame\\ChatFrameBackground",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border", edgeSize = 16,
        insets = { left = 4, right = 4, top = 4, bottom = 4 },
    })
    f:SetBackdropColor(0.02, 0.06, 0.18, 0.96)
    f:SetBackdropBorderColor(0.91, 0.71, 0.37, 1)
    f:EnableMouse(true)

    local titre = f:CreateFontString(nil, "ARTWORK", "GameFontNormalLarge")
    titre:SetPoint("TOPLEFT", f, "TOPLEFT", 16, -14)
    titre:SetText("Signaler une erreur de traduction")

    local aide = f:CreateFontString(nil, "ARTWORK", "GameFontHighlightSmall")
    aide:SetPoint("TOPLEFT", titre, "BOTTOMLEFT", 0, -6)
    aide:SetWidth(488)
    aide:SetJustifyH("LEFT")
    aide:SetText("1. Appuyez sur Ctrl+C : le texte ci-dessous est déjà sélectionné.\n2. Collez-le (Ctrl+V) dans le salon des signalements du Discord Azeroth_FR, et dites en un mot ce qui ne va pas.\n   Discord : " .. tostring(A.LIEN_DISCORD or "discord.gg/kFJGDJbeay"))

    local zone = CreateFrame("EditBox", nil, f)
    zone:SetMultiLine(true)
    zone:SetAutoFocus(false)
    zone:SetFontObject(ChatFontNormal or GameFontHighlightSmall)
    zone:SetWidth(484)
    zone:SetHeight(200)
    zone:SetPoint("TOPLEFT", aide, "BOTTOMLEFT", 2, -10)
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

    local fermer = CreateFrame("Button", nil, f)
    fermer:SetWidth(100)
    fermer:SetHeight(22)
    fermer:SetPoint("BOTTOMRIGHT", f, "BOTTOMRIGHT", -14, 12)
    fermer:SetNormalFontObject(GameFontNormal)
    fermer:SetHighlightFontObject(GameFontHighlight)
    fermer:SetText("Fermer")
    fermer:SetScript("OnClick", function() f:Hide() end)
    f.fermer = fermer

    f:Hide()
    fenetre = f
    return f
end

-- /azfr signaler : le compte rendu de ce qui est sous la souris, pret a copier.
function A.Signaler()
    local texte = "```\n" .. Texte() .. "\n```"
    local f = Fenetre()
    f.texte = texte
    f.zone:SetText(texte)
    f:Show()
    f.zone:SetFocus()
    f.zone:HighlightText()
end
A.Signaler = P("Signaler", A.Signaler)
function A.FenetreSignalement() return fenetre end
