-- ============================================================================
-- Azeroth_FR : sorts et talents. EMPLACEMENT RESERVE : rien n'est traduit dans l'essai 1.
--
-- Ce que l'analyse du 03/11/2026 a etabli (docs/collecte/2026-11-03_Rapport_LuaDBC-et-sorts.md) :
-- - les sorts se traduiront a l'AFFICHAGE, par numero, sans remplacer aucune fonction du jeu ;
-- - vrais numeros de sorts : barre d'action = 4e valeur de GetActionInfo(case) (la 2e est la
--   case du grimoire + 1) ; grimoire = GetSpellLink(case, "spell") ; infobulle = 3e valeur de
--   GameTooltip:GetSpell() ; auras = 11e valeur d'UnitAura ;
-- - LuaDBC ne fait que LIRE une copie d'un DBC : il ne traduit rien dans le jeu et ne doit pas
--   servir pour Spell.dbc (200 Mo).
-- Les textes des sorts et talents des classes sont tous relus ou retraduits avant d'etre
-- embarques (exigence de Dan) : la famille « sorts » n'existe pas encore dans les donnees.
-- ============================================================================
local A = AzerothFR
A.Sorts = { actif = false, raison = "réservé : pas dans l'essai 1" }
