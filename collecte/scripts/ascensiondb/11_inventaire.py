#!/usr/bin/env python3
"""Q1 : inventaire des familles d'AscensionDB (manifeste du site) annoté pour la traduction.
Usage: python3 -I 11_inventaire.py <manifest.json> <sortie.csv>"""
import csv, json, sys
m = json.load(open(sys.argv[1]))
# famille -> (d'où ça vient, textes affichés aux joueurs, intérêt pour Azeroth_FR)
A = {
 'item': ('caches client WDB (itemcache) + export Exiles', 'nom, description', 'preuve de l\'anglais par numéro (Q3)'),
 'npc': ('caches client WDB (creaturecache) + site Exiles', 'nom, sous-titre', 'preuve de l\'anglais par numéro (Q3)'),
 'gameobject': ('caches client WDB (gameobjectcache) + site Exiles', 'nom, texte de barre d\'incantation', 'preuve par numéro (Q3)'),
 'quest': ('caches client WDB (questcache) + site Exiles', 'titre, objectifs, description, textes de fin, objectifs 1-4', 'preuve par numéro (Q3) ; caches frFR (Q4)'),
 'gossip': ('caches client WDB (npccache)', 'textes de dialogue des PNJ', 'faible : l\'archive les range déjà par texte'),
 'page': ('caches client WDB (pagetextcache)', 'texte des livres et lettres', 'faible : l\'archive les range déjà par texte'),
 'item-name': ('caches client WDB (itemnamecache)', 'nom d\'objet', 'preuve par numéro (Q3)'),
 'spell': ('site Exiles (db.exil.es) + addon de récolte', 'nom, rang, description, infobulle', 'ÉLEVÉ : anglais des sorts par numéro (Q2) ; le Spell.dbc client est dans supplemental/client-dbc-snapshots'),
 'achievement': ('site Exiles', 'nom, description, récompense', 'ÉLEVÉ : anglais des hauts faits (Q2)'),
 'area': ('site Exiles', 'nom de zone', 'moyen : zones (Q2)'),
 'class': ('site Exiles', 'nom de classe', 'faible : déjà couvert'),
 'tree': ('site Exiles (pages d\'arbres de talents)', 'nom d\'arbre, cases (numéro de sort)', 'moyen : les textes sont ceux des sorts'),
 'skill': ('site Exiles', 'nom de compétence', 'moyen'),
 'dbc': ('cachedata/mapdata/dbc.tsv', 'aucun (inventaire de fichiers DBC)', 'nul'),
 'map': ('cachedata/mapdata + site Exiles', 'nom de carte', 'faible'),
 'dungeon': ('site Exiles + addon de récolte', 'nom de donjon', 'faible'),
 'currency': ('site Exiles', 'nom, description', 'faible'),
 'pets': ('site Exiles', 'nom de familier', 'faible'),
 'name': ('site Exiles : index de recherche (type de page, numéro, nom, adresse)', 'noms d\'entités du jeu (vérifié : aucun type joueur/guilde/compte)', 'faible (doublon)'),
 'history': ('site Exiles : historique par entité', 'aucun (dates et scores)', 'faible'),
 'change-log': ('site Exiles : journal quotidien 2026-06-11 -> 2026-08-29', 'anciens et nouveaux textes modifiés', 'moyen : repère les textes changés pendant l\'été 2026 (Q5)'),
 'mirror': ('site Exiles : index SHA-256 des fichiers aspirés', 'aucun', 'nul'),
 'raw-variant': ('caches client WDB : toutes les variantes captées', 'mêmes champs que les caches', 'ÉLEVÉ pour la preuve : toutes les versions d\'un même numéro (Q3)'),
 'listing': ('site Exiles : pages de listes', 'aucun texte propre', 'nul'),
 'planner-item': ('BisBeard (planificateur d\'équipement)', 'noms d\'objets', 'faible'),
 'display-icon': ('DBC client (icônes d\'affichage)', 'aucun', 'nul'),
 'loot-pin': ('addon LootCollector (positions de butin)', 'aucun', 'nul'),
 'source': ('cachedata/sources.tsv (fichiers soumis : royaume, mode, date)', 'aucun', 'nul ; non téléchargé'),
 'world-creature': ('catalogue du monde (addon de relevé)', 'noms', 'faible'),
 'world-object': ('catalogue du monde (addon de relevé)', 'noms', 'faible'),
 'advancement': ('addon de récolte : arbres Character Advancement (royaumes Season 10)', 'nom de case = nom de sort, onglets', 'faible : doublon du Spell.dbc'),
 'vendor': ('addon de récolte', 'aucun texte propre', 'nul'),
 'enum': ('addon de récolte (constantes d\'API)', 'aucun', 'nul'),
 'battleground': ('addon de récolte', 'noms de champs de bataille', 'faible'),
 'gossip-observation': ('addon de récolte (15 dialogues)', 'textes de dialogue', 'faible'),
 'observed': ('addon de récolte (valeurs d\'API observées)', 'aucun', 'nul'),
 'byRealm': ('addon de récolte, par royaume', 'non examiné (non téléchargé)', 'inconnu'),
 'skillCard': ('addon de récolte (API des cartes de compétence)', 'aucun', 'nul'),
 'coa-client-event': ('addon de récolte (5 événements client CoA)', 'aucun', 'nul'),
 'AIO_Client': ('interface poussée par le serveur Ascension (code Lua)', 'textes d\'interface Ascension, 110 traductions frFR', 'faible à moyen (Q5)'),
 'Auctionator': ('addon Auctionator (prix)', 'aucun', 'nul'),
 'apiSurface': ('addon de récolte', 'aucun', 'nul'),
 'roleRequirement': ('addon de récolte', 'aucun', 'nul'),
 'instance-floor': ('cartes d\'étages d\'instances', 'aucun', 'nul'),
 'route-npc': ('planificateur d\'itinéraires Exiles', 'noms de PNJ', 'nul'),
 'route-landmark': ('planificateur d\'itinéraires Exiles', 'noms de repères', 'nul'),
 'recovered-page': ('pages de db.ascension.gg récupérées sur la Wayback Machine', 'pages d\'objets et de sorts (anglais)', 'nul'),
 'guide': ('guides de db.ascension.gg récupérés (Wayback)', 'guides en anglais (saisons Ascension)', 'nul'),
 'home': ('page d\'accueil du site Exiles', 'aucun', 'nul'),
}
with open(sys.argv[2], 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['famille', 'libelle_site', 'enregistrements', 'provenance', 'textes_affiches_aux_joueurs', 'interet_pour_azeroth_fr'])
    for k, v in sorted(m['kinds'].items(), key=lambda x: -x[1]['records']):
        a = A.get(k, ('?', '?', '?'))
        w.writerow([k, v['label'], v['records'], a[0], a[1], a[2]])
print('familles', len(m['kinds']), 'enregistrements', m['records'])
