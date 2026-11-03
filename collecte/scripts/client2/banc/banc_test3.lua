-- Banc d'essai hors jeu pour AzerothFR_Test3.lua (Lua 5.1) : fausses fonctions du jeu,
-- uniquement pour repérer les erreurs d'exécution du code. Ne prouve rien sur le vrai client.
local journal = {}
local function trace(...) journal[#journal+1] = table.concat({...}, " ") end

-- LuaDBC simulé (même convention que le désassemblage : objet userdata, métatable LuaDBC)
LuaDBC = {}
LuaDBC.__index = LuaDBC
local objets = {}
function CreateDBC(nom)
  local o = objets[nom]
  if not o then o = { nom = nom, cols = {}, n = 0 }; objets[nom] = o end
  o.cols, o.n = {}, 0
  local u = newproxy(false)
  debug.setmetatable(u, LuaDBC)
  objets[u] = o
  return u
end
local function decl(w) return function(self, nom) local o = objets[self]; if not o then return end; o.cols[#o.cols+1] = nom; o.n = o.n + w end end
LuaDBC.SetInt32, LuaDBC.SetUInt32, LuaDBC.SetFloat, LuaDBC.SetString = decl(1), decl(1), decl(1), decl(1)
LuaDBC.SetLocalizedString = decl(17)
local CHAMPS = { ["SpellCastTimes.dbc"] = 4, ["SpellIcon.dbc"] = 2, ["ChrClasses.dbc"] = 60 }
function LuaDBC.Load(self)
  local o = objets[self]; if not o then return end
  if o.n + 1 ~= CHAMPS[o.nom] then error("DBFilesClient\\" .. o.nom .. " has wrong number of columns (found " .. CHAMPS[o.nom] .. ", expected " .. (o.n+1) .. ")") end
end
function LuaDBC.GetRecord(self, id) local o = objets[self]; if not o then return end
  if id == 999999 then return nil end
  local t = { ID = id }; for _, c in ipairs(o.cols) do t[c] = 0 end; return t end
function LuaDBC.GetRecordByColumn(self, c, v) return LuaDBC.GetRecord(self, 16) end
function LuaDBC.GetRecordsByColumn(self, c, v) return LuaDBC.GetRecord(self, 1), LuaDBC.GetRecord(self, 2) end

-- API du jeu simulée
function issecurevariable() return 1 end
function GetLocale() return "enUS" end
function GetBuildInfo() return "3.3.5", "12340", "Jun 24 2010", 30300 end
function date() return "2026-11-03 20:00:00" end
local barre = { [1] = {"spell", 20, "spell", 403}, [2] = {"spell", 1, "spell", 324}, [3] = {"macro", 5}, [5] = {"item", 6948} }
function GetActionInfo(s) local b = barre[s]; if b then return unpack(b) end end
function GetSpellInfo(id, livre) if id == 403 then return "Lightning Bolt", "Rank 1", "Interface\\Icons\\Spell_Nature_Lightning" end return "Sort" .. tostring(id), "", "Interface\\Icons\\X" end
function GetSpellLink(id, livre) if type(id) == "string" then return "|cff71d5ff|Hspell:403|h[Lightning Bolt]|h|r" end return "|cff71d5ff|Hspell:" .. (id * 10) .. "|h[x]|h|r" end
function GetMacroSpell(i) return "Lightning Bolt", "Rank 1" end
function GetNumSpellTabs() return 2 end
function GetSpellTabInfo(t) return "Onglet" .. t, "tex", (t-1)*5, 5 end
function GetSpellName(i, livre) return "Sort" .. i, "Rank 1" end
function UnitAura(u, i, f) if i <= 2 then return "Aura" .. i, "", "ic", 0, nil, 0, 0, "player", nil, nil, 1000 + i end end
C_CharacterAdvancement = { GetKnownTalentEntries = function() return { { ID = 7, Type = "Talent", Spells = { 403 } } } end,
                           GetKnownSpellEntries = function() error("boum") end }
local function nouveauCadre(nom)
  local c = { scripts = {}, shown = false }
  function c:RegisterEvent() end
  function c:UnregisterAllEvents() end
  function c:SetScript(k, f) self.scripts[k] = f end
  function c:HookScript(k, f) local old = self.scripts[k]; self.scripts[k] = function(...) if old then old(...) end; f(...) end end
  function c:GetName() return nom end
  function c:SetOwner() end
  function c:ClearAllPoints() end
  function c:SetPoint() end
  function c:Show() self.shown = true end
  function c:Hide() self.shown = false end
  function c:IsShown() return self.shown end
  function c:SetAction(s) local _, _, _, id = GetActionInfo(s); self.sid = id; if self.scripts.OnTooltipSetSpell then self.scripts.OnTooltipSetSpell(self) end end
  function c:SetSpell(i) self.sid = i * 10; if self.scripts.OnTooltipSetSpell then self.scripts.OnTooltipSetSpell(self) end end
  function c:SetHyperlink(l) self.sid = tonumber(l:match("spell:(%d+)")); _G[nom .. "TextLeft1"].t = "Flamestrike"; if self.scripts.OnTooltipSetSpell then self.scripts.OnTooltipSetSpell(self) end end
  function c:GetSpell() return "Flamestrike", "Rank 1", self.sid end
  if nom then _G[nom] = c; _G[nom .. "TextLeft1"] = { t = "", SetText = function(s, x) s.t = x end, GetText = function(s) return s.t end } end
  return c
end
UIParent = nouveauCadre("UIParent")
GameTooltip = nouveauCadre("GameTooltip")
ItemRefTooltip = nouveauCadre("ItemRefTooltip")
local cadres = {}
function CreateFrame(typ, nom) local c = nouveauCadre(nom); cadres[#cadres+1] = c; return c end
DEFAULT_CHAT_FRAME = { AddMessage = function(_, m) trace("CHAT", m) end }
SlashCmdList = {}

dofile(arg[1])
local f = cadres[1]
f.scripts.OnEvent(f, "PLAYER_ENTERING_WORLD")
f.scripts.OnUpdate(f, 3.5)
SlashCmdList["AZEROTHFRTEST3"]("essai")
local b = _G["AzerothFR_Test3Bulle"]; if b.scripts.OnUpdate then b.scripts.OnUpdate(b, 25) end

-- sortie : étapes, quelques valeurs clés
local db = AzerothFR_Test3DB
for k, v in pairs(db.etapes) do print("etape", k, v) end
print("premier_sort_reel", db.premier_sort_reel)
print("schema faux:", db.LuaDBC.SpellCastTimes.load_schema_faux.ok, db.LuaDBC.SpellCastTimes.load_schema_faux.erreur)
print("metatable LuaDBC:", db.LuaDBC.SpellCastTimes.metatable_est_LuaDBC)
print("contournement 16:", db.LuaDBC.ChrClasses.contournement["16"].ID)
print("barre[1] valeur4:", db.barre[1].valeur4, "lien:", db.barre[1].id_par_lien_grimoire, "bulle:", db.barre[1].infobulle_SetAction.GetSpell_id)
print("votes:", db.spell_dbc_votes.patchT, db.spell_dbc_votes.area52)
print("talents:", db.talents.GetKnownTalentEntries.nombre, db.talents.GetKnownSpellEntries.erreur)
print("essai ligne1:", db.essai_affichage.ligne1_affichee, "GetSpellInfo apres:", db.essai_affichage.GetSpellInfo_apres[2])
print("bulle cachée après 20 s:", not b.shown)
for _, l in ipairs(journal) do print(l) end
