-- ============================================================================
-- Azeroth_FR : livres, lettres et courriers du jeu.
-- Pages des livres (fenetre de lecture) et courriers des hauts faits (objet et corps).
-- Par texte anglais exact. Affichage seulement.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger

local function PT() return A.TableDe("pages", "PT") end

function A.TextePage(texte)
    return A.Traduire(PT(), texte)
end

-- Pages des livres : le jeu pose le texte au signal ITEM_TEXT_READY, nous passons apres.
local f = CreateFrame("Frame")
f:RegisterEvent("ITEM_TEXT_READY")
f:SetScript("OnEvent", P("Pages.ITEM_TEXT_READY", function()
    if not A.Actif() or type(ItemTextGetText) ~= "function" then return end
    local fr = A.TextePage(ItemTextGetText())
    if fr and ItemTextPageText then A.Ecrire(ItemTextPageText, fr) end
end))

-- Courrier ouvert : objet et corps.
local function TraduireCourrier()
    if not A.Actif() or not InboxFrame or not InboxFrame.openMailID then return end
    local id = InboxFrame.openMailID
    local corps = GetInboxText and GetInboxText(id)
    local fr = A.TextePage(corps)
    if fr and OpenMailBodyText then A.Ecrire(OpenMailBodyText, fr) end
    local objet = OpenMailSubject and OpenMailSubject:GetText()
    local fr2 = A.TextePage(objet)
    if fr2 then A.Ecrire(OpenMailSubject, fr2) end
end

-- Liste du courrier : les objets des lettres.
local function TraduireBoite()
    if not A.Actif() then return end
    for i = 1, (INBOXITEMS_TO_DISPLAY or 7) do
        local zone = _G["MailItem" .. i .. "Subject"]
        local texte = zone and zone:GetText()
        if texte and texte ~= "" and not A.DejaEcrit(zone, texte) then
            local fr = A.TextePage(texte)
            if fr then A.Ecrire(zone, fr) end
        end
    end
end

if type(OpenMail_Update) == "function" then
    hooksecurefunc("OpenMail_Update", P("OpenMail_Update", TraduireCourrier))
end
if type(InboxFrame_Update) == "function" then
    hooksecurefunc("InboxFrame_Update", P("InboxFrame_Update", TraduireBoite))
end
