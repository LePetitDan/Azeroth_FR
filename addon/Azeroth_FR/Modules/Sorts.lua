-- ============================================================================
-- Azeroth_FR : sorts (0.9.4 : sorts cites sous un sort, balises @s ; version 0.5 : lieu $z de la pierre de foyer retrouve sans GetBindLocation ; 0.4 : barre d'incantation ;
-- rangs de tous les sorts, lignes de puissance PvE/PvP). Nom, rang et description en francais, A L'AFFICHAGE
-- SEULEMENT, par le VRAI numero du sort (analyse du 03/11/2026, test 3 confirme en jeu) :
--   - infobulle de sort      : 3e valeur de GameTooltip:GetSpell()      (OnTooltipSetSpell)
--   - barre d'action         : 4e valeur de GetActionInfo(case)          (GameTooltip:SetAction)
--   - grimoire               : GetSpellLink(case, livre) -> « spell:N »  (GameTooltip:SetSpell, noms)
--   - auras (buffs, debuffs) : 11e valeur de UnitAura                    (GameTooltip:SetUnitAura…)
--   - lignes « Use: » / « Equip: » des objets : le sort de l'objet (GetItemSpell, s'il rend un
--     numero), sinon le sort dont le texte anglais a la meme forme (index par « squelette »).
-- GetSpellInfo continue de repondre en anglais : aucune fonction du jeu n'est remplacee.
-- Seules les lignes officiel / machine / relu de la source sont embarquees.
--
-- LES NOMBRES : le client calcule lui-meme les nombres de la description ($s1 degats, $d
-- duree…). Comme l'ancien AscensionFR, on aligne le modele anglais sur l'infobulle affichee
-- pour recuperer ces nombres, puis on les replace dans le modele francais :
--   modele EN  : "Shock an enemy for $s1 Nature damage over $d."
--   affiche EN : "Shock an enemy for 15 Nature damage over 6 sec."   -> $s1 = 15, $d = 6 sec
--   modele FR  : "Choque un ennemi et inflige $s1 points de dégâts de Nature en $d."
--   resultat   : "Choque un ennemi et inflige 15 points de dégâts de Nature en 6 sec."
-- Si l'alignement echoue, l'anglais reste : jamais un « $s1 » visible.
-- ============================================================================
local A = AzerothFR
local find, gsub, sub, match, gmatch, lower, len, format = string.find, string.gsub, string.sub, string.match,
    string.gmatch, string.lower, string.len, string.format
local P = A.Proteger

-- ----------------------------------------------------------------------------
-- Formes « plate » et « squelette » : IDENTIQUES a plat() et squelette() de outils/fabriquer.py
-- ----------------------------------------------------------------------------
local function SansCouleurs(t)
    t = gsub(t, "|c%x%x%x%x%x%x%x%x", "")
    return (gsub(t, "|r", ""))
end
A.SansCouleurs = SansCouleurs

function A.Plat(t)
    t = gsub(SansCouleurs(t), "%s+", " ")
    return (match(t, "^ *(.-) *$"))
end

local UNITES_SQ = { "seconds", "second", "secs", "sec", "minutes", "minute", "mins", "min", "hours", "hour",
    "hrs", "hr", "days", "day" }
function A.Squelette(t)
    t = SansCouleurs(t)
    t = gsub(t, "%d+", "#")
    repeat
        local avant = t
        t = gsub(t, "#[%.,]#", "#")
    until t == avant
    t = gsub(t, "#%s+to%s+#", "#")
    for _, u in ipairs(UNITES_SQ) do t = gsub(t, "#%s*" .. u .. "%f[%A]", "#") end
    t = gsub(t, "%s+", " ")
    return (match(t, "^ *(.-) *$"))
end

-- ----------------------------------------------------------------------------
-- Moteur d'alignement (repris de l'ancien AscensionFR, Modules/Sorts.lua, et resserre)
-- ----------------------------------------------------------------------------
local MOTIFS_VARIABLE = {
    "%$%b{}",                       -- ${ calcul }
    "%$%?[^%[]*%b[]%b[]",           -- $?condition[oui][non]
    "%$%?[^%[]*%b[]",               -- $?condition[texte]
    "%$[/%*%+%-]%d+;%d*%a%d*",      -- $/1000;s1 $*15;s1 (operations)
    "%$[GgLl][^;]*;",               -- $gm:f;  $lseconde:secondes;
    "%$@%a+%d*",                    -- $@spellname123
    "%$<%a+>",                      -- $<percent> (variable nommee)
    "%$%d+%a%d*",                   -- $64843s2 (valeur d'un autre sort)
    "%$%a%d*",                      -- $s1 $d $h $u $t $o $q $a $x $e $z…
    "%$%d+",                        -- $1
    -- marquage d'Ascension, resolu par le client avant l'affichage : traite comme une variable
    "@ifknown:.-:ifknown@", "@ifnotknown:.-:ifnotknown@", "@wflocation:[^@]*@",
    "@%a+:%d+:%-?%d+@", "@%a+:%d+:%a+@", "@%a+:%d+:?@", "@ext:", ":ext@",
}

local function Echapper(t) return (gsub(t, "([%^%$%(%)%%%.%[%]%*%+%-%?])", "%%%1")) end

-- Litteral avec espaces de tete et de queue souples ; un separateur tout blanc reste exige. 0.4 : les suites
-- d'espaces INTERIEURES sont souples aussi (« $z.  Speak to an Innkeeper » : double espace du DBC, que le
-- client peut afficher simple).
local function Souple(litteral)
    if litteral == "" then return "" end
    if find(litteral, "^%s*$") then return "%s+" end
    local coeur = match(litteral, "^%s*(.-)%s*$")
    local motif = gsub(Echapper(coeur), "%s+", "%%s+")
    if find(litteral, "^%s") then motif = "%s*" .. motif end
    if find(litteral, "%s$") then motif = motif .. "%s*" end
    return motif
end

local function ProchaineVariable(modele, position)
    local md, mf
    for _, motif in ipairs(MOTIFS_VARIABLE) do
        local d, f = find(modele, motif, position)
        if d and (not md or d < md or (d == md and f > mf)) then md, mf = d, f end
    end
    return md, mf
end

