-- ============================================================================
-- Azeroth_FR : cris et paroles des PNJ dans la discussion.
-- Filtres de messages CHAT_MSG_MONSTER_* : le texte (par texte anglais, $n reconstitue
-- avec le nom du joueur ou celui de la cible de la replique) et le nom du PNJ qui parle.
-- Un filtre ne modifie que ce qui s'affiche dans la fenetre de discussion.
-- Les bulles au-dessus des PNJ : Modules/Bulles.lua (memes tables). Les emotes de boss au centre de
-- l'ecran (RaidBossEmoteFrame) restent en anglais.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger

local function CT() return A.TableDe("cris", "CT") end

local function TraduireCri(message, emetteur, cible)
    local nouveau, nouvelEmetteur
    if type(message) == "string" and message ~= "" then
        nouveau = A.Traduire(CT(), message, cible)
    end
    if type(emetteur) == "string" and emetteur ~= "" then
        nouvelEmetteur = A.NomCreature(emetteur)
    end
    return nouveau, nouvelEmetteur
end
A.TraduireCri = TraduireCri

-- Arguments d'un message : texte, emetteur, langue, canal, cible ($n), … (3.3.5)
local function Filtre(self, evenement, message, emetteur, ...)
    if not A.Actif() then return false end
    pcall(A.Trace, "filtre cris")
    local ok, nouveau, nouvelEmetteur = pcall(TraduireCri, message, emetteur, (select(3, ...)))
    if not ok then
        A.NoterErreur("filtre " .. tostring(evenement), nouveau)
        return false
    end
    if nouveau or nouvelEmetteur then
        return false, nouveau or message, nouvelEmetteur or emetteur, ...
    end
    return false
end

if type(ChatFrame_AddMessageEventFilter) == "function" then
    for _, evenement in ipairs({ "CHAT_MSG_MONSTER_SAY", "CHAT_MSG_MONSTER_YELL", "CHAT_MSG_MONSTER_EMOTE",
        "CHAT_MSG_MONSTER_WHISPER", "CHAT_MSG_MONSTER_PARTY", "CHAT_MSG_RAID_BOSS_EMOTE",
        "CHAT_MSG_RAID_BOSS_WHISPER" }) do
        ChatFrame_AddMessageEventFilter(evenement, Filtre)
    end
end
