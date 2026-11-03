-- Azeroth_FR : test 3 (diagnostic).
--
-- PARTIE A (automatique, lecture seule), lancée 3 secondes après l'entrée en jeu :
--   1. LuaDBC appelé comme le montre le désassemblage d'Extensions.dll :
--        local db = CreateDBC("Fichier.dbc")   -- objet (userdata), métatable = LuaDBC
--        db:SetInt32("Colonne") ...            -- DÉCLARE les colonnes (l'ID est implicite)
--        db:Load()                             -- lit DBFilesClient\Fichier.dbc
--        db:GetRecord(id)                      -- table { ID = id, Colonne = valeur, ... }
--      sur trois petites tables : SpellCastTimes.dbc, SpellIcon.dbc, ChrClasses.dbc.
--      Spell.dbc n'est PAS chargé (209 510 sorts : trop lourd, voir la notice).
--   2. Les vrais numéros de sorts : barre d'action (4e valeur de GetActionInfo), grimoire
--      (GetSpellLink), infobulles (GameTooltip:GetSpell) sur une infobulle privée.
--   3. Quel Spell.dbc le jeu utilise (sorts témoins), talents (C_CharacterAdvancement), auras.
--
-- PARTIE B (facultative, seulement si Dan tape /azfr3 essai) : essai d'AFFICHAGE.
--   Le nom « Flamestrike » (sort 2120) est remplacé par « Choc de flammes » dans les
--   infobulles, et rien d'autre. Aucune donnée du jeu n'est modifiée : GetSpellInfo(2120)
--   reste « Flamestrike ». Tout disparaît au /reload ou en quittant le jeu.
--
-- Le résultat va dans WTF\...\SavedVariables\AzerothFR_Test3.lua (écrit au /reload).
-- Aucune variable globale du jeu n'est remplacée. Tout appel passe par pcall.
-- Pour annuler : supprimer le dossier Interface\AddOns\AzerothFR_Test3.

local NOM = "AzerothFR_Test3"
local db                                  -- = AzerothFR_Test3DB (créé à l'entrée en jeu)

local function dire(texte)
    if DEFAULT_CHAT_FRAME then
        DEFAULT_CHAT_FRAME:AddMessage("|cff33ff99Azeroth_FR (test 3)|r : " .. texte)
    end
end

local function pack(...) return { n = select("#", ...), ... } end

-- Décrit une valeur Lua sans jamais lever d'erreur (tables : 2 niveaux, 40 clés au plus).
local function decrire(v, profondeur)
    profondeur = profondeur or 0
    local t = type(v)
    if t == "table" then
        local d, n = {}, 0
        for k, val in pairs(v) do
            n = n + 1
            if n <= 40 then
                if type(val) == "table" and profondeur < 1 then
                    d[tostring(k)] = decrire(val, profondeur + 1)
                elseif type(val) == "table" then
                    d[tostring(k)] = "table"
                else
                    d[tostring(k)] = val
                end
            end
        end
        if n > 40 then d["(cles en plus)"] = n - 40 end
        return d
    elseif t == "string" or t == "number" or t == "boolean" or t == "nil" then
        return v
    else
        return t .. " : " .. tostring(v)
    end
end

-- Appel protégé : rend { ok, n (nombre de valeurs), r1, r2... , erreur }.
local function appel(fn, ...)
    if type(fn) ~= "function" then
        return { ok = false, erreur = "pas une fonction (" .. type(fn) .. ")" }
    end
    local r = pack(pcall(fn, ...))
    local out = { ok = r[1], n = r.n - 1 }
    if not r[1] then
        out.erreur = tostring(r[2])
    else
        for i = 2, math.min(r.n, 7) do out["r" .. (i - 1)] = decrire(r[i]) end
    end
    return out, r
end

local function idDepuisLien(lien)
    if type(lien) ~= "string" then return nil end
    return tonumber(string.match(lien, "spell:(%d+)"))
end

---------------------------------------------------------------------------
-- 1. LuaDBC
---------------------------------------------------------------------------
local function essaiLuaDBC()
    local L = { }
    db.LuaDBC = L
    L.type_CreateDBC = type(CreateDBC)
    L.type_LuaDBC = type(LuaDBC)
    L.CreateDBC_sure = issecurevariable and issecurevariable("CreateDBC")
    if type(CreateDBC) ~= "function" then
        L.conclusion = "CreateDBC absente : partie LuaDBC sautée"
        return
    end

    -- 1a. SpellCastTimes.dbc : schéma FAUX d'abord (2 colonnes au lieu de 3) -> erreur attendue
    --     « ... has wrong number of columns (found 4, expected 3) ».
    local s = {}
    L.SpellCastTimes = s
    local _, r = appel(CreateDBC, "SpellCastTimes.dbc")
    local obj = r and r[1] and r[2]
    s.creation = { type = type(obj), texte = tostring(obj) }
    if obj ~= nil then
        local okMeta, mt = pcall(getmetatable, obj)
        s.metatable_est_LuaDBC = okMeta and (mt == LuaDBC) or false
        appel(obj.SetInt32, obj, "Base")
        appel(obj.SetInt32, obj, "PerLevel")
        s.load_schema_faux = appel(obj.Load, obj)
    end

    -- 1b. SpellCastTimes.dbc : bon schéma (ID implicite + 3 colonnes = 4 champs).
    _, r = appel(CreateDBC, "SpellCastTimes.dbc")
    obj = r and r[1] and r[2]
    if obj ~= nil then
        s.declarations = {
            appel(obj.SetInt32, obj, "Base"),
            appel(obj.SetInt32, obj, "PerLevel"),
            appel(obj.SetInt32, obj, "Minimum"),
        }
        s.load = appel(obj.Load, obj)
        s.GetRecord_1 = appel(obj.GetRecord, obj, 1)
        s.GetRecord_16 = appel(obj.GetRecord, obj, 16)
        s.GetRecord_999999 = appel(obj.GetRecord, obj, 999999)
        s.GetRecordByColumn_Base_1500 = appel(obj.GetRecordByColumn, obj, "Base", 1500)
        s.GetRecordsByColumn_Base_0 = appel(obj.GetRecordsByColumn, obj, "Base", 0)
        -- même chose par la table LuaDBC (forme « non objet »), pour comparaison
        s.LuaDBC_GetRecord_16 = appel(LuaDBC and LuaDBC.GetRecord, obj, 16)
    end

    -- 1c. SpellIcon.dbc : une colonne texte ; recherche par texte.
    local ic = {}
    L.SpellIcon = ic
    _, r = appel(CreateDBC, "SpellIcon.dbc")
    obj = r and r[1] and r[2]
    if obj ~= nil then
        appel(obj.SetString, obj, "TextureFilename")
        ic.load = appel(obj.Load, obj)
        ic.GetRecord_62 = appel(obj.GetRecord, obj, 62)
        ic.recherche_Spell_Nature_Lightning =
            appel(obj.GetRecordByColumn, obj, "TextureFilename", "Interface\\Icons\\Spell_Nature_Lightning")
        -- l'icône du premier sort de la barre d'action, retrouvée par son chemin
        if db.premier_sort_reel then
            local okI, _, _, icone = pcall(GetSpellInfo, db.premier_sort_reel)
            ic.icone_premier_sort = okI and icone or nil
            if okI and type(icone) == "string" then
                ic.recherche_icone_premier_sort = appel(obj.GetRecordByColumn, obj, "TextureFilename", icone)
            end
        end
    end

    -- 1d. ChrClasses.dbc (60 champs) : avec SetLocalizedString (schéma « naïf ») puis
    --     avec le contournement (chaque champ déclaré un par un). Le désassemblage prévoit
    --     que le schéma naïf lit mal toutes les colonnes placées après une colonne localisée.
    local cc = {}
    L.ChrClasses = cc
    _, r = appel(CreateDBC, "ChrClasses.dbc")
    obj = r and r[1] and r[2]
    if obj ~= nil then
        appel(obj.SetUInt32, obj, "Champ01")
        appel(obj.SetUInt32, obj, "DisplayPower")
        appel(obj.SetUInt32, obj, "Champ03")
        appel(obj.SetLocalizedString, obj, "Name")
        appel(obj.SetLocalizedString, obj, "NameFemale")
        appel(obj.SetLocalizedString, obj, "NameMale")
        appel(obj.SetString, obj, "Filename")
        appel(obj.SetUInt32, obj, "SpellClassSet")
        appel(obj.SetUInt32, obj, "Flags")
        appel(obj.SetUInt32, obj, "CinematicSequenceID")
        appel(obj.SetUInt32, obj, "RequiredExpansion")
        cc.naif_load = appel(obj.Load, obj)
        cc.naif_GetRecord_1 = appel(obj.GetRecord, obj, 1)
        cc.naif_GetRecord_16 = appel(obj.GetRecord, obj, 16)
    end
    _, r = appel(CreateDBC, "ChrClasses.dbc")      -- même objet, colonnes remises à zéro
    obj = r and r[1] and r[2]
    if obj ~= nil then
        appel(obj.SetUInt32, obj, "Champ01")
        appel(obj.SetUInt32, obj, "DisplayPower")
        appel(obj.SetUInt32, obj, "Champ03")
        for _, base in ipairs({ "Name", "NameFemale", "NameMale" }) do
            appel(obj.SetString, obj, base .. "_enUS")
            for k = 2, 16 do appel(obj.SetUInt32, obj, base .. "_" .. k) end
            appel(obj.SetUInt32, obj, base .. "_drapeaux")
        end
        appel(obj.SetString, obj, "Filename")
        appel(obj.SetUInt32, obj, "SpellClassSet")
        appel(obj.SetUInt32, obj, "Flags")
        appel(obj.SetUInt32, obj, "CinematicSequenceID")
        appel(obj.SetUInt32, obj, "RequiredExpansion")
        cc.contournement_load = appel(obj.Load, obj)
        local res = {}
        for _, id in ipairs({ 1, 16 }) do
            local ok, t = pcall(obj.GetRecord, obj, id)
            if ok and type(t) == "table" then
                res[tostring(id)] = { ID = t.ID, Name_enUS = t.Name_enUS, Filename = t.Filename,
                                      SpellClassSet = t.SpellClassSet }
            else
                res[tostring(id)] = { erreur = tostring(t) }
            end
        end
        cc.contournement = res
    end
end

---------------------------------------------------------------------------
-- 2. Vrais numéros de sorts : barre, grimoire, infobulles
---------------------------------------------------------------------------
local bulle   -- infobulle privée : n'utilise pas GameTooltip

local function lireBulle(prepare)
    if not bulle then return { erreur = "pas d'infobulle" } end
    local ok, err = pcall(function()
        bulle:SetOwner(UIParent, "ANCHOR_NONE")
        prepare(bulle)
    end)
    local out = { ok = ok, erreur = (not ok) and tostring(err) or nil }
    if ok then
        local okG, nom, rang, id = pcall(bulle.GetSpell, bulle)
        out.GetSpell_nom, out.GetSpell_rang, out.GetSpell_id = nom, rang, id
        local l1 = _G[NOM .. "BulleTextLeft1"]
        out.ligne1 = l1 and l1:GetText()
    end
    pcall(bulle.Hide, bulle)
    return out
end

local function essaiBarre()
    local barre = {}
    db.barre = barre
    for slot = 1, 144 do
        local ok, typ, id, sousType, idGlobal = pcall(GetActionInfo, slot)
        if ok and typ then
            local e = { slot = slot, type = typ, valeur2 = id, valeur3 = sousType, valeur4 = idGlobal }
            if typ == "spell" then
                e.GetSpellInfo_valeur2 = { pcall(GetSpellInfo, id) }               -- l'erreur du test 2
                e.GetSpellInfo_valeur4 = { pcall(GetSpellInfo, idGlobal) }          -- le vrai sort
                local okL, lien = pcall(GetSpellLink, id, sousType == "pet" and "pet" or "spell")
                e.lien_grimoire = okL and lien or nil
                e.id_par_lien_grimoire = idDepuisLien(okL and lien)
                db.premier_sort_reel = db.premier_sort_reel or idGlobal
                if slot <= 12 then
                    e.infobulle_SetAction = lireBulle(function(t) t:SetAction(slot) end)
                end
            elseif typ == "macro" then
                local okM, nomM, rangM = pcall(GetMacroSpell, id)
                e.GetMacroSpell = okM and { nomM, rangM } or nil
                if okM and nomM then
                    local okL, lien = pcall(GetSpellLink, nomM)
                    e.id_par_lien_macro = idDepuisLien(okL and lien)
                end
            end
            barre[#barre + 1] = e
        end
    end
end

local function essaiGrimoire()
    local g = { onglets = {}, sorts = {} }
    db.grimoire = g
    local okN, nbOnglets = pcall(GetNumSpellTabs)
    if not okN or type(nbOnglets) ~= "number" then g.erreur = "GetNumSpellTabs"; return end
    local total = 0
    for onglet = 1, nbOnglets do
        local ok, nom, _, decalage, nb = pcall(GetSpellTabInfo, onglet)
        if ok then
            g.onglets[#g.onglets + 1] = { onglet = onglet, nom = nom, decalage = decalage, nb = nb }
            for i = (decalage or 0) + 1, (decalage or 0) + (nb or 0) do
                total = total + 1
                if total > 400 then break end
                local okS, nomS, rangS = pcall(GetSpellName, i, "spell")
                local okL, lien = pcall(GetSpellLink, i, "spell")
                local e = { case = i, onglet = onglet, nom = okS and nomS or nil, rang = okS and rangS or nil,
                            id = idDepuisLien(okL and lien) }
                if total <= 30 then
                    e.infobulle_SetSpell = lireBulle(function(t) t:SetSpell(i, "spell") end)
                end
                g.sorts[#g.sorts + 1] = e
            end
        end
    end
    g.total = total
end

---------------------------------------------------------------------------
-- 3. Quel Spell.dbc, talents, auras
---------------------------------------------------------------------------
local TEMOINS = {   -- [id] = { nom dans patch-T, nom dans area-52 (patch-D) } ; "" = absent
    [1]     = { "UPDATE YOUR CLIENT!", "UPDATE YOUR CLIENT!" },
    [2120]  = { "Flamestrike", "Flamestrike" },
    [2782]  = { "Remove Curse", "Abolish Curse" },
    [11190] = { "Improved Cone of Cold", "Flash Freeze" },
    [12297] = { "Anticipation", "Adaptive Defense" },
    [12308] = { "Puncture", "Fracture" },
    [1681]  = { "", "Whirlwind" },
    [5572]  = { "Insect Swarm", "" },
}

local function essaiTemoins()
    local t = {}
    db.spell_dbc_temoins = t
    local votesT, votesD = 0, 0
    for id, attendu in pairs(TEMOINS) do
        local ok, nom, rang = pcall(GetSpellInfo, id)
        local vu = (ok and nom) or ""
        t[tostring(id)] = { vu = vu, rang = ok and rang or nil, patchT = attendu[1], area52 = attendu[2] }
        if attendu[1] ~= attendu[2] then
            if vu == attendu[1] then votesT = votesT + 1 end
            if vu == attendu[2] then votesD = votesD + 1 end
        end
    end
    db.spell_dbc_votes = { patchT = votesT, area52 = votesD }
end

local function essaiTalents()
    local ca = {}
    db.talents = ca
    ca.type_C_CharacterAdvancement = type(C_CharacterAdvancement)
    if type(C_CharacterAdvancement) ~= "table" then return end
    for _, fn in ipairs({ "GetKnownTalentEntries", "GetKnownSpellEntries" }) do
        local ok, liste = pcall(C_CharacterAdvancement[fn])
        local d = { ok = ok }
        if ok and type(liste) == "table" then
            d.nombre = #liste
            d.exemples = {}
            for i = 1, math.min(#liste, 5) do
                local e = liste[i]
                local ex = { brut = decrire(e) }
                if type(e) == "table" and type(e.Spells) == "table" and e.Spells[1] then
                    local okI, nomS = pcall(GetSpellInfo, e.Spells[1])
                    ex.sort1 = e.Spells[1]
                    ex.nom_sort1 = okI and nomS or nil
                end
                d.exemples[i] = ex
            end
        else
            d.erreur = tostring(liste)
        end
        ca[fn] = d
    end
end

local function essaiAuras()
    local a = {}
    db.auras = a
    for i = 1, 8 do
        local ok, nom, rang, _, _, _, _, _, _, _, _, idSort = pcall(UnitAura, "player", i, "HELPFUL")
        if not ok or not nom then break end
        a[#a + 1] = { nom = nom, rang = rang, id = idSort }
    end
end

---------------------------------------------------------------------------
-- PARTIE B : essai d'affichage (facultatif, /azfr3 essai)
---------------------------------------------------------------------------
local ESSAI_ID, ESSAI_FR = 2120, "Choc de flammes"
local essaiActif, crochetsPoses = false, false

local function remplacerNom(tip)
    if not essaiActif or not tip or not tip.GetSpell then return end
    local ok, _, _, id = pcall(tip.GetSpell, tip)
    if ok and id == ESSAI_ID then                  -- par numéro prouvé, jamais par le nom seul
        local l1 = tip.GetName and _G[tip:GetName() .. "TextLeft1"]
        if l1 then
            l1:SetText(ESSAI_FR)
            if tip:IsShown() then tip:Show() end   -- recalcule la taille
        end
    end
end

local function essaiAffichage()
    if not crochetsPoses then
        for _, tip in ipairs({ GameTooltip, ItemRefTooltip, bulle }) do
            if tip and tip.HookScript then pcall(tip.HookScript, tip, "OnTooltipSetSpell", remplacerNom) end
        end
        crochetsPoses = true
    end
    essaiActif = true
    local e = {}
    db.essai_affichage = e
    e.GetSpellInfo_avant = { pcall(GetSpellInfo, ESSAI_ID) }
    -- infobulle privée affichée au centre de l'écran pendant 20 secondes
    local ok, err = pcall(function()
        bulle:SetOwner(UIParent, "ANCHOR_NONE")
        bulle:ClearAllPoints()
        bulle:SetPoint("CENTER", UIParent, "CENTER", 0, 120)
        bulle:SetHyperlink("spell:" .. ESSAI_ID)
        bulle:Show()
    end)
    e.affichage_ok = ok
    e.affichage_erreur = (not ok) and tostring(err) or nil
    local l1 = _G[NOM .. "BulleTextLeft1"]
    e.ligne1_affichee = l1 and l1:GetText()
    local okG, nom, rang, id = pcall(bulle.GetSpell, bulle)
    e.GetSpell_de_l_infobulle = { nom, rang, id }
    e.GetSpellInfo_apres = { pcall(GetSpellInfo, ESSAI_ID) }
    local reste = 20
    bulle:SetScript("OnUpdate", function(self, ecoule)
        reste = reste - ecoule
        if reste <= 0 then self:SetScript("OnUpdate", nil); self:Hide() end
    end)
    dire("essai d'affichage actif : l'infobulle du sort " .. ESSAI_ID .. " doit montrer « " .. ESSAI_FR ..
         " ». Tapez /reload pour enregistrer et tout annuler.")
end

---------------------------------------------------------------------------
-- Lancement
---------------------------------------------------------------------------
local function diagnostic()
    db = {}
    AzerothFR_Test3DB = db
    db.date = date("%Y-%m-%d %H:%M:%S")
    db.langue = GetLocale and GetLocale()
    db.version = { GetBuildInfo() }
    db.etapes = {}
    for _, etape in ipairs({
        { "barre", essaiBarre }, { "grimoire", essaiGrimoire }, { "luadbc", essaiLuaDBC },
        { "temoins", essaiTemoins }, { "talents", essaiTalents }, { "auras", essaiAuras },
    }) do
        local ok, err = pcall(etape[2])
        db.etapes[etape[1]] = ok and "ok" or ("erreur : " .. tostring(err))
    end
    dire("diagnostic terminé. Tapez /reload pour enregistrer le résultat.")
end

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_ENTERING_WORLD")
f:SetScript("OnEvent", function(self)
    self:UnregisterAllEvents()
    local okB, b = pcall(CreateFrame, "GameTooltip", NOM .. "Bulle", UIParent, "GameTooltipTemplate")
    bulle = okB and b or nil
    local attente = 3
    self:SetScript("OnUpdate", function(s, ecoule)
        attente = attente - ecoule
        if attente <= 0 then
            s:SetScript("OnUpdate", nil)
            local ok, err = pcall(diagnostic)
            if not ok then dire("erreur : " .. tostring(err)) end
        end
    end)
end)

SLASH_AZEROTHFRTEST31 = "/azfr3"
SlashCmdList["AZEROTHFRTEST3"] = function(msg)
    msg = string.lower(msg or "")
    if msg == "essai" then
        if not db then dire("attendez la fin du diagnostic (3 secondes après l'entrée en jeu).") return end
        local ok, err = pcall(essaiAffichage)
        if not ok then dire("erreur de l'essai : " .. tostring(err)) end
    else
        local ok, err = pcall(diagnostic)
        if not ok then dire("erreur : " .. tostring(err)) end
    end
end
