-- ============================================================================
-- Azeroth_FR : dialogues des PNJ.
-- Texte d'accueil (npc_text), options de dialogue, titres des quetes proposees, accueil
-- des maitres de classe, nom du PNJ en tete de la fenetre (UnitName("npc"), par le numero de
-- la creature tire de son GUID). Par texte anglais, variables $n $g $r $c reconstituees.
-- ============================================================================
local A = AzerothFR
local match = string.match
local P = A.Proteger

local function DT() return A.TableDe("dialogues", "DT") end

function A.TexteDialogue(texte)
    return A.Traduire(DT(), texte)
end

-- Bouton de dialogue : option (table des dialogues) ou titre de quete (avec couleur).
local function TraduireBouton(bouton)
    local texte = bouton:GetText()
    if not texte or texte == "" or A.DejaEcrit(bouton, texte) then return end
    local fr = A.TexteDialogue(texte)
    if not fr then
        local couleur, nu = match(texte, "^(|c%x%x%x%x%x%x%x%x)(.-)|r$")
        if nu and nu ~= "" then
            local fr2 = A.TexteDialogue(nu) or (A.TitreQuete and A.TitreQuete(nu))
            if fr2 then fr = couleur .. fr2 .. "|r" end
        end
    end
    if not fr and A.TitreQuete then fr = A.TitreQuete(texte) end
    -- (1.2, signalement de Dan du 18/11 : le Gardien du temps) Des modules du serveur mettent une icone devant
    -- l'option : « |TInterface/ICONS/nom:30:30:-18:0|t|r » puis le texte (mod-worldforged-upgrades, IconText).
    -- On traduit le texte qui suit et on garde l'icone telle quelle.
    if not fr then
        local icone, suite = match(texte, "^(|T.-|t)(.+)$")
        if icone then
            if string.sub(suite, 1, 2) == "|r" then icone, suite = icone .. "|r", string.sub(suite, 3) end
            local espaces, nu = match(suite, "^(%s*)(.+)$")
            local fr2 = nu and (A.TexteDialogue(nu) or (A.TitreQuete and A.TitreQuete(nu)))
            if fr2 then fr = icone .. espaces .. fr2 end
        end
    end
    if fr and fr ~= texte then
        A.Ecrire(bouton, fr)
        -- meme mise en page que le jeu (hauteur selon le texte). 0.4 : on n'appelle plus GossipResize du jeu
        -- (une fonction du jeu appelee par l'add-on s'execute « entachee ») ; on fait ici exactement ce qu'elle
        -- fait dans le client CoA (patch-B, GossipFrame.lua : SetHeight(GetTextHeight() + 2)), hors combat et
        -- seulement sur un bouton non protege.
        if not A.EnCombat() and not A.EstProtege(bouton) and type(bouton.GetTextHeight) == "function" then
            bouton:SetHeight(bouton:GetTextHeight() + 2)
        end
    end
end

local function TraduireGossip()
    if not A.Actif() then return end
    if A.TraduireNomPNJ then A.TraduireNomPNJ(GossipFrameNpcNameText, { "npc" }) end
    local zone = GossipGreetingText
    local texte = zone and zone:GetText()
    if texte and texte ~= "" and not A.DejaEcrit(zone, texte) then
        local fr = A.TexteDialogue(texte)
        -- 1.2.1 : texte composé par le serveur avec des nombres variables (loterie de Gallywix) : gabarit à nombres
        if not fr and A.TexteClient then fr = A.TexteClient(texte) end
        if fr then A.Ecrire(zone, fr) end
    end
    for i = 1, 32 do
        local bouton = _G["GossipTitleButton" .. i]
        if not bouton then break end
        if bouton:IsShown() then TraduireBouton(bouton) end
    end
end

if type(GossipFrameUpdate) == "function" then
    hooksecurefunc("GossipFrameUpdate", P("GossipFrameUpdate", TraduireGossip))
end

-- Accueil des maitres de classe et de metier (Blizzard_TrainerUI, charge a la demande par le jeu).
-- ClassTrainerFrame_Update repose le texte anglais a chaque mise a jour (TRAINER_UPDATE) : on
-- l'accroche des que l'add-on du jeu est charge (appele par son nom global dans ce client).
local function TraduireMaitre()
    if not A.Actif() then return end
    local zone = ClassTrainerGreetingText
    local texte = zone and zone:GetText()
    if texte and texte ~= "" and not A.DejaEcrit(zone, texte) then
        local fr = A.TexteDialogue(texte)
        if fr then A.Ecrire(zone, fr) end
    end
end
local maitre_accroche = false
local function AccrocherMaitre()
    if maitre_accroche or type(ClassTrainerFrame_Update) ~= "function" then return end
    maitre_accroche = true
    hooksecurefunc("ClassTrainerFrame_Update", P("ClassTrainerFrame_Update", TraduireMaitre))
end

local f = CreateFrame("Frame")
f:RegisterEvent("GOSSIP_SHOW")
f:RegisterEvent("TRAINER_SHOW")
f:RegisterEvent("ADDON_LOADED")
f:SetScript("OnEvent", P("Dialogues.OnEvent", function(self, evenement, nom)
    if evenement == "ADDON_LOADED" then
        if nom == "Blizzard_TrainerUI" then AccrocherMaitre() end
        return
    end
    if not A.Actif() then return end
    if evenement == "GOSSIP_SHOW" then
        TraduireGossip()
    elseif evenement == "TRAINER_SHOW" then
        AccrocherMaitre()
        TraduireMaitre()
    end
end))
AccrocherMaitre()
