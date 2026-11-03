-- ============================================================================
-- Azeroth_FR : le coeur de l'add-on (essai 1).
--
-- PRINCIPE : AFFICHAGE SEULEMENT. Le jeu affiche son texte anglais ; l'add-on le
-- reconnait et pose le francais par-dessus, dans le cadre affiche (FontString:SetText,
-- filtres de discussion). Il n'ecrit dans AUCUNE variable globale du jeu (lecon payee
-- par AscensionFR : cinq versions bloquees par la « souillure »). Ses seules globales
-- sont les siennes : la table AzerothFR, ses reglages AzerothFR_Reglages et sa
-- commande /azfr.
--
-- SURETE : tout ce qui est appele par le jeu passe par pcall (A.Proteger) ; une
-- erreur ne s'affiche jamais chez le joueur, elle est comptee (/azfr stats).
--
-- RECONNAISSANCE :
-- - par numero quand le jeu le donne (objets, creatures, quetes du journal), avec
--   une verification : l'empreinte de l'anglais affiche doit etre celle de l'anglais
--   traduit (si le serveur a change un texte, on garde l'anglais) ;
-- - sinon par texte anglais exact : on calcule l'empreinte de sa forme
--   « canonique » (meme calcul que outils/fabriquer.py) apres avoir remis en
--   variables ($n, $r, $c) ce que le jeu a deja remplace.
--
-- DONNEES : des add-ons « LoadOnDemand » par famille (Azeroth_FR_Quetes, …), au
-- format paresseux : rien n'est compile avant d'etre demande.
-- ============================================================================
AzerothFR = AzerothFR or {}
local A = AzerothFR

local byte, find, gsub, sub, match, lower, len = string.byte, string.find, string.gsub, string.sub, string.match,
    string.lower, string.len
local floor, pairs, ipairs, type, pcall, tostring, tonumber = math.floor, pairs, ipairs, type, pcall, tostring, tonumber

A.Tables = A.Tables or {}       -- famille -> nom -> table paresseuse
A.Erreurs = 0
A.DerniereErreur = nil
A.Charges = {}                  -- add-on de donnees -> true (charge) / false (echec)
A.RaisonsEchec = {}
A.DureesChargement = {}         -- add-on -> millisecondes
A.EnAttente = {}                -- add-ons a charger apres le combat
A.Compteurs = { traduits = 0, recherches = 0 }

-- ----------------------------------------------------------------------------
-- Surete
-- ----------------------------------------------------------------------------
local function NoterErreur(nom, err)
    A.Erreurs = A.Erreurs + 1
    A.DerniereErreur = tostring(nom) .. " : " .. tostring(err)
end
A.NoterErreur = NoterErreur

-- Enveloppe une fonction appelee par le jeu (crochet, evenement) : jamais d'erreur visible.
function A.Proteger(nom, fn)
    return function(...)
        local ok, err = pcall(fn, ...)
        if not ok then NoterErreur(nom, err) end
    end
end

function A.Actif()
    return not (type(AzerothFR_Reglages) == "table" and AzerothFR_Reglages.inactif)
end

-- Un cadre protege ne doit jamais etre touche (sinon le jeu bloque les actions du joueur).
function A.EstProtege(cadre)
    if not cadre or type(cadre.IsProtected) ~= "function" then return false end
    local ok, protege = pcall(cadre.IsProtected, cadre)
    return ok and protege
end

-- Ce que l'add-on a lui-meme ecrit dans une zone de texte (table a cles faibles : rien n'est
-- ajoute aux objets du jeu).
A.Ecrits = setmetatable({}, { __mode = "k" })

function A.Ecrire(zone, texte)
    if not zone or not texte then return false end
    zone:SetText(texte)
    A.Ecrits[zone] = zone:GetText()
    A.Compteurs.traduits = A.Compteurs.traduits + 1
    return true
end

function A.DejaEcrit(zone, texte)
    return A.Ecrits[zone] ~= nil and A.Ecrits[zone] == texte
end

-- ----------------------------------------------------------------------------
-- Empreinte d'un texte : IDENTIQUE a empreintes() de outils/fabriquer.py.
-- Deux hachages polynomiaux modulo des nombres premiers ; tout reste exact en
-- nombres a virgule de Lua (moins de 2^53).
-- ----------------------------------------------------------------------------
local P1, P2, D25 = 67108859, 33554393, 33554432

