# -*- coding: utf-8 -*-
"""importer.py : reconstruit la source unique `textes/` depuis les donnees de `collecte/`.

Usage (depuis la racine du depot) :
    python3 -I outils/importer.py            (Windows : py -I outils\\importer.py)
Options :
    --sans-ecrire   calcule tout et affiche le resume, sans toucher a textes/

Ce que fait l'import, dans l'ordre :
1. Relit `textes/` et met de cote toutes les lignes `relu` : elles ne sont JAMAIS ecrasees.
   Si l'anglais d'une ligne relue a change (empreinte differente), la ligne passe en
   `a_revoir` et l'ancien francais relu est garde dans `note`. Une ligne relue dont le
   texte a disparu des sources part dans `textes/orphelins.tsv` (rien n'est perdu).
2. Serveur : l'amorce du croisement (`collecte/donnees/croisement/amorce_traductions.csv.xz`),
   puis les trouvailles d'AscensionDB :
   - `reprises_devenues_sures` : a_revoir -> machine (francais de l'archive) si le controle passe ;
   - `reprises_prouvees_mais_liste_interdite` : reste a_revoir, la proposition va dans `note` ;
   - les autres lignes a_revoir recoivent l'indice de l'archive dans `note` (`a_revoir.csv`).
   Les sorts serveur venus de l'archive passent a_revoir (sorts retraduits a neuf).
3. Client : sorts des 21 classes CoA et des talents (anglais du Spell.dbc d'Ascension, avec ses
   variables), arbres de talents, classes, hauts faits, zones. Tout francais d'archive sur les
   sorts et talents des classes est mis en `a_revoir` (proposition dans `fr`), jamais en machine.
4. Corrections mecaniques et sures du glossaire deja tranche (`glossaire/corrections_sures.tsv`)
   sur les lignes `machine` ; une correction n'est gardee que si le controle passe ensuite.
5. Controle d'entree (outils/controle.py) : une ligne `machine` qui echoue passe `a_revoir`
   avec la raison dans `note` (son francais reste dans `fr` comme proposition).
6. Ecrit un fichier TSV par famille (objets decoupes par tranches fixes), verifie qu'aucun
   fichier ne depasse 45 Mo, et ecrit le resume dans work/etape1/import_resume.json.

Regle d'or : aucune traduction n'est reprise par numero seul ; la preuve est toujours
« meme anglais ».
"""
import csv
import json
import lzma
import os
import re
import sys
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import controle as C  # noqa: E402

csv.field_size_limit(1 << 30)
D = K.COLLECTE

ETAT_AMORCE = {'officiel': 'officiel', 'machine_archive': 'machine', 'a_revoir': 'a_revoir',
               'a_traduire': 'a_traduire', 'technique': 'technique'}
TYPES_SORTS_SERVEUR = ('sort_dbc_serveur', 'coa_description_sort_client')
CLASSES_COA = {  # glossaire herite, section « Classes et specialisations »
    'Barbarian': 'Barbare', 'Witch Doctor': 'Féticheur', 'Felsworn': 'Gangrelige', 'Witch Hunter': 'Chasseur de sorcières',
    'Stormbringer': 'Porte-tempête', 'Knight of Xoroth': 'Chevalier de Xoroth', 'Templar': 'Templier',
    'Bloodmage': 'Mage de sang', 'Chronomancer': 'Chronomancien', 'Necromancer': 'Nécromancien', 'Pyromancer': 'Pyromancien',
    'Starcaller': 'Mande-étoiles', 'Sun Cleric': 'Clerc du soleil', 'Tinker': 'Bricoleur', 'Venomancer': 'Vénomancien',
    'Reaper': 'Faucheur', 'Primalist': 'Primaliste', 'Runemaster': 'Maître des runes',
}
CHAMP_ORDRE = ['LogTitle', 'LogDescription', 'QuestDescription', 'AreaDescription', 'QuestCompletionLog',
               'ObjectiveText1', 'ObjectiveText2', 'ObjectiveText3', 'ObjectiveText4', 'CompletionText', 'RewardText',
               'Greeting', 'name', 'subname', 'castBarCaption', 'description', 'Name', 'NameSubtext', 'Rank',
               'Description', 'ToolTip', 'AuraDescription', 'nom', 'reward', 'male_name', 'female_name', 'area_name',
               'title', 'Subject', 'Body', 'Text', 'MaleText', 'FemaleText', 'OptionText', 'BoxText', 'content_default',
               'Message']
RANG_CHAMP = {c: i for i, c in enumerate(CHAMP_ORDRE)}


