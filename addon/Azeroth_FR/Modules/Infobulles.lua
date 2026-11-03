-- ============================================================================
-- Azeroth_FR : infobulles d'objets (nom, description, ensemble, lignes « Use: »/« Equip: »)
-- et de creatures (nom, sous-titre, faction).
-- Par numero : lien de l'objet, numero de creature tire du GUID. Le francais n'est pose
-- que si l'anglais affiche est bien celui qu'on a traduit (empreinte).
-- Les lignes fixes (« Binds when picked up », « Requires Level 10 »…) viennent des textes
-- d'interface : c'est le paquet PTRXML qui les met en francais, pas l'add-on.
-- Les lignes « Use: » / « Equip: » sont des descriptions de SORTS : Modules/Sorts.lua.
-- ============================================================================
local A = AzerothFR
local match, sub, len = string.match, string.sub, string.len
local P = A.Proteger

local function Ligne(bulle, i, cote)
    local nom = bulle:GetName()
    return nom and _G[nom .. (cote or "TextLeft") .. i]
end
A.LigneBulle = Ligne

-- ----------------------------------------------------------------------------
-- Etiquettes @…@ : l'essai n'en traduit que TROIS (decision de Dan : trancher apres un test
-- en jeu ; « Bloodforged » -> « forgé par le sang », decision du 03/11). On reconnait la ligne
-- qui ne porte QUE l'etiquette, sous toutes ses formes : avec ou sans les @, entre guillemets
-- (description), en couleur. Une description plus longue est traduite par la source
-- (outils/fabriquer.py), etiquette comprise.
-- ----------------------------------------------------------------------------
local function CoeurEtiquette(t)
    local n = match(t, "^Mythic (%d+)$")
    if n then return "Mythique " .. n end
    if t == "Heroic Raid" then return "Raid héroïque" end
    if t == "Bloodforged" then return "forgé par le sang" end
    return nil
end

local function EtiquetteAffichee(texte)
    if type(texte) ~= "string" or texte == "" then return nil end
    local q1, corps, q2 = match(texte, '^("?)(.-)("?)$')
    if q1 ~= q2 then q1, q2, corps = "", "", texte end
    local a1, c2, a2 = match(corps, "^(@?)(.-)(@?)$")
    if a1 ~= a2 then a1, a2, c2 = "", "", corps end
    local fr = CoeurEtiquette(c2)
    if fr then return q1 .. a1 .. fr .. a2 .. q2 end
    local couleur, coeur = match(c2, "^(|c%x%x%x%x%x%x%x%x)(.-)|r$")
    fr = coeur and CoeurEtiquette(coeur)
    if fr then return q1 .. a1 .. couleur .. fr .. "|r" .. a2 .. q2 end
    return nil
end
A.EtiquetteAffichee = EtiquetteAffichee

-- ----------------------------------------------------------------------------
-- Objets
-- ----------------------------------------------------------------------------
local en_cours = false

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
    if type(o) == "table" then
        local l1 = Ligne(bulle, 1)
        local t1 = l1 and l1:GetText()
        local fr = t1 and nomEN and t1 == nomEN and A.NomObjetAffiche(id, nomEN)
        if fr then l1:SetText(fr); modifie = true end
        if o[3] then
            for i = 2, n do
                local l = Ligne(bulle, i)
                local t = l and not cachees[i] and l:GetText()
                if t and len(t) >= 2 and sub(t, 1, 1) == "\"" and sub(t, -1) == "\"" then
                    if A.H1(sub(t, 2, -2)) == o[4] then
                        l:SetText("\"" .. o[3] .. "\""); modifie = true
                        break
                    end
                end
            end
        end
    end
    for i = 2, n do
        local l = Ligne(bulle, i)
        local t = l and not cachees[i] and l:GetText()
        if t and t ~= "" then
            local fr = EtiquetteAffichee(t)
            if not fr then
                -- ligne d'ensemble : « Armor of the Fang (0/5) »
                local nom, x, y = match(t, "^(.-) %((%d+)/(%d+)%)$")
                local ens = nom and A.Nom("ensemble", nom)
                if ens then fr = ens .. " (" .. x .. "/" .. y .. ")" end
            end
            if fr and fr ~= t then l:SetText(fr); modifie = true end
        end
    end
    -- lignes « Use: » / « Equip: » / « Chance on hit: » (descriptions de sorts)
    if A.TraduireEffetsObjet and A.TraduireEffetsObjet(bulle, id, cachees) then modifie = true end
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
-- Branchements (HookScript : on passe APRES le jeu, sans rien remplacer)
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