local function Empreintes(s)
    local h1, h2, n, i = 0, 0, len(s), 1
    while i + 7 <= n do
        local a, b, c, d, e, f, g, h = byte(s, i, i + 7)
        h1 = (h1 * 31 + a) % P1; h2 = (h2 * 37 + a) % P2
        h1 = (h1 * 31 + b) % P1; h2 = (h2 * 37 + b) % P2
        h1 = (h1 * 31 + c) % P1; h2 = (h2 * 37 + c) % P2
        h1 = (h1 * 31 + d) % P1; h2 = (h2 * 37 + d) % P2
        h1 = (h1 * 31 + e) % P1; h2 = (h2 * 37 + e) % P2
        h1 = (h1 * 31 + f) % P1; h2 = (h2 * 37 + f) % P2
        h1 = (h1 * 31 + g) % P1; h2 = (h2 * 37 + g) % P2
        h1 = (h1 * 31 + h) % P1; h2 = (h2 * 37 + h) % P2
        i = i + 8
    end
    while i <= n do
        local a = byte(s, i)
        h1 = (h1 * 31 + a) % P1; h2 = (h2 * 37 + a) % P2
        i = i + 1
    end
    return h1, h2
end
A.Empreintes = Empreintes

-- Empreinte courte (26 bits) : sert a verifier qu'un texte affiche est bien l'anglais traduit.
function A.H1(s)
    local h1 = Empreintes(s)
    return h1
end

-- Cle complete (51 bits) et numero de seau.
function A.Cle(s)
    local h1, h2 = Empreintes(s)
    return h1 * D25 + h2, h2
end

-- ----------------------------------------------------------------------------
-- Forme canonique : IDENTIQUE a canon() de outils/fabriquer.py (fins de ligne, espaces
-- resserres, espaces autour des retours a la ligne, bords).
-- ----------------------------------------------------------------------------
function A.Canon(s)
    s = gsub(s, "\r\n", "\n")
    s = gsub(s, "\r", "\n")
    s = gsub(s, "[ \t]+", " ")
    s = gsub(s, " ?\n ?", "\n")
    return (match(s, "^[ \n]*(.-)[ \n]*$"))
end

local function Motif(s)
    return (gsub(s, "([%^%$%(%)%%%.%[%]%*%+%-%?])", "%%%1"))
end