# Textes d'interface qui restent TOUJOURS en anglais (etat technique) : valeurs lues ou comparees par
# le code du jeu, ou pieges payes par AscensionFR (Modules/InterfaceUI.lua de l'archive). Dans le doute,
# la cle reste en anglais.
INTERFACE_CLES_TECHNIQUES = {
    'DELETE_ITEM_CONFIRM_STRING': 'mot à taper pour détruire un objet (comparé par le code)',
    'UNITNAME_SUMMON_TITLE1': 'motif analysé par les add-ons de combat',
    'LARGE_NUMBER_SEPERATOR': 'séparateur des nombres',
    'DECIMAL_SEPERATOR': 'séparateur décimal',
    'ITEM_SPELL_TRIGGER_ONEQUIP': 'le client cache des lignes d\'objet en reconnaissant « Equip: » en anglais (piège AscensionFR du 18/07/2026)',
}
INTERFACE_MOTIFS_TECHNIQUES = [
    (re.compile(r'^SLASH_'), 'commande /…'),
    (re.compile(r'_CMD\d*$'), 'commande d\'émote'),
    (re.compile(r'CONFIRM_STRING$'), 'mot à taper (comparé par le code)'),
    (re.compile(r'^UNITNAME_SUMMON_TITLE'), 'motif analysé par les add-ons de combat'),
]
_URL_OU_MAIL = re.compile(r'https?://|www\.|[\w.+-]+@[\w-]+\.[a-z]{2,}', re.I)
_CHEMIN = re.compile(r'\.(?:ttf|blp|tga|mp3|wav|ogg|m2|txt)\b', re.I)


def technique_interface(cle_v, en):
    """Raison pour laquelle un texte d'interface reste en anglais, ou ''."""
    if cle_v in INTERFACE_CLES_TECHNIQUES:
        return 'clé ' + INTERFACE_CLES_TECHNIQUES[cle_v]
    for rx, raison in INTERFACE_MOTIFS_TECHNIQUES:
        if rx.search(cle_v):
            return 'clé ' + raison
    t = en.strip()
    if not re.search(r'[A-Za-z]{2}', K.denuder(t)):
        return 'vide_ou_sans_mot'
    if t.startswith('/'):
        return 'commande'
    if _URL_OU_MAIL.search(t):
        return 'adresse_web'
    if _CHEMIN.search(re.sub(r'\|T[^|]*\|t', '', t)):
        return 'chemin_de_fichier'
    if re.fullmatch(r'[A-Z][A-Z0-9_\-]+', t):
        return 'jeton_en_majuscules'
    if re.search(r'%[^%]', t.replace('%%', '')) and C.specs_printf(t) is not None:
        reste = C._PRINTF.sub('', t.replace('%%', ''))
        if '%' in reste:
            return 'format_de_date_ou_inconnu'
    if C.specs_printf(t) is None:
        return 'format_mixte'
    return ''


def lire_csv_xz(*chemin):
    with lzma.open(os.path.join(D, *chemin), 'rt', encoding='utf-8', newline='') as f:
        yield from csv.DictReader(f)


def joindre(*parts):
    return ' | '.join(p for p in parts if p)


def cite(t, n=300):
    """Cite un texte dans une note (sur une ligne : les retours sont echappes a l'ecriture)."""
    return '« %s »' % t if len(t) <= n else '« %s… »' % t[:n]


def cle(l):
    return (l[K.I_TYPE], l[K.I_ID], l[K.I_SOUS], l[K.I_CHAMP])


def tri(l):
    i = l[K.I_ID]
    s = l[K.I_SOUS]
    return (l[K.I_TYPE], (0, int(i), '') if i.isdigit() else (1, 0, i),
            (0, int(s), '') if s.isdigit() else (1, 0, s), RANG_CHAMP.get(l[K.I_CHAMP], 999), l[K.I_CHAMP])