local function Decouper(modele)
    local litteraux, variables, position = {}, {}, 1
    while true do
        local d, f = ProchaineVariable(modele, position)
        if not d then break end
        litteraux[#litteraux + 1] = sub(modele, position, d - 1)
        variables[#variables + 1] = sub(modele, d, f)
        position = f + 1
    end
    litteraux[#litteraux + 1] = sub(modele, position)
    return litteraux, variables
end
A.DecouperModele = Decouper

local function PrefixeConditionnel(v) return match(v, "^(%$%?[^%[]*)%[") end
local function EstMarqueur(v) return sub(v, 1, 1) == "@" or v == ":ext@" end
-- 0.9.5 (audit des sorts) : BALISE pure du client (bornes @ext: et :ext@, @s:N:0@, @req:N:@) : le client la retire,
-- il n'en reste rien (au plus un blanc) ; sa capture « (.-) » prenait la phrase d'une conditionnelle voisine
-- (« …$s2%.$?s560595[ Your critical…][]\r\n\r\n@ext:Only 1… » : la conditionnelle vide, l'anglais dans @ext:)
local function EstBalise(v) return v == "@ext:" or v == ":ext@" or match(v, "^@%a+:[%d:%-]*@$") ~= nil end

-- Capture typee (repli) : un nombre pour une valeur, un nombre et son unite pour une duree.
local function CaptureTypee(v)
    if EstBalise(v) then return "(%s*)" end
    -- conditionnelle dont les crochets n'ont que des balises (« $?s804286[@s:806252:0@][] ») : rien d'affiche non plus
    local pre = match(v, "^(%$%?[^%[]*)%[")
    if pre and gsub(gsub(sub(v, #pre + 1), "@%a+:[%d:%-]*@", ""), "[%s%[%]]", "") == "" then return "(%s*)" end
    -- 0.9.5 (audit des sorts) : un nombre ne finit plus par une virgule (« plus 15, stunning… » : la virgule allait
    -- dans le nombre et manquait a la conditionnelle qui suit) ; decimales « 1.5 » gardees
    if match(v, "^%$%d*[dD]%d*$") then return "(%-?%d+%.?%d*%s*%a*)" end
    -- ($z : le lieu de la pierre de foyer, un texte : pas de capture typee)
    if match(v, "^%$[suohtqaxeSUOHTQAXE]%d*$") or match(v, "^%$%d+%a%d*$") or match(v, "^%$%b{}$")
        or match(v, "^%$<%a+>$") or match(v, "^%$[/%*%+%-]") then
        return "(%-?%d+%.?%d*)"
    end
    return "(.-)"
end

-- mode « typee » (0.9.5) : captures typees seulement (nombres, durees) ; « souple » : (.-) puis typees ; nil : souple
local function Extraire(modele, affiche, mode)
    local litteraux, variables = Decouper(modele)
    if #variables == 0 then return {} end
    local function essayer(motif)
        local caps = { match(affiche, motif) }
        if #caps ~= #variables then return nil end
        local valeurs, rangs = {}, {}
        for i, v in ipairs(variables) do
            local val = caps[i]
            if val == nil then return nil end
            if EstMarqueur(v) then
                rangs[v] = rangs[v] or {}
                rangs[v][#rangs[v] + 1] = val
                if valeurs[v] == nil then valeurs[v] = val end
            else
                if valeurs[v] and valeurs[v] ~= val then return nil end   -- meme variable, deux valeurs
                -- 0.9.5 (audit, « Disengage » de Witch Hunter) : une valeur NUMERIQUE ou une duree ne prend pas une
                -- phrase entiere (« $d. » avalait les conditionnelles collees qui suivent) : courte, un chiffre, une ligne
                local ct = CaptureTypee(v)
                if ct ~= "(.-)" and ct ~= "(%s*)" and (#val > 24 or find(val, "\n") or not find(val, "%d")) then
                    return nil
                end
                valeurs[v] = val
            end
        end
        return caps, valeurs, rangs
    end
    local motif, typee, differe = "^", "^", false
    for i, l in ipairs(litteraux) do
        local sl = Souple(l)
        -- 0.9.5 (audit des sorts) : un separateur tout blanc en FIN de modele (« …effects.:ext@ ») ou contre une
        -- balise (@ext:, :ext@, @s:…@, que le client retire) peut disparaitre a l'affichage : facultatif
        if sl == "%s+" and (i == #litteraux or (variables[i] and EstMarqueur(variables[i]))
            or (i > 1 and EstMarqueur(variables[i - 1]))) then
            sl = "%s*"
        end
        motif = motif .. sl
        typee = typee .. sl
        if i <= #variables then
            motif = motif .. (CaptureTypee(variables[i]) == "(%s*)" and "(%s*)" or "(.-)")
            local c = CaptureTypee(variables[i])
            typee = typee .. c
            if c ~= "(.-)" then differe = true end
        end
    end
    local caps, valeurs, rangs
    if mode == "typee" then
        if not differe then return nil end
        caps, valeurs, rangs = essayer(typee .. "$")
    else
        caps, valeurs, rangs = essayer(motif .. "$")
        if not caps and differe then caps, valeurs, rangs = essayer(typee .. "$") end
    end
    if not caps then return nil end
    local conds, ordre = {}, {}
    for i, v in ipairs(variables) do
        local pre = PrefixeConditionnel(v)
        if pre then
            -- 0.9.5 (essai 8, « Loa's Brew ») : une meme condition peut revenir dans plusieurs conditionnelles
            -- (« health$?s705848[ and …][].$?s705848[@ext…][] ») : chaque occurrence est gardee, dans l'ordre ; le
            -- francais les reprend dans le meme ordre (occ). Ambigu seulement si deux occurrences de la MEME
            -- conditionnelle ont donne deux textes differents.
            local e = conds[pre]
            if not e then e = { valeur = caps[i], var = v, occ = {} }; conds[pre] = e end
            e.occ[#e.occ + 1] = { valeur = caps[i], var = v }
            if e.var == v and e.valeur ~= caps[i] then e.ambigu = true end
        end
        if match(v, "^%$[GgLl]") then ordre[#ordre + 1] = v end
    end
    return valeurs, conds, ordre, rangs
end

local function OptionsGL(v)
    local corps = match(v, "^%$[GgLl](.*);$")
    if not corps then return nil end
    local out = {}
    for m in gmatch(corps, "[^:]+") do out[#out + 1] = m end
    return out
end

local function Crochet(v, rang)
    local n = 0
    for bloc in gmatch(v, "%b[]") do
        n = n + 1
        if n == rang then return sub(bloc, 2, -2) end
    end
end

-- Le client anglais ecrit ses unites et ses plages : on les francise dans la VALEUR seulement.
local UNITES = { hour = "heure", hours = "heures", day = "jour", days = "jours", yard = "mètre",
    yards = "mètres", min = "min", mins = "min", minute = "minute", minutes = "minutes", sec = "sec",
    secs = "sec", second = "seconde", seconds = "secondes", hr = "h", hrs = "h" }
local function Unites(v)
    v = gsub(v, "(%d)%s+to%s+(%d)", "%1 à %2")
    return (gsub(v, "(%d)(%s+)(%a+)", function(n, e, mot) return n .. e .. (UNITES[lower(mot)] or mot) end))
end

local TexteSort

-- Nombre de conditionnelles de prefixe pre dans un modele (0.9.5)
local function NbConds(modele, pre)
    local _, vars = Decouper(modele)
    local n = 0
    for _, v in ipairs(vars) do if PrefixeConditionnel(SansCouleurs(v)) == pre then n = n + 1 end end
    return n
end

local function Appliquer(modele_fr, valeurs, conds, ordre, rangs)
    local litteraux, variables = Decouper(modele_fr)
    local rang_c = {}
    local nb_gl, nb_t, en_t, rang_t = 0, {}, {}, {}
    for _, v in ipairs(variables) do
        local nue = SansCouleurs(v)
        if match(nue, "^%$[GgLl]") then
            nb_gl = nb_gl + 1
            local t = lower(sub(nue, 2, 2))
            nb_t[t] = (nb_t[t] or 0) + 1
        end
    end
    -- 0.9.5 (audit des sorts, « Conjure Water » : $lbottle:bottles; et $ghis:her; en anglais, $l seul en francais
    -- officiel) : a defaut du meme nombre de $l/$g, appariement par SORTE ($l avec $l, $g avec $g), dans l'ordre
    for _, ven in ipairs(ordre) do
        local t = lower(sub(ven, 2, 2))
        en_t[t] = en_t[t] or {}
        en_t[t][#en_t[t] + 1] = ven
    end
    local rang_gl, rang_m, out = 0, {}, {}
    for i, l in ipairs(litteraux) do
        out[#out + 1] = l
        local v = variables[i]
        if v then
            local nue = SansCouleurs(v)
            local val = valeurs[nue]
            if rangs and rangs[nue] then
                local n = (rang_m[nue] or 0) + 1
                rang_m[nue] = n
                val = rangs[nue][n] or valeurs[nue]
            end
            -- $l / $g : options traduites -> appariement par rang, option au meme indice
            if match(nue, "^%$[GgLl]") then
                rang_gl = rang_gl + 1
                local t = lower(sub(nue, 2, 2))
                rang_t[t] = (rang_t[t] or 0) + 1
                local ven
                if #ordre == nb_gl then
                    ven = ordre[rang_gl]
                    if ven and lower(sub(ven, 2, 2)) ~= t then ven = nil end
                end
                if not ven and en_t[t] and #en_t[t] == nb_t[t] then ven = en_t[t][rang_t[t]] end
                if val == nil then
                    if ven then
                        local aff, oen, ofr = valeurs[ven], OptionsGL(ven), OptionsGL(nue)
                        if aff and oen and ofr and #oen == #ofr then
                            local choix, ambigu
                            for k = 1, #oen do
                                if oen[k] == aff then
                                    if choix ~= nil and choix ~= ofr[k] then ambigu = true end
                                    choix = ofr[k]
                                end
                            end
                            if not ambigu then val = choix end
                        end
                    end
                end
            end
            -- 0.9.5 (audit, « Invoque $s1 $lgâteau de manne:gâteaux de manne; ») : $l du francais SEUL : selon le
            -- dernier nombre deja ecrit (1 ou 0 : singulier)
            if val == nil and match(nue, "^%$[Ll]") and not en_t.l then
                local o = OptionsGL(nue)
                if o and #o == 2 then
                    local n
                    for x in gmatch(table.concat(out), "%d+[%.,]?%d*") do n = x end
                    if n then val = (tonumber((gsub(n, ",", "."))) or 2) < 2 and o[1] or o[2] end
                end
            end
            -- 0.9.5 : $g du francais SEUL (accord ajoute par la traduction : « $genragé:enragée; ») : selon le joueur
            if val == nil and match(nue, "^%$[Gg]") and not en_t.g then
                local o = OptionsGL(nue)
                if o and #o == 2 then
                    val = (A.Joueur and A.Joueur.genre == "f") and o[2] or o[1]
                end
            end
            -- 0.9.5 (audit des sorts, « @ifknown:704997:|cffffffffFrappe infernale|r … :ifknown@ ») : bloc « si le
            -- sort N est connu » ; son texte traduit ne retrouve pas la cle anglaise : par la sorte et le numero
            if val == nil then
                local sorte, num, corps = match(v, "^@(if%a*known):(%d+):(.*):if%a*known@$")
                if sorte then
                    local tete = "@" .. sorte .. ":" .. num .. ":"
                    for ke, ve in pairs(valeurs) do
                        if sub(ke, 1, #tete) == tete then
                            local corps_en = match(ke, "^@if%a*known:%d+:(.*):if%a*known@$")
                            if ve == "" then val = ""
                            elseif corps_en and A.Plat(ve) == A.Plat(corps_en) then val = corps
                            elseif corps_en then val = TexteSort(corps, corps_en, ve) end
                            break
                        end
                    end
                end
            end
            -- conditionnelle : texte des crochets traduit -> par le prefixe, puis recursion
            if val == nil then
                local pre = PrefixeConditionnel(nue)
                local c = pre and conds[pre]
                if c and c.occ and #c.occ > 1 then
                    -- occurrences dans l'ordre (meme nombre en francais qu'en anglais : sinon, seulement si toutes
                    -- les occurrences anglaises sont vides)
                    rang_c[pre] = (rang_c[pre] or 0) + 1
                    local o = c.occ[rang_c[pre]]
                    local vides = true
                    for _, x in ipairs(c.occ) do if x.valeur ~= "" then vides = false end end
                    if vides then c = { valeur = "" }
                    elseif o and NbConds(modele_fr, pre) == #c.occ then c = { valeur = o.valeur, var = o.var }
                    else c = nil end
                end
                if c and not c.ambigu then
                    if c.valeur == "" then
                        val = ""
                    else
                        for r = 1, 2 do
                            local be, bf = Crochet(c.var, r), Crochet(nue, r)
                            if be and bf then
                                val = TexteSort(bf, be, c.valeur)
                                if val then break end
                            end
                        end
                    end
                end
            end
            if val == nil then return nil end
            -- $z : le lieu de la pierre de foyer (« Northshire Abbey ») -> nom de zone francais
            if match(nue, "^%$%d*[zZ]$") and A.NomZone then val = A.NomZone(val) or val end
            out[#out + 1] = Unites(val)
        end
    end
    return table.concat(out)
end

-- Repli : seuls les NOMBRES different (le client les a recalcules pour ce personnage).
local function RemplacerNombres(texte, vers)
    local c, t = {}, {}
    texte = gsub(texte, "|c%x%x%x%x%x%x%x%x", function(x) c[#c + 1] = x; return "\1" end)
    texte = gsub(texte, "|T.-|t", function(x) t[#t + 1] = x; return "\2" end)
    texte = gsub(texte, "%d+", function(n) return vers[n] or n end)
    local i, j = 0, 0
    texte = gsub(texte, "\1", function() i = i + 1; return c[i] end)
    return (gsub(texte, "\2", function() j = j + 1; return t[j] end))
end

-- Litteral dont chaque suite d'espaces devient « %s+ » (le client seme parfois une espace de plus).
local function LitteralSouple(s)
    local out, pos = "", 1
    while true do
        local d, f = find(s, "%s+", pos)
        if not d then break end
        out = out .. Echapper(sub(s, pos, d - 1)) .. "%s+"
        pos = f + 1
    end
    return out .. Echapper(sub(s, pos))
end

local function MotifNombres(modele)
    local motif, position = "^", 1
    local lit = LitteralSouple
    while true do
        local d, f = find(modele, "%d+", position)
        if not d then break end
        motif = motif .. lit(sub(modele, position, d - 1)) .. "(%d+)"
        position = f + 1
    end
    return motif .. lit(sub(modele, position)) .. "$"
end

local function AlignerNombres(fr, en, affiche)
    local attendus = {}
    for n in gmatch(en, "%d+") do attendus[#attendus + 1] = n end
    if #attendus == 0 then return nil end
    local trouves = { match(affiche, MotifNombres(en)) }
    if #trouves ~= #attendus then return nil end
    local vers = {}
    for i, a in ipairs(attendus) do
        if vers[a] and vers[a] ~= trouves[i] then return nil end
        vers[a] = trouves[i]
    end
    return RemplacerNombres(fr, vers)
end

local INDICE_MAJ = "Hold SHIFT for more information"
-- 0.9.5 : phrase ecrite par le client lui-meme (absente de GlobalStrings) ; « MAJ » comme SHIFT_KEY officiel
-- (« Touche MAJ »)
local INDICE_MAJ_FR = "Maintenez MAJ pour plus d'informations"

-- Traduit un texte de sort affiche. en : le modele anglais (texte), ou l'empreinte de sa forme
-- plate (nombre) quand il n'a ni variable ni nombre. Renvoie le francais, ou nil.
local TexteSortSimple
TexteSortSimple = function(fr, en, affiche)
    if type(fr) ~= "string" or type(affiche) ~= "string" or affiche == "" then return nil end
    if type(en) == "number" then
        if A.H1(A.Plat(affiche)) ~= en then return nil end
        if not find(fr, "%$") then return fr end
        -- 0.9.5 : anglais sans variable, francais accorde au joueur (« $gProtégé:Protégée; contre les effets… »)
        local femme = A.Joueur and A.Joueur.genre == "f"
        local f2 = gsub(fr, "%$[Gg]([^:;]*):([^;]*);", function(m, f) return femme and f or m end)
        if not find(f2, "%$") then return f2 end
        return nil
    end
    if type(en) ~= "string" then return nil end
    local indice = ""
    if find(affiche, INDICE_MAJ, 1, true) and find(en, "@ext:", 1, true) then
        en = gsub(gsub(en, "%s*@ext:.-:ext@", ""), "%s+$", "")
        fr = gsub(gsub(fr, "%s*@ext:.-:ext@", ""), "%s+$", "")
        affiche = gsub(gsub(gsub(affiche, "%s*|c%x%x%x%x%x%x%x%x" .. INDICE_MAJ .. "|r", ""), "%s*" .. INDICE_MAJ, ""),
            "%s+$", "")
        indice = "\n\n" .. INDICE_MAJ_FR
    end
    -- 0.9.5 : balises @s:…@ en FIN de modele (le client montre ces sorts dans des lignes a part : la ligne de la
    -- description s'arrete avant) : retirees des deux modeles quand l'affiche n'en a pas la trace
    if find(en, "@%a+:[%d:%-]+@%s*$") and find(fr, "@%a+:[%d:%-]+@%s*$") then
        en = gsub(en, "[%s]*@%a+:[%d:%-]+@[%s@%a%d:%-]*$", "")
        fr = gsub(fr, "[%s]*@%a+:[%d:%-]+@[%s@%a%d:%-]*$", "")
    end
    local en_nu = gsub(SansCouleurs(en), "\r\n?", "\n")
    local aff_nu = gsub(SansCouleurs(affiche), "\r\n?", "\n")
    local _, vars_en = Decouper(en_nu)
    if #vars_en == 0 then
        local _, vars_fr = Decouper(fr)
        -- (0.9.5 : un « $ » seul, sans variable, que l'anglais affiche aussi : texte coupé par CoA lui-même, « up to $ »)
        local _, d_fr = gsub(fr, "%$", "")
        local _, d_en = gsub(en_nu, "%$", "")
        if #vars_fr > 0 or d_fr > d_en then return nil end
        if A.Plat(en_nu) == A.Plat(aff_nu) then return fr .. indice end
        local r = AlignerNombres(fr, A.Plat(en_nu), A.Plat(aff_nu))
        return r and (r .. indice) or nil
    end
    -- 0.9.5 : captures typees d'abord (« plus ${$m3+0}$?s807183[][, stunning…] » : deux variables collees, la
    -- capture souple coupait n'importe ou), puis souples
    local r
    for _, mode in ipairs({ "typee", "souple" }) do
        local valeurs, conds, ordre, rangs = Extraire(en_nu, aff_nu, mode)
        if valeurs then r = Appliquer(fr, valeurs, conds, ordre, rangs) end
        if r then break end
    end
    if not r then return nil end
    -- garde-fou : jamais plus de « $ » que dans l'anglais affiche (variable abimee)
    local _, dfr = gsub(r, "%$", "")
    local _, den = gsub(aff_nu, "%$", "")
    if dfr > den then return nil end
    r = gsub(r, "%s+$", "")
    r = gsub(r, "[Tt]outes les 1 secondes", "toutes les secondes")
    r = gsub(r, "[Tt]outes les 1 sec%f[%A]%.?", "toutes les secondes")
    return r .. indice
end

-- 0.9.1 (essai 8, talent « Storm Chaser ») : conditionnelles COLLEES (« next $?a|b[][Call Lightning]$?a[Aeroblast][]
-- $?b[Torrential Wrath][] by ») : rien ne les separe, le decoupage du texte affiche entre elles est arbitraire et
-- l'alignement echouait. Repli : on developpe les conditionnelles du haut (chaque condition, vraie ou fausse, prend
-- la meme branche en anglais et en francais), puis on aligne chaque variante ; le francais n'est garde que si toutes
-- les variantes qui collent au texte affiche donnent le meme.
local function Conditionnelles(modele)
    local out, pos = {}, 1
    while true do
        local d, e = find(modele, "%$%?[^%[%]%$]*%[", pos)
        if not d then break end
        local b1d, b1f = find(modele, "%b[]", e)
        if b1d ~= e then return nil end
        local c = { d = d, pre = sub(modele, d, e - 1), oui = sub(modele, b1d + 1, b1f - 1), non = "", f = b1f }
        local suite = sub(modele, b1f + 1, b1f + 1)
        if suite == "[" then
            local b2d, b2f = find(modele, "%b[]", b1f + 1)
            if b2d ~= b1f + 1 then return nil end
            c.non, c.f = sub(modele, b2d + 1, b2f - 1), b2f
            suite = sub(modele, b2f + 1, b2f + 1)
        end
        if suite == "?" then return nil end          -- chaine « $?a[x]?b[y][z] » : non geree
        out[#out + 1] = c
        pos = c.f + 1
    end
    return out
end

local function Developper(modele, cs, choix)
    local out, pos = {}, 1
    for _, c in ipairs(cs) do
        out[#out + 1] = sub(modele, pos, c.d - 1)
        out[#out + 1] = choix[c.pre] and c.oui or c.non
        pos = c.f + 1
    end
    out[#out + 1] = sub(modele, pos)
    return table.concat(out)
end

TexteSort = function(fr, en, affiche)
    local r = TexteSortSimple(fr, en, affiche)
    if r or type(en) ~= "string" or type(fr) ~= "string" or not find(en, "$?", 1, true) then return r end
    local ce, cf = Conditionnelles(en), Conditionnelles(fr)
    if not ce or not cf or #ce < 2 then return nil end
    local collees = false
    for k = 2, #ce do if ce[k].d == ce[k - 1].f + 1 then collees = true end end
    if not collees then return nil end             -- seulement des conditionnelles collees (le cas qui echouait)
    local pres, vu = {}, {}
    for _, c in ipairs(ce) do
        if not vu[c.pre] then vu[c.pre] = true; pres[#pres + 1] = c.pre end
    end
    for _, c in ipairs(cf) do if not vu[c.pre] then return nil end end
    if #pres > 5 then return nil end
    -- 0.9.5 (audit, « $?a524861[|cffff3232][|cffffffff]Requires Mortal Form|r ») : deux variantes qui ne different
    -- que par leurs codes de couleur collent toutes deux au texte nu : on garde celle dont les couleurs sont celles
    -- de l'affiche
    local function Couleurs(t)
        local c = {}
        for x in gmatch(t, "|c(%x%x%x%x%x%x%x%x)") do c[#c + 1] = lower(x) end
        return table.concat(c, ",")
    end
    local trouves, vus = {}, {}
    for masque = 0, 2 ^ #pres - 1 do
        local choix = {}
        for k, p in ipairs(pres) do choix[p] = math.floor(masque / 2 ^ (k - 1)) % 2 == 1 end
        local v = TexteSort(Developper(fr, cf, choix), Developper(en, ce, choix), affiche)
        if v and not vus[v] then vus[v] = true; trouves[#trouves + 1] = v end
    end
    if #trouves <= 1 then return trouves[1] end
    local nu = SansCouleurs(trouves[1])
    for k = 2, #trouves do if SansCouleurs(trouves[k]) ~= nu then return nil end end
    local ca, bon = Couleurs(affiche), nil
    for _, v in ipairs(trouves) do
        if Couleurs(v) == ca then
            if bon then return nil end
            bon = v
        end
    end
    return bon
end
A.TexteSort = TexteSort

-- ----------------------------------------------------------------------------
-- Donnees d'un sort : { nomFR, empreinte nomEN, rangFR, empreinte rangEN, descriptions, infobulles }
-- descriptions / infobulles : { fr1, en1, fr2, en2 } (en : modele anglais ou empreinte), ou false.
-- ----------------------------------------------------------------------------
local function Variantes(s)
    local out = {}
    for _, k in ipairs({ 5, 6 }) do
        local v = s[k]
        if type(v) == "table" then
            for i = 1, #v, 2 do out[#out + 1] = { v[i], v[i + 1] } end
        end
    end
    return out
end

-- Memoire des alignements : une infobulle de sort ou d'aura se redessine sans cesse (recharge,
-- duree qui s'ecoule) ; le meme texte n'est aligne qu'une fois.
local memo, n_memo = {}, 0
local function Memoriser(k, v)
    n_memo = n_memo + 1
    if n_memo > 400 then memo, n_memo = {}, 0 end
    memo[k] = v or false
    return v
end

-- Description d'un sort pour un texte affiche (une ligne d'infobulle, ou le corps d'une ligne
-- « Use: »). Renvoie le francais, ou nil.
function A.DescriptionSort(id, affiche)
    local k = id .. "\0" .. affiche
    local m = memo[k]
    if m ~= nil then return m or nil end
    local s = A.Sort(id)
    if type(s) ~= "table" then return nil end        -- (pas memorise : la tranche peut arriver apres un combat)
    for _, v in ipairs(Variantes(s)) do
        local fr = TexteSort(v[1], v[2], affiche)
        if fr then return Memoriser(k, fr) end
    end
    return Memoriser(k, nil)
end

-- Nom francais d'un sort par numero, verifie par l'empreinte du nom anglais affiche.
function A.NomSort(id, nomEN)
    local s = A.Sort(id)
    if type(s) ~= "table" or not s[1] then return nil end
    if nomEN and A.H1(nomEN) ~= s[2] then return nil end
    return s[1]
end

local function RangSort(s, rangEN)
    if type(rangEN) ~= "string" or rangEN == "" then return nil end
    if type(s) == "table" and s[3] and A.H1(rangEN) == s[4] then return s[3] end
    local e1, coeur, e2 = match(rangEN, "^(|c%x%x%x%x%x%x%x%x)(.-)(|r)$")
    if coeur then
        local fr = A.Nom("rang", coeur)
        return fr and (e1 .. fr .. e2)
    end
    return A.Nom("rang", rangEN)
end
A.RangSort = RangSort

-- ----------------------------------------------------------------------------
-- 0.9.4 (essai 8, fenetre des talents de CoA) : SORTS CITES. La description d'un sort de CoA peut porter des balises
-- « @s:N:0@ » (« … into |cffffffffTorrential Wrath|r.@s:807105:0@@s:804017:0@ ») ; le client y insere, dans la bulle,
-- un bloc par sort cite : separateur (|TInterface\Common\ui-tooltipdivider…|t), retour a la ligne, icone, nom en
-- blanc, puis la description du sort N (elle-meme avec ses balises : Conduction sous Torrential Wrath). Chaque bloc est
-- traduit a part : nom par le numero du sort cite (balises de la description anglaise du sort de la bulle, dans
-- l'ordre, de proche en proche), sinon par le nom ; description par ce numero, sinon par son texte.
-- ----------------------------------------------------------------------------
local SEPARATEUR = "|tinterface\\common\\ui%-tooltipdivider[^|]*|t"

local function IdsCites(id, out, vus, profondeur)
    if profondeur > 4 or type(id) ~= "number" then return out end
    local s = A.Sort(id)
    if type(s) ~= "table" then return out end
    for _, v in ipairs(Variantes(s)) do
        local en = v[2]
        if type(en) == "string" and find(en, "@s:", 1, true) then
            for n in gmatch(en, "@s:(%d+):") do
                local j = tonumber(n)
                if j and not vus[j] then
                    vus[j] = true
                    out[#out + 1] = j
                    IdsCites(j, out, vus, profondeur + 1)
                end
            end
            break                                   -- une seule variante (la description) suffit
        end
    end
    return out
end
A.IdsCites = function(id) return IdsCites(id, {}, {}, 0) end

local function TraduireBloc(seg, idc)
    local tete, c1, nom, c2, blanc, corps = match(seg, "^(%s*|T[^|]*|t%s*)(|c%x%x%x%x%x%x%x%x)(.-)(|r)(%s*)(.*)$")
    if not tete then
        tete, c1, nom, c2, blanc, corps = match(seg, "^(%s*)(|c%x%x%x%x%x%x%x%x)(.-)(|r)(%s*)(.*)$")
    end
    if not tete or nom == "" then return nil end
    local nomFR = (idc and A.NomSort(idc, nom)) or (A.NomSortParNom and A.NomSortParNom(nom))
    local corpsFR
    if corps ~= "" then
        corpsFR = idc and A.DescriptionSort(idc, corps)
        if not corpsFR and len(corps) >= 20 then corpsFR = A.TraduireCorpsEffet(corps, nil) end
    end
    if not nomFR and not corpsFR then return nil end
    return tete .. c1 .. (nomFR or nom) .. c2 .. blanc .. (corpsFR or corps)
end

-- Texte d'une ligne qui contient au moins un separateur ; ids : sorts cites (dans l'ordre), k : premier a utiliser.
-- Renvoie le texte (traduit en tout ou partie) ou nil, et le prochain indice.
function A.TraduireBlocsSorts(t, ids, k, idBulle)
    if type(t) ~= "string" then return nil, k end
    local bas = lower(t)
    local d, f = find(bas, SEPARATEUR)
    if not d then return nil, k end
    ids, k = ids or {}, k or 1
    local morceaux, change = {}, false
    local tete = sub(t, 1, d - 1)
    if tete ~= "" and not find(tete, "^%s*$") then
        local fr = (idBulle and A.DescriptionSort(idBulle, tete)) or A.LigneSortLibre(tete)
        if fr then tete, change = fr, true end
    end
    morceaux[1] = tete
    while d do
        local d2, f2 = find(bas, SEPARATEUR, f + 1)
        local seg = sub(t, f + 1, (d2 or (#t + 1)) - 1)
        morceaux[#morceaux + 1] = sub(t, d, f)
        local fr = TraduireBloc(seg, ids[k])
        if fr then change = true end
        morceaux[#morceaux + 1] = fr or seg
        k = k + 1
        d, f = d2, f2
    end
    return change and table.concat(morceaux) or nil, k
end

-- ----------------------------------------------------------------------------
-- Infobulles de sorts
-- ----------------------------------------------------------------------------
local Ligne = function(bulle, i, cote)
    local nom = bulle:GetName()
    return nom and _G[nom .. (cote or "TextLeft") .. i]
end
local en_cours = false

function A.TraduireBulleSort(bulle, id)
    if en_cours or not A.Actif() or type(id) ~= "number" or not bulle then return false end
    local s = A.Sort(id)
    local modifie = false
    -- Le RANG est traduit pour TOUS les sorts, CoA compris, meme sans donnees pour ce sort : « Passive »,
    -- « Racial », « Racial Passive »… sont des textes de rang (table RG), pas des noms.
    local r1 = Ligne(bulle, 1, "TextRight")
    local tr = r1 and r1:IsShown() and r1:GetText()
    if tr and tr ~= "" and not A.DejaEcrit(r1, tr) then
        local fr = RangSort(s, tr)
        if fr and fr ~= tr then A.Ecrire(r1, fr); modifie = true end
    end
    -- 0.9 : « Requires Cat Form », « Requires Anvil » (formes, objets de focalisation, outils), pour tous les sorts ;
    -- essai 8 : les bulles de talents de CoA ajoutent sous le sort ceux qu'il cite (« Thunder Grip » et sa
    -- description) : chaque ligne encore en anglais est essayée comme nom de sort ou description de sort
    -- 0.9.4 : blocs des sorts cites (balises @s, voir A.TraduireBlocsSorts) ; ligne « Niveau: 1 » de CoA (GameTooltip.lua,
    -- LEVEL..": "..niveau requis : LEVEL est deja « Niveau » par PTRXML, l'espace insecable manque)
    local ids, k = nil, 1
    local niveau = _G.LEVEL
    for i = 2, bulle:NumLines() do
        local l = Ligne(bulle, i)
        local t = l and l:GetText()
        if t and t ~= "" and not A.DejaEcrit(l, t) then
            local fr
            if find(t, "|T", 1, true) and find(lower(t), "ui-tooltipdivider", 1, true) then
                ids = ids or (A.IdsCites(id))
                fr, k = A.TraduireBlocsSorts(t, ids, k, id)
            elseif type(niveau) == "string" and niveau ~= "Level" and niveau ~= "" and sub(t, 1, #niveau + 2) == niveau .. ": " then
                fr = niveau .. "\194\160: " .. sub(t, #niveau + 3)
            else
                fr = (len(t) <= 80 and A.LigneRequiert and A.LigneRequiert(t)) or A.LigneSortLibre(t)
            end
            if fr and fr ~= t then A.Ecrire(l, fr); modifie = true end
        end
    end
    if type(s) ~= "table" then
        if modifie and bulle:IsShown() and not A.EstProtege(bulle) then
            en_cours = true
            pcall(bulle.Show, bulle)
            en_cours = false
        end
        return modifie
    end
    local l1 = Ligne(bulle, 1)
    local t1 = l1 and l1:GetText()
    if t1 and s[1] and not A.DejaEcrit(l1, t1) and A.H1(SansCouleurs(t1)) == s[2] then
        A.Ecrire(l1, s[1]); modifie = true
    end
    if type(s[5]) == "table" or type(s[6]) == "table" then
        for i = 2, bulle:NumLines() do
            local l = Ligne(bulle, i)
            local t = l and l:GetText()
            if t and len(t) > 10 and not A.DejaEcrit(l, t) then
                local fr = A.DescriptionSort(id, t)
                if fr and fr ~= t then A.Ecrire(l, fr); modifie = true end
            end
        end
    end
    if modifie then
        A.Compteurs.sorts = A.Compteurs.sorts + 1
        if bulle:IsShown() and not A.EstProtege(bulle) then
            en_cours = true
            pcall(bulle.Show, bulle)
            en_cours = false
        end
    end
    return modifie
end

local function IdDepuisGetSpell(bulle)
    if type(bulle.GetSpell) ~= "function" then return nil end
    local ok, _, _, id = pcall(bulle.GetSpell, bulle)
    if ok and type(id) == "number" then return id end
end

local function SurSort(bulle)
    if not A.Actif() then return end
    A.TraduireBulleSort(bulle, IdDepuisGetSpell(bulle))
end

local function Brancher(bulle)
    if not bulle or not bulle.HookScript then return end
    bulle:HookScript("OnTooltipSetSpell", P("infobulle sort", SurSort))
end
Brancher(GameTooltip)
Brancher(ItemRefTooltip)

if GameTooltip then
    -- barre d'action : la 4e valeur de GetActionInfo est le vrai numero (la 2e est la case du grimoire)
    if type(GameTooltip.SetAction) == "function" then
        hooksecurefunc(GameTooltip, "SetAction", P("SetAction", function(bulle, case)
            if not A.Actif() or type(GetActionInfo) ~= "function" then return end
            local genre, _, _, id = GetActionInfo(case)
            if genre == "spell" and type(id) == "number" then A.TraduireBulleSort(bulle, id) end
        end))
    end
    -- grimoire : la case -> le lien -> le numero
    if type(GameTooltip.SetSpell) == "function" then
        hooksecurefunc(GameTooltip, "SetSpell", P("SetSpell", function(bulle, case, livre)
            if not A.Actif() or type(GetSpellLink) ~= "function" then return end
            local id = A.IdDepuisLien(GetSpellLink(case, livre), "spell")
            if id then A.TraduireBulleSort(bulle, id) end
        end))
    end
    -- auras : la 11e valeur d'UnitAura
    local function SurAura(filtreParDefaut)
        return P("aura", function(bulle, unite, index, filtre)
            if not A.Actif() or type(UnitAura) ~= "function" then return end
            local id = select(11, UnitAura(unite, index, filtre or filtreParDefaut))
            if type(id) == "number" then A.TraduireBulleSort(bulle, id) end
        end)
    end
    if type(GameTooltip.SetUnitAura) == "function" then hooksecurefunc(GameTooltip, "SetUnitAura", SurAura(nil)) end
    if type(GameTooltip.SetUnitBuff) == "function" then hooksecurefunc(GameTooltip, "SetUnitBuff", SurAura("HELPFUL")) end
    if type(GameTooltip.SetUnitDebuff) == "function" then
        hooksecurefunc(GameTooltip, "SetUnitDebuff", SurAura("HARMFUL"))
    end
end

-- ----------------------------------------------------------------------------
-- Lignes « Use: », « Equip: », « Chance on hit: » des infobulles d'objets.
-- ----------------------------------------------------------------------------
local PREFIXES = { "ITEM_SPELL_TRIGGER_ONUSE", "ITEM_SPELL_TRIGGER_ONEQUIP", "ITEM_SPELL_TRIGGER_ONPROC" }
local prefixes_cache

local function Prefixes()
    if prefixes_cache then return prefixes_cache end
    local out = {}
    for _, cle in ipairs(PREFIXES) do
        local g = A.Gabarit and A.Gabarit(cle)
        local en = g and g.en
        local fr = g and type(g.fr) == "string" and g.fr or nil
        local cur = _G[cle]
        if type(cur) == "string" and cur ~= "" and cur ~= en then
            out[#out + 1] = { m = cur .. " ", f = cur .. " " }      -- deja en francais (PTRXML)
        end
        if en then out[#out + 1] = { m = en .. " ", f = (fr or en) .. " " } end
    end
    prefixes_cache = out
    return out
end

-- Morceaux d'un texte qui peuvent etre un NOM DE LIEU : suites de mots a majuscule (« Elwynn Forest », « Valley of
-- Trials », « The Crossroads »), reliees par des espaces seulement (une ponctuation coupe la suite), petits mots de
-- liaison permis au milieu (of, the, de, du…). Renvoie les positions { debut, fin }, de la plus longue a la plus courte.
local LIAISONS = { ["of"] = true, ["the"] = true, ["de"] = true, ["du"] = true, ["des"] = true, ["la"] = true, ["le"] = true }
local function SuitesMajuscules(t)
    local mots = {}
    for d, mot, f in string.gmatch(t, "()([%w'%-]+)()") do mots[#mots + 1] = { d, f - 1, mot } end
    local out = {}
    local i = 1
    while i <= #mots do
        if find(mots[i][3], "^%u") then
            local j, fin = i, i
            while j < #mots and find(sub(t, mots[j][2] + 1, mots[j + 1][1] - 1), "^ +$") do
                local m = mots[j + 1][3]
                if find(m, "^%u") then fin = j + 1 elseif not LIAISONS[m] then break end
                j = j + 1
            end
            out[#out + 1] = { mots[i][1], mots[fin][2] }
            i = fin + 1
        else
            i = i + 1
        end
    end
    table.sort(out, function(a, b) return (a[2] - a[1]) > (b[2] - b[1]) end)
    return out
end
A.SuitesMajuscules = SuitesMajuscules

-- Le sort dont le texte anglais a la meme forme (index par squelette, charge a la demande). Un texte qui contient
-- le lieu de la pierre de foyer ($z) est aussi cherche avec ce lieu remplace par une valeur (le squelette du modele
-- a « # » a la place de $z) ; la description est ensuite verifiee par l'alignement complet (litteraux du modele
-- exacts autour du lieu), et $z traduit par le nom de zone.
--   0.4 : le lieu donne par GetBindLocation() ;
--   0.5 : essai 4, « Returns you to Elwynn Forest. » restait en anglais : le $z affiche par le client n'est pas
--         forcement le texte de GetBindLocation() (zone ou sous-zone du foyer). On essaie donc aussi chaque suite de
--         mots a majuscule du texte (« Elwynn Forest »), sans dependre de GetBindLocation.
-- Renvoie la liste des sorts candidats, et false si l'index n'a pas pu etre lu (charge plus tard : pas de memoire).
local function SortsParTexte(corps)
    local sk = A.TableDe("sorts_index", "SK")
    if not sk then return {}, false end
    local ids = sk:ParTexte(A.Squelette(corps))
    if type(ids) == "table" then return ids, true end
    local essais = {}
    if type(GetBindLocation) == "function" then
        local ok, lieu = pcall(GetBindLocation)
        if ok and type(lieu) == "string" and lieu ~= "" then
            local d, f = find(corps, lieu, 1, true)
            if d then essais[1] = { d, f } end
        end
    end
    for _, p in ipairs(SuitesMajuscules(corps)) do essais[#essais + 1] = p end
    for _, p in ipairs(essais) do
        ids = sk:ParTexte(A.Squelette(sub(corps, 1, p[1] - 1) .. "1" .. sub(corps, p[2] + 1)))
        if type(ids) == "table" then return ids, true end
    end
    return {}, true
end

local memo_effets, n_effets = {}, 0
function A.TraduireCorpsEffet(corps, idObjet)
    local k = tostring(idObjet) .. "\0" .. corps
    local m = memo_effets[k]
    if m ~= nil then return m or nil end
    local fr, id, complet = A.TrouverCorpsEffet(corps, idObjet)
    -- (0.5) un echec n'est garde en memoire que si les donnees ont pu etre lues (index et tranches de sorts) : un
    -- premier survol en combat (chargement remis a la fin du combat) ne condamne plus la ligne pour la session
    if fr or complet then
        n_effets = n_effets + 1
        if n_effets > 300 then memo_effets, n_effets = {}, 0 end
        memo_effets[k] = fr or false
    end
    return fr, id
end

-- Renvoie le francais, le numero du sort, et si la recherche a pu lire toutes ses donnees.
function A.TrouverCorpsEffet(corps, idObjet)
    local essais = {}
    if idObjet and type(GetItemSpell) == "function" then
        -- (3.3.5 : GetItemSpell rend nom et rang ; certains clients rendent le numero en 2e valeur)
        local ok, _, idSort = pcall(GetItemSpell, idObjet)
        if ok and type(idSort) == "number" then essais[#essais + 1] = idSort end
    end
    local ids, lu = SortsParTexte(corps)
    for _, id in ipairs(ids) do essais[#essais + 1] = id end
    local complet = lu
    for _, id in ipairs(essais) do
        if type(A.Sort(id)) ~= "table" and A.EnCombat() then complet = false end
        local fr = A.DescriptionSort(id, corps)
        if fr then return fr, id, true end
    end
    return nil, nil, complet and not A.EnCombat()
end

-- Essai 8 : une ligne seule, sans numéro de sort : un nom de sort (tous les sorts de ce nom ont le même français)
-- ou la description d'un sort retrouvé par son texte (alignement prouvé, comme les lignes « Utiliser : »)
function A.LigneSortLibre(t)
    if type(t) ~= "string" or t == "" or not find(t, "%a") then return nil end
    local e1, coeur, e2 = A.Enrobage(t)
    if not coeur or coeur == "" then return nil end
    local fr
    if len(coeur) <= 60 and not find(coeur, "[%.%%]") and A.NomSortParNom then
        fr = A.NomSortParNom(coeur)
    end
    if not fr and len(coeur) >= 20 then fr = A.TraduireCorpsEffet(coeur, nil) end
    return fr and fr ~= coeur and (e1 .. fr .. e2) or nil
end

-- Essai 8 : le client ajoute le temps de recharge AU BOUT de la ligne « Utiliser : » (« … location. (30 min de
-- recharge) », gabarit ITEM_COOLDOWN_TOTAL, deja en francais par PTRXML) : on le met de cote pour retrouver le sort,
-- puis on le remet tel quel. Seulement une parenthese finale qui contient « recharge » ou « Cooldown ».
function A.SeparerRecharge(corps)
    if type(corps) ~= "string" then return corps, "" end
    local avant, paren = match(corps, "^(.-)(%s*%b())%s*$")
    if avant and avant ~= "" and (find(paren, "recharge", 1, true) or find(paren, "Cooldown", 1, true)) then
        return avant, paren
    end
    return corps, ""
end

-- Lignes d'effets : « Use: … », « Equip: … », « Chance on hit: … », et les lignes de statistiques que le
-- client montre SANS prefixe (CoA : « Increases PvE Power by 38. », sorts 101600-101799) : le sort dont le
-- texte anglais a la meme forme, verifie par l'alignement (jamais un francais sans l'anglais prouve).
function A.TraduireEffetsObjet(bulle, idObjet, cachees)
    if not A.Actif() then return false end
    local modifie = false
    for i = 2, bulle:NumLines() do
        local l = Ligne(bulle, i)
        local t = l and not (cachees and cachees[i]) and l:GetText()
        if t and t ~= "" and not A.DejaEcrit(l, t) then
            local vu = false
            for _, p in ipairs(Prefixes()) do
                if sub(t, 1, len(p.m)) == p.m then
                    vu = true
                    local corps, recharge = A.SeparerRecharge(sub(t, len(p.m) + 1))
                    local fr = A.TraduireCorpsEffet(corps, idObjet)
                    -- 0.8 (essai 7 n° 16) : CoA met parfois la DESCRIPTION de l'objet derriere « Use: » (« Teaches you
                    -- how to summon this mount. This is a Ground mount. ») : meme empreinte que la description traduite.
                    if not fr and idObjet then
                        local o = A.Objet(idObjet)
                        local nu = match(corps, "^%s*(.-)%s*$")
                        if type(o) == "table" and o[3] and nu and A.H1(nu) == o[4] then
                            fr = (match(corps, "^(%s*)") or "") .. o[3]
                        end
                    end
                    if fr then A.Ecrire(l, p.f .. fr .. recharge); modifie = true end
                    break
                end
            end
            if not vu and sub(t, 1, 10) == "Increases " then
                local e1, coeur, e2 = A.Enrobage(t)
                local fr = A.TraduireCorpsEffet(coeur, nil)
                if fr then A.Ecrire(l, e1 .. fr .. e2); modifie = true end
            end
        end
    end
    return modifie
end

-- ----------------------------------------------------------------------------
-- Grimoire : noms et rangs sur les boutons. Les boutons du grimoire de CoA sont des boutons
-- SECURISES : on ne touche ni a leurs methodes ni a leurs variables, seulement au texte de
-- leurs zones SpellName / SubSpellName (permis par le jeu). Le numero vient de
-- GetSpellLink(case, livre). Repasse 5 fois par seconde, grimoire ouvert seulement.
-- ----------------------------------------------------------------------------
local boutons_grimoire
local metiers_nouveaux = true

local function ChercherBoutons(cadre, profondeur, out)
    if not cadre or profondeur > 5 or type(cadre.GetChildren) ~= "function" then return end
    local enfants = { cadre:GetChildren() }
    for _, e in ipairs(enfants) do
        if type(e) == "table" and e.SpellName and e.SubSpellName then out[#out + 1] = e end
        ChercherBoutons(e, profondeur + 1, out)
    end
end

local function TraduireBoutonGrimoire(b, case, livre)
    if not case or not livre or not b:IsShown() or type(GetSpellLink) ~= "function" then return end
    local id = A.IdDepuisLien(GetSpellLink(case, livre), "spell")
    local s = id and A.Sort(id)
    local nom, sous = b.SpellName, b.SubSpellName
    local t = nom and nom:GetText()
    if type(s) == "table" and t and t ~= "" and s[1] and not A.DejaEcrit(nom, t) and A.H1(t) == s[2] then A.Ecrire(nom, s[1]) end
    -- le rang, pour tous les sorts (meme sans donnees : « Passive » -> « Passif »)
    local r = sous and sous:GetText()
    if r and r ~= "" and not A.DejaEcrit(sous, r) then
        local fr = RangSort(s, r)
        if fr and fr ~= r then A.Ecrire(sous, fr) end
    end
end

local function TraduireGrimoire()
    if not A.Actif() then return end
    local cadre = AscensionSpellbookFrame
    if cadre and cadre:IsShown() then
        if not boutons_grimoire then
            boutons_grimoire = {}
            ChercherBoutons(cadre, 0, boutons_grimoire)
        end
        for _, b in ipairs(boutons_grimoire) do TraduireBoutonGrimoire(b, b.spell, b.bookType) end
        -- 0.4 : livre des metiers (Modules/Fenetres.lua)
        if A.TraduireMetiers then A.TraduireMetiers(cadre, metiers_nouveaux) end
        metiers_nouveaux = false
    end
    -- 0.4 : plus d'appel a SpellBook_GetSpellID (fonction du jeu appelee par l'add-on) : dans le client CoA
    -- (patch-B, SpellBookFrame.lua) c'est une fonction VIDE et le grimoire standard n'est pas utilise.
end
A.TraduireGrimoire = TraduireGrimoire

local guetteur = CreateFrame("Frame")
local cumul, ouvert = 0, false
guetteur:SetScript("OnUpdate", P("Sorts.grimoire", function(_, ecoule)
    cumul = cumul + (ecoule or 0)
    if cumul < 0.2 then return end
    cumul = 0
    local visible = AscensionSpellbookFrame and AscensionSpellbookFrame:IsShown()
    if visible then
        A.Trace("Sorts.grimoire")
        -- a chaque ouverture, on recherche les boutons (les pages du grimoire peuvent etre creees plus tard)
        if not ouvert then boutons_grimoire = nil; metiers_nouveaux = true end
        TraduireGrimoire()
    end
    ouvert = visible and true or false
end, true))

-- ----------------------------------------------------------------------------
-- 0.4 : barre d'incantation du joueur. CastingBarFrameTemplate (patch-enUS, CastingBarFrame.xml) appelle
-- CastingBarFrame_OnEvent PAR SON NOM (<OnEvent> en ligne) ; patch-B, CastingBarFrame.lua : au debut d'un sort
-- ou d'une canalisation, barText:SetText(text) avec le nom anglais (UnitCastingInfo, sans numero de sort). Le
-- numero vient de GetSpellLink(nom) (sorts du grimoire du joueur) ; le francais n'est pose que si l'empreinte
-- du nom anglais affiche est celle du sort traduit (A.NomSort). Une zone de texte d'un cadre non protege.
-- ----------------------------------------------------------------------------
local EVENEMENTS_BARRE = { UNIT_SPELLCAST_START = true, UNIT_SPELLCAST_CHANNEL_START = true, PLAYER_ENTERING_WORLD = true }
function A.TraduireBarreIncantation(barre, evenement)
    if not A.Actif() or not barre or barre ~= CastingBarFrame or not EVENEMENTS_BARRE[evenement] then return end
    local zone = CastingBarFrameText
    local t = zone and zone:GetText()
    if not t or t == "" or A.DejaEcrit(zone, t) or type(GetSpellLink) ~= "function" then return end
    local ok, lien = pcall(GetSpellLink, t)
    local id = ok and A.IdDepuisLien(lien, "spell")
    local fr = id and A.NomSort(id, t)
    if fr and fr ~= t then A.Ecrire(zone, fr) end
end
if type(CastingBarFrame_OnEvent) == "function" then
    hooksecurefunc("CastingBarFrame_OnEvent", P("CastingBarFrame_OnEvent", function(barre, evenement)
        A.TraduireBarreIncantation(barre, evenement)
    end))
end

-- Liens de sort dans la discussion : « |Hspell:2120|h[Flamestrike]|h » -> nom francais.
function A.TraduireLiensSort(texte)
    if type(texte) ~= "string" or not find(texte, "|Hspell:", 1, true) then return texte end
    return (gsub(texte, "(|Hspell:(%d+)[^|]*|h%[)(.-)(%]|h)", function(debut, id, nom, fin)
        local fr = A.NomSort(tonumber(id), nom)
        return debut .. (fr or nom) .. fin
    end))
end

A.SortsActif = true