-- Le jeu a deja remplace $n (nom), $r (race) et $c (classe) : on essaie de les remettre.
-- Renvoie une liste de candidats { forme, nom utilise }, les plus substitues d'abord.
function A.Candidats(s, noms, race, classe)
    local liste = { { s, nil } }
    local function etendre(variantes, marque, estNom)
        local nouvelle = {}
        for _, c in ipairs(liste) do
            for _, v in ipairs(variantes) do
                if v and v ~= "" and find(c[1], v, 1, true) then
                    nouvelle[#nouvelle + 1] = { (gsub(c[1], Motif(v), marque)), estNom and v or c[2] }
                end
            end
        end
        if #nouvelle > 0 then
            for _, c in ipairs(liste) do nouvelle[#nouvelle + 1] = c end
            liste = nouvelle
        end
    end
    etendre(noms or {}, "\1N", true)
    if race and race ~= "" then
        local r2 = lower(race)
        etendre(r2 ~= race and { race, r2 } or { race }, "\1R")
    end
    if classe and classe ~= "" then
        local c2 = lower(classe)
        etendre(c2 ~= classe and { classe, c2 } or { classe }, "\1C")
    end
    return liste
end

-- ----------------------------------------------------------------------------
-- Tables paresseuses
-- ----------------------------------------------------------------------------
local Paresseuse = {}
Paresseuse.__index = Paresseuse

function Paresseuse:Seau(s)
    local seau = self.seaux[s]
    if seau then return seau end
    local src = self.morceaux[s]
    if not src then return nil end
    self.morceaux[s] = nil              -- un seau ne se compile qu'une fois
    local tbl
    local f = loadstring("return {" .. src .. "}")
    if f then
        local ok, t = pcall(f)
        if ok and type(t) == "table" then tbl = t end
    end
    if not tbl then
        tbl = {}
        self.echecs = self.echecs + 1
        NoterErreur("seau " .. self.famille .. "." .. self.nom, s)
    end
    self.seaux[s] = tbl
    self.compiles = self.compiles + 1
    return tbl
end

function Paresseuse:ParId(id)
    if type(id) ~= "number" then return nil end
    local seau = self:Seau(floor(id / self.nb))
    return seau and seau[id]
end

function Paresseuse:ParCle(cle, h2)
    local seau = self:Seau(h2 % self.nb)
    return seau and seau[cle]
end

-- Appele par les fichiers de donnees (Azeroth_FR_<Famille>\DonneesN.lua).
function A.Recevoir(famille, nom, sorte, nb, morceaux)
    if type(morceaux) ~= "table" then return end
    local fam = A.Tables[famille]
    if not fam then fam = {}; A.Tables[famille] = fam end
    local t = fam[nom]
    if not t then
        t = setmetatable({ famille = famille, nom = nom, sorte = sorte, nb = nb, morceaux = {}, seaux = {},
            n_morceaux = 0, compiles = 0, echecs = 0 }, Paresseuse)
        fam[nom] = t
    end
    for s, src in pairs(morceaux) do
        if not t.seaux[s] then
            t.morceaux[s] = src
            t.n_morceaux = t.n_morceaux + 1
        end
    end
end

-- ----------------------------------------------------------------------------
-- Chargement des add-ons de donnees
-- ----------------------------------------------------------------------------
local function Chrono()
    if type(debugprofilestop) == "function" then return debugprofilestop() end
    return 0
end

function A.ChargerAddon(addon)
    local etat = A.Charges[addon]
    if etat ~= nil then return etat end
    if type(InCombatLockdown) == "function" and InCombatLockdown() then
        A.EnAttente[addon] = true       -- jamais de gros chargement en plein combat
        return false
    end
    local t0 = Chrono()
    local ok, charge, raison = pcall(LoadAddOn, addon)
    A.DureesChargement[addon] = Chrono() - t0
    A.Charges[addon] = (ok and charge) and true or false
    A.EnAttente[addon] = nil
    if not A.Charges[addon] then
        A.RaisonsEchec[addon] = ok and tostring(raison) or tostring(charge)
    end
    return A.Charges[addon]
end

-- Renvoie les tables d'une famille, en chargeant son add-on si besoin.
function A.Famille(famille)
    local fam = A.Tables[famille]
    if fam then return fam end
    for _, f in ipairs(A.FAMILLES or {}) do
        if f.famille == famille and not f.debut then A.ChargerAddon(f.addon) end
    end
    return A.Tables[famille]
end

function A.TableDe(famille, nom)
    local fam = A.Famille(famille)
    return fam and fam[nom]
end

-- Objet par numero : la tranche d'objets qui le contient est chargee a la demande.
function A.Objet(id)
    if type(id) ~= "number" then return nil end
    for _, f in ipairs(A.FAMILLES or {}) do
        if f.famille == "objets" and f.debut and id >= f.debut and id <= f.fin then
            if A.Charges[f.addon] == nil then A.ChargerAddon(f.addon) end
            break
        end
    end
    local t = A.Tables.objets and A.Tables.objets.O
    return t and t:ParId(id)
end

-- ----------------------------------------------------------------------------
-- Le joueur : nom, race, classe, genre (lus une fois, a la connexion)
-- ----------------------------------------------------------------------------
A.Joueur = {}

function A.LireJoueur()
    local j = A.Joueur
    j.nom = UnitName and UnitName("player") or nil
    j.race = UnitRace and UnitRace("player") or nil
    j.classe = UnitClass and UnitClass("player") or nil
    local sexe = UnitSex and UnitSex("player") or 2
    j.genre = (sexe == 3) and "f" or "m"
    return j
end

local function NomRace(raceEN, genre)
    local r = raceEN and A.RACES and A.RACES[raceEN]
    if r then return (genre == "f" and r[2]) or r[1] end
    return raceEN or ""
end

local function NomClasse(classeEN)
    return (classeEN and A.CLASSES and A.CLASSES[classeEN]) or classeEN or ""
end

-- « |2 mot » : elision du client francais (« de » / « d' »), faite ici.
local VOYELLES = { a = true, e = true, i = true, o = true, u = true, y = true, h = true,
    A = true, E = true, I = true, O = true, U = true, Y = true, H = true }
local function Elision(fr)
    if not find(fr, "|2", 1, true) then return fr end
    return (gsub(fr, "|2 ?(%S)", function(c)
        local b = byte(c)
        if VOYELLES[c] or (b and b >= 195) then return "d'" .. c end   -- 195 : premier octet de É, À, Â…
        return "de " .. c
    end))
end

-- Rend un francais stocke (modele avec variables) pour l'affichage.
-- nom : le nom reconnu dans l'anglais ($n), sinon celui du joueur.
function A.Rendre(fr, nom)
    if type(fr) ~= "string" then return nil end
    local j = A.Joueur
    local genre = j.genre or "m"
    local b1 = byte(fr, 1)
    if b1 == 2 then genre = "m"; fr = sub(fr, 2) elseif b1 == 3 then genre = "f"; fr = sub(fr, 2) end
    if not find(fr, "$", 1, true) and not find(fr, "|2", 1, true) then return fr end
    fr = gsub(fr, "%$[Bb]", "\n")
    fr = gsub(fr, "%$[Gg]([^:;]*):([^;]*);", function(m, f)
        if genre == "f" then return f end
        return m
    end)
    local n = nom or j.nom or ""
    fr = gsub(fr, "%$[Nn]", function() return n end)
    fr = gsub(fr, "%$[Rr]", function() return NomRace(j.race, genre) end)
    fr = gsub(fr, "%$[Cc]", function() return NomClasse(j.classe) end)
    return Elision(fr)
end

-- ----------------------------------------------------------------------------
-- Recherche par texte anglais (tables QT, DT, CT, PT) avec memoire des resultats
-- ----------------------------------------------------------------------------
A.Memo = setmetatable({}, { __mode = "k" })
local memo_taille = 0

-- tab : table paresseuse par texte ; texte : l'anglais affiche ; autreNom : un second nom
-- possible pour $n (cible d'une replique). Renvoie le francais rendu, ou nil.
function A.Traduire(tab, texte, autreNom)
    if not tab or type(texte) ~= "string" or texte == "" then return nil end
    local memo = A.Memo[tab]
    if not memo then memo = {}; A.Memo[tab] = memo end
    local mk = autreNom and (texte .. "\0" .. autreNom) or texte
    local m = memo[mk]
    if m ~= nil then return m or nil end
    A.Compteurs.recherches = A.Compteurs.recherches + 1
    local resultat = false
    local s = A.Canon(texte)
    if s ~= "" then
        local j = A.Joueur
        local noms = { j.nom }
        if autreNom and autreNom ~= "" and autreNom ~= j.nom then noms[2] = autreNom end
        for _, c in ipairs(A.Candidats(s, noms, j.race, j.classe)) do
            local h1, h2 = Empreintes(c[1])
            local v = tab:ParCle(h1 * D25 + h2, h2)
            if v ~= nil then
                if v ~= "" then resultat = A.Rendre(v, c[2]) or false end
                break
            end
        end
    end
    memo_taille = memo_taille + 1
    if memo_taille > 3000 then
        A.Memo = setmetatable({}, { __mode = "k" })
        memo_taille = 0
        memo = {}
        A.Memo[tab] = memo
    end
    memo[mk] = resultat
    return resultat or nil
end

-- Nom de creature par son nom anglais (index NC ; homonymes aux francais differents : nil).
function A.NomCreature(nomEN)
    if type(nomEN) ~= "string" or nomEN == "" then return nil end
    local nc = A.TableDe("creatures", "NC")
    if not nc then return nil end
    local cle, h2 = A.Cle(nomEN)
    local v = nc:ParCle(cle, h2)
    if v and v ~= "" then return v end
    return nil
end

-- Numero de creature tire du GUID 3.3.5 : 0xF130 EEEEEE SSSSSS (EEEEEE = numero, en hexadecimal).
function A.IdCreatureDepuisGUID(guid)
    if type(guid) ~= "string" then return nil end
    local genre = sub(guid, 3, 6)
    if genre == "F130" or genre == "F530" or genre == "F150" then
        local id = tonumber(sub(guid, 7, 12), 16)
        if id and id > 0 then return id end
    end
    return nil
end

function A.IdDepuisLien(lien, quoi)
    if type(lien) ~= "string" then return nil end
    return tonumber(match(lien, quoi .. ":(%d+)"))
end

function A.Message(texte)
    if DEFAULT_CHAT_FRAME then
        DEFAULT_CHAT_FRAME:AddMessage("|cff3399ffAzeroth_FR|r : " .. tostring(texte))
    end
end

-- ----------------------------------------------------------------------------
-- Demarrage : lecture du joueur et chargement des familles « auto » pendant l'ecran
-- de chargement ; les add-ons mis en attente pendant un combat sont charges apres.
-- ----------------------------------------------------------------------------
local demarrage = CreateFrame("Frame")
demarrage:RegisterEvent("PLAYER_LOGIN")
demarrage:RegisterEvent("PLAYER_REGEN_ENABLED")
demarrage:SetScript("OnEvent", A.Proteger("demarrage", function(self, evenement)
    if evenement == "PLAYER_LOGIN" then
        if type(AzerothFR_Reglages) ~= "table" then AzerothFR_Reglages = {} end
        A.LireJoueur()
        local avant = collectgarbage("count")
        for _, f in ipairs(A.FAMILLES or {}) do
            if f.auto then A.ChargerAddon(f.addon) end
        end
        A.MemoireAuDemarrage = collectgarbage("count") - avant
    elseif evenement == "PLAYER_REGEN_ENABLED" then
        for addon in pairs(A.EnAttente) do
            A.EnAttente[addon] = nil
            A.ChargerAddon(addon)
        end
    end
end))
