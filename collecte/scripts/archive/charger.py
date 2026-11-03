# -*- coding: utf-8 -*-
"""Lecture commune des fichiers de traductions/ de l'archive AscensionFR.
Produit une liste d'enregistrements normalises (une ligne par texte francais).
Aucun script de l'archive n'est execute : on lit seulement les JSON."""
import json, os

def _L(d, f):
    with open(os.path.join(d, f), encoding='utf-8') as fh:
        return json.load(fh)

CHAMPS_QUETE = {'T': 'titre', 'O': 'objectifs', 'D': 'description', 'A': 'texte_fin_journal',
                'P': 'progression', 'R': 'recompense', 'F': 'texte_fin'}

def enregistrements(d):
    """Genere des dicts : type, cle_nature, cle, champ, texte_en, texte_fr, fichier, statut, note."""
    R = []
    def add(type_, nature, cle, champ, en, fr, fichier, statut='store_vivant', note=''):
        R.append(dict(type=type_, cle_nature=nature, cle=str(cle), champ=champ,
                      texte_en=en or '', texte_fr=fr, fichier_source='traductions/' + fichier,
                      statut=statut, note=note))
    # --- fichiers indexes par identifiant numerique ---
    q = _L(d, 'quetes.json')
    for qid, e in q.items():
        for k, v in e.items():
            if k == 'OT':
                for i, x in enumerate(v, 1):
                    if x:
                        add('quete', 'id_quete', qid, 'objectif_%d' % i, '', x, 'quetes.json')
            else:
                add('quete', 'id_quete', qid, CHAMPS_QUETE.get(k, k), '', v, 'quetes.json')
    for f, t, nat, champs in (('objets.json', 'objet', 'id_objet', {'N': 'nom', 'D': 'description'}),
                              ('creatures.json', 'creature', 'id_creature', {'N': 'nom', 'S': 'sous_titre'}),
                              ('objets_monde.json', 'objet_monde', 'id_objet_monde', {'N': 'nom'}),
                              ('sorts_recoltes.json', 'sort', 'id_sort', {'N': 'nom', 'D': 'description'})):
        for i, e in _L(d, f).items():
            for k, v in e.items():
                add(t, nat, i, champs.get(k, k), '', v, f)
    # --- fichiers indexes par texte anglais ---
    s = _L(d, 'sorts.json')
    for en, fr in s['noms'].items():
        add('sort', 'texte_en', en, 'nom', en, fr, 'sorts.json')
    for en, fr in s['descriptions'].items():
        add('sort', 'texte_en', en, 'description', en, fr, 'sorts.json')
    o = _L(d, 'objets_dbc.json')
    for en, fr in o['noms'].items():
        add('objet', 'texte_en', en, 'nom', en, fr, 'objets_dbc.json')
    for en, fr in o['descriptions'].items():
        add('objet', 'texte_en', en, 'description', en, fr, 'objets_dbc.json')
    simples = [('divers.json', 'divers', 'texte'), ('gossip.json', 'dialogue_option', 'texte'),
               ('textes_pnj.json', 'dialogue_pnj', 'texte'), ('pages.json', 'page_livre', 'texte'),
               ('gisement_brut.json', 'interface', 'texte'), ('libelles.json', 'libelle_interface', 'texte'),
               ('taxinodes.json', 'point_de_vol', 'nom'), ('zones_officielles_id.json', 'zone', 'nom')]
    for f, t, champ in simples:
        for en, fr in _L(d, f).items():
            add(t, 'texte_en', en, champ, en, fr, f)
    paires = [('boss.json', 'boss', 'nom'), ('enchantements.json', 'enchantement', 'texte'),
              ('ensembles.json', 'ensemble_objets', 'nom'), ('fenetres_perso.json', 'interface', 'texte'),
              ('interieurs.json', 'zone', 'nom_interieur'), ('poi_carte.json', 'zone', 'point_carte'),
              ('vanity_obtention.json', 'collection', 'texte_obtention')]
    for f, t, champ in paires:
        for en, fr in _L(d, f)['paires'].items():
            add(t, 'texte_en', en, champ, en, fr, f)
    cs = _L(d, 'chrspecs.json')
    for en, fr in cs['arbres'].items():
        add('specialisation', 'texte_en', en, 'nom_arbre', en, fr, 'chrspecs.json')
    for en, fr in cs['descriptions'].items():
        add('specialisation', 'texte_en', en, 'description', en, fr, 'chrspecs.json')
    fe = _L(d, 'fetes.json')
    for en, fr in fe['noms'].items():
        add('fete', 'texte_en', en, 'nom', en, fr, 'fetes.json')
    for en, fr in fe['descriptions'].items():
        add('fete', 'texte_en', en, 'description', en, fr, 'fetes.json')
    em = _L(d, 'emotes.json')
    for k, e in em['commandes'].items():
        add('emote', 'etiquette_globalstring', k, 'commande', e.get('en', ''), e.get('fr', ''), 'emotes.json',
            note='jeton=%s' % e.get('jeton', ''))
    for en, fr in em['tchat'].items():
        add('emote', 'texte_en', en, 'phrase_tchat', en, fr, 'emotes.json')
    # --- etiquettes d'interface (cle = nom de variable globale) ---
    g = _L(d, 'gisement_brut.json')
    fr2en = {}
    for en, fr in g.items():
        fr2en.setdefault(fr, set()).add(en)
    for k, fr in _L(d, 'interface_maison.json').items():
        ens = fr2en.get(fr, set())
        en = next(iter(ens)) if len(ens) == 1 else ''
        note = 'texte_en deduit de gisement_brut (valeur FR unique)' if en else (
            'texte_en ambigu dans gisement_brut' if ens else 'texte_en absent')
        add('interface', 'etiquette_globalstring', k, 'texte', en, fr, 'interface_maison.json',
            statut='fichier_reconstruit', note=note)
    for k, fr in _L(d, 'glue_classes_manuel.json').items():
        add('interface_connexion', 'etiquette_globalstring', k, 'texte', '', fr, 'glue_classes_manuel.json')
    # --- copies / caches de travail ---
    for en, fr in _L(d, 'cache_noms_incrustes.json').items():
        add('sort', 'texte_en', en, 'description', en, fr, 'cache_noms_incrustes.json',
            statut='cache_de_travail', note='retraduction des noms incrustes ; recoupe sorts.json')
    for e in _L(d, 'noms_pont_retraduits.json'):
        add('sort', 'texte_en', e['en'], 'nom', e['en'], e['fr'], 'noms_pont_retraduits.json',
            statut='cache_de_travail', note='copie de sorts.json (noms)')
    # --- jamais posees en jeu ---
    rn = _L(d, 'recolte_non_posee.json')
    for k, fr in rn['quetes'].items():
        qid, champ = k.split(':')
        add('quete', 'id_quete', qid, CHAMPS_QUETE.get(champ, champ), '', fr, 'recolte_non_posee.json',
            statut='jamais_pose')
    for en, fr in rn['textes_pnj'].items():
        add('dialogue_pnj', 'texte_en', en, 'texte', en, fr, 'recolte_non_posee.json', statut='jamais_pose')
    for en, fr in rn['gossip'].items():
        add('dialogue_option', 'texte_en', en, 'texte', en, fr, 'recolte_non_posee.json', statut='jamais_pose')
    for sid, e in rn['corrections_sorts'].items():
        add('sort', 'id_sort', sid, 'description_aura', e['en'], e['fr'], 'recolte_non_posee.json',
            statut='jamais_pose')
    # --- propositions de joueurs (non arbitrees) ---
    for k, e in _L(d, 'propositions_joueurs.json').items():
        for prop, n in e['propositions'].items():
            add('proposition_joueur', e['cible'], e['id'] if e['id'] is not None else e['actuel'],
                'proposition', e['actuel'] if e['cible'] in ('texte', 'interface') else '', prop,
                'propositions_joueurs.json', statut='proposition_non_arbitree',
                note='texte affiche au moment du signalement=%s' % e['actuel'][:120])
    return R

FICHIERS_CONTROLE = ['appariements_officiels_interdits.json', 'cles_interdites_readoption.json',
                     'divergences_officielles_decisions.json', 'objets_interdits.json',
                     'lignes_client_proposees.json', 'recolte_ecartes.json', 'rejets_chroniques.json',
                     'sorts_exceptions_visibilite.json', 'sorts_objet_tdb.json', 'sorts_references.json']
