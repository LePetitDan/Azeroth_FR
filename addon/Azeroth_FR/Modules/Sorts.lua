-- ============================================================================
-- Azeroth_FR : sorts (version 0.2). Nom, rang et description en francais, A L'AFFICHAGE
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
    "@%a+:%d+:%-?%d+@", "@%a+:%d+:%a+@", "@%a+:%d+@", "@ext:", ":ext@",
}

local function Echapper(t) return (gsub(t, "([%^%$%(%)%%%.%[%]%*%+%-%?])", "%%%1")) end

-- Litteral avec espaces de tete et de queue souples ; un separateur tout blanc reste exige.
local function Souple(litteral)
    if litteral == "" then return "" end
    if find(litteral, "^%s*$") then return "%s+" end
    local coeur = match(litteral, "^%s*(.-)%s*$")
    local motif = Echapper(coeur)
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

-- Capture typee (repli) : un nombre pour une valeur, un nombre et son unite pour une duree.
local function CaptureTypee(v)
    if match(v, "^%$%d*[dD]%d*$") then return "(%-?[%d%.,]+%s*%a*)" end
    if match(v, "^%$[suohtqaxezSUOHTQAXEZ]%d*$") or match(v, "^%$%d+%a%d*$") or match(v, "^%$%b{}$")
        or match(v, "^%$<%a+>$") or match(v, "^%$[/%*%+%-]") then
        return "(%-?[%d%.,]+)"
    end
    return "(.-)"
end

local function Extraire(modele, affiche)
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
                valeurs[v] = val
            end
        end
        return caps, valeurs, rangs
    end
    local motif, typee, differe = "^", "^", false
    for i, l in ipairs(litteraux) do
        motif = motif .. Souple(l)
        typee = typee .. Souple(l)
        if i <= #variables then
            motif = motif .. "(.-)"
            local c = CaptureTypee(variables[i])
            typee = typee .. c
            if c ~= "(.-)" then differe = true end
        end
    end
    local caps, valeurs, rangs = essayer(motif .. "$")
    if not caps and differe then caps, valeurs, rangs = essayer(typee .. "$") end
    if not caps then return nil end
    local conds, ordre = {}, {}
    for i, v in ipairs(variables) do
        local pre = PrefixeConditionnel(v)
        if pre then
            local e = conds[pre]
            if e and (e.valeur ~= caps[i] or e.var ~= v) then conds[pre] = { ambigu = true }
            elseif not e then conds[pre] = { valeur = caps[i], var = v } end
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

local function Appliquer(modele_fr, valeurs, conds, ordre, rangs)
    local litteraux, variables = Decouper(modele_fr)
    local nb_gl = 0
    for _, v in ipairs(variables) do if match(SansCouleurs(v), "^%$[GgLl]") then nb_gl = nb_gl + 1 end end
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
                if val == nil and #ordre == nb_gl then
                    local ven = ordre[rang_gl]
                    if ven and lower(sub(ven, 2, 2)) == lower(sub(nue, 2, 2)) then
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
            -- conditionnelle : texte des crochets traduit -> par le prefixe, puis recursion
            if val == nil then
                local pre = PrefixeConditionnel(nue)
                local c = pre and conds[pre]
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

