-- ============================================================================
-- Azeroth_FR : messages systeme dans la discussion (version 0.4 : hauts faits accomplis).
-- « Quest accepted: A Threat Within », « A Threat Within completed. », « Experience gained:
-- 55. », « Reputation with Stormwind increased by 55. », butin, argent, competences…
--
-- Le GABARIT (« Quest accepted: %s ») vient des GlobalStrings : sa traduction est l'affaire du
-- paquet PTRXML, avant meme le chargement de l'add-on (seul moyen sur). Le MORCEAU (%s) vient du
-- serveur, en anglais : c'est lui que l'add-on remplace, par un filtre de messages
-- (ChatFrame_AddMessageEventFilter), qui ne change que ce qui s'affiche dans la fenetre de
-- discussion. Le message est reconnu par le gabarit anglais (source : textes/client/interface.tsv)
-- ou par le gabarit actuel du jeu, puis reconstruit avec le gabarit actuel du jeu (francais si
-- PTRXML l'a pose) et les morceaux traduits. Rien de reconnu : le message passe tel quel.
-- Les liens d'objets, de sorts et de quetes portent aussi leur nom francais (meme verification
-- par numero et empreinte que les infobulles), y compris dans les canaux des joueurs.
-- Noms de canaux « 1. General - Northshire Valley » : la zone passe en francais (message
-- « Joined Channel », le seul ou le client affiche la zone).
-- ============================================================================
local A = AzerothFR
local find, gsub, gmatch, match, sub, upper, len = string.find, string.gsub, string.gmatch, string.match, string.sub,
    string.upper, string.len

-- ----------------------------------------------------------------------------
-- Liens : |Hitem:N:…|h[Nom]|h, |Hspell:N|h[Nom]|h, |Hquest:N:niveau|h[Titre]|h
-- ----------------------------------------------------------------------------
function A.TraduireLiens(texte)
    if type(texte) ~= "string" or not find(texte, "|H", 1, true) then return texte end
    if find(texte, "|Hitem:", 1, true) then
        texte = gsub(texte, "(|Hitem:(%d+)[^|]*|h%[)(.-)(%]|h)", function(debut, id, nom, fin)
            local fr = A.NomObjetAffiche(tonumber(id), nom)
            return debut .. (fr or nom) .. fin
        end)
    end
    if find(texte, "|Hquest:", 1, true) then
        texte = gsub(texte, "(|Hquest:(%d+)[^|]*|h%[)(.-)(%]|h)", function(debut, id, nom, fin)
            local fr = A.TitreParId and A.TitreParId(tonumber(id), nom)
            return debut .. (fr or nom) .. fin
        end)
    end
    if A.TraduireLiensSort then texte = A.TraduireLiensSort(texte) end
    -- 0.4 : |Hachievement:N:…|h[Nom]|h (table des hauts faits, chargee a la demande ; empreinte de l'anglais)
    if find(texte, "|Hachievement:", 1, true) then
        texte = gsub(texte, "(|Hachievement:(%d+)[^|]*|h%[)(.-)(%]|h)", function(debut, id, nom, fin)
            local fr = A.NomHautFait(tonumber(id), nom)
            return debut .. (fr or nom) .. fin
        end)
    end
    return texte
end

-- Nom francais d'un haut fait par numero, verifie par l'empreinte du nom anglais affiche.
function A.NomHautFait(id, nomEN)
    if type(id) ~= "number" then return nil end
    local t = A.TableDe("hauts_faits", "HF")
    local r = t and t:ParId(id)
    if type(r) ~= "table" or not r[1] then return nil end
    if nomEN and A.H1(nomEN) ~= r[2] then return nil end
    return r[1]
end

-- ----------------------------------------------------------------------------
-- Traduction d'un morceau selon sa nature (voir GABARITS dans outils/fabriquer.py).
-- ----------------------------------------------------------------------------
-- Titre de quete d'un message (« Quête acceptée : %s », « %s terminée. ») : par le JOURNAL des
-- quetes d'abord (titre -> numero par la 9e valeur de GetQuestLogTitle ou GetQuestLink -> titre
-- francais verifie par TitreParId), puis par le texte (titres homonymes resolus a la fabrication).
local function TitreQuete(x)
    local id = A.IdQueteParTitreJournal and A.IdQueteParTitreJournal(x)
    local fr = id and A.TitreParId(id, x)
    if fr then return fr end
    local corr = A.CorrespondancesJournal and A.CorrespondancesJournal()
    fr = corr and corr[x]
    if fr then return fr end
    fr = A.TexteQuete and A.TexteQuete(x)
    if fr then return fr end
    id = A.QueteParTitre and A.QueteParTitre(x)
    return id and A.TitreParId(id, x)
end
A.TitreQueteMessage = TitreQuete

local function Objet(x)
    if find(x, "|H", 1, true) then
        local t = A.TraduireLiens(x)
        if t ~= x then return t end
        return nil
    end
    if type(GetItemInfo) == "function" then
        local ok, _, lien = pcall(GetItemInfo, x)
        local id = ok and A.IdDepuisLien(lien, "item")
        local o = id and A.Objet(id)
        if type(o) == "table" and o[1] and A.H1(x) == o[2] then return o[1] end
    end
    return nil
