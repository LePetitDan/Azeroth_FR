-- Azeroth_FR : diagnostic en lecture seule.
-- Il examine l'outil LuaDBC du client et les sorts de la barre d'action, puis range le
-- résultat dans WTF\...\SavedVariables\AzerothFR_Diag.lua (écrit à la déconnexion ou au /reload).
-- Aucune fonction d'écriture (Set...) n'est appelée. Pour annuler : supprimer le dossier
-- Interface\AddOns\AzerothFR_Diag.

local function pack(...) return { n = select("#", ...), ... } end

local function decrire(v, profondeur)
    profondeur = profondeur or 0
    local t = type(v)
    if t == "table" then
        local d = { type = "table", cles = {} }
        local n = 0
        for k, val in pairs(v) do
            n = n + 1
            if n <= 60 then
                if profondeur < 1 and (type(val) == "table") then
                    d.cles[tostring(k)] = decrire(val, profondeur + 1)
                else
                    d.cles[tostring(k)] = type(val) .. " : " .. tostring(val)
                end
            end
        end
        d.nombre = n
        local ok, mt = pcall(getmetatable, v)
        if ok and type(mt) == "table" then
            d.meta = {}
            for k, val in pairs(mt) do d.meta[tostring(k)] = type(val) end
            if type(mt.__index) == "table" then
                d.meta_index = {}
                for k, val in pairs(mt.__index) do d.meta_index[tostring(k)] = type(val) end
            end
        end
        return d
    elseif t == "userdata" then
        local d = { type = "userdata", texte = tostring(v) }
        local ok, mt = pcall(getmetatable, v)
        if ok and type(mt) == "table" then
            d.meta = {}
            for k, val in pairs(mt) do d.meta[tostring(k)] = type(val) end
            if type(mt.__index) == "table" then
                d.meta_index = {}
                for k, val in pairs(mt.__index) do d.meta_index[tostring(k)] = type(val) end
            end
        end
        return d
    else
        return t .. " : " .. tostring(v)
    end
end

local function essai(db, nom, fn, ...)
    if type(fn) ~= "function" then
        db.essais[nom] = "pas une fonction"
        return nil
    end
    local r = pack(pcall(fn, ...))
    local out = { ok = tostring(r[1]), n = r.n - 1 }
    for i = 2, math.min(r.n, 6) do
        out["resultat" .. (i - 1)] = decrire(r[i])
    end
    db.essais[nom] = out
    if r[1] then return r[2] end
    return nil
end

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:SetScript("OnEvent", function(self)
    self:UnregisterAllEvents()
    local db = { essais = {}, sorts_barre = {} }
    AzerothFR_DiagDB = db
    db.date = date("%Y-%m-%d %H:%M:%S")
    db.langue = GetLocale and GetLocale()
    db.version = { GetBuildInfo() }
    db.LuaDBC = decrire(LuaDBC)

    -- Sorts de la barre d'action : numéro, nom et rang tels que le jeu les voit.
    local premier
    for slot = 1, 12 do
        local typ, id = GetActionInfo(slot)
        if typ == "spell" and id then
            local nom, rang = GetSpellInfo(id)
            db.sorts_barre[#db.sorts_barre + 1] = { slot = slot, id = id, nom = nom, rang = rang }
            premier = premier or id
        end
    end
    db.premier_sort = premier

    local L = LuaDBC
    if type(L) == "table" then
        -- Appels sans argument : les messages d'erreur donnent souvent la façon de s'en servir.
        for _, nom in ipairs({ "Load", "GetRecord", "GetRecordByColumn", "GetRecordsByColumn" }) do
            essai(db, nom .. "()", L[nom])
        end
        -- Ouverture de la table des sorts sous plusieurs noms possibles.
        local poignee
        for _, nomTable in ipairs({ "Spell", "Spell.dbc", "DBFilesClient\\Spell.dbc", "DBFilesClient/Spell.dbc" }) do
            local p = essai(db, "Load(" .. nomTable .. ")", L.Load, nomTable)
            if p ~= nil and poignee == nil then poignee = p; db.nom_table_qui_marche = nomTable end
        end
        essai(db, "Load(GlobalStrings)", L.Load, "GlobalStrings")
        -- Lecture d'un enregistrement : sur la poignée, puis par nom de table.
        local id = premier or 133
        db.id_lu = id
        if poignee ~= nil then
            if type(poignee) == "table" or type(poignee) == "userdata" then
                local ok, meth = pcall(function() return poignee.GetRecord end)
                if ok and type(meth) == "function" then
                    essai(db, "poignee:GetRecord(id)", meth, poignee, id)
                end
            end
            essai(db, "GetRecord(poignee, id)", L.GetRecord, poignee, id)
        end
        essai(db, "GetRecord(Spell, id)", L.GetRecord, "Spell", id)
        essai(db, "GetRecordByColumn(Spell, ID, id)", L.GetRecordByColumn, "Spell", "ID", id)
    end

    if DEFAULT_CHAT_FRAME then
        DEFAULT_CHAT_FRAME:AddMessage("|cff33ff99Azeroth_FR (diagnostic)|r : termine. Tapez /reload pour enregistrer le resultat.")
    end
end)