class Importeur:
    def __init__(self):
        self.lignes = {}               # cle -> ligne (liste de 10 champs)
        self.famille = {}              # cle -> famille (pour les sorts du client)
        self.cr = Counter()            # compte rendu
        self.exemples = defaultdict(list)
        K.charger_lexique()
        self.regles = C.charger_regles()
        self.noms = C.charger_noms()
        self.talents = set()
        self.charger_corrections()
        K.journal('import : %d mots anglais, %d règles de glossaire, %d corrections sûres, %d noms officiels contrôlés'
                  % (len(K.EN_SEUL), len(self.regles), len(self.corrections), self.noms.n))

    def ex(self, cat, l, n=5):
        if len(self.exemples[cat]) < n:
            self.exemples[cat].append({'cle': '/'.join(cle(l)), 'en': l[K.I_EN][:160], 'fr': l[K.I_FR][:160]})

    def ajouter(self, l, famille=None):
        k = cle(l)
        if k in self.lignes:
            self.cr['doublon_ignore'] += 1
            return
        self.lignes[k] = l
        if famille:
            self.famille[k] = famille

    def controle(self, en, fr, etat, type_=None):
        return C.controle(en, fr, etat, self.regles, self.noms, type_)

    # ------------------------------------------------------------------
    # 1. Lignes relues existantes
    # ------------------------------------------------------------------
    def charger_relus(self):
        self.relus = {}
        for p in K.fichiers_textes():
            lignes, err = K.lire_tsv(p)
            if err:
                raise SystemExit('ERREUR : %s illisible (%s). Corrigez le fichier avant de relancer.' % (p, err[:3]))
            for l in lignes:
                if l[K.I_ETAT] == 'relu':
                    self.relus[cle(l)] = l
        K.journal('import : %d lignes relues protégées' % len(self.relus))

    # ------------------------------------------------------------------
    # 2. Serveur
    # ------------------------------------------------------------------
    def charger_indices_serveur(self):
        self.sures, self.interdites, self.indices = {}, {}, {}
        for r in lire_csv_xz('ascensiondb', 'reprises_devenues_sures.csv.xz'):
            self.sures[(r['type'], r['id'], '', r['champ'])] = r
        for r in lire_csv_xz('ascensiondb', 'reprises_prouvees_mais_liste_interdite.csv.xz'):
            self.interdites[(r['type'], r['id'], '', r['champ'])] = r
        nb = Counter()
        for r in lire_csv_xz('croisement', 'a_revoir.csv.xz'):
            k = (r['type'], r['id'], r['sous_id'], r['champ'])
            nb[k] += 1
            old = self.indices.get(k)
            if old is None or (old['controle_qualite'] != 'ok' and r['controle_qualite'] == 'ok'):
                self.indices[k] = r
        self.nb_indices = nb
        K.journal('import : %d reprises sûres, %d prouvées mais interdites, %d lignes avec indice'
                  % (len(self.sures), len(self.interdites), len(self.indices)))

    @staticmethod
    def source_amorce(src, note):
        if src in ('officiel_locale', 'officiel_texte_identique'):
            return 'blizzard_frFR'
        if src in ('archive_sur', 'archive_texte'):
            return 'release_3.5.1' if re.search(r'fichier=(?:fichier=)?release', note) else 'archive_ascensionfr'
        if src == 'modele':
            return 'modele'
        return ''

    def importer_serveur(self):
        self.charger_indices_serveur()
        n = 0
        for r in lire_csv_xz('croisement', 'amorce_traductions.csv.xz'):
            n += 1
            en = r['texte_en']
            l = [r['type'], r['id'], r['sous_id'], r['champ'], en, r['empreinte_en'], r['texte_fr'],
                 ETAT_AMORCE[r['etat']], self.source_amorce(r['source'], r['note']), r['note']]
            if l[K.I_EMP] != K.empreinte(en):
                raise SystemExit('ERREUR : empreinte incohérente dans l\'amorce pour %s' % '/'.join(cle(l)))
            k = cle(l)
            self.cr['serveur_amorce_' + l[K.I_ETAT]] += 1
            if l[K.I_ETAT] == 'a_revoir':
                self.traiter_a_revoir(l, k)
            if l[K.I_TYPE] in TYPES_SORTS_SERVEUR and l[K.I_ETAT] == 'machine':
                l[K.I_ETAT] = 'a_revoir'
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'sort serveur : le français de l\'archive n\'est qu\'une proposition, '
                                                   'les sorts serveur sont retraduits et relus (décision du 03/11/2026)')
                self.cr['sort_serveur_machine_vers_a_revoir'] += 1
            self.ajouter(l)
            if n % 200000 == 0:
                K.journal('import : amorce, %d lignes' % n)
        K.journal('import : amorce terminée, %d lignes' % n)

    def traiter_a_revoir(self, l, k):
        en = l[K.I_EN]
        s = self.sures.get(k)
        if s is not None:
            if K.norm(s['texte_en_coa']) != K.norm(en):
                self.cr['sure_anglais_incoherent'] += 1
                return
            modes = [m for m in s['modes_ascension_meme_anglais'].split(',') if m]
            preuve = ('reprise devenue sûre : anglais Ascension identique au même numéro dans tous les modes captés '
                      '(%d modes%s, %s)' % (len(modes), ', dont conquest-of-azeroth' if 'conquest-of-azeroth' in modes else '',
                                           s['fichier_archive']))
            fr, faites = self.corriger(en, s['texte_fr_archive'])
            refus = self.controle(en, fr, 'machine')
            if refus:
                fr, faites = s['texte_fr_archive'], []
            if not refus:
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'machine', 'archive_ascensionfr'
                l[K.I_NOTE] = joindre(l[K.I_NOTE], preuve,
                                      'correction mécanique du glossaire : ' + ', '.join(faites) if faites else '')
                self.cr['sure_adoptee_machine'] += 1
            else:
                l[K.I_FR] = fr
                l[K.I_SRC] = 'archive_ascensionfr'
                l[K.I_NOTE] = joindre(l[K.I_NOTE], preuve, 'refusée au contrôle d\'entrée : ' + ', '.join(refus))
                self.cr['sure_refusee_controle'] += 1
                self.ex('sure_refusee_controle', l)
            return
        s = self.interdites.get(k)
        if s is not None and K.norm(s['texte_en_coa']) == K.norm(en):
            modes = [m for m in s['modes_ascension_meme_anglais'].split(',') if m]
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'proposition de l\'archive NON adoptée (anglais prouvé identique dans %d modes, '
                                               'mais condamnée par objets_interdits.json) : %s' % (len(modes), cite(s['texte_fr_archive'])))
            self.cr['interdite_proposition_en_note'] += 1
            return
        h = self.indices.get(k)
        if h is not None and h['texte_fr_archive']:
            parts = ['indice de l\'archive (%s, %d candidat%s) : %s' % (h['motif'], self.nb_indices[k],
                                                                   's' if self.nb_indices[k] > 1 else '', cite(h['texte_fr_archive']))]
            if h['motif'] == 'anglais_different' and h['texte_en_archive']:
                parts.append('anglais que traduisait l\'archive : ' + cite(h['texte_en_archive']))
            l[K.I_NOTE] = joindre(l[K.I_NOTE], *parts)
            self.cr['a_revoir_indice_en_note'] += 1

    # ------------------------------------------------------------------
    # 3. Client
    # ------------------------------------------------------------------
    def charger_francais_client(self):
        """Index des francais par anglais IDENTIQUE (normalise), par famille, en ordre de priorite."""
        idx = defaultdict(list)     # (famille, en_norm) -> [(prio, fr, origine, officiel)]
        f_arch = {
            ('sort', 'nom'): ('nom_sort', {'traductions/sorts.json': 1, 'traductions/noms_pont_retraduits.json': 3}),
            ('sort', 'description'): ('desc_sort', {'traductions/sorts.json': 2, 'traductions/cache_noms_incrustes.json': 4}),
            ('sort', 'description_aura'): ('desc_sort', {}),
            ('zone', 'nom'): ('lieu', {'traductions/zones_officielles_id.json': 1}),
            ('zone', 'nom_interieur'): ('lieu', {'traductions/interieurs.json': 2}),
            ('zone', 'point_carte'): ('lieu', {'traductions/poi_carte.json': 3}),
            ('specialisation', 'nom_arbre'): ('arbre_nom', {'traductions/chrspecs.json': 1}),
            ('specialisation', 'description'): ('arbre_desc', {'traductions/chrspecs.json': 1}),
            ('libelle_interface', 'texte'): ('interface', {'traductions/libelles.json': 1}),
            ('interface', 'texte'): ('interface', {'traductions/fenetres_perso.json': 2, 'traductions/gisement_brut.json': 3}),
        }
        exclus = Counter()
        for r in lire_csv_xz('archive', 'traductions_archive_index.csv.xz'):
            m = f_arch.get((r['type'], r['champ']))
            if m is None or r['cle_nature'] != 'texte_en' or not r['texte_en'] or not r['texte_fr']:
                continue
            if r['statut'] not in ('store_vivant', 'cache_de_travail'):
                exclus['statut_' + r['statut']] += 1
                continue
            prio = m[1].get(r['fichier_source'])
            if prio is None:
                continue
            if K.famille_exclue(r['texte_en'], r['texte_fr']):
                exclus['donnee_exclue'] += 1
                continue
            officiel = r['fichier_source'] == 'traductions/zones_officielles_id.json'
            idx[(m[0], K.norm(r['texte_en']))].append((prio, r['texte_fr'], 'archive:' + r['fichier_source'].split('/')[-1], officiel))
        p_rel = {('nom_sort', 'DB_SortsNoms.lua'): 2, ('desc_sort', 'DB_SortsCorrections.lua'): 1,
                 ('desc_sort', 'DB_Sorts.lua'): 3, ('hauts_faits', 'DB_HautsFaits.lua'): 1, ('lieu', 'DB_Zones.lua'): 1,
                 ('interface', 'DB_Libelles.lua'): 1}
        for r in lire_csv_xz('release', 'paires_release_client.csv.xz'):
            prio = p_rel.get((r['famille'], r['fichier_release']))
            if prio is None:
                continue
            officiel = r['fichier_release'] == 'DB_Zones.lua'
            idx[(r['famille'], K.norm(r['texte_en']))].append((prio, r['texte_fr'], 'release:' + r['fichier_release'], officiel))
        for k in idx:
            vus, out = set(), []
            for c in sorted(idx[k], key=lambda x: x[0]):
                if c[1] not in vus:
                    vus.add(c[1])
                    out.append(c)
            idx[k] = out
        self.fr_client = idx
        K.journal('import : index des français du client, %d anglais (%s exclus)' % (len(idx), dict(exclus)))
        filt = os.path.join(K.GLOSSAIRE, 'filtres')
        with open(os.path.join(filt, 'divergences_officielles_decisions.json'), encoding='utf-8') as f:
            self.divergences = json.load(f)
        with open(os.path.join(filt, 'cles_interdites_readoption.json'), encoding='utf-8') as f:
            self.cles_purgees = {K.norm(k): v for k, v in json.load(f).items()}
        with open(os.path.join(filt, 'appariements_officiels_interdits.json'), encoding='utf-8') as f:
            self.app_interdits = {K.norm(k[6:]): v for k, v in json.load(f).items() if k.startswith('texte:')}

    def choisir(self, fam, en):
        """Renvoie (candidat choisi, refus de structure, autre candidat valable)."""
        cands = self.fr_client.get((fam, K.norm(en)), [])
        if not cands:
            return None, None, None
        bons = [c for c in cands if not C.controle_structure(en, c[1])]
        if bons:
            autre = next((c for c in bons[1:] if c[1] != bons[0][1]), None)
            return bons[0], [], autre
        return cands[0], C.controle_structure(en, cands[0][1]), None

    def ligne_client(self, typ, i, champ, en, tech, note_base, fam_fr, regle):
        """regle : 'sort_classe' (a_revoir toujours), 'machine', 'zone'."""
        l = [typ, i, '', champ, en, K.empreinte(en), '', 'a_traduire', '', note_base]
        if tech:
            l[K.I_ETAT] = 'technique'
            l[K.I_NOTE] = joindre(note_base, 'technique=' + tech)
            return l
        en_n = K.norm(en)
        if regle == 'sort_classe':
            if champ in ('Name',) and en_n in self.divergences:
                d = self.divergences[en_n]
                if d['verdict'] == 'adopter':
                    l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = d['officiel'], 'officiel', 'blizzard_frFR'
                    l[K.I_NOTE] = joindre(note_base, 'nom officiel Blizzard (arbitrage hérité, règle %s : adopter)' % d['regle'])
                    self.cr['client_sort_nom_officiel'] += 1
                    return l
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = d['nous'], 'a_revoir', 'archive_ascensionfr'
                l[K.I_NOTE] = joindre(note_base, 'arbitrage hérité (règle %s) : garder notre forme face à l\'officiel %s'
                                      % (d['regle'], cite(d['officiel'])))
                self.cr['client_sort_arbitrage_garder'] += 1
                return l
            m = re.fullmatch(r'Rank (\d+)', en_n)
            if champ == 'Rank' and m:
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = 'Rang ' + m.group(1), 'machine', 'modele'
                l[K.I_NOTE] = joindre(note_base, 'modèle « Rank N » → « Rang N » (usage officiel Blizzard : « (Rank 3) » '
                                                 '→ « (Rang 3) » dans les textes officiels du serveur)')
                self.cr['client_sort_rang_modele'] += 1
                return l
            purge = self.cles_purgees.get(en_n) or self.app_interdits.get(en_n)
            if purge:
                l[K.I_NOTE] = joindre(note_base, 'français de l\'archive écarté : ' + purge)
                self.cr['client_sort_cle_purgee'] += 1
                return l
        c, refus, autre = self.choisir(fam_fr, en)
        if c is None:
            return l
        prio, fr, origine, officiel = c
        src = 'release_3.5.1' if origine.startswith('release:') else 'archive_ascensionfr'
        if regle == 'sort_classe':
            l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'a_revoir', src
            l[K.I_NOTE] = joindre(note_base, 'proposition %s (traduction machine, même anglais) : sorts et talents des classes '
                                             'relus un par un (décision du 03/11/2026)' % origine,
                                  'contrôle : ' + ', '.join(refus) if refus else '',
                                  'autre proposition (%s) : %s' % (autre[2], cite(autre[1])) if autre else '')
            return l
        etat = 'officiel' if (regle == 'zone' and officiel) else 'machine'
        faites = []
        if etat == 'officiel':
            src = 'blizzard_frFR'
        elif not refus:
            fr2, faites = self.corriger(en, fr)
            if faites and not self.controle(en, fr2, etat):
                fr = fr2
            else:
                faites = []
        refus = refus or self.controle(en, fr, etat)
        l[K.I_FR], l[K.I_SRC] = fr, src
        if refus:
            l[K.I_ETAT] = 'a_revoir'
            l[K.I_NOTE] = joindre(note_base, 'proposition %s refusée au contrôle d\'entrée : %s' % (origine, ', '.join(refus)))
            self.cr['client_refus_controle'] += 1
            self.ex('client_refus_controle', l)
        else:
            l[K.I_ETAT] = etat
            quoi = {'release:DB_HautsFaits.lua': 'release 3.5.1 (DB_HautsFaits) : officiel Blizzard ou machine, indiscernable',
                    'release:DB_Zones.lua': 'table ZONES_OFFICIELLES d\'AscensionFR (frFR officiel figé), même anglais',
                    'archive:zones_officielles_id.json': 'zones_officielles_id.json d\'AscensionFR (frFR officiel), même anglais'}
            l[K.I_NOTE] = joindre(note_base, quoi.get(origine, 'proposition %s, même anglais' % origine),
                                  'correction mécanique du glossaire : ' + ', '.join(faites) if faites else '')
        return l

    def importer_client(self):
        self.charger_francais_client()
        arbres = {}
        for r in lire_csv_xz('site-coa', 'talents_classes_en.csv.xz'):
            if r['id_sort']:
                self.talents.add(r['id_sort'])
            if r['champ'] in ('nom_arbre', 'description_arbre'):
                arbres[(r['id'], 'nom' if r['champ'] == 'nom_arbre' else 'description')] = r
        tal_dbc = set()
        for r in lire_csv_xz('ascensiondb', 'textes_client_en.csv.xz'):
            t = r['type']
            if t == 'sort':
                if not r['source'].startswith('Spell.dbc'):
                    continue
                talent = r['id'] in self.talents
                if not talent and r['sort_classe_coa'] != 'oui':
                    continue
                if r['serveur_coa_core'].startswith('meme_id'):
                    self.cr['client_sort_remplace_par_serveur'] += 1
                    continue
                if talent:
                    tal_dbc.add(r['id'])
                fam = 'talents' if talent else 'sorts_classes'
                note = 'Spell.dbc d\'Ascension (été 2026)' + (' ; sort de talent CoA (coa-development.org)' if talent else ' ; sort de classe CoA')
                l = self.ligne_client('sort', r['id'], r['champ'], r['texte_en'], r['technique'], note,
                                      'nom_sort' if r['champ'] in ('Name', 'Rank') else 'desc_sort', 'sort_classe')
                self.ajouter(l, fam)
                self.cr['client_%s_%s' % (fam, l[K.I_ETAT])] += 1
            elif t in ('haut_fait', 'haut_fait_categorie'):
                l = self.ligne_client(t, r['id'], r['champ'], r['texte_en'], r['technique'], 'base db.exil.es (site CoA)',
                                      'hauts_faits', 'machine')
                self.ajouter(l)
                self.cr['client_hauts_faits_' + l[K.I_ETAT]] += 1
            elif t in ('zone', 'carte', 'carte_monde'):
                l = self.ligne_client(t, r['id'], r['champ'], r['texte_en'], r['technique'], 'base db.exil.es (site CoA)',
                                      'lieu', 'zone')
                self.ajouter(l)
                self.cr['client_zones_' + l[K.I_ETAT]] += 1
            elif t == 'classe':
                l = [t, r['id'], '', r['champ'], r['texte_en'], K.empreinte(r['texte_en']), '', 'a_traduire', '',
                     'base db.exil.es (ChrClasses du client)']
                fr = CLASSES_COA.get(K.norm(r['texte_en']))
                if fr and int(r['id']) >= 12:
                    l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'machine', 'glossaire'
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'nom de classe CoA tranché (glossaire hérité d\'AscensionFR)')
                else:
                    l = self.ligne_client(t, r['id'], r['champ'], r['texte_en'], '', l[K.I_NOTE], 'interface', 'machine')
                    if int(r['id']) >= 12 and l[K.I_ETAT] == 'machine':
                        l[K.I_ETAT] = 'a_revoir'
                        l[K.I_NOTE] = joindre(l[K.I_NOTE], 'classe CoA sans décision de glossaire : voir glossaire/A_TRANCHER.md')
                self.ajouter(l, 'talents')
                self.cr['client_classes_' + l[K.I_ETAT]] += 1
            elif t == 'arbre_talents':
                l = self.ligne_client(t, r['id'], r['champ'], r['texte_en'], r['technique'], 'base db.exil.es (TalentTab)',
                                      'arbre_nom', 'sort_classe')
                self.ajouter(l, 'talents')
                self.cr['client_arbres_' + l[K.I_ETAT]] += 1
        for (i, champ), r in sorted(arbres.items()):
            note = 'arbre « %s » (%s) de la classe %s, numéro du site coa-development.org' % (r['arbre'], r['type_arbre'], r['classe'])
            l = self.ligne_client('arbre_coa', i, champ, r['texte_en'], '', note,
                                  'arbre_nom' if champ == 'nom' else 'arbre_desc', 'sort_classe')
            self.ajouter(l, 'talents')
            self.cr['client_arbres_' + l[K.I_ETAT]] += 1
        self.cr['client_talents_sans_texte_spell_dbc'] = len(self.talents - tal_dbc)
        K.journal('import : client terminé (%d sorts de talents dans le Spell.dbc, %d sans texte client propre)'
                  % (len(tal_dbc), len(self.talents - tal_dbc)))

    # ------------------------------------------------------------------
    # 3 bis. Client : textes d'interface (GlobalStrings.dbc), etape 2
    # ------------------------------------------------------------------
    def importer_interface(self):
        """Une ligne par cle de GlobalStrings.dbc (type chaine_interface, id = nom de la variable).

        Le francais n'est repris qu'avec la preuve d'un anglais identique :
        - l'ancien fichier des ecrans de connexion d'AscensionFR (release 3.5.1, francais donne pour
          officiel Blizzard sur les cles standard) : cle identique ET (anglais standard 3.3.5 identique
          OU archive « cle + anglais identiques ») ; jamais si l'archive a note un autre anglais ;
        - l'archive (interface_maison, gisement_brut, fenetres_perso, libelles) : « cle + anglais
          identiques » ou « anglais identique » (rapprochement du rapport client).
        Les cles techniques (commandes, mots a taper, formats de date, chemins, jetons…) restent en anglais.
        """
        vues = Counter()
        n = 0
        for r in lire_csv_xz('client', 'interface_en.csv.xz'):
            if not r['fichier'].endswith('GlobalStrings.dbc'):
                continue
            n += 1
            cle_v, en = r['cle'], r['texte_en']
            vues[cle_v] += 1
            sous = '' if vues[cle_v] == 1 else str(vues[cle_v])
            note = 'GlobalStrings.dbc (%s), %s, %s' % (r['source'], r['contexte'], {
                'standard_335_identique': 'anglais standard 3.3.5', 'standard_335_modifie': 'anglais 3.3.5 modifié',
                'propre_ascension_coa': 'texte propre à Ascension/CoA'}.get(r['anglais_standard_335'], r['anglais_standard_335']))
            l = ['chaine_interface', cle_v, sous, 'texte', en, K.empreinte(en), '', 'a_traduire', '', note]
            tech = technique_interface(cle_v, en)
            if tech:
                l[K.I_ETAT] = 'technique'
                l[K.I_NOTE] = joindre(note, 'technique=' + tech)
                self.ajouter(l)
                self.cr['interface_technique:' + tech.split(' ')[0]] += 1
                continue
            rap = r['rapprochement_archive']
            cands = []
            glue, arch = r['fr_ancien_glue_ascensionfr'], r['fr_archive']
            if glue and 'anglais différent' not in rap and (
                    r['anglais_standard_335'] == 'standard_335_identique' or rap == 'clé + anglais identiques'):
                cands.append((glue, 'release_3.5.1', 'ancien fichier des écrans de connexion d\'AscensionFR (release 3.5.1), '
                              'clé identique, %s' % ('anglais standard 3.3.5' if r['anglais_standard_335'] == 'standard_335_identique'
                                                     else 'anglais prouvé par l\'archive')))
            if arch and rap in ('clé + anglais identiques', 'anglais identique'):
                cands.append((arch, 'archive_ascensionfr', 'archive AscensionFR, ' + rap))
            choisi = None
            refus_vus = []
            for fr, src, preuve in cands:
                fr2, faites = self.corriger(en, fr)
                if faites and not self.controle(en, fr2, 'machine', 'chaine_interface'):
                    fr = fr2
                else:
                    faites = []
                refus = self.controle(en, fr, 'machine', 'chaine_interface')
                if not refus:
                    choisi = (fr, src, preuve, faites)
                    break
                refus_vus.append((fr, src, preuve, refus))
            if choisi:
                fr, src, preuve, faites = choisi
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'machine', src
                autres = [c for c in cands if c[0] != fr]
                l[K.I_NOTE] = joindre(note, preuve,
                                      'correction mécanique du glossaire : ' + ', '.join(faites) if faites else '',
                                      'autre proposition (%s) : %s' % (autres[0][1], cite(autres[0][0])) if autres else '')
                self.cr['interface_machine:' + src] += 1
            elif refus_vus:
                fr, src, preuve, refus = refus_vus[0]
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'a_revoir', src
                l[K.I_NOTE] = joindre(note, preuve, 'refusée au contrôle d\'entrée : ' + ', '.join(refus))
                self.cr['interface_a_revoir_controle'] += 1
                self.ex('interface_refus', l)
            elif glue or arch:
                l[K.I_FR], l[K.I_ETAT] = (arch or glue), 'a_revoir'
                l[K.I_SRC] = 'archive_ascensionfr' if arch else 'release_3.5.1'
                l[K.I_NOTE] = joindre(note, 'proposition sans preuve d\'anglais identique (%s)' % (rap or 'ancien fichier '
                                                                                               'des écrans de connexion, anglais non prouvé'))
                self.cr['interface_a_revoir_sans_preuve'] += 1
            else:
                self.cr['interface_a_traduire'] += 1
            self.ajouter(l)
        K.journal('import : interface, %d clés de GlobalStrings.dbc' % n)

    # ------------------------------------------------------------------
    # 4-5. Corrections mecaniques puis controle d'entree des lignes machine
    # ------------------------------------------------------------------
    def charger_corrections(self):
        self.corrections = []
        p = os.path.join(K.GLOSSAIRE, 'corrections_sures.tsv')
        if not os.path.exists(p):
            return
        with open(p, encoding='utf-8') as f:
            tete = False
            for l in f:
                l = l.rstrip('\n').rstrip('\r')
                if not l or l.startswith('#'):
                    continue
                if not tete:
                    tete = True
                    continue
                nom, garde, motif, rempl = (l.split('\t') + ['', '', '', ''])[:4]
                self.corrections.append((nom, C._rx(garde), C._rx(motif), rempl))

    def corriger(self, en, fr):
        """Applique les corrections sures ; renvoie (francais corrige, noms des corrections faites)."""
        faites = []
        for nom, garde, motif, rempl in self.corrections:
            if garde is not None and not (garde.search(en) or garde.search(K.denuder(en))):
                continue
            if motif.search(fr):
                fr2 = motif.sub(lambda m: rempl, fr)
                if fr2 != fr:
                    fr = fr2
                    faites.append(nom)
        return fr, faites

    def corriger_et_controler(self):
        cpt = Counter()
        for k, l in self.lignes.items():
            if l[K.I_ETAT] != 'machine':
                continue
            en, typ = l[K.I_EN], l[K.I_TYPE]
            fr, faites = self.corriger(en, l[K.I_FR])
            if faites:
                if not self.controle(en, fr, 'machine', typ):
                    l[K.I_FR] = fr
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'correction mécanique du glossaire : ' + ', '.join(faites))
                    for n in faites:
                        cpt['corrigee:' + n] += 1
                    self.ex('correction:' + faites[0], l, 3)
                else:
                    for n in faites:
                        cpt['correction_annulee_controle:' + n] += 1
            refus = self.controle(l[K.I_EN], l[K.I_FR], 'machine', typ)
            if refus:
                l[K.I_ETAT] = 'a_revoir'
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'refusée au contrôle d\'entrée de l\'étape 1 : ' + ', '.join(refus))
                for r in set(x.split(':')[0] if x.startswith('nom_officiel') else x for x in refus):
                    cpt['refus:' + r] += 1
                cpt['machine_vers_a_revoir'] += 1
                self.ex('refus:' + refus[0].split(':')[0], l, 8)
        self.cr.update(cpt)
        K.journal('import : corrections et contrôle %s' % dict(cpt))

    # ------------------------------------------------------------------
    # 1 bis. Fusion avec les lignes relues
    # ------------------------------------------------------------------
    def fusionner_relus(self):
        self.orphelins = []
        for k, rl in self.relus.items():
            l = self.lignes.get(k)
            if l is None:
                self.orphelins.append(rl)
                continue
            if rl[K.I_EMP] == l[K.I_EMP]:
                self.lignes[k] = rl
                self.cr['relu_conserve'] += 1
            else:
                l[K.I_ETAT] = 'a_revoir'
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'anglais modifié depuis la relecture ; ancien français relu : %s ; '
                                                   'ancien anglais : %s' % (cite(rl[K.I_FR], 2000), cite(rl[K.I_EN], 2000)))
                self.cr['relu_anglais_modifie'] += 1
        self.cr['relu_orphelin'] = len(self.orphelins)

    # ------------------------------------------------------------------
    # 6. Ecriture
    # ------------------------------------------------------------------
    def famille_de(self, k, l):
        f = self.famille.get(k)
        if f:
            return f
        t = l[K.I_TYPE]
        for fam, _, types, _ in K.FAMILLES:
            if t in types and fam not in ('sorts_classes', 'talents'):
                return fam
        raise SystemExit('ERREUR : type sans famille : %s' % t)

    def ecrire(self, ecrire=True):
        par_fichier = defaultdict(list)
        cibles = {fam: cible for fam, cible, _, _ in K.FAMILLES}
        for k, l in self.lignes.items():
            fam = self.famille_de(k, l)
            cible = cibles[fam]
            if fam == 'objets':
                cible = cible + '/' + K.fichier_tranche_objets(int(l[K.I_ID]))
            par_fichier[cible].append(l)
        tailles = {}
        attendus = set()
        for cible, ls in sorted(par_fichier.items()):
            ls.sort(key=tri)
            chemin = os.path.join(K.TEXTES, *cible.split('/'))
            attendus.add(os.path.normpath(chemin))
            if ecrire:
                tailles[cible] = K.ecrire_tsv(chemin, ls)
                if tailles[cible] > K.TAILLE_MAX:
                    raise SystemExit('ERREUR : %s dépasse 45 Mo (%d octets) : ajoutez une tranche.' % (cible, tailles[cible]))
            K.journal('import : %-45s %8d lignes %s' % (cible, len(ls), ('%.1f Mo' % (tailles[cible] / 1e6)) if ecrire else ''))
        orph = os.path.join(K.TEXTES, 'orphelins.tsv')
        if self.orphelins:
            attendus.add(os.path.normpath(orph))
            if ecrire:
                K.ecrire_tsv(orph, sorted(self.orphelins, key=tri))
        if ecrire:
            for p in K.fichiers_textes():
                if os.path.normpath(p) not in attendus:
                    K.journal('import : fichier inattendu laissé en place (à vérifier) : %s' % p)
        return tailles

    def resume(self, tailles):
        etats = Counter()
        for l in self.lignes.values():
            etats[l[K.I_ETAT]] += 1
        res = {'lignes': len(self.lignes), 'etats': dict(etats), 'compte_rendu': dict(sorted(self.cr.items())),
               'tailles_octets': tailles, 'exemples': self.exemples}
        os.makedirs(K.TRAVAIL, exist_ok=True)
        with open(os.path.join(K.TRAVAIL, 'import_resume.json'), 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
        K.journal('import : %d lignes, états %s' % (len(self.lignes), dict(etats)))
        return res


def main():
    ecrire = '--sans-ecrire' not in sys.argv
    imp = Importeur()
    imp.charger_relus()
    imp.importer_serveur()
    imp.importer_client()
    imp.importer_interface()
    imp.corriger_et_controler()
    imp.fusionner_relus()
    tailles = imp.ecrire(ecrire)
    imp.resume(tailles)


if __name__ == '__main__':
    main()