end

local function GabaritsDe(ev)
    local out = {}
    for _, g in ipairs(A.GABARITS or {}) do
        if find(" " .. g.ev .. " ", " " .. ev .. " ", 1, true) then out[#out + 1] = g end
    end
    return out
end

-- Somme d'argent « 1 Gold, 5 Silver, 3 Copper » : chaque unite par son gabarit (GOLD_AMOUNT…).
local function Argent(x)
    local res, change = x, false
    for _, g in ipairs(GabaritsDe("argent")) do
        local cur = _G[g.cle]
        local vers = (type(cur) == "string" and cur ~= g.en and cur) or (type(g.fr) == "string" and g.fr) or nil
        if vers and g.en then
            local motif = gsub(A.MotifGabarit(g.en), "^%^", "")
            motif = gsub(motif, "%$$", "")
            res = gsub(res, motif, function(n) change = true; return A.Formater(vers, { n }) end)
        end
    end
    return change and res or nil
end

-- Rang de reputation (« Friendly ») : le libelle actuel du jeu si PTRXML l'a traduit.
local function Rang(x)
    for _, g in ipairs(GabaritsDe("etiquette")) do
        if g.en == x then
            local cur = _G[g.cle]
            if type(cur) == "string" and cur ~= x then return cur end
            if type(g.fr) == "string" then return g.fr end
        end
    end
    return nil
end

local NATURES = {
    q = TitreQuete,
    b = function(x) return (A.TraduireObjectif and A.TraduireObjectif(x)) or (A.NomObjectif and A.NomObjectif(x)) end,
    f = function(x) return A.Nom("faction", x) end,
    c = function(x) return A.NomCreature(x) end,
    z = function(x) return A.NomZone and A.NomZone(x) or A.Nom("zone", x) end,
    o = Objet,
    s = function(x) local t = A.TraduireLiens(x); return t ~= x and t or nil end,
    k = function(x) return A.Nom("competence", x) end,
    a = Argent,
    r = Rang,
    e = function(x) return A.Nom("ensemble", x) end,
}

-- Gabarits d'un evenement de discussion, les plus longs d'abord (« Received item: %s. » avant
-- « Received %s. »).
local par_evenement = {}
local function Liste(evenement)
    local l = par_evenement[evenement]
    if l then return l end
    l = {}
    local court = match(evenement, "^CHAT_MSG_(.+)$")
    if court then
        for _, g in ipairs(GabaritsDe(court)) do l[#l + 1] = g end
    end
    table.sort(l, function(a, b) return len(a.en) > len(b.en) end)
    par_evenement[evenement] = l
    return l
end

-- 0.9.4 (essai 8, n° 29) : avertissement d'arret du serveur. Le client anglais ecrit lui-meme « [SERVER] Restart in »
-- (ou « Shutdown in ») devant la duree que le serveur envoie (« 14 Minute(s). », AzerothCore secsToTimeString) ; c'est
-- ce texte que le compte a rebours de CoA (FrameXML/RestartTimer.lua) lit dans l'evenement, jamais modifie ici : seule
-- la ligne affichee dans la discussion change.
local UNITES_DUREE = { ["Day(s)"] = "jour(s)", ["Hour(s)"] = "heure(s)", ["Minute(s)"] = "minute(s)",
    ["Second(s)"] = "seconde(s)" }
local function ArretServeur(message)
    local quoi, duree = match(message, "^%[SERVER%] (%a+) in (.+)$")
    local debut = (quoi == "Restart" and "Redémarrage dans ") or (quoi == "Shutdown" and "Arrêt dans ") or nil
    if debut then
        return "[SERVEUR] " .. debut .. gsub(duree, "(%a+%(s%))", function(u) return UNITES_DUREE[u] end)
    end
    local annule = match(message, "^%[SERVER%] (%a+) cancelled%.?$")
    if annule == "Restart" then return "[SERVEUR] Redémarrage annulé." end
    if annule == "Shutdown" then return "[SERVEUR] Arrêt annulé." end
    return nil
end

-- Reconnait et reconstruit un message ; renvoie le nouveau texte ou nil.
local function TraduireMessage(evenement, message)
    if evenement == "CHAT_MSG_SYSTEM" and sub(message, 1, 9) == "[SERVER] " then
        local fr = ArretServeur(message)
        if fr then return fr end
    end
    for _, g in ipairs(Liste(evenement)) do
        local cur = _G[g.cle]
        if type(cur) ~= "string" or cur == "" then cur = g.en end
        local args = A.LireGabarit(cur, message)
        if not args and cur ~= g.en then args = A.LireGabarit(g.en, message) end
        if args then
            local change = (cur ~= g.en) and not A.LireGabarit(cur, message)
            local n = len(g.t)
            for i = 1, n do
                local nature = sub(g.t, i, i)
                local fn = NATURES[nature]
                local v = args[i]
                if fn and type(v) == "string" and v ~= "" then
                    local ok, fr = pcall(fn, v)
                    if ok and fr and fr ~= v then args[i] = fr; change = true end
                end
            end
            -- liens restes en anglais dans les autres morceaux
            for i, v in pairs(args) do
                if type(v) == "string" then
                    local t = A.TraduireLiens(v)
                    if t ~= v then args[i] = t; change = true end
                end
            end
            if not change then return nil end
            local r = A.Formater(cur, args)
            -- « Réputation auprès |2 %s » : l'elision du client francais, faite ici
            if A.Elision then r = A.Elision(r) end
            return r
        end
    end
    local t = A.TraduireLiens(message)
    if t ~= message then return t end
    return nil
end
A.TraduireMessage = TraduireMessage

-- Memoire des derniers messages (chaque fenetre de discussion appelle le filtre).
local memo, n_memo = {}, 0
local function Traduit(evenement, message)
    local k = evenement .. "\0" .. message
    local m = memo[k]
    if m ~= nil then return m or nil end
    local ok, r = pcall(TraduireMessage, evenement, message)
    if not ok then A.NoterErreur("discussion " .. evenement, r); r = nil end
    n_memo = n_memo + 1
    if n_memo > 200 then memo, n_memo = {}, 0 end
    memo[k] = r or false
    if r then A.Compteurs.discussion = A.Compteurs.discussion + 1 end
    return r
end
A.TraduitDiscussion = Traduit

-- Filtre : (cadre, evenement, message, emetteur, …11 arguments) -> false, nouveaux arguments.
local function Filtre(self, evenement, message, ...)
    if not A.Actif() or type(message) ~= "string" or message == "" then return false end
    pcall(A.Trace, "filtre discussion")
    local r = Traduit(evenement, message)
    if r then return false, r, ... end
    return false
end

-- Canaux : « Joined Channel: [1. General - Northshire Valley] » -> zone en francais (4e argument).
local function FiltreCanal(self, evenement, a1, a2, a3, a4, ...)
    if not A.Actif() or type(a4) ~= "string" then return false end
    local ok, nouveau = pcall(function()
        local debut, zone = match(a4, "^(.-%s%-%s)(.+)$")
        local fr = zone and A.NomZone and A.NomZone(zone)
        if fr then return debut .. fr end
    end)
    if ok and nouveau then return false, a1, a2, a3, nouveau, ... end
    return false
end

if type(ChatFrame_AddMessageEventFilter) == "function" then
    for _, e in ipairs({ "CHAT_MSG_SYSTEM", "CHAT_MSG_COMBAT_FACTION_CHANGE", "CHAT_MSG_COMBAT_XP_GAIN",
        "CHAT_MSG_COMBAT_HONOR_GAIN", "CHAT_MSG_LOOT", "CHAT_MSG_MONEY", "CHAT_MSG_SKILL", "CHAT_MSG_TRADESKILLS",
        -- liens seulement
        "CHAT_MSG_SAY", "CHAT_MSG_YELL", "CHAT_MSG_PARTY", "CHAT_MSG_PARTY_LEADER", "CHAT_MSG_RAID",
        "CHAT_MSG_RAID_LEADER", "CHAT_MSG_GUILD", "CHAT_MSG_OFFICER", "CHAT_MSG_WHISPER", "CHAT_MSG_WHISPER_INFORM",
        "CHAT_MSG_CHANNEL", "CHAT_MSG_BATTLEGROUND", "CHAT_MSG_BATTLEGROUND_LEADER",
        -- 0.4 : « %s has earned the achievement [X]! » (joueur, guilde)
        "CHAT_MSG_ACHIEVEMENT", "CHAT_MSG_GUILD_ACHIEVEMENT" }) do
        ChatFrame_AddMessageEventFilter(e, Filtre)
    end
    ChatFrame_AddMessageEventFilter("CHAT_MSG_CHANNEL_NOTICE", FiltreCanal)
end

-- 0.9.4 (essai 8, n° 29) : barre du compte a rebours de CoA (RestartTimerFrame, FrameXML/RestartTimer.lua : texte
-- « Server Restart - 14:32 » refait a chaque image par son OnUpdate) : reprise juste apres, a l'affichage seulement.
local function BarreRedemarrage(self)
    if not A.Actif() or type(self) ~= "table" or not self.Text or type(self.Text.GetText) ~= "function" then return end
    local t = self.Text:GetText()
    if type(t) ~= "string" then return end
    local quoi, temps = match(t, "^Server (%a+) %- (.+)$")
    local fr = (quoi == "Restart" and "Redémarrage du serveur - ") or (quoi == "Shutdown" and "Arrêt du serveur - ") or nil
    if fr then self.Text:SetText(fr .. temps) end
end
if RestartTimerFrame and type(RestartTimerFrame.HookScript) == "function" then
    RestartTimerFrame:HookScript("OnUpdate", A.Proteger("RestartTimerFrame.OnUpdate", BarreRedemarrage, true))
end
