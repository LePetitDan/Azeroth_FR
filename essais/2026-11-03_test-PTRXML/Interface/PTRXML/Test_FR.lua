-- Test Azeroth_FR : quatre textes des écrans de connexion passent en français.
-- Pour annuler : supprimer le dossier Interface\PTRXML (rien d'autre n'est modifié).
LOGIN = "Connexion"
QUIT = "Quitter"
ENTER_WORLD = "Entrer dans le monde"
CREATE_NEW_CHARACTER = "Créer un nouveau personnage"

-- En jeu seulement : un message dans la discussion dit si le fichier a été chargé
-- et si le jeu considère la variable comme « sûre » (pas de souillure).
local ok, f = pcall(CreateFrame, "Frame")
if ok and f then
    local inscrit = pcall(f.RegisterEvent, f, "PLAYER_ENTERING_WORLD")
    if inscrit then
        f:SetScript("OnEvent", function(self)
            self:UnregisterAllEvents()
            local sure = issecurevariable and issecurevariable("ENTER_WORLD")
            if DEFAULT_CHAT_FRAME then
                DEFAULT_CHAT_FRAME:AddMessage("|cff33ff99Azeroth_FR (test)|r : fichier charge en jeu. Variable sure : " .. tostring(sure)
                    .. " ; LuaDBC : " .. type(LuaDBC) .. " ; langue du client : " .. tostring(GetLocale and GetLocale()))
            end
        end)
    end
end