-- Traduit un texte de sort affiche. en : le modele anglais (texte), ou l'empreinte de sa forme
-- plate (nombre) quand il n'a ni variable ni nombre. Renvoie le francais, ou nil.
TexteSort = function(fr, en, affiche)
    if type(fr) ~= "string" or type(affiche) ~= "string" or affiche == "" then return nil end
    if type(en) == "number" then
        if A.H1(A.Plat(affiche)) == en and not find(fr, "%$") then return fr end
        return nil
    end
    if type(en) ~= "string" then return nil end
    local indice = ""
    if find(affiche, INDICE_MAJ, 1, true) and find(en, "@ext:", 1, true) then
        en = gsub(gsub(en, "%s*@ext:.-:ext@", ""), "%s+$", "")
        fr = gsub(gsub(fr, "%s*@ext:.-:ext@", ""), "%s+$", "")
        affiche = gsub(gsub(gsub(affiche, "%s*|c%x%x%x%x%x%x%x%x" .. INDICE_MAJ .. "|r", ""), "%s*" .. INDICE_MAJ, ""),
            "%s+$", "")
        indice = "\n\n" .. INDICE_MAJ        -- (la phrase d'interface reste en anglais : pas de francais prouve)
    end
    local en_nu = gsub(SansCouleurs(en), "\r\n?", "\n")
    local aff_nu = gsub(SansCouleurs(affiche), "\r\n?", "\n")
    local _, vars_en = Decouper(en_nu)
    if #vars_en == 0 then
        local _, vars_fr = Decouper(fr)
        if #vars_fr > 0 or find(fr, "%$") then return nil end
        if A.Plat(en_nu) == A.Plat(aff_nu) then return fr .. indice end
        local r = AlignerNombres(fr, A.Plat(en_nu), A.Plat(aff_nu))
        return r and (r .. indice) or nil
    end
    local valeurs, conds, ordre, rangs = Extraire(en_nu, aff_nu)
    if not valeurs then return nil end
    local r = Appliquer(fr, valeurs, conds, ordre, rangs)
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
    return A.Nom("rang", rangEN)
end
A.RangSort = RangSort

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
    if type(s) ~= "table" then return false end
    local modifie = false
    local l1 = Ligne(bulle, 1)
    local t1 = l1 and l1:GetText()
    if t1 and s[1] and not A.DejaEcrit(l1, t1) and A.H1(SansCouleurs(t1)) == s[2] then
        A.Ecrire(l1, s[1]); modifie = true
    end
    local r1 = Ligne(bulle, 1, "TextRight")
    local tr = r1 and r1:IsShown() and r1:GetText()
    if tr and tr ~= "" and not A.DejaEcrit(r1, tr) then
        local fr = RangSort(s, tr)
        if fr and fr ~= tr then A.Ecrire(r1, fr); modifie = true end
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
        if bulle:IsShown() then
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

-- Le sort dont le texte anglais a la meme forme (index par squelette, charge a la demande).
local function SortsParTexte(corps)
    local sk = A.TableDe("sorts_index", "SK")
    local ids = sk and sk:ParTexte(A.Squelette(corps))
    if type(ids) == "table" then return ids end
    return {}
end

local memo_effets, n_effets = {}, 0
function A.TraduireCorpsEffet(corps, idObjet)
    local k = tostring(idObjet) .. "\0" .. corps
    local m = memo_effets[k]
    if m ~= nil then return m or nil end
    local fr, id = A.TrouverCorpsEffet(corps, idObjet)
    n_effets = n_effets + 1
    if n_effets > 300 then memo_effets, n_effets = {}, 0 end
    memo_effets[k] = fr or false
    return fr, id
end

function A.TrouverCorpsEffet(corps, idObjet)
    local essais = {}
    if idObjet and type(GetItemSpell) == "function" then
        local ok, _, idSort = pcall(GetItemSpell, idObjet)
        if ok and type(idSort) == "number" then essais[#essais + 1] = idSort end
    end
    for _, id in ipairs(SortsParTexte(corps)) do essais[#essais + 1] = id end
    for _, id in ipairs(essais) do
        local fr = A.DescriptionSort(id, corps)
        if fr then return fr, id end
    end
    return nil
end

function A.TraduireEffetsObjet(bulle, idObjet, cachees)
    if not A.Actif() then return false end
    local modifie = false
    for i = 2, bulle:NumLines() do
        local l = Ligne(bulle, i)
        local t = l and not (cachees and cachees[i]) and l:GetText()
        if t and t ~= "" and not A.DejaEcrit(l, t) then
            for _, p in ipairs(Prefixes()) do
                if sub(t, 1, len(p.m)) == p.m then
                    local fr = A.TraduireCorpsEffet(sub(t, len(p.m) + 1), idObjet)
                    if fr then A.Ecrire(l, p.f .. fr); modifie = true end
                    break
                end
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
    if type(s) ~= "table" then return end
    local nom, sous = b.SpellName, b.SubSpellName
    local t = nom and nom:GetText()
    if t and t ~= "" and s[1] and not A.DejaEcrit(nom, t) and A.H1(t) == s[2] then A.Ecrire(nom, s[1]) end
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
    end
    -- grimoire standard 3.3.5 (si le client l'affiche)
    if SpellBookFrame and SpellBookFrame:IsShown() and type(SpellBook_GetSpellID) == "function" then
        for i = 1, 12 do
            local b = _G["SpellButton" .. i]
            if b then
                local nom, sous = _G["SpellButton" .. i .. "SpellName"], _G["SpellButton" .. i .. "SubSpellName"]
                local faux = { SpellName = nom, SubSpellName = sous, IsShown = function() return b:IsShown() end }
                TraduireBoutonGrimoire(faux, SpellBook_GetSpellID(b:GetID()), SpellBookFrame.bookType)
            end
        end
    end
end
A.TraduireGrimoire = TraduireGrimoire

local guetteur = CreateFrame("Frame")
local cumul = 0
guetteur:SetScript("OnUpdate", P("Sorts.grimoire", function(_, ecoule)
    cumul = cumul + (ecoule or 0)
    if cumul < 0.2 then return end
    cumul = 0
    if (AscensionSpellbookFrame and AscensionSpellbookFrame:IsShown()) or (SpellBookFrame and SpellBookFrame:IsShown()) then
        TraduireGrimoire()
    end
end))

-- Liens de sort dans la discussion : « |Hspell:2120|h[Flamestrike]|h » -> nom francais.
function A.TraduireLiensSort(texte)
    if type(texte) ~= "string" or not find(texte, "|Hspell:", 1, true) then return texte end
    return (gsub(texte, "(|Hspell:(%d+)[^|]*|h%[)(.-)(%]|h)", function(debut, id, nom, fin)
        local fr = A.NomSort(tonumber(id), nom)
        return debut .. (fr or nom) .. fin
    end))
end

A.SortsActif = true
