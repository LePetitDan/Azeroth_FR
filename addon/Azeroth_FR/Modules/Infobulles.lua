-- ============================================================================
-- Azeroth_FR : infobulles d'objets (nom, description) et de creatures (nom, sous-titre).
-- Par numero : lien de l'objet, numero de creature tire du GUID. Le francais n'est pose
-- que si l'anglais affiche est bien celui qu'on a traduit (empreinte).
-- Les lignes fixes (« Lie quand ramasse », « Niveau 10 requis »…) viennent des textes
-- d'interface : c'est le paquet PTRXML qui les met en francais, pas l'add-on.
-- ============================================================================
local A = AzerothFR
local match, sub, len = string.match, string.sub, string.len
local P = A.Proteger

local function Ligne(bulle, i, cote)
    local nom = bulle:GetName()
    return nom and _G[nom .. (cote or "TextLeft") .. i]
end

-- ----------------------------------------------------------------------------
-- Etiquettes @…@ : l'essai 1 n'en traduit que TROIS (decision de Dan : trancher apres un
-- test en jeu). Si le client les affiche sur une ligne a part, sans les @, on les
-- reconnait ici ; s'il les affiche telles quelles dans la description, c'est la
-- description qui les porte deja traduites (outils/fabriquer.py).
-- ----------------------------------------------------------------------------
local function EtiquetteAffichee(texte)
    local n = match(texte, "^Mythic (%d+)$")
    if n then return "Mythique " .. n end
    if texte == "Heroic Raid" then return "Raid héroïque" end
    if texte == "Bloodforged" then return "Forgé par le sang" end
    local c = match(texte, "^(|c%x%x%x%x%x%x%x%x)Bloodforged|r$")
    if c then return c .. "Forgé par le sang|r" end
    c, n = match(texte, "^(|c%x%x%x%x%x%x%x%x)Mythic (%d+)|r$")
    if c then return c .. "Mythique " .. n .. "|r" end
    c = match(texte, "^(|c%x%x%x%x%x%x%x%x)Heroic Raid|r$")
    if c then return c .. "Raid héroïque|r" end
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
        if o[1] and nomEN and t1 == nomEN and A.H1(nomEN) == o[2] then
            l1:SetText(o[1]); modifie = true
        end
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
        local fr = t and t ~= "" and EtiquetteAffichee(t)
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

-- ----------------------------------------------------------------------------
-- Creatures
-- ----------------------------------------------------------------------------
local function SurUnite(bulle)
    if en_cours or not A.Actif() then return end
    local _, unite = bulle:GetUnit()
    if not unite or UnitIsPlayer(unite) then return end
    local id = A.IdCreatureDepuisGUID(UnitGUID(unite))
    local c = id and A.TableDe("creatures", "C")
    c = c and c:ParId(id)
    if type(c) ~= "table" then return end
    local modifie = false
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
            end
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

-- ----------------------------------------------------------------------------
-- Branchements (HookScript : on passe APRES le jeu, sans rien remplacer)
-- ----------------------------------------------------------------------------
local function Brancher(bulle, objets, unites)
    if not bulle or not bulle.HookScript then return end
    if objets then bulle:HookScript("OnTooltipSetItem", P("infobulle objet", SurObjet)) end
    if unites then bulle:HookScript("OnTooltipSetUnit", P("infobulle unité", SurUnite)) end
end

Brancher(GameTooltip, true, true)
Brancher(ItemRefTooltip, true, false)
Brancher(ShoppingTooltip1, true, false)
Brancher(ShoppingTooltip2, true, false)
Brancher(ShoppingTooltip3, true, false)
