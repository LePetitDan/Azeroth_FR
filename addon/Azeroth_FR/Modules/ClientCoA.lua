-- ============================================================================
-- Azeroth_FR : textes propres au client CoA (version 0.9, 07/11/2026). Affichage seulement.
-- Donnees : famille « client » (Azeroth_FR_Client) : XT (texte anglais -> francais), XG (gabarits a nombres),
-- EM (gabarits d'emotes a noms). Branchements verifies contre le code que le client CoA charge vraiment :
--   - tutoriels (Ascension_PathToAscension, PathObjectiveDisplayMixin.lua) : SetTutorial(id) lit
--     C_Tutorial.GetTutorialDisplay, coupe la description aux « {page} » (SplitPages) puis l'affiche
--     (RefreshDisplay -> FormatDescription, des SimpleHTML sans GetText) : apres l'appel, la description est
--     remplacee par son francais (meme {T:image} et memes {page}, verifie a la fabrication) et la page reaffichee ;
--   - bulles des mots-cles (SharedXML/KeywordTooltip.lua) : KeywordTooltipMixin:SetKeyword(keyword) lit
--     C_Tutorial.GetKeywordInfo ; les bulles sont des cadres d'une reserve (CreateFramePool) crees a la demande avec
--     ce mixin : le crochet est pose sur le mixin avant la premiere bulle ; apres l'appel, titre et texte en francais
--     (on refait la mise en page comme OnHide : reserves videes, hauteur 58) ;
--   - fenetres CoA (Epreuves ChallengesFrame, Chemin de l'Ascension PathToAscensionFrame, Collections…) et
--     fenetres Blizzard nourries par des tables du client (recherche de groupe, calendrier, champs de bataille,
--     salon de coiffure, titres) ou par des noms deja traduits (reputation, competences, trajets aeriens, amis et
--     guilde, sauvegardes d'instance, metiers) : tant qu'elles sont visibles, leurs zones de texte (FontString) sont
--     relues toutes les 0,4 s ; une zone dont le texte est EXACTEMENT un texte connu (ou un gabarit a nombres), ou
--     EXACTEMENT un nom du domaine de la fenetre, recoit son francais ;
--   - emotes (CHAT_MSG_TEXT_EMOTE, texte compose par le client depuis EmotesTextData.dbc) : filtre de messages ;
--   - infobulles simples : chaque ligne est cherchee telle quelle (description d'une regle d'Epreuve, d'un jeton…).
-- Rien n'est ecrit dans les tables du jeu : seulement des crochets (hooksecurefunc, HookScript) et SetText.
-- ============================================================================
local A = AzerothFR
local P = A.Proteger
local find, sub, gsub, match, format, tonumber = string.find, string.sub, string.gsub, string.match, string.format, tonumber

-- ----------------------------------------------------------------------------
-- Recherche : texte exact (XT), puis gabarit a nombres (XG)
-- ----------------------------------------------------------------------------
-- Les nombres d'un texte, dans l'ordre, et le texte ou chaque nombre devient \2 (comme gabarit_nombres()).
local function Nombres(s)
    local vals, out, pos = {}, {}, 1
    while true do
        local d, f = find(s, "%d+", pos)
        if not d then break end
        local d2, f2 = find(s, "^[%.,]%d+", f + 1)
        if d2 then f = f2 end
        out[#out + 1] = sub(s, pos, d - 1)
        out[#out + 1] = "\2"
        vals[#vals + 1] = sub(s, d, f)
        pos = f + 1
    end
    out[#out + 1] = sub(s, pos)
    return table.concat(out), vals
end

local function ParGabarit(texte)
    if not find(texte, "%d") then return nil end
    local xg = A.TableDe("client", "XG")
    if not xg then return nil end
    local squelette, vals = Nombres(A.Canon(texte))
    local g = xg:ParTexte(squelette)
    if type(g) ~= "table" or type(g[1]) ~= "table" or type(g[2]) ~= "table" or #g[1] ~= #vals then return nil end
    local args = {}
    for i, place in ipairs(g[1]) do
        if place[1] == "l" then
            if place[2] ~= vals[i] then return nil end          -- nombre ecrit en dur : doit etre le meme
        else
            args[place[2]] = vals[i]
        end
    end
    local out = {}
    for _, m in ipairs(g[2]) do
        if type(m) == "table" then
            if not args[m[2]] then return nil end
            out[#out + 1] = args[m[2]]
        else
            out[#out + 1] = m
        end
    end
    return table.concat(out)
end

function A.TexteClient(texte)
    if type(texte) ~= "string" or texte == "" then return nil end
    local xt = A.TableDe("client", "XT")
    local fr = xt and A.Traduire(xt, texte)
    if fr then return fr end
    return ParGabarit(texte)
end

-- Une zone de texte : son francais si son texte entier est connu (textes du client), ou si c'est EXACTEMENT un nom
-- connu d'un des domaines donnes (zones, factions, competences…), espaces de bord gardes.
local function NomConnu(t, domaines)
    if not domaines then return nil end
    local avant, coeur, apres = match(t, "^(%s*)(.-)(%s*)$")
    if not coeur or coeur == "" or #coeur > 120 then return nil end
    for i = 1, #domaines do
        local d = domaines[i]
        local fr
        if d == "sort" then
            fr = A.NomSortParNom and A.NomSortParNom(coeur)
        else
            fr = A.Nom(d, coeur)
        end
        if fr and fr ~= coeur then return avant .. fr .. apres end
    end
    return nil
end

local function Zone(zone, domaines)
    if not zone or type(zone.GetText) ~= "function" then return false end
    local t = zone:GetText()
    if not t or t == "" or A.DejaEcrit(zone, t) then return false end
    local fr = A.TexteClient(t)
    if fr then
        -- la recherche se fait sur la forme canonique (bords ôtés) : on remet les espaces de bord de l'affichage
        local avant, apres = match(t, "^([ \t]*)"), match(t, "([ \t]*)$")
        if avant ~= "" and sub(fr, 1, #avant) ~= avant then fr = avant .. fr end
        if apres ~= "" and apres ~= t and sub(fr, -#apres) ~= apres then fr = fr .. apres end
    else
        fr = NomConnu(t, domaines)
    end
    if fr and fr ~= t then
        A.Ecrire(zone, fr)
        return true
    end
    return false
end
A.ZoneClient = Zone

-- ----------------------------------------------------------------------------
-- Balayage des fenetres visibles : { nom du cadre, domaines de noms essayes apres les textes du client }
-- ----------------------------------------------------------------------------
local LIEUX = { "zone", "donjon" }
local PERSONNES = { "zone", "classe", "race" }
local RACINES = {
    -- CoA
    { "ChallengesFrame" }, { "PathToAscensionFrame" }, { "Collections" }, { "ManastormObjectiveTracker" },
    { "MythicPlusObjectiveTracker" }, { "SocketKeystoneFrame" }, { "DraftHelpFrame" }, { "HelpMenuFrame" },
    -- Blizzard, nourries par les tables du client ou par des noms deja traduits
    { "LFDParentFrame", LIEUX }, { "LFRParentFrame", LIEUX }, { "PVPBattlegroundFrame", LIEUX }, { "BattlefieldFrame", LIEUX },
    { "CalendarFrame", { "fete" } }, { "CalendarViewHolidayFrame", { "fete" } }, { "WorldStateAlwaysUpFrame" },
    { "WorldStateScoreFrame", LIEUX }, { "BarberShopFrame", { "coiffure" } }, { "PlayerTitlePickerFrame", { "titre" } },
    { "PlayerTitleFrame", { "titre" } }, { "PetPaperDollFrame", { "type_creature" } }, { "TokenFrame", { "competence" } },
    -- 0.9 : fenetres du § 1 de l'inventaire dont les textes sont des noms deja traduits
    { "ReputationFrame", { "faction" } }, { "ReputationDetailFrame", { "faction" } }, { "SkillFrame", { "competence" } },
    { "TaxiFrame", LIEUX }, { "FriendsFrame", PERSONNES }, { "WhoFrame", PERSONNES }, { "GuildFrame", PERSONNES },
    { "RaidInfoFrame", LIEUX }, { "TradeSkillFrame", { "competence", "sort" } }, { "CraftFrame", { "competence", "sort" } },
}
local LIMITE = 4000           -- zones de texte lues au plus par passe et par fenetre

local function Parcourir(cadre, budget, profondeur, domaines)
    if budget.n <= 0 or profondeur > 14 or not cadre or type(cadre.IsVisible) ~= "function" or not cadre:IsVisible() then
        return
    end
    if type(cadre.GetRegions) == "function" then
        local regions = { cadre:GetRegions() }
        for i = 1, #regions do
            local r = regions[i]
            if r and r.GetObjectType and r:GetObjectType() == "FontString" and r:IsVisible() then
                budget.n = budget.n - 1
                Zone(r, domaines)
            end
        end
    end
    if type(cadre.GetChildren) == "function" then
        local enfants = { cadre:GetChildren() }
        for i = 1, #enfants do Parcourir(enfants[i], budget, profondeur + 1, domaines) end
    end
end

function A.BalayerFenetre(cadre, domaines)
    if not A.ModuleActif("client") or not cadre then return end
    Parcourir(cadre, { n = LIMITE }, 0, domaines)
end

local veille = CreateFrame("Frame")
local ecoule = 0
veille:SetScript("OnUpdate", P("ClientCoA.veille", function(self, dt)
    ecoule = ecoule + (dt or 0)
    if ecoule < 0.4 then return end
    ecoule = 0
    if not A.ModuleActif("client") then return end
    for i = 1, #RACINES do
        local c = _G[RACINES[i][1]]
        if c and type(c.IsVisible) == "function" and c:IsVisible() then A.BalayerFenetre(c, RACINES[i][2]) end
    end
end, true))

-- ----------------------------------------------------------------------------
-- Tutoriels du Chemin de l'Ascension
-- ----------------------------------------------------------------------------
local function ApresTutoriel(self)
    if not A.ModuleActif("client") or type(self) ~= "table" or type(self.description) ~= "string" then return end
    local fr = A.TexteClient(self.description)
    if not fr or fr == self.description or type(self.SplitPages) ~= "function" then return end
    local page = self.page or 1
    self.description = fr
    self.pages = self:SplitPages(fr)
    if type(self.pages) ~= "table" or #self.pages == 0 then return end
    if page > #self.pages then page = #self.pages end
    self.page = page
    if type(self.RefreshDisplay) == "function" then self:RefreshDisplay() end
end

local tutoriel_branche = false
local function BrancherTutoriels()
    if tutoriel_branche then return end
    local d = PathToAscensionFrame and PathToAscensionFrame.Display
    if type(d) == "table" and type(d.SetTutorial) == "function" then
        hooksecurefunc(d, "SetTutorial", P("PathObjectiveDisplay.SetTutorial", ApresTutoriel))
        tutoriel_branche = true
    end
end

-- ----------------------------------------------------------------------------
-- Bulles des mots-cles
-- ----------------------------------------------------------------------------
local function ApresMotCle(self)
    if not A.ModuleActif("client") or type(self) ~= "table" then return end
    if self.Title then Zone(self.Title) end
    if type(C_Tutorial) ~= "table" or type(C_Tutorial.GetKeywordInfo) ~= "function" or not self.keyword then return end
    local ok, _, texte = pcall(C_Tutorial.GetKeywordInfo, self.keyword)
    if not ok or type(texte) ~= "string" then return end
    local fr = A.TexteClient(texte)
    if not fr or fr == texte or type(self.FormatLine) ~= "function" or not self.TextPool or not self.ImagePool then return end
    self.TextPool:ReleaseAll()
    self.ImagePool:ReleaseAll()
    self:SetHeight(58)
    self:FormatLine(fr)
end

local motcle_branche = false
local function BrancherMotsCles()
    if motcle_branche then return end
    if type(KeywordTooltipMixin) == "table" and type(KeywordTooltipMixin.SetKeyword) == "function" then
        hooksecurefunc(KeywordTooltipMixin, "SetKeyword", P("KeywordTooltip.SetKeyword", ApresMotCle))
        motcle_branche = true
    end
end

-- ----------------------------------------------------------------------------
-- Emotes
-- ----------------------------------------------------------------------------
local gabarits_emotes
local function Emotes()
    if gabarits_emotes then return gabarits_emotes end
    local em = A.TableDe("client", "EM")
    if not em then return nil end
    gabarits_emotes = {}
    local i = 1
    while true do
        local g = em:ParId(i)
        if type(g) ~= "table" then break end
        gabarits_emotes[#gabarits_emotes + 1] = g
        i = i + 1
    end
    return gabarits_emotes
end

function A.TraduireEmote(message)
    if type(message) ~= "string" or message == "" then return nil end
    local xt = A.TableDe("client", "XT")
    local fr = xt and A.Traduire(xt, message)          -- « You agree. »
    if fr then return fr end
    for _, g in ipairs(Emotes() or {}) do
        local a, b = match(message, g[1])
        if a then
            local n = 0
            local r = gsub(g[2], "%%s", function()
                n = n + 1
                return n == 1 and a or (b or "")
            end)
            return r
        end
    end
    return nil
end

local function FiltreEmote(_, _, message, ...)
    if not A.ModuleActif("client") then return false end
    local ok, fr = pcall(A.TraduireEmote, message)
    if ok and fr and fr ~= message then return false, fr, ... end
    return false
end
if type(ChatFrame_AddMessageEventFilter) == "function" then
    ChatFrame_AddMessageEventFilter("CHAT_MSG_TEXT_EMOTE", FiltreEmote)
end

-- ----------------------------------------------------------------------------
-- Infobulles simples (sans unite, objet ni sort) : chaque ligne, telle quelle
-- ----------------------------------------------------------------------------
local function SurBulle(bulle)
    if not A.ModuleActif("client") or not bulle or not bulle.NumLines then return end
    if bulle.GetUnit and bulle:GetUnit() then return end
    if bulle.GetItem and bulle:GetItem() then return end
    if bulle.GetSpell and bulle:GetSpell() then return end
    local nom = bulle:GetName()
    if not nom then return end
    for i = 1, bulle:NumLines() do
        Zone(_G[nom .. "TextLeft" .. i])
        Zone(_G[nom .. "TextRight" .. i])
    end
end
if GameTooltip and GameTooltip.HookScript then
    GameTooltip:HookScript("OnShow", P("ClientCoA.GameTooltip.OnShow", SurBulle))
end

-- ----------------------------------------------------------------------------
-- Branchements : maintenant, puis a chaque add-on charge (fenetres chargees a la demande)
-- ----------------------------------------------------------------------------
local ev = CreateFrame("Frame")
ev:RegisterEvent("ADDON_LOADED")
ev:RegisterEvent("PLAYER_LOGIN")
ev:SetScript("OnEvent", P("ClientCoA.OnEvent", function()
    BrancherMotsCles()
    BrancherTutoriels()
end, true))
BrancherMotsCles()
BrancherTutoriels()
