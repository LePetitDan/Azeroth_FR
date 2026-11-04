-- ============================================================================
-- Azeroth_FR : messages du centre de l'ecran (version 0.3).
-- « Kobold Vermin slain: 1/8 », « Quest accepted: … » (UI_INFO_MESSAGE), et les erreurs (UI_ERROR_MESSAGE)
-- quand un francais officiel existe.
--
-- Methode courante des add-ons de filtre : le cadre du jeu UIErrorsFrame ne recoit plus ces deux
-- evenements (UnregisterEvent), notre cadre les recoit a sa place et appelle UIErrorsFrame:AddMessage avec
-- le texte traduit, EXACTEMENT comme le fait UIErrorsFrame_OnEvent du client CoA (patch-B,
-- Interface\FrameXML\UIErrorsFrame.lua, lu le 04/11/2026) :
--     UI_INFO_MESSAGE  -> self:AddMessage(arg1, 1.0, 1.0, 0.0, 1.0)   (jaune)
--     UI_ERROR_MESSAGE -> self:AddMessage(arg1, 1.0, 0.1, 0.1, 1.0)   (rouge)
-- (pas d'identifiant ni de duree particuliere ni de son dans ce client : la duree est celle du cadre,
-- displayDuration="5" dans UIErrorsFrame.xml). SYSMSG n'est pas touche.
-- Les gabarits sont ceux de la discussion (Modules/Discussion.lua) et des objectifs (Modules/Quetes.lua).
--
-- SURETE : UIErrorsFrame est un MessageFrame sans modele securise (verifie a l'execution par IsProtected) ;
-- (des)enregistrer un evenement et y ajouter un message ne change aucune variable du jeu et ne passe par
-- aucun code securise : aucun blocage possible, meme en combat. En cas d'erreur, ou avec /azfr off, le jeu
-- reprend la main (UIErrorsFrame:RegisterEvent) ; un message en cours est rendu tel quel.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger

local EVENEMENTS = { "UI_INFO_MESSAGE", "UI_ERROR_MESSAGE" }
local COULEURS = { UI_INFO_MESSAGE = { 1.0, 1.0, 0.0 }, UI_ERROR_MESSAGE = { 1.0, 0.1, 0.1 } }
local cadre = CreateFrame("Frame")
local pris = false
A.Compteurs.centre = 0

-- Traduit un message du centre de l'ecran ; nil si rien de reconnu.
local function Traduire(message)
    if type(message) ~= "string" or message == "" then return nil end
    local fr = A.TraduireObjectif and A.TraduireObjectif(message)
    if fr and fr ~= message then return fr end
    fr = A.TraduitDiscussion and A.TraduitDiscussion("CHAT_MSG_SYSTEM", message)
    if fr and fr ~= message then return fr end
    fr = A.MESSAGES_ERREURS and A.MESSAGES_ERREURS[message]
    if fr then return fr end
    return nil
end
A.TraduireMessageCentre = Traduire

-- Exactement UIErrorsFrame_OnEvent du client CoA pour ces deux evenements.
local function Afficher(evenement, texte)
    local c = COULEURS[evenement]
    if c and UIErrorsFrame and UIErrorsFrame.AddMessage then
        UIErrorsFrame:AddMessage(texte, c[1], c[2], c[3], 1.0)
    end
end

local function Prendre()
    if pris or not UIErrorsFrame or type(UIErrorsFrame.UnregisterEvent) ~= "function" then return end
    if A.EstProtege(UIErrorsFrame) or A.CentreEnPanne then return end
    for _, e in ipairs(EVENEMENTS) do
        cadre:RegisterEvent(e)
        UIErrorsFrame:UnregisterEvent(e)
    end
    pris = true
end

local function Rendre()
    if not pris or not UIErrorsFrame then return end
    for _, e in ipairs(EVENEMENTS) do
        pcall(UIErrorsFrame.RegisterEvent, UIErrorsFrame, e)
        cadre:UnregisterEvent(e)
    end
    pris = false
end
A.CentrePrendre, A.CentreRendre = Prendre, Rendre
function A.CentrePris() return pris end

cadre:SetScript("OnEvent", function(self, evenement, message, ...)
    local ok, err = pcall(function()
        local fr = A.Actif() and Traduire(message) or nil
        if fr then A.Compteurs.centre = A.Compteurs.centre + 1 end
        Afficher(evenement, fr or message)
    end)
    if not ok then
        -- le jeu reprend la main pour toute la session ; le message est rendu tel quel
        A.NoterErreur("messages du centre", err)
        A.CentreEnPanne = true
        Rendre()
        pcall(Afficher, evenement, message)
    end
end)

-- /azfr on et /azfr off (Modules/Commande.lua) ; prise en main au chargement de l'add-on.
table.insert(A.QuandActivation, function(actif)
    if actif then Prendre() else Rendre() end
end)
local ok, err = pcall(function() if A.Actif() then Prendre() end end)
if not ok then A.NoterErreur("messages du centre (prise)", err) end
table.insert(A.AuDemarrage, function() if A.Actif() then Prendre() else Rendre() end end)
