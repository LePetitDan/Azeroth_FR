-- ============================================================================
-- Azeroth_FR : infobulles d'objets et de creatures (version 0.3).
-- Objets : nom, description, etiquette @…@, ensemble, bonus de sertissage et enchantements, colonne de
-- droite (sous-classe : « Mace », « Mail »), lignes « Use: » / « Equip: » (descriptions de sorts,
-- Modules/Sorts.lua), puis, EN DERNIER, le prefixe « Equip: » affiche « Équipé : ».
-- Creatures : nom, sous-titre, ligne de faction.
-- Par numero (lien de l'objet, numero de creature tire du GUID) ou par texte anglais exact ; le francais
-- n'est pose que si l'anglais affiche est bien celui qu'on a traduit (empreinte ou table de noms).
-- Les lignes fixes (« Binds when picked up », « Requires Level 10 », « Sell Price »…) viennent des textes
-- d'interface : c'est le paquet PTRXML qui les met en francais, pas l'add-on.
--
-- Le client CoA (patch-B, GameTooltip.lua) accroche lui-meme OnTooltipSetItem (GameTooltip_OnLoad) :
-- GameTooltip_ItemVersionReplacer vide la ligne de description « "@Mythic 5@reste" » (il n'en garde que
-- « "reste" ») et pose « Mythic 5 » (couleurs comprises) a la place de la ligne « Heroic ». Notre crochet
-- passe APRES le sien : on traduit donc la ligne d'etiquette telle qu'il l'a posee, et le reste de la
-- description par son empreinte (outils/fabriquer.py embarque le reste seul).
-- ============================================================================
local A = AzerothFR
local match, sub, len, gsub, find = string.match, string.sub, string.len, string.gsub, string.find
local P = A.Proteger

local function Ligne(bulle, i, cote)
    local nom = bulle:GetName()
    return nom and _G[nom .. (cote or "TextLeft") .. i]
end
A.LigneBulle = Ligne

-- Texte sans couleur d'enrobage : « |cffxxxxxxTexte|r » -> « |cffxxxxxx », « Texte », « |r ».
local function Enrobage(t)
    local c1, coeur, c2 = match(t, "^(|c%x%x%x%x%x%x%x%x)(.-)(|r)$")
    if coeur then return c1, coeur, c2 end
    return "", t, ""
end
A.Enrobage = Enrobage

-- ----------------------------------------------------------------------------
-- Etiquettes @…@ (decision 9 de Dan, 04/11/2026) : la table UNIQUE glossaire/etiquettes.tsv, embarquee
-- par outils/fabriquer.py (A.ETIQUETTES : coeur anglais -> francais ; A.ETIQUETTES_MOTIFS : « Mythic N »).
-- Seules les etiquettes decidees ou au nom officiel prouve y sont ; les autres restent en anglais.
-- ----------------------------------------------------------------------------
local function CoeurEtiquette(t)
    if type(t) ~= "string" or t == "" then return nil end
    local e = A.ETIQUETTES and A.ETIQUETTES[t]
    if e then return e end
    for _, m in ipairs(A.ETIQUETTES_MOTIFS or {}) do
        local caps = { match(t, m[1]) }
        if caps[1] then
            local k = 0
            return (gsub(m[2], "{N}", function() k = k + 1; return caps[k] or "" end))
        end
    end
    return nil
end
A.CoeurEtiquette = CoeurEtiquette

-- Etiquette affichee seule sur sa ligne, sous toutes ses formes : avec ou sans les @, entre guillemets,
-- en couleur (« |cFFCC0000Bloodforged|r » -> « |cFFCC0000Forgé par le sang|r »).
local function EtiquetteAffichee(texte)
    if type(texte) ~= "string" or texte == "" then return nil end
    local q1, corps, q2 = match(texte, '^("?)(.-)("?)$')
    if q1 ~= q2 then q1, q2, corps = "", "", texte end
    local a1, c2, a2 = match(corps, "^(@?)(.-)(@?)$")
    if a1 ~= a2 then a1, a2, c2 = "", "", corps end
    local e1, coeur, e2 = Enrobage(c2)
    local fr = CoeurEtiquette(coeur)
    if fr then return q1 .. a1 .. e1 .. fr .. e2 .. a2 .. q2 end
    return nil
end
A.EtiquetteAffichee = EtiquetteAffichee

-- ----------------------------------------------------------------------------
-- Gabarits d'une ligne (« Socket Bonus: %s », « Enchanted: %s ») : forme actuelle du jeu (francaise si
-- PTRXML l'a posee) ou anglaise ; le morceau est un nom d'enchantement officiel (SpellItemEnchantment.dbc).
-- ----------------------------------------------------------------------------
local function Enchantement(x)
    return A.Nom("enchantement", x)
end
A.NomEnchantement = Enchantement

local function LigneGabarit(t, cle)
    local g = A.Gabarit and A.Gabarit(cle)
    if not g then return nil end
    local cur = _G[cle]
    if type(cur) ~= "string" or cur == "" then cur = g.en end
    local args = A.LireGabarit(cur, t)
    if not args and cur ~= g.en then args = A.LireGabarit(g.en, t) end
    if not args or type(args[1]) ~= "string" then return nil end
    local fr = Enchantement(args[1])
    if not fr then return nil end
    return A.Formater(cur, { fr })
end

-- Une ligne d'objet (colonne de gauche) hors nom, description et effets : etiquette, ensemble, bonus de
-- sertissage, enchantement, gemme sertie. Renvoie le francais ou nil.
local function LigneObjet(t)
    local fr = EtiquetteAffichee(t)
    if fr then return fr end
    local e1, coeur, e2 = Enrobage(t)
    -- ligne d'ensemble : « Armor of the Fang (0/5) »
    local nom, x, y = match(coeur, "^(.-) %((%d+)/(%d+)%)$")
    local ens = nom and A.Nom("ensemble", nom)
    if ens then return e1 .. ens .. " (" .. x .. "/" .. y .. ")" .. e2 end
    fr = LigneGabarit(coeur, "ITEM_SOCKET_BONUS") or LigneGabarit(coeur, "ENCHANTED_TOOLTIP_LINE")
    if fr then return e1 .. fr .. e2 end
    -- gemme sertie : la ligne est le nom de son enchantement (« +8 Strength »)
    if find(coeur, "%d") then
        fr = Enchantement(coeur)
        if fr then return e1 .. fr .. e2 end
    end
    return nil
end
A.LigneObjet = LigneObjet

-- Prefixes des effets d'objets, affiches en francais EN DERNIER sur la ligne visible seulement :
-- « Equip: » -> « Équipé : » (francais officiel de ITEM_SPELL_TRIGGER_ONEQUIP ; la cle reste technique,
-- la variable du jeu n'est jamais changee), « Use: », « Chance on hit: » si le jeu les montre encore en
-- anglais.
local PREFIXES_AFFICHES = { "ITEM_SPELL_TRIGGER_ONEQUIP", "ITEM_SPELL_TRIGGER_ONUSE", "ITEM_SPELL_TRIGGER_ONPROC" }
local function PrefixeFrancais(t)
    for _, cle in ipairs(PREFIXES_AFFICHES) do
        local g = A.Gabarit and A.Gabarit(cle)
        local vers = g and (g.aff or (type(g.fr) == "string" and g.fr) or nil)
        if g and g.en and vers and vers ~= g.en and sub(t, 1, len(g.en)) == g.en then
            return vers .. sub(t, len(g.en) + 1)
        end
    end
    return nil
end
A.PrefixeFrancais = PrefixeFrancais

-- ----------------------------------------------------------------------------
-- Objets
-- ----------------------------------------------------------------------------
local en_cours = false

-- Description : « "reste" » (apres le client) ou « "@X@reste" » (tooltip non traite par le client).
local function Description(t, o)
    if len(t) < 2 or sub(t, 1, 1) ~= "\"" or sub(t, -1) ~= "\"" then return nil end
    local corps = sub(t, 2, -2)
    if A.H1(corps) == o[4] then return "\"" .. o[3] .. "\"" end
    if sub(corps, 1, 1) == "@" then
        local v, reste = match(t, "@(.+)@(.-)\"")
        if v and reste and reste ~= "" and A.H1(reste) == o[4] then
            local e1, coeur, e2 = Enrobage(v)
            local fv = CoeurEtiquette(coeur)
            return "\"@" .. (fv and (e1 .. fv .. e2) or v) .. "@" .. o[3] .. "\""
        end
    end
    return nil
end

local function SurObjet(bulle)
    if en_cours or not A.Actif() then return end
    local nomEN, lien = bulle:GetItem()
    local id = A.IdDepuisLien(lien, "item")
    if not id then return end
    local o = A.Objet(id)
    local n = bulle:NumLines()
    -- Lignes que le client a cachees lui-meme (piege du client d'Ascension) : notre remise
    -- en page ne doit pas les faire reapparaitre.
    local cachees = {}
    for i = 2, n do
        local l = Ligne(bulle, i)
        if l and l:GetText() and l:GetText() ~= "" and not l:IsShown() then cachees[i] = true end
    end
    local modifie = false
    local ligneDesc
    if type(o) == "table" then
        local l1 = Ligne(bulle, 1)
        local t1 = l1 and l1:GetText()
        local fr = t1 and nomEN and t1 == nomEN and A.NomObjetAffiche(id, nomEN)
        if fr then l1:SetText(fr); modifie = true end
        if o[3] then
            for i = 2, n do
                local l = Ligne(bulle, i)
                local t = l and not cachees[i] and l:GetText()
                local d = t and Description(t, o)
                if d then l:SetText(d); modifie = true; ligneDesc = i; break end
            end
        end
    end
    for i = 2, n do
        local l = Ligne(bulle, i)
        local t = i ~= ligneDesc and l and not cachees[i] and l:GetText()
        if t and t ~= "" then
            local fr = LigneObjet(t)
            if fr and fr ~= t then l:SetText(fr); modifie = true end
        end
    end
    -- colonne de droite : sous-classe d'objet (« Mace » -> « Masse », « Mail » -> « Mailles »)
    for i = 1, n do
        local r = Ligne(bulle, i, "TextRight")
        local t = r and r:IsShown() and r:GetText()
        if t and t ~= "" then
            local e1, coeur, e2 = Enrobage(t)
            local fr = A.Nom("sous_classe", coeur)
            if fr and fr ~= coeur then r:SetText(e1 .. fr .. e2); modifie = true end
        end
    end
    -- lignes « Use: » / « Equip: » / « Chance on hit: » et « Increases PvE Power by N. » (descriptions de sorts)
    if A.TraduireEffetsObjet and A.TraduireEffetsObjet(bulle, id, cachees) then modifie = true end
    -- EN DERNIER : prefixe « Equip: » -> « Équipé : » sur la ligne affichee
    for i = 2, n do
        local l = Ligne(bulle, i)
        local t = l and not cachees[i] and l:GetText()
        local fr = t and t ~= "" and PrefixeFrancais(t)
        if fr then l:SetText(fr); modifie = true end
    end
    if modifie then
        A.Compteurs.traduits = A.Compteurs.traduits + 1
        if bulle:IsShown() then
            en_cours = true
            pcall(bulle.Show, bulle)
            en_cours = false
        end
        for i in pairs(cachees) do
            local l = Ligne(bulle, i)
            if l and l:GetText() and l:GetText() ~= "" then l:SetText("") end
        end
    end
end
A.SurObjet = SurObjet

-- ----------------------------------------------------------------------------
-- Creatures : nom, sous-titre, ligne de faction (« Stormwind » -> « Hurlevent »).
-- ----------------------------------------------------------------------------
local function SurUnite(bulle)
    if en_cours or not A.Actif() then return end
    local _, unite = bulle:GetUnit()
    if not unite or UnitIsPlayer(unite) then return end
    local modifie = false
    local id = A.IdCreatureDepuisGUID(UnitGUID(unite))
    local c = id and A.TableDe("creatures", "C")
    c = c and c:ParId(id)
    local ligneSousTitre
    if type(c) == "table" then
        local nomEN = UnitName(unite)
        local l1 = Ligne(bulle, 1)
        local t1 = l1 and l1:GetText()
        if c[1] and nomEN and t1 and A.H1(nomEN) == c[2] then
            if t1 == nomEN then
                l1:SetText(c[1]); modifie = true
            else
                local debut, fin = string.find(t1, nomEN, 1, true)
                if debut then
                    l1:SetText(sub(t1, 1, debut - 1) .. c[1] .. sub(t1, fin + 1)); modifie = true
                end
            end
        end
        if c[3] then
            local l2 = Ligne(bulle, 2)
            local t2 = l2 and l2:GetText()
            if t2 and t2 ~= "" then
                local ouvre, coeur, ferme = match(t2, "^(<?)(.-)(>?)$")
                if coeur and A.H1(coeur) == c[4] then
                    l2:SetText(ouvre .. c[3] .. ferme); modifie = true
                    ligneSousTitre = 2
                end
            end
        end
    end
    -- ligne de faction : le nom exact d'une faction, sur une ligne a lui seul
    for i = 2, bulle:NumLines() do
        if i ~= ligneSousTitre then
            local l = Ligne(bulle, i)
            local t = l and l:GetText()
            local fr = t and t ~= "" and A.Nom("faction", t)
            if fr and fr ~= t then l:SetText(fr); modifie = true end
        end
    end
    if modifie then
        A.Compteurs.traduits = A.Compteurs.traduits + 1
        if bulle:IsShown() then
            en_cours = true
            pcall(bulle.Show, bulle)
            en_cours = false
        end
    end
end
A.SurUnite = SurUnite

-- ----------------------------------------------------------------------------
-- Branchements (HookScript : on passe APRES le jeu, et apres le crochet du client CoA, sans rien remplacer)
-- ----------------------------------------------------------------------------
local function Brancher(bulle, objets, unites)
    if not bulle or not bulle.HookScript then return end
    if objets then bulle:HookScript("OnTooltipSetItem", P("infobulle objet", SurObjet)) end
    if unites then bulle:HookScript("OnTooltipSetUnit", P("infobulle unité", SurUnite)) end
end
A.BrancherInfobulle = Brancher

Brancher(GameTooltip, true, true)
Brancher(ItemRefTooltip, true, false)
Brancher(ShoppingTooltip1, true, false)
Brancher(ShoppingTooltip2, true, false)
Brancher(ShoppingTooltip3, true, false)
