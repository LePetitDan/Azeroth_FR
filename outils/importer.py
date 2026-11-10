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
5 bis. Noms d'enchantements propres a CoA (decision n° 14 de Dan, 04/11/2026) : francais du modele officiel de
   Blizzard, au nombre pres, regles strictes de outils/modele_officiel.py (etat machine, source modele_officiel).
6 bis. Fusion des lignes relues (etape 1), puis de la COUCHE DES TRADUCTIONS DE CLAUDE (atelier du 05/11/2026,
   `traductions/<famille>/<lot>.tsv`, outils/couche.py) : jamais sur officiel, relu ni technique ; empreinte de
   l'anglais identique et controle d'entree passe -> machine, source claude ; anglais change -> a_revoir avec
   l'ancien francais de Claude en note ; refusee -> etat d'avant, refus dans work/etape1/couche_refus.tsv.
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
import unicodedata
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import controle as C  # noqa: E402
import officiel as O  # noqa: E402
import vocabulaire as V  # noqa: E402
import quetes_cata as Q  # noqa: E402
import modele_officiel as MO  # noqa: E402
import couche as CO  # noqa: E402

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
    # décision de vocabulaire n° 7 de Dan (03/11/2026) : les formes de l'ancien projet, pas celles de Blizzard
    'Guardian': 'Gardien', 'Ranger': 'Rôdeur', 'Cultist': 'Cultiste',
}
# Decision de vocabulaire n° 17 de Dan (04/11/2026) : classes CoA accordees au feminin, comme Blizzard (Guerriere,
# Chasseresse). Invariables : Barbare, Gangrelige, Porte-tempete, Mage de sang, Cultiste, Mande-etoiles, Clerc du soleil,
# Primaliste ; Chevalier de Xoroth reste invariable comme l'officiel « Chevalier de la mort » du client 3.3.5.
CLASSES_COA_F = {
    'Hero': 'Héroïne', 'Witch Doctor': 'Féticheuse', 'Witch Hunter': 'Chasseuse de sorcières', 'Guardian': 'Gardienne',
    'Templar': 'Templière', 'Ranger': 'Rôdeuse', 'Chronomancer': 'Chronomancienne', 'Necromancer': 'Nécromancienne',
    'Pyromancer': 'Pyromancienne', 'Tinker': 'Bricoleuse', 'Venomancer': 'Vénomancienne', 'Reaper': 'Faucheuse',
    'Runemaster': 'Maîtresse des runes',
    'Barbarian': 'Barbare', 'Felsworn': 'Gangrelige', 'Stormbringer': 'Porte-tempête', 'Bloodmage': 'Mage de sang',
    'Cultist': 'Cultiste', 'Starcaller': 'Mande-étoiles', 'Sun Cleric': 'Clerc du soleil', 'Primalist': 'Primaliste',
    'Knight of Xoroth': 'Chevalier de Xoroth',
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
# Add-on 0.5 (essai 4, « Le coup Timber Wolf's touche… ») : formes du JOURNAL DE COMBAT. Ces cles seraient
# « techniques » (sans mot, ou drapeau) ; elles prennent le francais officiel de Blizzard quand il differe de l'anglais
# ET que le code du client CoA (patch-B, AddOns/Blizzard_CombatLog/Blizzard_CombatLog.lua, chargee a la demande)
# s'en sert comme texte ou comme drapeau. Verifie le 05/11/2026 : toutes les autres cles techniques lues par ce
# fichier (ACTION_*_POSSESSIVE « 0 »/« 1 », TEXT_MODE_A_STRING_2/3, …) ont un officiel identique a l'anglais ;
# TEXT_MODE_A_STRING_POSSESSIVE_STRING (« 's » / « |2  ») differe mais n'est lu par aucun code du client.
INTERFACE_JOURNAL_COMBAT = {
    'TEXT_MODE_A_STRING_POSSESSIVE': 'possessif du journal de combat, Blizzard_CombatLog.lua (patch-B) l. 2926 et 2931 : '
                                     'format(TEXT_MODE_A_STRING_POSSESSIVE, nom) ; « |2 » résolu par le client (essai 4)',
    'TEXT_MODE_A_STRING_1': 'ordre des morceaux du journal de combat, Blizzard_CombatLog.lua (patch-B) l. 2206 et 2665 '
                            '(formatString hors mode « texte complet »)',
    'COMBAT_LOG_UNIT_YOU_ENABLED': 'drapeau du journal de combat, Blizzard_CombatLog.lua (patch-B) l. 1497 et 2901 '
                                   '(comparé à "1" : « Vous » à la place du nom du joueur)',
}
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
        self.off_interface = O.interface()
        self.off_sorts = O.sorts()
        self.off_dbc = O.dbc()
        self.coa_sorts = O.sorts_coa()
        self.coa_dbc = O.dbc_coa()
        K.journal('import : sources officielles frFR : %d clés d\'interface, %d textes de sorts, %d textes de DBC ; '
                  'client CoA : %d textes de sorts (patch-T), %d textes de DBC'
                  % (len(self.off_interface), len(self.off_sorts), len(self.off_dbc), len(self.coa_sorts), len(self.coa_dbc)))
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

    def controle(self, en, fr, etat, type_=None, cle=None):
        return C.controle(en, fr, etat, self.regles, self.noms, type_, cle)

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

    def mise_a_jour_coa(self):
        """08/11/2026 : le CoA du 08/11 (commit b39aa861 : 238 mises à jour de la base du monde depuis 042b38a4, paquet de
        base inchangé) par-dessus l'amorce, qui reste celle du 02/11. Le fichier ne garde que les 17 824 textes nouveaux ou
        modifiés (collecte/donnees/coa-core/textes_coa_core_maj_20261108.csv.xz ; reconstruction : rapport
        docs/collecte/2026-11-08_Rapport_Erydal-et-CoA-recent.md).
        - texte nouveau : français de la table locale d'AzerothCore s'il y en a un (officiel), sinon à traduire ;
          les noms techniques comme à l'amorce (est_technique) et les créatures de travail (numéro >= 9 000 000) : technique ;
        - texte dont l'anglais a changé : le français ancien n'est plus prouvé, la ligne repasse à traduire (l'ancien
          anglais et l'ancien français vont dans la note) ; jamais sur relu ;
        - ensuite, un texte à traduire dont le même anglais a UN SEUL français officiel ailleurs dans la source le prend."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'croisement_commun', os.path.join(K.RACINE, 'collecte', 'scripts', 'croisement', 'commun.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        est_technique = mod.est_technique           # la règle de l'amorce (croisement/commun.py)
        n = Counter()
        nouvelles = []
        for r in lire_csv_xz('coa-core', 'textes_coa_core_maj_20261108.csv.xz'):
            en = r['texte_en']
            k = (r['type'], r['id'], r['sous_id'], r['champ'])
            l = self.lignes.get(k)
            note = 'CoA du 08/11/2026 (commit b39aa861)'
            tech = est_technique(en, r['type'], r['champ'])
            if not tech and r['type'] == 'creature':
                try:
                    if int(r['id']) >= 9000000:
                        tech = 'créature de travail (numéro >= 9 000 000)'
                except ValueError:
                    pass
            if r['fr_existant'] and r['origine'] == 'azerothcore' and r['modifie_par_coa'] != '1':
                fr, etat, src = r['fr_existant'], 'officiel', 'blizzard_frFR'
                note = joindre(note, r['fr_source'])
            elif tech:
                fr, etat, src = '', 'technique', ''
                note = joindre(note, 'technique : %s' % tech)
            else:
                fr, etat, src = '', 'a_traduire', ''
            if l is None:
                l = [r['type'], r['id'], r['sous_id'], r['champ'], en, K.empreinte(en), fr, etat, src, note]
                self.ajouter(l)
                n['nouvelle:' + etat] += 1
                nouvelles.append(l)
                continue
            if l[K.I_EN] == en:
                n['inchangee'] += 1
                continue
            if l[K.I_ETAT] == 'relu':
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'ATTENTION : anglais changé par CoA le 08/11 (« %s »), ligne relue gardée'
                                      % cite(en, 120))
                n['relue_gardee'] += 1
                continue
            avant = 'anglais avant le 08/11 : %s' % cite(l[K.I_EN], 120)
            if l[K.I_FR]:
                avant = joindre(avant, 'français avant (%s) : %s' % (l[K.I_SRC] or l[K.I_ETAT], cite(l[K.I_FR], 120)))
            l[K.I_EN], l[K.I_EMP], l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = en, K.empreinte(en), fr, etat, src
            l[K.I_NOTE] = joindre(joindre(l[K.I_NOTE], note), avant)
            n['modifiee:' + etat] += 1
            nouvelles.append(l)
        # même anglais, un seul français officiel ailleurs dans la source (comme « officiel_texte_identique » de l'amorce)
        a_chercher = {l[K.I_EN] for l in nouvelles if l[K.I_ETAT] == 'a_traduire'}
        par = defaultdict(set)
        if a_chercher:
            for l in self.lignes.values():
                if l[K.I_ETAT] == 'officiel' and l[K.I_FR] and l[K.I_EN] in a_chercher:
                    par[l[K.I_EN]].add(l[K.I_FR])
        for l in nouvelles:
            if l[K.I_ETAT] != 'a_traduire':
                continue
            frs = par.get(l[K.I_EN], set())
            if len(frs) != 1:
                continue
            fr = next(iter(frs))
            if self.controle(l[K.I_EN], fr, 'officiel', l[K.I_TYPE], l[K.I_ID]):
                n['meme_anglais_refuse'] += 1
                continue
            l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'officiel', 'blizzard_frFR'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'même anglais qu\'un texte officiel de la source : son français')
            n['meme_anglais_officiel'] += 1
        self.cr.update({'maj_coa_20261108:' + a: b for a, b in n.items()})
        K.journal('import : CoA du 08/11 par-dessus l\'amorce : %s' % dict(sorted(n.items())))

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
    # 2 bis. Donnees 0.2 : qualite des quetes « officielles » (textes de Cataclysm), TDB en second avis
    # ------------------------------------------------------------------
    TYPES_QUETES = ('quete', 'quete_demande', 'quete_recompense')

    def verifier_quetes(self):
        """Le francais « officiel » des quetes (AzerothCore, releve sur des clients recents) peut traduire le texte de
        Cataclysm et non l'anglais WotLK de CoA (quete 783). outils/quetes_cata.py repere ces lignes : elles passent
        a_revoir (raison en note), sauf si la base TrinityCore TDB a un francais different pour le meme anglais, qui
        passe le controle : il les remplace (source trinitycore_frFR). Les textes sans francais sont combles par TDB
        quand l'anglais de TDB est identique a celui de CoA."""
        tdb = O.tdb_quetes()
        noms = []
        with open(os.path.join(K.GLOSSAIRE, 'noms_officiels.tsv'), encoding='utf-8') as f:
            tete = None
            for ligne in f:
                p = ligne.rstrip('\n').split('\t')
                if tete is None:
                    tete = {c: j for j, c in enumerate(p)}
                    continue
                if p[tete['controle']] == 'oui':
                    noms.append((K.desechapper(p[tete['en']]), K.desechapper(p[tete['fr']])))
        off = [l for l in self.lignes.values() if l[K.I_TYPE] in self.TYPES_QUETES and l[K.I_ETAT] == 'officiel']
        vus, avec = Counter(), Counter()                  # noms gardés tels quels en français (« Thrall », « McBride »)
        for l in off:
            en_nu, fr = Q._nu(l[K.I_EN]), l[K.I_FR]
            for w in set(Q.MOT_NOM.findall(en_nu)):
                vus[w] += 1
                if w in fr:
                    avec[w] += 1
        gardes = {w for w, n in vus.items() if n >= 5 and avec[w] >= 0.95 * n and w.lower() not in K.EN_SEUL}
        det = Q.Detecteur(noms, gardes)
        self.detecteur_quetes = det
        for l in off:
            if l[K.I_CHAMP] == 'LogTitle':
                continue
            k = (l[K.I_TYPE], l[K.I_ID], l[K.I_CHAMP])
            t = tdb.get(k)
            fr_tdb = t[1] if t and t[1] and O.meme_anglais(t[0], l[K.I_EN]) else None
            r = det.signaux(l[K.I_EN], l[K.I_FR], l[K.I_CHAMP], fr_tdb)
            if not det.douteux(r):
                continue
            self.cr['quetes_officiel_douteux'] += 1
            cat = 'pas_du_francais' if any(x.startswith('pas_du_francais') for x in r) else 'cataclysm_probable'
            self.cr['quetes_officiel_douteux:' + cat] += 1
            if fr_tdb and K.norm(fr_tdb) != K.norm(l[K.I_FR]) and not det.douteux(det.signaux(l[K.I_EN], fr_tdb, l[K.I_CHAMP])) \
                    and not C.controle_structure(l[K.I_EN], fr_tdb):
                ancien = l[K.I_FR]
                l[K.I_FR], l[K.I_SRC] = fr_tdb, 'trinitycore_frFR'
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'français d\'AzerothCore douteux (%s) : remplacé par celui de la base TrinityCore '
                                                   'TDB 335.25101 (même anglais) ; ancien : %s' % (', '.join(r), cite(ancien)))
                self.cr['quetes_officiel_remplace_par_tdb'] += 1
                continue
            l[K.I_ETAT] = 'a_revoir'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], ('le « français officiel » d\'AzerothCore n\'est pas une traduction de ce texte '
                                                if cat == 'pas_du_francais' else
                                                'le « français officiel » d\'AzerothCore traduit sans doute un autre texte '
                                                '(Cataclysm ou plus récent), pas l\'anglais WotLK de CoA ')
                                  + '(contrôle des quêtes, données 0.2 : %s)' % ', '.join(r))
            self.ex('quete_douteuse:' + cat, l, 8)
        # quêtes standard sans français : TDB, si l'anglais de TDB est celui de CoA
        for l in self.lignes.values():
            if l[K.I_TYPE] not in self.TYPES_QUETES or l[K.I_ETAT] != 'a_traduire':
                continue
            t = tdb.get((l[K.I_TYPE], l[K.I_ID], l[K.I_CHAMP]))
            if not (t and t[1] and O.meme_anglais(t[0], l[K.I_EN])):
                continue
            r = det.signaux(l[K.I_EN], t[1], l[K.I_CHAMP])
            refus = C.controle_structure(l[K.I_EN], t[1])
            if det.douteux(r) or refus:
                self.cr['quetes_tdb_refuse'] += 1
                continue
            l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = t[1], 'officiel', 'trinitycore_frFR'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'français de la base TrinityCore TDB 335.25101 (relevé client %s), même anglais que CoA'
                                  % (t[2] or '?'))
            self.cr['quetes_comblees_par_tdb:' + l[K.I_TYPE]] += 1
        K.journal('import : quêtes officielles %s' % {k: v for k, v in self.cr.items() if k.startswith('quetes_')})

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

    # ------------------------------------------------------------------
    # Donnees 0.2 : sorts des classes et des talents rebases sur patch-T ; sorts standard
    # ------------------------------------------------------------------
    TECHNIQUE_SORT = re.compile(r'\b(?:DND|NYI|UNUSED|TEST|Test|PH|QA|DEBUG|Debug)\b|\(OLD\)|^zz|[Dd]ummy|Trigger|Bunny|'
                                r'\[[^\]]*\]|^Copy of\b', re.S)

    def officialiser_sort(self, l, i, champ, en, note_base):
        """Le francais officiel du Spell.dbc frFR (patch-frFR-3) si l'anglais du sort dans le Spell.dbc actif
        de CoA (patch-T) est identique a l'anglais Blizzard du meme numero. Renvoie True si adopte."""
        b = self.off_sorts.get((i, champ))
        if not (b and b[1] and O.meme_anglais(en, b[0])):
            return False
        ancien = l[K.I_FR] if l[K.I_FR] and l[K.I_FR] != b[1] else ''
        l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = b[1], 'officiel', 'blizzard_frFR'
        l[K.I_NOTE] = joindre(note_base, 'Spell.dbc frFR officiel (patch-frFR-3, client 3.3.5a) : anglais de patch-T '
                                         'identique à celui de Blizzard (patch-enUS-3) au même numéro',
                              'ancienne proposition (archive) : ' + cite(ancien) if ancien else '')
        return True

    def importer_sorts_classes(self, sorts_asc):
        """Sorts des 21 classes CoA et des talents : l'anglais de reference est celui du Spell.dbc ACTIF de CoA
        (patch-T, test 3 du 03/11/2026), et non plus celui du Spell.dbc d'Ascension. Une ligne dont l'anglais
        change repasse a_revoir, l'ancien francais en note."""
        ids = {}
        for (i, champ), r in sorts_asc.items():
            ids[i] = 'talents' if i in self.talents else 'sorts_classes'
        ids_t = {i for (i, _) in self.coa_sorts}
        cles = set(sorts_asc)
        for i in ids:
            if i in ids_t:
                for champ in ('Name', 'Rank', 'Description', 'ToolTip'):
                    if (i, champ) in self.coa_sorts and (i, champ) not in self.sorts_serveur_ids:
                        cles.add((i, champ))
        self.ids_sorts_classes = set(ids)
        for (i, champ) in sorted(cles, key=lambda x: (int(x[0]), x[1])):
            fam = ids[i]
            r = sorts_asc.get((i, champ))
            en_asc = r['texte_en'] if r else None
            note = ('Spell.dbc de CoA (patch-T)' if i in ids_t else 'Spell.dbc d\'Ascension (été 2026), sort absent du Spell.dbc de CoA (patch-T)') + \
                   (' ; sort de talent CoA (coa-development.org)' if fam == 'talents' else ' ; sort de classe CoA')
            if i in ids_t:
                en = self.coa_sorts.get((i, champ))
                if en is None:
                    self.cr['client_sort_champ_vide_dans_patchT'] += 1
                    continue
            else:
                en = en_asc
            tech = r['technique'] if (r and en_asc == en) else ''
            fam_fr = 'nom_sort' if champ in ('Name', 'Rank') else 'desc_sort'
            l = self.ligne_client('sort', i, champ, en, tech, note, fam_fr, 'sort_classe')
            if en_asc is not None and not O.meme_anglais(en_asc, en):
                self.cr['client_sort_anglais_rebase_patchT'] += 1
                ancien = self.ligne_client('sort', i, champ, en_asc, r['technique'], note, fam_fr, 'sort_classe')
                if self.officialiser_sort(l, i, champ, en, note):
                    pass
                elif l[K.I_ETAT] in ('a_traduire', 'technique') and ancien[K.I_FR]:
                    l[K.I_ETAT], l[K.I_FR], l[K.I_SRC] = 'a_revoir', '', ancien[K.I_SRC]
                    l[K.I_NOTE] = joindre(note, 'anglais modifié par CoA (patch-T) ; ancien anglais (Ascension) : %s ; '
                                                'ancien français proposé : %s' % (cite(en_asc, 2000), cite(ancien[K.I_FR], 2000)))
                    self.cr['client_sort_anglais_change_vers_a_revoir'] += 1
                else:
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'anglais de patch-T, différent de celui d\'Ascension : ' + cite(en_asc))
            elif en_asc is None:
                self.cr['client_sort_champ_ajoute_patchT'] += 1
                self.officialiser_sort(l, i, champ, en, note)
            else:
                self.officialiser_sort(l, i, champ, en, note)
            self.ajouter(l, fam)
            self.cr['client_%s_%s' % (fam, l[K.I_ETAT])] += 1
        K.journal('import : sorts des classes et talents rebasés sur patch-T (%d sorts)' % len(ids))

    def importer_sorts_standard(self):
        """Sorts standard (numeros du Spell.dbc 3.3.5a de Blizzard, hors sorts des classes CoA) : textes du
        Spell.dbc actif de CoA (patch-T) ; officiel si l'anglais est identique a celui de Blizzard."""
        ids_b = {i for (i, _) in self.off_sorts}
        for (i, champ), en in sorted(self.coa_sorts.items(), key=lambda x: (int(x[0][0]), x[0][1])):
            if i not in ids_b or i in self.ids_sorts_classes or (i, champ) in self.sorts_serveur_ids:
                continue
            l = ['sort', i, '', champ, en, K.empreinte(en), '', 'a_traduire', '', 'Spell.dbc de CoA (patch-T) ; sort standard']
            if self.officialiser_sort(l, i, champ, en, l[K.I_NOTE]):
                pass
            else:
                b = self.off_sorts.get((i, champ))
                if self.TECHNIQUE_SORT.search(en) or (champ == 'Name' and self.TECHNIQUE_SORT.search(self.coa_sorts.get((i, 'Name'), ''))):
                    l[K.I_ETAT] = 'technique'
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'technique=sort de test ou interne')
                elif b and b[1]:
                    l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = b[1], 'a_revoir', 'blizzard_frFR'
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'anglais modifié par CoA : le français officiel traduit l\'anglais '
                                                       'Blizzard %s' % cite(b[0]))
                else:
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'texte ajouté par CoA à un sort standard')
            self.ajouter(l, 'sorts_standard')
            self.cr['client_sorts_standard_' + l[K.I_ETAT]] += 1
        K.journal('import : sorts standard terminés')

    # ------------------------------------------------------------------
    # Add-on 0.3 : sorts propres a CoA qui portent la puissance PvE / PvP des objets
    # ------------------------------------------------------------------
    RX_PUISSANCE_NOM = re.compile(r'^(PvE|PvP) Power \(\+(\d+)\)$')
    RX_PUISSANCE_TXT = re.compile(r'^Increases (PvE|PvP) Power by (\d+)\.$')

    def importer_sorts_coa_puissance(self):
        """Sorts 101600-101799 du Spell.dbc de CoA (patch-T) : « PvE Power (+N) », « Increases PvE Power by N. ».
        Ce sont les lignes « Increases PvE Power by 38. » des infobulles d'objets. Français sur le modèle officiel des
        statistiques d'objets (« Augmente la puissance d'attaque de %d. », ITEM_MOD_ATTACK_POWER) ; PvE et PvP restent
        tels quels (glossaire) : « Augmente la puissance PvE de N. ». État machine, source « modele » (comme « Rang N »)."""
        ids_b = {i for (i, _) in self.off_sorts}
        n = 0
        for (i, champ), en in sorted(self.coa_sorts.items(), key=lambda x: (int(x[0][0]), x[0][1])):
            if i in ids_b or i in self.ids_sorts_classes or champ not in ('Name', 'Description', 'ToolTip'):
                continue
            m = (self.RX_PUISSANCE_NOM if champ == 'Name' else self.RX_PUISSANCE_TXT).match(en)
            if not m:
                continue
            quoi, nombre = m.groups()
            if champ == 'Name':
                fr = 'Puissance %s (+%s)' % (quoi, nombre)
                modele = 'nom sur le modèle de PVE_POWER_LABEL / PVP_POWER_LABEL (« Puissance PvE »)'
            else:
                fr = 'Augmente la puissance %s de %s.' % (quoi, nombre)
                modele = ('modèle officiel des statistiques d\'objets « Augmente la puissance d\'attaque de %d. » '
                          '(ITEM_MOD_ATTACK_POWER) ; PvE/PvP gardés (glossaire)')
            l = ['sort', i, '', champ, en, K.empreinte(en), fr, 'machine', 'modele',
                 joindre('Spell.dbc de CoA (patch-T) ; sort propre à CoA (puissance %s des objets)' % quoi, modele)]
            refus = self.controle(en, fr, 'machine', 'sort')
            if refus:
                l[K.I_ETAT] = 'a_revoir'
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'refusé au contrôle : ' + ', '.join(refus))
            self.ajouter(l, 'sorts_coa')
            self.cr['client_sorts_coa_puissance_' + l[K.I_ETAT]] += 1
            n += 1
        K.journal('import : sorts CoA de puissance PvE/PvP : %d textes' % n)

    def importer_sorts_interface(self):
        """Add-on 0.8 (essai 7 n° 10) : sorts que le code d'interface du client CoA designe par leur numero
        (collecte/donnees/client/sorts_interface.tsv : HasBuff(9931032) = mode JcE…), absents des autres familles.
        Texte de Blizzard identique : son francais officiel ; sinon a_traduire (atelier de traduction)."""
        p = os.path.join(K.COLLECTE, 'client', 'sorts_interface.tsv')
        if not os.path.exists(p):
            return
        ids = set()
        with open(p, encoding='utf-8') as f:
            next(f)
            for ligne in f:
                c = ligne.rstrip('\n').split('\t')
                if c and c[0].isdigit():
                    ids.add(c[0])
        deja = {k[1] for k in self.lignes if k[0] == 'sort'}
        n = Counter()
        for (i, champ), en in sorted(self.coa_sorts.items(), key=lambda x: (int(x[0][0]), x[0][1])):
            if i not in ids or i in deja or champ not in ('Name', 'Rank', 'Description', 'ToolTip') or not en.strip():
                continue
            off = self.off_sorts.get((i, champ))
            if off and off[0] == en and off[1]:
                l = ['sort', i, '', champ, en, K.empreinte(en), off[1], 'officiel', 'blizzard_frFR',
                     'Spell.dbc de CoA (patch-T) ; sort cité par l\'interface du client | Spell.dbc frFR officiel : '
                     'anglais identique']
                if self.controle(en, off[1], 'officiel', 'sort'):
                    l[K.I_ETAT], l[K.I_FR] = 'a_traduire', ''
            else:
                l = ['sort', i, '', champ, en, K.empreinte(en), '', 'a_traduire', 'coa_client',
                     'Spell.dbc de CoA (patch-T) ; sort cité par l\'interface du client (collecte/donnees/client/'
                     'sorts_interface.tsv)']
            self.ajouter(l, 'sorts_coa')
            n[l[K.I_ETAT]] += 1
        for k, v in n.items():
            self.cr['client_sorts_interface_' + k] = v
        K.journal('import : sorts cités par l\'interface du client : %s' % dict(n))

    TECHNIQUE_NOM_SORT = re.compile(r'^(?:Dummy|DND|DNT|zz|QA|TEST|Test)\b|\[(?:DND|DNT|PH|NYI)\]|\b(?:DEPRECATED|UNUSED)\b')

    def importer_sorts_objets(self):
        """Essai 8 (07/11/2026) : sorts du Spell.dbc de CoA (patch-T) que les objets déclenchent (lignes « Utiliser : »
        de l'infobulle : collecte/donnees/coa-core/sorts_objets.csv.xz), auras des Épreuves (sorts_epreuves.csv.xz) et
        sorts appris (rangs 2 et plus des sorts de classe, sorts des maîtres : sorts_appris.csv.xz), absents des autres
        familles. Anglais de Blizzard identique : son français officiel ; sinon à traduire."""
        obj, ep = {}, {}
        for r in lire_csv_xz('coa-core', 'sorts_objets.csv.xz'):
            obj[r['sort']] = (r['objets'], r['exemple'])
        for r in lire_csv_xz('coa-core', 'sorts_epreuves.csv.xz'):
            ep[r['sort']] = r['epreuves']
        appris = {r['sort']: r['quoi'] for r in lire_csv_xz('coa-core', 'sorts_appris.csv.xz')}
        # sorts relevés pendant les essais (barre d'incantation…) : collecte/donnees/client/sorts_vus_en_jeu.tsv
        p = os.path.join(K.COLLECTE, 'client', 'sorts_vus_en_jeu.tsv')
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                for ligne in list(f)[1:]:
                    c = ligne.rstrip('\n').split('\t')
                    if c and c[0].isdigit():
                        appris.setdefault(c[0], c[1] if len(c) > 1 else 'vu en jeu')
        deja = {k[1] for k in self.lignes if k[0] == 'sort'}
        # 0.9.5 (exigence de Dan du 09/11 : tous les sorts des classes en français) : sorts de l'avancement du personnage
        # du client (CharacterAdvancementData.json, collecte avancement_sorts.py), classes de CoA (pas « Reborn… »
        # d'Ascension) : capacités, talents et leurs rangs ; ceux qui manquaient (1 254) entrent ici
        p_av = os.path.join(K.COLLECTE, 'client', 'avancement_sorts.tsv')
        n_av = 0
        if os.path.exists(p_av):
            with open(p_av, encoding='utf-8') as f:
                for ligne in list(f)[1:]:
                    c = ligne.rstrip('\n').split('\t')
                    if len(c) < 6 or c[1].startswith('Reborn') or c[1] in ('', 'None'):
                        continue
                    if c[0] not in deja and (c[0], 'Name') in self.coa_sorts and c[0] not in appris:
                        appris[c[0]] = 'avancement du personnage de CoA : %s de la classe %s (arbre %s, rang %s)' % (
                            {'Ability': 'capacité', 'Talent': 'talent', 'TalentAbility': 'capacité de talent'}.get(
                                c[2], c[2]), c[1], c[3] or '-', c[5])
                        n_av += 1
        self.cr['client_sorts_avancement'] = n_av
        # 0.9.4 (essai 8, fenêtre des talents de CoA) : sorts que le client insère dans la bulle d'un autre sort (balise
        # « @s:N:0@ » d'une description : séparateur, icône, nom puis description du sort N, « Brine » sous « Tempest
        # Sovereign ») et sorts d'exemple des spécialisations (rang « Specialization » ou « Spec Passive » :
        # « Air Elemental ») ; les sorts cités par ceux-là aussi, de proche en proche
        connus = deja | set(obj) | set(ep) | set(appris)
        RE_CITE = re.compile(r'@s:(\d+):')
        # (ordre fixe : un ensemble se parcourt dans un ordre qui change d'une exécution à l'autre, la note « cité dans
        # la bulle du sort n° … » changeait avec lui)
        a_voir, cites = sorted(connus, key=lambda x: (len(x), x)), {}
        for (i, champ), en in self.coa_sorts.items():
            if champ == 'Rank' and en in ('Specialization', 'Spec Passive') and i not in connus:
                cites[i] = 'sort de spécialisation (rang « %s »)' % en
                a_voir.append(i)
        vus = set(a_voir)
        while a_voir:
            i = a_voir.pop()
            for champ in ('Description', 'ToolTip'):
                for j in RE_CITE.findall(self.coa_sorts.get((i, champ), '')):
                    if j not in vus and j not in connus:
                        vus.add(j)
                        cites[j] = 'cité dans la bulle du sort n° %s (balise @s)' % i
                        a_voir.append(j)
        for i, q in cites.items():
            appris.setdefault(i, q)
        self.cr['client_sorts_cites_ou_specialisation'] = len(cites)
        n = Counter()
        for (i, champ), en in sorted(self.coa_sorts.items(), key=lambda x: (int(x[0][0]), x[0][1])):
            if (i not in obj and i not in ep and i not in appris) or i in deja \
                    or champ not in ('Name', 'Rank', 'Description', 'ToolTip') or not en.strip():
                continue
            quoi = []
            if i in appris:
                quoi.append(appris[i])
            if i in obj:
                quoi.append('déclenché par %s objet(s), dont le n° %s' % obj[i])
            if i in ep:
                quoi.append('aura des Épreuves n° %s' % ep[i])
            note = 'Spell.dbc de CoA (patch-T) ; sort %s' % ' ; '.join(quoi)
            off = self.off_sorts.get((i, champ))
            if off and off[0] == en and off[1] and not self.controle(en, off[1], 'officiel', 'sort'):
                l = ['sort', i, '', champ, en, K.empreinte(en), off[1], 'officiel', 'blizzard_frFR',
                     joindre(note, 'Spell.dbc frFR officiel : anglais identique')]
            elif champ == 'Name' and self.TECHNIQUE_NOM_SORT.search(en):
                l = ['sort', i, '', champ, en, K.empreinte(en), '', 'technique', '',
                     joindre(note, 'technique=nom interne (Dummy, DND…) ; l\'infobulle de l\'objet montre la description')]
            elif champ == 'Rank' and re.fullmatch(r'Rank (\d+)', en):
                # 0.9.4 : même modèle que les sorts des classes (« (Rank 3) » → « (Rang 3) », usage officiel)
                l = ['sort', i, '', champ, en, K.empreinte(en), 'Rang ' + en.split()[1], 'machine', 'modele',
                     joindre(note, 'modèle « Rank N » → « Rang N »')]
            else:
                l = ['sort', i, '', champ, en, K.empreinte(en), '', 'a_traduire', 'coa_client', note]
            self.ajouter(l, 'sorts_objets')
            n[l[K.I_ETAT]] += 1
        for k, v in n.items():
            self.cr['client_sorts_objets_' + k] = v
        K.journal('import : sorts des objets et auras des Épreuves : %s' % dict(n))

    def reprise_meme_anglais(self):
        """Essai 8 : une ligne de sorts_objets encore à traduire dont l'anglais exact (même champ) a déjà UN SEUL
        français affichable dans un autre sort (ou, pour un nom, dans un autre nom : objet, créature…) prend ce français
        (état machine, source reprise_meme_anglais). Évite de faire retraduire 40 % des textes."""
        TYPES_SORT = ('sort', 'coa_description_sort_client', 'sort_dbc_serveur')
        par, par_off = defaultdict(set), defaultdict(set)
        for l in self.lignes.values():
            if not l[K.I_FR] or l[K.I_ETAT] not in ('officiel', 'relu', 'machine'):
                continue
            c = l[K.I_CHAMP]
            cles = []
            if l[K.I_TYPE] in TYPES_SORT:
                cles.append((c, l[K.I_EN]))
            # 0.9.4 : un nom d'une autre table resté en anglais (la créature « Brine ») n'est pas une traduction : le
            # sort « Brine » n'en hérite pas (il est « Saumure » dans la description qui le cite)
            if c in ('name', 'Name') and (l[K.I_TYPE] in TYPES_SORT or l[K.I_FR] != l[K.I_EN]):
                cles.append(('Name', l[K.I_EN]))
            for cl in cles:
                par[cl].add(l[K.I_FR])
                if l[K.I_ETAT] in ('officiel', 'relu'):
                    par_off[cl].add(l[K.I_FR].replace('’', "'"))
        n = Counter()
        for k, l in self.lignes.items():
            if self.famille.get(k) != 'sorts_objets' or l[K.I_ETAT] != 'a_traduire':
                continue
            # 0.9.1 : un seul français officiel (ou relu) l'emporte sur les traductions machine du même anglais
            # (« Call Lightning », rangs 2 à 12 : l'officiel « Appel d'éclair » et une ancienne traduction machine que
            # harmoniser_officiel ne remplace qu'ensuite)
            frs = par_off.get((l[K.I_CHAMP], l[K.I_EN]), set())
            if len(frs) != 1:
                frs = par.get((l[K.I_CHAMP], l[K.I_EN]), set())
            if len(frs) != 1:
                n['sans' if not frs else 'plusieurs'] += 1
                continue
            fr = next(iter(frs))
            if self.controle(l[K.I_EN], fr, 'machine', l[K.I_TYPE], k[1]):
                n['refus'] += 1
                continue
            l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'machine', 'reprise_meme_anglais'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'même anglais qu\'un texte déjà traduit : son français')
            n['repris'] += 1
        self.cr.update({'reprise_meme_anglais:' + a: b for a, b in n.items()})
        K.journal('import : sorts des objets, reprise du même anglais : %s' % dict(n))

    def libelles_lua_coa(self):
        """0.9.2 : libellés que les add-ons de CoA définissent eux-mêmes hors de GlobalStrings.dbc (« Change Active
        Specialization », « Reset Trees » ; collecte libelles_lua_coa.py) : type coa_libelle_lua, famille progression.
        Affichés par le balayage des fenêtres CoA (texte exact), jamais écrits dans la variable du jeu."""
        p = os.path.join(K.COLLECTE, 'client', 'libelles_lua_coa.tsv')
        if not os.path.exists(p):
            return
        n = 0
        with open(p, encoding='utf-8') as f:
            for ligne in list(f)[1:]:
                c = ligne.rstrip('\n').split('\t')
                if len(c) < 3:
                    continue
                en = K.desechapper(c[1])
                self.ajouter(['coa_libelle_lua', c[0], '', 'texte', en, K.empreinte(en), '', 'a_traduire', 'coa_client',
                              'libellé défini par %s (variable %s, absente de GlobalStrings.dbc)' % (c[2], c[0])], 'progression')
                n += 1
        self.cr['libelles_lua_coa'] = n
        K.journal('import : %d libellés propres aux add-ons de CoA' % n)

    def categories_competences(self):
        """0.9.4 (essai 8, captures du 08/11) : catégories de la fenêtre des compétences (SkillLineCategory.dbc du client
        CoA, collecte categories_competences.py) : type categorie_competence, famille competences ; le français officiel
        vient de glossaire/noms_officiels_web.tsv (décision 31), sinon à traduire."""
        p = os.path.join(K.COLLECTE, 'client', 'categories_competences.tsv')
        if not os.path.exists(p):
            return
        n = 0
        with open(p, encoding='utf-8') as f:
            for ligne in list(f)[1:]:
                c = ligne.rstrip('\n').split('\t')
                if len(c) < 3 or not c[1]:
                    continue
                k = ('categorie_competence', c[0], '', 'name')
                if k in self.lignes:
                    continue
                self.ajouter(['categorie_competence', c[0], '', 'name', c[1], K.empreinte(c[1]), '', 'a_traduire',
                              'coa_client', 'SkillLineCategory.dbc du client CoA (%s) : en-tête de la fenêtre des '
                              'compétences' % c[2]], 'competences')
                n += 1
        self.cr['categories_competences'] = n

    def hauts_faits_officiels(self):
        """0.9.2 (essai 8, niveau 10) : hauts faits du client CoA (Achievement, Achievement_Criteria et
        Achievement_Category de patch-M ; collecte e03_complements_dbc.py).
        - noms, descriptions, récompenses et catégories : les lignes de db.exil.es restent, l'anglais du client l'emporte
          s'il diffère ; même numéro et même anglais que Blizzard : son français officiel (patch-frFR-3), qui remplace
          la traduction machine de la release 3.5.1 ;
        - critères (type haut_fait_critere, famille hauts_faits_criteres) : même numéro et même anglais que Blizzard :
          officiel ; sinon même anglais qu'un critère officiel (un seul français) : officiel ; sinon à traduire (les noms
          seront repris plus loin, criteres_par_nom). Jamais sur relu."""
        liens = {}
        p = os.path.join(K.COLLECTE, 'client', 'hauts_faits_liens.tsv')
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                for ligne in list(f)[1:]:
                    c = ligne.rstrip('\n').split('\t')
                    if len(c) == 3:
                        liens[(c[0], c[1])] = c[2]
        self.liens_hf = liens
        off_texte = defaultdict(set)
        for (dbc, i, champ), (en, fr) in self.off_dbc.items():
            if dbc == 'Achievement_Criteria' and en and fr:
                off_texte[en].add(fr)
        n = Counter()
        TYPES = {'Achievement': 'haut_fait', 'Achievement_Category': 'haut_fait_categorie', 'Achievement_Criteria': 'haut_fait_critere'}
        for (dbc, i, champ), (arch, en) in sorted(self.coa_dbc.items(), key=lambda x: (x[0][0], self._cle_num(x[0][1]), x[0][2])):
            typ = TYPES.get(dbc)
            if not typ or not en.strip():
                continue
            fam = 'hauts_faits_criteres' if typ == 'haut_fait_critere' else 'hauts_faits'
            k = (typ, i, '', champ)
            l = self.lignes.get(k)
            note = '%s.dbc du client CoA (%s)' % (dbc, arch)
            if typ == 'haut_fait_critere':
                hf = liens.get(('critere_haut_fait', i.split('-')[0]))
                if hf:
                    note = joindre(note, 'critère du haut fait n° %s' % hf)
            if l is None:
                l = [typ, i, '', champ, en, K.empreinte(en), '', 'a_traduire', '', note]
                self.ajouter(l, fam)
                n[typ + ':nouvelle'] += 1
            elif l[K.I_EN] != en and l[K.I_ETAT] != 'relu':
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'anglais du client CoA (%s) différent de db.exil.es (avant : %s)'
                                      % (arch, cite(l[K.I_EN], 120)))
                l[K.I_EN], l[K.I_EMP], l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = en, K.empreinte(en), '', 'a_traduire', ''
                n[typ + ':anglais_client'] += 1
            if l[K.I_ETAT] in ('relu', 'officiel', 'technique'):
                continue
            b = self.off_dbc.get((dbc, i, champ))
            fr, quoi = None, None
            if b and b[1] and O.meme_anglais(en, b[0]):
                fr, quoi = b[1], '%s.dbc frFR officiel (patch-frFR-3), même numéro et même anglais que Blizzard' % dbc
            elif typ == 'haut_fait_critere' and len(off_texte.get(en, ())) == 1:
                fr, quoi = next(iter(off_texte[en])), ('Achievement_Criteria.dbc frFR officiel (patch-frFR-3) : même anglais, '
                                                       'un seul français officiel pour ce texte')
            if fr is None:
                # 0.9.4 (essai 8, captures du 08/11) : la traduction machine de la release 3.5.1 est écartée pour les
                # noms, descriptions, récompenses et catégories (« Level 70 » pour « Nightmare Mode: Level 70 »,
                # « [Mort Knight] », une même classe en « Docteur Sorcier » et « Docteur Vaudou », décision 24 jamais
                # appliquée) : retraduite au chantier M, l'ancien français reste en note (jamais donné en indice)
                if typ in ('haut_fait', 'haut_fait_categorie') and l[K.I_SRC] == 'release_3.5.1' \
                        and l[K.I_ETAT] in ('machine', 'a_revoir') and l[K.I_FR]:
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'traduction machine de la release 3.5.1 écartée le 08/11/2026 '
                                                       '(erreurs de noms et de classes) ; ancien français : %s'
                                                       % cite(l[K.I_FR], 200))
                    l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = '', 'a_traduire', ''
                    n['%s:release_ecartee_%s' % (typ, champ)] += 1
                continue
            refus = self.controle(en, fr, 'officiel', typ, i)
            # Blizzard écrit parfois les nombres autrement (« ten » / « 10 », « 2 man » / « 2c2 ») : l'officiel est gardé
            # quand seul le contrôle des nombres le refuse (même tolérance que la fabrique : officiel_tolere_nombres)
            if refus and {x.split(':')[0] for x in refus} != {'nombres'}:
                n[typ + ':officiel_refuse'] += 1
                continue
            if refus:
                quoi = joindre(quoi, 'nombres écrits autrement par Blizzard : officiel gardé')
                n[typ + ':officiel_nombres_toleres'] += 1
            if l[K.I_FR] and l[K.I_FR] != fr:
                quoi = joindre(quoi, 'avant (%s) : %s' % (l[K.I_SRC] or l[K.I_ETAT], cite(l[K.I_FR], 120)))
            l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'officiel', 'blizzard_frFR'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], quoi)
            n['%s:officiel_%s' % (typ, champ)] += 1
        self.cr.update({'hauts_faits_officiels:' + a: b for a, b in n.items()})
        K.journal('import : hauts faits du client, français officiel : %s' % dict(sorted(n.items())))

    def criteres_par_nom(self):
        """0.9.2 : un critère de haut fait (ou une catégorie) encore à traduire dont l'anglais EXACT est un nom déjà
        traduit (zone, créature, objet, quête, sort…) avec UN SEUL français prend ce français : officiel si ce nom est
        officiel (ou relu), sinon machine (source nom_meme_anglais). « Molten Core », « Ragnaros », « Thunderfury »."""
        TYPES_NOM = ('name', 'Name', 'title')
        par, par_off = defaultdict(set), defaultdict(set)
        for l in self.lignes.values():
            if not l[K.I_FR] or l[K.I_CHAMP] not in TYPES_NOM or l[K.I_ETAT] not in ('officiel', 'relu', 'machine'):
                continue
            if l[K.I_TYPE] in ('haut_fait_critere', 'haut_fait_categorie'):
                continue
            fr = l[K.I_FR].replace('’', "'")
            par[l[K.I_EN]].add(fr)
            if l[K.I_ETAT] in ('officiel', 'relu'):
                par_off[l[K.I_EN]].add(fr)
        n = Counter()
        for k, l in self.lignes.items():
            if l[K.I_TYPE] not in ('haut_fait_critere', 'haut_fait_categorie') or l[K.I_ETAT] != 'a_traduire':
                continue
            frs, etat = par_off.get(l[K.I_EN], set()), 'officiel'
            if len(frs) != 1:
                frs, etat = par.get(l[K.I_EN], set()), 'machine'
            if len(frs) != 1:
                n['sans' if not frs else 'plusieurs'] += 1
                continue
            fr = next(iter(frs))
            if fr == l[K.I_EN] or self.controle(l[K.I_EN], fr, etat, l[K.I_TYPE], k[1]):
                n['refus_ou_identique'] += 1
                continue
            l[K.I_FR], l[K.I_ETAT] = fr, etat
            l[K.I_SRC] = 'blizzard_frFR' if etat == 'officiel' else 'nom_meme_anglais'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'même anglais qu\'un nom %s déjà traduit : son français' % ('officiel' if etat == 'officiel' else ''))
            n['repris_' + etat] += 1
        self.cr.update({'criteres_par_nom:' + a: b for a, b in n.items()})
        K.journal('import : critères et catégories des hauts faits repris d\'un nom : %s' % dict(n))

    def noms_vanite(self):
        """Essai 8 : noms des objets de la collection de vanité (la fenêtre les écrit entre crochets, ou en
        majuscules) : une ligne coa_vanite_objet par objet, avec le nom et le français de l'objet."""
        p = os.path.join(K.COLLECTE, 'client', 'vanite_objets.tsv')
        if not os.path.exists(p):
            return
        with open(p, encoding='utf-8') as f:
            objets = sorted({c.split('\t')[1].strip() for c in list(f)[1:] if c.strip()}, key=int)
        n = Counter()
        for o in objets:
            src = self.lignes.get(('objet', o, '', 'name'))
            if not src or not src[K.I_EN].strip():
                n['objet_absent'] += 1
                continue
            ok = src[K.I_FR] and src[K.I_ETAT] in ('officiel', 'relu', 'machine')
            l = ['coa_vanite_objet', o, '', 'name', src[K.I_EN], K.empreinte(src[K.I_EN]),
                 src[K.I_FR] if ok else '', ('officiel' if src[K.I_ETAT] == 'officiel' else 'machine') if ok else 'a_traduire',
                 'nom_objet_meme_anglais' if ok else '', 'nom de l\'objet n° %s (collection de vanité)' % o]
            if ok and self.controle(l[K.I_EN], l[K.I_FR], l[K.I_ETAT], l[K.I_TYPE], o):
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = '', 'a_traduire', ''
            self.ajouter(l, 'vanite')
            n[l[K.I_ETAT]] += 1
        self.cr.update({'noms_vanite:' + a: b for a, b in n.items()})
        K.journal('import : noms des objets de la collection de vanité : %s' % dict(n))

    def importer_client(self):
        self.zones_exil = {}
        self.charger_francais_client()
        arbres = {}
        for r in lire_csv_xz('site-coa', 'talents_classes_en.csv.xz'):
            if r['id_sort']:
                self.talents.add(r['id_sort'])
            if r['champ'] in ('nom_arbre', 'description_arbre'):
                arbres[(r['id'], 'nom' if r['champ'] == 'nom_arbre' else 'description')] = r
        tal_dbc = set()
        sorts_asc = {}            # (id, champ) -> ligne du Spell.dbc d'Ascension (sorts des classes et des talents CoA)
        self.sorts_serveur_ids = set()
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
                    self.sorts_serveur_ids.add((r['id'], r['champ']))
                    continue
                if talent:
                    tal_dbc.add(r['id'])
                sorts_asc[(r['id'], r['champ'])] = r
            elif t in ('haut_fait', 'haut_fait_categorie'):
                l = self.ligne_client(t, r['id'], r['champ'], r['texte_en'], r['technique'], 'base db.exil.es (site CoA)',
                                      'hauts_faits', 'machine')
                self.ajouter(l)
                self.cr['client_hauts_faits_' + l[K.I_ETAT]] += 1
            elif t in ('zone', 'carte'):
                self.zones_exil[(t, r['id'], r['champ'])] = r      # remplacées par les DBC du client CoA (importer_dbc)
            elif t == 'carte_monde':
                l = self.ligne_client(t, r['id'], r['champ'], r['texte_en'], r['technique'], 'base db.exil.es (site CoA)',
                                      'lieu', 'zone')
                self.ajouter(l)
                self.cr['client_zones_' + l[K.I_ETAT]] += 1
            elif t == 'classe':
                l = [t, r['id'], '', r['champ'], r['texte_en'], K.empreinte(r['texte_en']), '', 'a_traduire', '',
                     'base db.exil.es (ChrClasses du client)']
                fr = CLASSES_COA.get(K.norm(r['texte_en']))
                b = self.off_dbc.get(('ChrClasses', r['id'], 'name'))
                if b and b[1] and O.meme_anglais(b[0], r['texte_en']) and int(r['id']) < 12:
                    l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = b[1], 'officiel', 'blizzard_frFR'
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'ChrClasses.dbc frFR officiel (patch-frFR-3), même anglais')
                    self.ajouter(l, 'talents')
                    self.cr['client_classes_officiel'] += 1
                    for g in ('name_female', 'name_male'):        # formes accordées, pour $c et l'infobulle
                        bg = self.off_dbc.get(('ChrClasses', r['id'], g))
                        if bg and bg[1]:
                            self.ajouter([t, r['id'], '', g, r['texte_en'], K.empreinte(r['texte_en']), bg[1], 'officiel',
                                          'blizzard_frFR', 'ChrClasses.dbc frFR officiel (patch-frFR-3) : forme %s ; '
                                          'anglais du nom, identique' % ('féminine' if g == 'name_female' else 'masculine')],
                                         'talents')
                            self.cr['client_classes_officiel'] += 1
                    continue
                if fr and int(r['id']) >= 12:
                    l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'machine', 'glossaire'
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'nom de classe CoA tranché (glossaire hérité d\'AscensionFR ; '
                                                       'Guardian, Ranger, Cultist : décision de Dan du 03/11/2026)')
                else:
                    l = self.ligne_client(t, r['id'], r['champ'], r['texte_en'], '', l[K.I_NOTE], 'interface', 'machine')
                    if int(r['id']) >= 12 and l[K.I_ETAT] == 'machine':
                        l[K.I_ETAT] = 'a_revoir'
                        l[K.I_NOTE] = joindre(l[K.I_NOTE], 'classe CoA sans décision de glossaire : voir glossaire/A_TRANCHER.md')
                self.ajouter(l, 'talents')
                self.cr['client_classes_' + l[K.I_ETAT]] += 1
                # forme feminine (decision n° 17 de Dan) : seulement si le masculin est affichable
                ff = CLASSES_COA_F.get(K.norm(r['texte_en']))
                if ff and r['champ'] == 'name' and l[K.I_ETAT] in ('machine', 'relu') and l[K.I_FR]:
                    self.ajouter([t, r['id'], '', 'name_female', r['texte_en'], K.empreinte(r['texte_en']), ff, 'machine',
                                  'glossaire', 'forme féminine, décision de vocabulaire n° 17 de Dan (04/11/2026) ; '
                                  'masculin : ' + l[K.I_FR] + (' (invariable)' if ff == l[K.I_FR] else '')], 'talents')
                    self.cr['client_classes_feminin_decision17'] += 1
            elif t == 'arbre_talents':
                l = self.ligne_client(t, r['id'], r['champ'], r['texte_en'], r['technique'], 'base db.exil.es (TalentTab)',
                                      'arbre_nom', 'sort_classe')
                self.ajouter(l, 'talents')
                self.cr['client_arbres_' + l[K.I_ETAT]] += 1
        self.importer_sorts_classes(sorts_asc)
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
    # Donnees 0.2 : DBC du client CoA (factions, zones, races, competences…), officiel quand l'anglais correspond
    # ------------------------------------------------------------------
    DBC_TYPES = {
        'Faction': ('faction', 'factions'), 'AreaTable': ('zone', 'zones'), 'Map': ('carte', 'zones'),
        'WMOAreaTable': ('zone_interieure', 'zones'), 'AreaPOI': ('point_carte', 'zones'), 'TaxiNodes': ('point_vol', 'zones'),
        'ChatChannels': ('canal', 'zones'), 'ChrRaces': ('race', 'races'), 'ItemSubClass': ('sous_classe_objet', 'sous_classes_objets'),
        'SkillLine': ('competence', 'competences'), 'ItemSet': ('ensemble_objets_client', 'ensembles_objets_client'),
        'ItemRandomSuffix': ('suffixe_objet', 'suffixes_objets'), 'MailTemplate': ('courrier', 'courriers'),
        'DungeonEncounter': ('rencontre_donjon', 'rencontres_donjon'),
        'SpellItemEnchantment': ('enchantement', 'enchantements'),
    }
    # Add-on 0.9 (07/11/2026) : tables du client encore absentes (collecte e03_complements_dbc.py)
    DBC_TYPES_09 = {
        # propres à CoA : Épreuves
        'Challenge': ('coa_epreuve', 'epreuves'), 'ChallengeRuleTypes': ('coa_epreuve_regle', 'epreuves'),
        'ChallengeConditionTypes': ('coa_epreuve_condition', 'epreuves'),
        'ChallengeRequirementTypes': ('coa_epreuve_exigence', 'epreuves'),
        'ChallengeModifierTypes': ('coa_epreuve_modificateur', 'epreuves'),
        # propres à CoA : création de personnage
        'CharacterCreationArchetypes': ('coa_archetype', 'creation_personnage'),
        'CharacterCreationArchetypeCategories': ('coa_archetype_categorie', 'creation_personnage'),
        'CharacterCreationArchetypeRoles': ('coa_archetype_role', 'creation_personnage'),
        'CharacterCreationClassGuideRoles': ('coa_guide_role', 'creation_personnage'),
        'CharacterCreationClassGuideSubroles': ('coa_guide_sous_role', 'creation_personnage'),
        'ChrSpecs': ('coa_specialisation', 'creation_personnage'),
        'Startup_Strings': ('coa_message_demarrage', 'creation_personnage'),
        # propres à CoA : tutoriels, astuces
        'Tutorial': ('coa_tutoriel', 'tutoriels'), 'TutorialKeywords': ('coa_tutoriel_mot_cle', 'tutoriels'),
        'TutorialObjectives': ('coa_tutoriel_objectif', 'tutoriels'),
        'TutorialCategories': ('coa_tutoriel_categorie', 'tutoriels'), 'GameTips': ('astuce', 'tutoriels'),
        # propres à CoA : jetons, avancement, étiquettes de sorts
        'TokenTypes': ('coa_jeton', 'progression'),
        'CharacterAdvancementCategories': ('coa_avancement_categorie', 'progression'),
        'CharacterAdvancementTabTypes': ('coa_avancement_onglet', 'progression'),
        'CharacterAdvancementClassTypes': ('coa_avancement_classe', 'progression'),
        'SpellTagTypes': ('coa_etiquette_sort', 'progression'),
        # Blizzard (français officiel dans patch-frFR-3)
        'MapDifficulty': ('difficulte_carte', 'monde_client'), 'LFGDungeons': ('donjon_recherche', 'monde_client'),
        'LFGDungeonGroup': ('groupe_donjon_recherche', 'monde_client'),
        'BattlemasterList': ('champ_bataille', 'monde_client'), 'WorldStateUI': ('etat_monde', 'monde_client'),
        'EmotesTextData': ('emote', 'monde_client'), 'SpellFocusObject': ('objet_focalisation', 'monde_client'),
        'TotemCategory': ('categorie_totem', 'monde_client'), 'SpellShapeshiftForm': ('forme', 'monde_client'),
        'BarberShopStyle': ('style_coiffure', 'monde_client'),
        'ItemLimitCategory': ('categorie_limite_objet', 'monde_client'),
        # Blizzard sans français dans patch-frFR-3 : noms officiels (décision 31)
        'CharTitles': ('titre', 'noms_client'), 'HolidayNames': ('fete', 'noms_client'),
        'HolidayDescriptions': ('fete_description', 'noms_client'), 'QuestSort': ('categorie_quete', 'noms_client'),
        'CreatureFamily': ('famille_creature', 'noms_client'),
        'ItemRandomProperties': ('propriete_aleatoire', 'noms_client'),
        # essai 8 : collection de vanité
        'VanityCollection': ('coa_vanite', 'vanite'),
    }
    DBC_TYPES.update(DBC_TYPES_09)
    GROUPE_LIEU = ('AreaTable', 'WMOAreaTable', 'AreaPOI', 'Map', 'TaxiNodes')
    TECHNIQUE_DBC = re.compile(r'\b(?:DND|NYI|UNUSED|TEST|QA|DEBUG)\b|^zz|\[PH\]|\bunused\b', re.I)
    # 0.9 : plus strict sur la casse (« The ultimate test of grit » est un vrai texte), et les tables CoA
    # marquent leurs restes par DEPRECATED, REUSE, (OLD), PLACEHOLDER
    TECHNIQUE_DBC_09 = re.compile(r'\b(?:DND|NYI|UNUSED|DEPRECATED|PLACEHOLDER|TODO|DEBUG)\b|^(?:REUSE|QA|TEST|Test|JSB)\b|'
                                  r'\[PH\]|\(OLD\)|^zz|^Test test$')
    # 0.9 : tables de Blizzard sans français dans patch-frFR-3 : le nom officiel est à reprendre (décision 31)
    # (ItemRandomProperties : les suffixes officiels viennent d'ItemRandomSuffix par le même anglais ; le reste se traduit)
    ATTENTE_NOM_OFFICIEL_09 = ('CharTitles', 'HolidayNames', 'HolidayDescriptions', 'QuestSort', 'CreatureFamily')
    # 0.9 : même anglais, un seul français officiel dans une table voisine (champ name seulement)
    SECOURS_TEXTE_09 = {
        'LFGDungeons': ['lieu'], 'BattlemasterList': ['lieu'], 'LFGDungeonGroup': [],
        'ItemRandomProperties': ['ItemRandomSuffix'],
        'QuestSort': ['SkillLine', 'ChrClasses', 'lieu'], 'CreatureFamily': ['SkillLine'],
    }

    def importer_dbc(self):
        """Une ligne par texte des DBC effectifs du client CoA (patch-M, sinon archives de langue). Francais officiel :
        - par numero : meme numero et meme anglais que le DBC Blizzard 3.3.5a (patch-enUS-3), francais de patch-frFR-3 ;
        - sinon par texte : le meme anglais a un seul francais officiel dans le meme DBC (zones : dans tous les
          DBC de lieux), comme la regle « texte identique » des quetes."""
        par_texte = defaultdict(set)
        for (dbc, i, champ), (en, fr) in self.off_dbc.items():
            if en and fr:
                g = 'lieu' if dbc in self.GROUPE_LIEU else dbc
                par_texte[(g, champ, K.norm(en))].add(fr)
        coa_ids = defaultdict(set)
        accord = Counter()
        liens_famille = O.familles_creature_competence()
        for (dbc, i, champ), (arch, en) in sorted(self.coa_dbc.items(), key=lambda x: (x[0][0], self._cle_num(x[0][1]), x[0][2])):
            if dbc not in self.DBC_TYPES:          # ChrClasses : noms de classes dans talents.tsv (type classe)
                continue
            typ, fam = self.DBC_TYPES[dbc]
            coa_ids[typ].add(i)
            note = '%s.dbc du client CoA (%s)' % (dbc, arch)
            l = [typ, i, '', champ, en, K.empreinte(en), '', 'a_traduire', '', note]
            b = self.off_dbc.get((dbc, i, champ))
            g = 'lieu' if dbc in self.GROUPE_LIEU else dbc
            frs = par_texte.get((g, champ, K.norm(en)), set())
            nouveau = dbc in self.DBC_TYPES_09
            secours = None
            if nouveau and champ == 'name' and len(frs) != 1:
                sk = liens_famille.get(i) if dbc == 'CreatureFamily' else None
                bs = self.off_dbc.get(('SkillLine', sk, 'name')) if sk else None
                if bs and bs[1] and O.meme_anglais(en, bs[0]):
                    secours = (bs[1], 'SkillLine.dbc frFR officiel (patch-frFR-3) : compétence n° %s de cette famille '
                                      '(CreatureFamily.dbc), même anglais' % sk)
                elif bs and bs[1] and O.meme_anglais('Pet - ' + en, bs[0]) and bs[1].startswith('Familier - '):
                    # « Pet - Cat » / « Familier - félin » : la compétence de familier de cette famille, préfixe ôté
                    nomf = bs[1][len('Familier - '):]
                    secours = (nomf[:1].upper() + nomf[1:],
                               'SkillLine.dbc frFR officiel (patch-frFR-3) : compétence n° %s de cette famille (CreatureFamily.dbc), '
                               '« %s » / « %s », préfixe « Familier - » ôté, majuscule initiale' % (sk, bs[0], bs[1]))
                for g2 in self.SECOURS_TEXTE_09.get(dbc, []):
                    if secours:
                        break
                    f2 = par_texte.get((g2, 'name', K.norm(en)), set())
                    if len(f2) == 1:
                        secours = (next(iter(f2)), '%s frFR officiel (patch-frFR-3) : même anglais, un seul français officiel '
                                                   'pour ce texte' % ('DBC de lieux' if g2 == 'lieu' else g2 + '.dbc'))
            if b and b[1] and O.meme_anglais(en, b[0]):
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = b[1], 'officiel', 'blizzard_frFR'
                l[K.I_NOTE] = joindre(note, '%s.dbc frFR officiel (patch-frFR-3), même numéro et même anglais que Blizzard' % dbc)
                quoi = 'par_numero'
            elif len(frs) == 1:
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = next(iter(frs)), 'officiel', 'blizzard_frFR'
                l[K.I_NOTE] = joindre(note, '%s frFR officiel (patch-frFR-3) : même anglais, un seul français officiel pour ce texte'
                                      % ('DBC de lieux' if g == 'lieu' else dbc + '.dbc'))
                quoi = 'par_texte'
            elif secours:
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = secours[0], 'officiel', 'blizzard_frFR'
                l[K.I_NOTE] = joindre(note, secours[1])
                quoi = 'par_table_voisine'
            elif nouveau and self.TECHNIQUE_DBC_09.search(en):
                l[K.I_ETAT] = 'technique'
                l[K.I_NOTE] = joindre(note, 'technique=texte de test, interne ou abandonné')
                quoi = 'technique'
            elif dbc in self.ATTENTE_NOM_OFFICIEL_09 and b and O.meme_anglais(en, b[0]):
                # anglais de Blizzard 3.3.5a, mais son français n'est pas dans patch-frFR-3 : nom officiel à reprendre
                # (décision 31 : Wowhead en français) ; jamais envoyé à la traduction
                l[K.I_SRC] = 'attente_nom_officiel'
                l[K.I_NOTE] = joindre(note, 'même anglais que %s.dbc de Blizzard 3.3.5a, français absent de patch-frFR-3 : '
                                            'nom officiel à reprendre (décision 31)' % dbc)
                quoi = 'attente_nom_officiel'
            elif not nouveau and self.TECHNIQUE_DBC.search(en):
                l[K.I_ETAT] = 'technique'
                l[K.I_NOTE] = joindre(note, 'technique=texte de test ou interne')
                quoi = 'technique'
            elif typ in ('zone', 'carte'):
                l = self.ligne_client(typ, i, champ, en, '', note, 'lieu', 'zone')
                if l[K.I_ETAT] == 'officiel':          # « officiel » de l'outil d'AscensionFR, sans preuve Blizzard
                    l[K.I_ETAT], l[K.I_SRC] = 'machine', 'archive_ascensionfr'
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'donné pour officiel par AscensionFR, absent du client frFR de Blizzard : classé machine')
                    if self.controle(en, l[K.I_FR], 'machine', typ):
                        l[K.I_ETAT] = 'a_revoir'
                quoi = 'archive_' + l[K.I_ETAT]
            else:
                quoi = 'a_traduire'
            if typ in ('zone', 'carte') and l[K.I_ETAT] == 'officiel':
                ex = self.zones_exil.get((typ, i, champ))
                if ex is not None:
                    vieux = self.ligne_client(typ, i, champ, ex['texte_en'], '', '', 'lieu', 'zone')
                    if vieux[K.I_ETAT] == 'officiel':
                        accord['zones_ascensionfr_officiel_' + ('identique' if vieux[K.I_FR] == l[K.I_FR] else 'different')] += 1
                        if vieux[K.I_FR] != l[K.I_FR]:
                            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'ancienne forme d\'AscensionFR : ' + cite(vieux[K.I_FR]))
            self.ajouter(l, fam)
            self.cr['dbc_%s_%s' % (typ, quoi)] += 1
            # formes feminine et masculine des races (le DBC enUS ne les a pas : l'anglais est celui du nom)
            if dbc == 'ChrRaces' and champ == 'name' and quoi == 'par_numero':
                for gch in ('name_female', 'name_male'):
                    bg = self.off_dbc.get(('ChrRaces', i, gch))
                    if bg and bg[1] and (dbc, i, gch) not in self.coa_dbc:
                        self.ajouter([typ, i, '', gch, en, K.empreinte(en), bg[1], 'officiel', 'blizzard_frFR',
                                      'ChrRaces.dbc frFR officiel (patch-frFR-3) : forme %s ; anglais du nom, identique'
                                      % ('féminine' if gch == 'name_female' else 'masculine')], fam)
                        self.cr['dbc_race_par_numero'] += 1
        disparues = [k for k in self.zones_exil if k[1] not in coa_ids[k[0]]]
        self.cr['zones_exil_absentes_du_client_coa'] = len(disparues)
        self.cr.update(accord)
        K.journal('import : DBC du client CoA (%d textes) ; zones db.exil.es absentes du client : %d ; %s'
                  % (len(self.coa_dbc), len(disparues), dict(accord)))

    @staticmethod
    def _cle_num(i):
        return tuple(int(p) for p in i.split('-')) if re.fullmatch(r'\d+(?:-\d+)*', i) else (10 ** 9,)

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
            if cle_v in INTERFACE_JOURNAL_COMBAT:
                # add-on 0.5 : forme du journal de combat, officiel si l'anglais est celui de Blizzard et le francais differe
                off = [o for o in self.off_interface.get(cle_v, []) if o[0] == 'GlobalStrings.lua' and o[1] == en
                       and o[2] and o[2] != en]
                if off and not self.controle(en, off[0][2], 'officiel', 'chaine_interface', cle_v):
                    l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = off[0][2], 'officiel', 'blizzard_frFR'
                    l[K.I_NOTE] = joindre(note, 'français officiel Blizzard (GlobalStrings.lua du client 3.3.5a frFR, '
                                          'patch-frFR-3.MPQ), anglais identique à celui de Blizzard (patch-enUS-3) pour la '
                                          'même clé', 'clé technique utilisée par le client : ' + INTERFACE_JOURNAL_COMBAT[cle_v])
                    self.ajouter(l)
                    self.cr['interface_officiel:journal_de_combat'] += 1
                    continue
            if tech:
                l[K.I_ETAT] = 'technique'
                l[K.I_NOTE] = joindre(note, 'technique=' + tech)
                self.ajouter(l)
                self.cr['interface_technique:' + tech.split(' ')[0]] += 1
                continue
            rap = r['rapprochement_archive']
            glue, arch = r['fr_ancien_glue_ascensionfr'], r['fr_archive']
            # Données 0.2 : le français OFFICIEL de Blizzard (GlobalStrings.lua / GlueStrings.lua du client 3.3.5a
            # frFR) d'abord, si l'anglais du client CoA est exactement celui de Blizzard pour la même clé.
            off = self.off_interface.get(cle_v, [])
            if 'glue' in r['contexte']:
                off = sorted(off, key=lambda x: x[0] != 'GlueStrings.lua')
            off = [o for o in off if o[2] and o[1] == en]
            if off:
                fichier, _, fr = off[0]
                preuve = ('français officiel Blizzard (%s du client 3.3.5a frFR, patch-frFR-3.MPQ), anglais identique à '
                          'celui de Blizzard (patch-enUS-3) pour la même clé' % fichier)
                ancien = arch or glue
                refus = self.controle(en, fr, 'officiel', 'chaine_interface')
                if not refus:
                    l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'officiel', 'blizzard_frFR'
                    l[K.I_NOTE] = joindre(note, preuve, 'ancienne proposition de l\'archive : ' + cite(ancien)
                                          if ancien and ancien != fr else '')
                    self.cr['interface_officiel:' + fichier] += 1
                    if ancien and ancien != fr:
                        self.cr['interface_officiel_remplace_archive'] += 1
                else:
                    l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'a_revoir', 'blizzard_frFR'
                    l[K.I_NOTE] = joindre(note, preuve, 'refusé au contrôle strict d\'interface : ' + ', '.join(refus))
                    self.cr['interface_officiel_refuse_controle'] += 1
                    self.ex('interface_officiel_refuse', l)
                self.ajouter(l)
                continue
            cands = []
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

    def appliquer_vocabulaire(self):
        """Decisions de vocabulaire de Dan du 03/11/2026 qui ne sont pas des substitutions simples (outils/vocabulaire.py)."""
        v = V.Vocabulaire(self.lignes, self.off_sorts)
        v.appliquer()
        for k, n in v.cr.items():
            self.cr['vocabulaire:' + k] += n
        for k, e in v.exemples.items():
            self.exemples['vocabulaire:' + k] = e
        K.journal('import : décisions de vocabulaire %s' % dict(v.cr))

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
    # Donnees 0.4 : enchantements propres a CoA, modele officiel (decision n° 14 de Dan, 04/11/2026)
    # ------------------------------------------------------------------
    def importer_enchantements_modele(self):
        """Noms d'enchantements CoA sans francais officiel (`a_traduire`) : francais du modele officiel de Blizzard pris
        sur les noms officiels de meme forme, au nombre pres (regles strictes : outils/modele_officiel.py). Fait APRES
        les corrections du glossaire (rien ne retouche ce francais) ; le controle d'entree passe quand meme. Etat
        machine, source modele_officiel, gabarits en note."""
        mo = MO.Modeles()
        ench = sorted((l for l in self.lignes.values() if l[K.I_TYPE] == 'enchantement'), key=tri)
        for l in ench:
            if l[K.I_ETAT] == 'officiel':
                mo.apprendre(l[K.I_EN], l[K.I_FR])
        mo.finir()
        self.cr.update({'enchantement_modele:' + k: v for k, v in mo.cr.items()})
        if ' and ' in mo.liant:
            fr_li, n, total = mo.liant[' and ']
            self.cr['enchantement_modele:liant_and_atteste'] = n
        for l in ench:
            if l[K.I_ETAT] != 'a_traduire':
                continue
            fr, info = mo.traduire(l[K.I_EN])
            if fr is None:
                self.cr['enchantement_modele_reste_anglais:' + info] += 1
                continue
            note = 'modèle officiel (décision n° 14 de Dan, 04/11/2026) : ' + ' ; '.join(info)
            refus = self.controle(l[K.I_EN], fr, 'machine', l[K.I_TYPE]) + mo.controle(l[K.I_EN], fr)
            if refus:
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'a_revoir', MO.SOURCE
                l[K.I_NOTE] = joindre(l[K.I_NOTE], note, 'refusé au contrôle d\'entrée : ' + ', '.join(refus))
                self.cr['enchantement_modele_refuse_controle'] += 1
                self.ex('enchantement_modele_refuse', l)
                continue
            l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'machine', MO.SOURCE
            l[K.I_NOTE] = joindre(l[K.I_NOTE], note)
            self.cr['enchantement_modele_machine:' + ('plusieurs_lignes' if MO.SAUTS.search(l[K.I_EN]) else 'une_ligne')] += 1
            self.ex('enchantement_modele_machine', l, 10)
        K.journal('import : enchantements CoA par le modèle officiel %s'
                  % {k: v for k, v in sorted(self.cr.items()) if k.startswith('enchantement_modele')})

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
    # 7. Atelier de traduction (05/11/2026) : la couche des traductions de Claude (`traductions/`)
    # ------------------------------------------------------------------
    def appliquer_couche(self):
        """Fusionne `traductions/<famille>/<lot>.tsv` (outils/couche.py) APRES tout le reste, relus compris : une
        traduction de Claude ne remplace jamais une ligne officiel, relu ou technique ; elle s'applique sur une ligne
        a_traduire ou a_revoir (ou machine de l'archive pour les sorts et talents des classes) si l'empreinte de
        l'anglais est la meme et si le controle d'entree passe (etat machine, source claude). Anglais change : la ligne
        passe a_revoir, l'ancien francais de Claude en note. Refusee : la ligne reste a son etat d'avant."""
        couche, doublons, erreurs = CO.lire_couche()
        if erreurs:
            raise SystemExit('ERREUR : couche des traductions mal formée : %s' % erreurs[:5])
        cr, refus, perimees, orphelines = CO.appliquer(
            self.lignes, self.famille_de, couche,
            lambda en, fr, typ, i: self.controle(en, fr, 'machine', typ, i))
        cr['doublon_ecarte'] = len(doublons)
        for k, n in cr.items():
            self.cr['couche_claude:' + k] += n
        self.cr['couche_claude:lignes_lues'] = len(couche)
        os.makedirs(K.TRAVAIL, exist_ok=True)
        with open(os.path.join(K.TRAVAIL, 'couche_refus.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('quoi\tfichier\ttype\tid\tsous_id\tchamp\traisons\ten\tfr\n')
            for k, rel, r, en, fr in refus:
                f.write('\t'.join(['refusee', rel] + [K.echapper(x) for x in k] + [', '.join(r), K.echapper(en), K.echapper(fr)]) + '\n')
            for k, rel in perimees:
                f.write('\t'.join(['perimee', rel] + [K.echapper(x) for x in k] + ['anglais modifié', '', '']) + '\n')
            for k, rel in orphelines:
                f.write('\t'.join(['orpheline', rel] + [K.echapper(x) for x in k] + ['clé absente de textes/', '', '']) + '\n')
            for k, garde, ecarte in doublons:
                f.write('\t'.join(['doublon', ecarte] + [K.echapper(x) for x in k] + ['déjà dans ' + garde, '', '']) + '\n')
        for k, rel, r, en, fr in refus[:10]:
            self.exemples['couche_claude_refus'].append({'cle': '/'.join(k), 'fichier': rel, 'raisons': r,
                                                         'en': en[:160], 'fr': fr[:160]})
        K.journal('import : couche des traductions de Claude, %d lignes lues ; %s ; refus dans %s'
                  % (len(couche), dict(cr), os.path.join(K.TRAVAIL, 'couche_refus.tsv')))

    def harmoniser_officiel(self):
        """Une meme phrase anglaise, un meme francais, l'officiel d'abord (essai 7, 07/11/2026) : une ligne `machine`
        dont l'anglais EXACT (meme type et meme champ) a un seul francais officiel ailleurs prend ce francais.
        Exemples : la pierre de foyer de CoA (sort 80133) avait une traduction machine differente de l'officielle des
        sorts 8690… ; l'add-on, devant deux francais pour un meme anglais, n'affichait rien. « Tallstrider » ->
        « Haut-trotteur » (officiel) et non « Grand trotteur ». Meme type exige : « Sunny » (creature) ne prend pas
        « Temps ensoleille » (meteo). Jamais sur relu ni technique ; controle de structure de l'officiel."""
        off = defaultdict(set)
        for l in self.lignes.values():
            if l[K.I_ETAT] == 'officiel' and l[K.I_FR] and l[K.I_FR] != l[K.I_EN]:
                off[(l[K.I_TYPE], l[K.I_CHAMP], l[K.I_EN])].add(l[K.I_FR])
        n = 0
        for k, l in self.lignes.items():
            if l[K.I_ETAT] != 'machine':
                continue
            frs = off.get((l[K.I_TYPE], l[K.I_CHAMP], l[K.I_EN]))
            if not frs or len(frs) != 1:
                continue
            fr = next(iter(frs)).replace('’', "'")      # typographie du projet : apostrophe droite
            # controle d'une ligne machine (glossaire compris : PvP garde, decision 30) ; refusee : on n'y touche pas
            if fr == l[K.I_FR] or self.controle(l[K.I_EN], fr, 'machine', l[K.I_TYPE], k[1]):
                continue
            self.ex('harmonise_officiel', l)
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'harmonisé sur le français officiel du même anglais (avant : « %s »)'
                                  % cite(l[K.I_FR], 120))
            l[K.I_FR] = fr
            l[K.I_SRC] = 'blizzard_frFR_meme_anglais'
            n += 1
        self.cr['harmonise_officiel'] = n
        K.journal('import : %d lignes machine harmonisées sur le français officiel du même anglais' % n)

    def noms_officiels_web(self):
        """Décisions 23 et 31 : noms officiels de Blizzard absents de nos fichiers, relevés sur Wowhead en français
        (glossaire/noms_officiels_web.tsv : type, champ, en, fr, id facultatif, url). Une ligne de ce type et de ce champ
        dont l'anglais est EXACTEMENT celui du relevé prend ce français (état officiel, source wowhead_frFR, adresse
        en note). Jamais sur relu, officiel ni technique ; contrôle d'une ligne officielle."""
        p = os.path.join(K.RACINE, 'glossaire', 'noms_officiels_web.tsv')
        if not os.path.exists(p):
            return
        par_en, par_id = {}, {}
        with open(p, encoding='utf-8') as f:
            for i, ligne in enumerate(f):
                c = ligne.rstrip('\n').split('\t')
                if i == 0 or len(c) < 6 or not c[3]:
                    continue
                typ, champ, en, fr, id_, url = (K.desechapper(x) for x in c[:6])
                (par_id if id_ else par_en)[(typ, champ, en) + ((id_,) if id_ else ())] = (fr, url)
        n = Counter()
        for k, l in self.lignes.items():
            if l[K.I_ETAT] not in ('a_traduire', 'a_revoir', 'machine'):
                continue
            t = par_id.get((l[K.I_TYPE], l[K.I_CHAMP], l[K.I_EN], l[K.I_ID])) or par_en.get((l[K.I_TYPE], l[K.I_CHAMP], l[K.I_EN]))
            if not t:
                continue
            refus = self.controle(l[K.I_EN], t[0], 'officiel', l[K.I_TYPE], k[1])
            if refus:
                n['refus'] += 1
                self.ex('nom_officiel_web_refuse', l)
                continue
            ancien = l[K.I_FR] if l[K.I_ETAT] == 'machine' else ''
            l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = t[0], 'officiel', 'wowhead_frFR'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'nom officiel de Blizzard relevé sur Wowhead en français (décisions 23 et 31) : '
                                  + t[1], 'ancienne traduction : ' + cite(ancien, 120) if ancien else '')
            n[l[K.I_TYPE]] += 1
        # un type relevé : ses lignes « en attente du nom officiel » absentes du relevé partent à la traduction
        releves = {k[0] for k in par_en} | {k[0] for k in par_id}
        for l in self.lignes.values():
            if l[K.I_SRC] == 'attente_nom_officiel' and l[K.I_TYPE] in releves:
                l[K.I_SRC] = ''
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'absent du relevé Wowhead (glossaire/noms_officiels_web.tsv) : à traduire')
                n['libere:' + l[K.I_TYPE]] += 1
        self.cr.update({'nom_officiel_web:' + a: b for a, b in n.items()})
        K.journal('import : noms officiels relevés sur Wowhead : %s' % dict(n))

    def focalisation_interface(self):
        """0.9 : CoA définit ses objets de focalisation dans GlobalStrings (SPELL_FOCUS_OBJECT_<n> = « Anvil »…) :
        même numéro que SpellFocusObject.dbc et même anglais -> le français officiel de la table (« ForgeRune » de
        l'archive devient « Forge runique »)."""
        n = 0
        for k, l in self.lignes.items():
            m = re.fullmatch(r'SPELL_FOCUS_OBJECT_(\d+)', l[K.I_ID]) if l[K.I_TYPE] == 'chaine_interface' else None
            if not m or l[K.I_ETAT] not in ('machine', 'a_traduire', 'a_revoir'):
                continue
            o = self.lignes.get(('objet_focalisation', m.group(1), '', 'name'))
            if not o or o[K.I_ETAT] != 'officiel' or o[K.I_EN] != l[K.I_EN] or not o[K.I_FR]:
                continue
            if self.controle(l[K.I_EN], o[K.I_FR], 'officiel', l[K.I_TYPE], l[K.I_ID]):
                continue
            ancien = l[K.I_FR]
            l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = o[K.I_FR], 'officiel', 'blizzard_frFR_meme_anglais'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'SpellFocusObject.dbc frFR officiel (patch-frFR-3), même numéro et même anglais'
                                  + (' (avant : %s)' % cite(ancien, 80) if ancien else ''))
            n += 1
        self.cr['focalisation_interface'] = n
        K.journal('import : %d objets de focalisation de GlobalStrings sur le français officiel' % n)

    def limites_objets_par_nom(self):
        """0.9 : une catégorie d'objets limités (« Unique-Equipped: <nom> (1) ») qui porte EXACTEMENT le nom anglais
        d'un objet prend le français de ce nom s'il est unique (officiel -> officiel, sinon machine)."""
        noms = defaultdict(set)
        for l in self.lignes.values():
            if l[K.I_TYPE] == 'objet' and l[K.I_CHAMP] == 'name' and l[K.I_FR] and l[K.I_ETAT] in ('officiel', 'relu', 'machine'):
                noms[l[K.I_EN]].add((l[K.I_FR], l[K.I_ETAT] == 'officiel', l[K.I_ID]))
        n = Counter()
        for k, l in self.lignes.items():
            if l[K.I_TYPE] != 'categorie_limite_objet' or l[K.I_ETAT] != 'a_traduire':
                continue
            cands = noms.get(l[K.I_EN], set())
            frs = {c[0] for c in cands}
            if len(frs) != 1:
                n['sans_nom_unique'] += 1
                continue
            fr = next(iter(frs))
            off = all(c[1] for c in cands)
            if self.controle(l[K.I_EN], fr, 'officiel' if off else 'machine', l[K.I_TYPE], k[1]):
                n['refus'] += 1
                continue
            l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'officiel' if off else 'machine', 'nom_objet_meme_anglais'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'même anglais que le nom de l\'objet n° %s : son français'
                                  % ', '.join(sorted({c[2] for c in cands}, key=self._cle_num)[:3]))
            n['officiel' if off else 'machine'] += 1
        self.cr.update({'limite_objet_par_nom:' + a: b for a, b in n.items()})
        K.journal('import : catégories d\'objets limités nommées comme un objet : %s' % dict(n))

    # ------------------------------------------------------------------
    # 6. Ecriture
    # ------------------------------------------------------------------
    def famille_de(self, k, l):
        f = self.famille.get(k)
        if f:
            return f
        t = l[K.I_TYPE]
        for fam, _, types, _ in K.FAMILLES:
            if t in types and fam not in ('sorts_classes', 'talents', 'sorts_standard', 'sorts_coa', 'sorts_objets'):
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


RE_VOIE = re.compile(
    r"(?P<art>\b(?:[Ll]e|[Ll]a|[Dd]u|[Aa]u|[Dd]ans(?: le| la)?|[Dd]e(?: la)?|[Àà](?: la)?|[Ss]ur(?: le| la)?"
    r"|[Pp]our(?: le| la)?)\s+)?"
    r"(?P<nom>(?:[Cc]hemin|[Vv]oie|[Rr]oute|[Ss]entier)\s+(?:vers|de)\s+l['’]\s*[Aa]scension\b|Path to Ascension\b)")
ARTICLES_VOIE = {'le': 'la', 'la': 'la', 'du': 'de la', 'de': 'de la', 'de la': 'de la', 'au': 'à la', 'à': 'à la',
                 'à la': 'à la', 'dans': 'dans la', 'dans le': 'dans la', 'dans la': 'dans la', 'sur': 'sur la',
                 'sur le': 'sur la', 'sur la': 'sur la', 'pour': 'pour la', 'pour le': 'pour la', 'pour la': 'pour la'}


def voie_ascension_fr(en, fr):
    """Décision 34 : « Path to Ascension » se dit « Voie de l'Ascension » partout, avec l'article qui va (« de la Voie
    de l'Ascension », « dans la Voie de l'Ascension ») ; un titre « Path to Ascension: X » commence sans article."""
    def rempl(m):
        art = (m.group('art') or '').strip()
        if not art:
            return "Voie de l'Ascension"
        if m.start() == 0 and art in ('La', 'Le') and en.startswith('Path to Ascension'):
            return "Voie de l'Ascension"
        nouv = ARTICLES_VOIE[art.lower()]
        if art[0].isupper():
            nouv = nouv[0].upper() + nouv[1:]
        return nouv + " Voie de l'Ascension"
    return RE_VOIE.sub(rempl, fr)


def _voie_ascension(self):
    """0.9.4 : décision 34 (Dan, 08/11/2026), après la couche des traductions : toute ligne (sauf officielle) dont
    l'anglais contient « Path to Ascension » prend « Voie de l'Ascension » (« Chemin vers l'Ascension », « La voie de
    l'Ascension », « Path to Ascension » laissé en anglais…). Contrôle d'entrée refait ; refus : ligne inchangée."""
    n = Counter()
    for l in self.lignes.values():
        if 'Path to Ascension' not in l[K.I_EN] or not l[K.I_FR] or l[K.I_ETAT] in ('officiel', 'technique'):
            continue
        fr = voie_ascension_fr(l[K.I_EN], l[K.I_FR])
        if fr == l[K.I_FR]:
            n['deja'] += 1
            continue
        if self.controle(l[K.I_EN], fr, 'machine' if l[K.I_ETAT] != 'relu' else 'relu', l[K.I_TYPE]):
            n['refus_controle'] += 1
            continue
        l[K.I_FR] = fr
        l[K.I_NOTE] = joindre(l[K.I_NOTE], 'décision 34 : « Voie de l\'Ascension »')
        n['harmonisees_' + l[K.I_ETAT]] += 1
    self.cr.update({'voie_ascension:' + a: b for a, b in n.items()})
    K.journal('import : décision 34, Voie de l\'Ascension : %s' % dict(n))


Importeur.voie_ascension = _voie_ascension


# ---------------------------------------------------------------------------------------------------------------
# Décision 35 (Dan, 10/11/2026) : la difficulté « Ascended » de CoA se dit « transcendé », accordé.
# ---------------------------------------------------------------------------------------------------------------
_ESP = '[   ]'
RE_ASC_EN = re.compile(r'(?i)ascen[ns]*ded')   # aussi après un code couleur, en minuscules, ou avec la coquille (« Ascennded », « Ascensded »)
# têtes au féminin ou au pluriel, juste avant le mot ou plus haut dans le même groupe de mots
_DEB = r"(?<![A-Za-zÀ-ÿ])"
_GROUPE = r"(?:(?!" + _ESP + r"[-–—]" + _ESP + r")[^.,;:()@|<>\n])*?"
RE_ASC_ACCORDS = [
    (re.compile(_DEB + r"[Dd]e" + _ESP + r"l'Ascended\b"), lambda m: m.group(0)[0] + 'u Transcendé'),
    (re.compile(_DEB + r"l'Ascended\b"), 'le Transcendé'),
    (re.compile(_DEB + r"L'Ascended\b"), 'Le Transcendé'),
    (re.compile(_DEB + r"([Dd]es)(" + _ESP + r")Ascended\b"), r'\1\2Transcendés'),
    (re.compile(_DEB + r"(en)(" + _ESP + r")Ascended\b"), r'\1\2mode transcendé'),
    (re.compile(_DEB + r"((?:[Mm]ode|Cauchemar|royaume|raid|Raid|butin|Butin)" + _ESP + r")Ascended\b"), r'\1transcendé'),
    (re.compile(_DEB + r"(Vaincre|Battez|Vainquez)(" + _ESP + r")Ascended\b"), r'\1\2Transcendé'),
    (re.compile(_DEB + r"([Dd]ifficulté" + _ESP + r"[Mm]ythique" + _ESP + r"et" + _ESP + r")Ascended\b"), r'\1transcendée'),
    (re.compile(_DEB + r"((?:[Dd]ifficulté|Montre|Crinière-céleste|Protection|Bénédiction|l'Horreur|l'Abomination)"
                + _ESP + r")Ascended\b"), r'\1transcendée'),
    (re.compile(_DEB + r"((?:Caverne|[Bb]ataille)" + _GROUPE + _ESP + r")Ascended\b"), r'\1transcendée'),
    (re.compile(_DEB + r"((?:Ruines)" + _GROUPE + _ESP + r")Ascended\b"), r'\1transcendées'),
    (re.compile(_DEB + r"(Mécaniques" + _ESP + r")Ascended\b"), r'\1transcendées'),
    (re.compile(_DEB + r"((?:[Rr]aids|Pantalons|Anciens|[ÉE]clats|[Bb]oss)" + _ESP + r")Ascended\b"), r'\1transcendés'),
]
# une majuscule en tête de texte, d'étiquette, de titre ou après une ponctuation forte
RE_ASC_MAJ = re.compile(r"(^|[@>/]|[:!\-–—]" + _ESP + r"|\|c[0-9a-fA-F]{8})Ascended\b")
RE_ASC_VAINCRE = re.compile(r"^(Vaincre|Battez|Vainquez)" + _ESP + r"Transcendé" + _ESP + r":" + _ESP
                            + r"(.+?)" + _ESP + r"(dans|à|au|sur)" + _ESP + r"([^.]+)\.$")
RE_ASC_RESTE = re.compile(r"\bAscended\b")
RE_ASC_ELEVE = re.compile(r"\bélevé(e?s?)\b")


def transcende_fr(fr):
    """Remplace « Ascended » resté dans le français par « transcendé », accordé quand la tête est connue."""
    fr = fr.replace('@Ascended Raid@', '@Raid transcendé@')
    for motif, rempl in RE_ASC_ACCORDS:
        fr = motif.sub(rempl, fr)
    fr = RE_ASC_MAJ.sub(lambda m: m.group(1) + 'Transcendé', fr)
    fr = RE_ASC_RESTE.sub('transcendé', fr)
    # « Vaincre Transcendé : X dans Y. » (calque de « Defeat Ascended: X in Y. ») -> « Vaincre X dans Y (transcendé). »
    return RE_ASC_VAINCRE.sub(r'\1 \2 \3 \4 (transcendé).', fr)


def _transcende(self):
    """10/11/2026 : décision 35 (remplace la décision 3). Toute ligne non officielle dont l'anglais dit « Ascended »
    et dont le français porte encore « Ascended » (ou « élevé », traduction machine du même mot) prend
    « transcendé ». Les cas que la règle ne sait pas accorder sont dans glossaire/transcende.tsv (anglais exact →
    français, appliqué à chaque import). Les textes officiels de Blizzard ne sont pas touchés (« Alumeth le Sublimé »). Contrôle d'entrée
    refait ; refus : ligne inchangée (le contrôle final la signalera)."""
    manuel = {}
    chemin = os.path.join(K.GLOSSAIRE, 'transcende.tsv')
    if os.path.exists(chemin):
        with open(chemin, encoding='utf-8', newline='') as h:
            for ligne in h:
                ligne = ligne.rstrip('\r\n')
                if not ligne or ligne.startswith('#'):
                    continue
                c = ligne.split('\t')
                if c[0] == 'en':
                    continue
                manuel[c[0]] = c[1]
    n = Counter()
    for l in self.lignes.values():
        en = l[K.I_EN]
        if not RE_ASC_EN.search(en):
            continue
        if l[K.I_ETAT] in ('officiel', 'technique'):
            continue
        fr = l[K.I_FR]
        if en in manuel:
            nouv = manuel[en]
        elif not fr:
            continue
        elif 'Ascended' in fr:
            nouv = transcende_fr(fr)
        elif RE_ASC_ELEVE.search(fr):
            nouv = RE_ASC_ELEVE.sub(r'transcendé\1', fr)
        else:
            continue
        if nouv == fr:
            n['deja'] += 1
            continue
        # une ligne déjà « à revoir » le reste (elle a d'autres défauts) : on y écrit quand même le bon mot
        if l[K.I_ETAT] != 'a_revoir' and self.controle(en, nouv, 'relu' if l[K.I_ETAT] == 'relu' else 'machine',
                                                        l[K.I_TYPE]):
            n['refus_controle'] += 1
            continue
        n[('manuel_' if en in manuel else 'regle_') + (l[K.I_ETAT] or 'vide')] += 1
        l[K.I_FR] = nouv
        # la table est rejouée à chaque import : pas d'état « relu » (une ligne dérivée, créée par une passe
        # tardive, deviendrait orpheline à l'import suivant)
        if en in manuel and l[K.I_ETAT] in ('a_traduire', 'a_revoir', ''):
            l[K.I_ETAT] = 'machine'
        l[K.I_NOTE] = joindre(l[K.I_NOTE], 'décision 35 : « transcendé »')
    # ce qui reste : « Ascended » encore dans un français non officiel (à corriger à la main dans transcende.tsv)
    reste = [l for l in self.lignes.values()
             if 'Ascended' in l[K.I_FR] and l[K.I_ETAT] not in ('officiel', 'technique')]
    n['reste_ascended_dans_le_francais'] = len(reste)
    for l in reste[:40]:
        K.journal('import : décision 35, reste : %s %s | %s | %s' % (l[K.I_TYPE], l[K.I_ID], l[K.I_EN][:90], l[K.I_FR][:90]))
    self.cr.update({'transcende:' + a: b for a, b in n.items()})
    K.journal('import : décision 35, « transcendé » : %s' % dict(n))


Importeur.transcende = _transcende

RE_PREMS_EN = re.compile(r"^Realm First! (?:.+?: )?Level (\d+)(?: .+)?$")
_E = '[ \u00a0\u202f]'
RE_PREMS_FR = [re.compile(r"^(?P<pre>.+?" + _E + r":" + _E + r")?[Nn]iveau" + _E + r"(?P<n>\d+)" + _E + r"(?P<g>«.*?»)"
                          + _E + r"du" + _E + r"royaume$"),
               re.compile(r"^(?P<pre>.+?" + _E + r":" + _E + r")?(?P<x>.+?)" + _E + r"de" + _E + r"niveau" + _E
                          + r"(?P<n>\d+)" + _E + r"(?P<g>«.*?»)" + _E + r"du" + _E + r"royaume$")]


def _prems_niveau(self):
    """0.9.4 : décision 24, modèle de niveau de Blizzard (« Guerrier « Prem's » au niveau 80 sur le royaume ») pour les
    « Realm First! [X: ]Level N [Y] » restés au modèle « … de niveau N « Prem's » du royaume » (chantier M)."""
    n = Counter()
    for l in self.lignes.values():
        if l[K.I_TYPE] != 'haut_fait' or l[K.I_CHAMP] != 'name' or not l[K.I_FR] or l[K.I_ETAT] in ('officiel', 'relu'):
            continue
        m = RE_PREMS_EN.match(l[K.I_EN])
        if not m:
            continue
        for rx in RE_PREMS_FR:
            f = rx.match(l[K.I_FR])
            if f and f.group('n') == m.group(1):
                fr = (f.group('pre') or '') + ((f.group('x') + ' ') if 'x' in rx.groupindex and f.group('x') else '') \
                    + f.group('g') + ' au niveau ' + f.group('n') + ' sur le royaume'
                if fr != l[K.I_FR] and not self.controle(l[K.I_EN], fr, 'machine', l[K.I_TYPE]):
                    l[K.I_FR] = fr
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'décision 24 : modèle de niveau de Blizzard')
                    n['corrigees'] += 1
                break
    self.cr.update({'prems_niveau:' + a: b for a, b in n.items()})
    K.journal('import : décision 24, modèle de niveau : %s' % dict(n))


Importeur.prems_niveau = _prems_niveau


def _pierres_de_retraite(self):
    """0.9.4 (essai 8, n° 26) : pierres de retraite de la collection de vanité (« Stone of Retreat: Eastvale Logging
    Camp ») : l'objet prend le nom français du sort qu'il lance (même anglais exact, un seul français), qui suit les
    noms de lieux officiels (« … : Camp de bûcherons du Val d'est ») ; la traduction de l'archive (« camp forestier
    d'Eastvale ») est écartée. Avant noms_vanite (les objets de vanité reprennent le nom de l'objet)."""
    sorts = defaultdict(set)
    for l in self.lignes.values():
        if l[K.I_TYPE] == 'sort' and l[K.I_CHAMP] == 'Name' and l[K.I_FR] and l[K.I_EN].startswith('Stone of Retreat: ') \
                and l[K.I_ETAT] in ('officiel', 'relu', 'machine'):
            sorts[l[K.I_EN]].add(l[K.I_FR])
    n = Counter()
    for l in self.lignes.values():
        if l[K.I_TYPE] != 'objet' or l[K.I_CHAMP] != 'name' or l[K.I_EN] not in sorts \
                or l[K.I_ETAT] not in ('machine', 'a_traduire', 'a_revoir'):
            continue
        if len(sorts[l[K.I_EN]]) != 1:
            n['plusieurs_francais'] += 1
            continue
        fr = next(iter(sorts[l[K.I_EN]]))
        if fr == l[K.I_FR]:
            n['deja'] += 1
            continue
        if self.controle(l[K.I_EN], fr, 'machine', 'objet'):
            n['refus'] += 1
            continue
        ancien = l[K.I_FR]
        l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = fr, 'machine', 'nom_sort_meme_anglais'
        l[K.I_NOTE] = joindre(l[K.I_NOTE], 'nom du sort lancé (même anglais)'
                              + (' ; avant : %s' % cite(ancien, 120) if ancien else ''))
        n['repris'] += 1
    self.cr.update({'pierres_de_retraite:' + a: b for a, b in n.items()})
    K.journal('import : pierres de retraite, nom du sort : %s' % dict(n))


Importeur.pierres_de_retraite = _pierres_de_retraite

RE_STATIQUE = re.compile(r"(Génère|Épuise|Consomme)([ \u00a0])(\d+)[ \u00a0]Statique\b")   # (après « |cffcc99ff » : pas de \b)


def _harmoniser_statique(self):
    """0.9.4 : ligne de ressource des sorts de CoA (« |cffcc99ffDepletes 40 Static|r ») : la forme majoritaire des
    traductions, « Épuise 40 points de Statique » (111 textes contre 72 « Épuise 40 Statique ») ; décision 20 inchangée
    (Static = Statique)."""
    n = 0
    for l in self.lignes.values():
        if 'Static' not in l[K.I_EN] or not l[K.I_FR] or l[K.I_ETAT] in ('officiel', 'technique'):
            continue
        fr = RE_STATIQUE.sub(lambda m: '%s%s%s points de Statique' % (m.group(1), m.group(2), m.group(3)), l[K.I_FR])
        if fr != l[K.I_FR] and not self.controle(l[K.I_EN], fr, 'machine' if l[K.I_ETAT] != 'relu' else 'relu',
                                                 l[K.I_TYPE]):
            l[K.I_FR] = fr
            n += 1
    self.cr['harmoniser_statique'] = n
    K.journal('import : « N points de Statique » : %d lignes' % n)


Importeur.harmoniser_statique = _harmoniser_statique

RE_MOT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿŒœ]+")
RE_PROTEGE = re.compile(r"(\|c[0-9a-fA-F]{8}|\|r|\|H.*?\|h|\$\S*|@[^@\n]*@|<[^>\n]*>)")
ACCENTS_MAJ = {'E': 'ÉÈÊ', 'A': 'ÂÀ', 'I': 'Î', 'O': 'Ô', 'U': 'Û'}
PAS_FRANCAIS = {'Epic'}   # mot anglais gardé tel quel dans certains textes


def _plat(t):
    t = unicodedata.normalize('NFD', t.lower())
    return ''.join(c for c in t if unicodedata.category(c) != 'Mn').replace('\u2019', "'").strip()


def _majuscules_accentuees(self):
    """0.9.5 (version publique, justesse de la langue) : capitale sans son accent dans les traductions machine
    (« Eclat de lave », « Ame affaiblie », « Epaulières ») : la typographie française garde l'accent sur les capitales,
    comme le français officiel de Blizzard (« Éclair de givre »). Un mot capitalisé est corrigé seulement si sa forme
    sans accent n'apparaît JAMAIS en minuscule dans le français officiel, et sa forme accentuée au moins 3 fois."""
    vocab = Counter()
    for l in self.lignes.values():
        if l[K.I_ETAT] == 'officiel' and l[K.I_FR]:
            for m in RE_MOT.findall(l[K.I_FR]):
                if m[0].islower():
                    vocab[m] += 1
    memo = {}

    def corr(m):
        w = m.group(0)
        if w not in memo:
            r = None
            if len(w) > 1 and w[0] in ACCENTS_MAJ and w[1:].islower() and vocab[w.lower()] == 0 \
                    and w not in PAS_FRANCAIS:
                c = [(vocab[a.lower() + w[1:]], a + w[1:]) for a in ACCENTS_MAJ[w[0]]]
                c = [x for x in c if x[0] >= 3]
                if c:
                    r = max(c)[1]
            memo[w] = r
        return memo[w] or w

    n = Counter()
    for l in self.lignes.values():
        if l[K.I_ETAT] != 'machine' or not l[K.I_FR]:
            continue
        morceaux = RE_PROTEGE.split(l[K.I_FR])
        fr = ''.join(x if i % 2 else RE_MOT.sub(corr, x) for i, x in enumerate(morceaux))
        if fr != l[K.I_FR] and not self.controle(l[K.I_EN], fr, 'machine', l[K.I_TYPE]):
            l[K.I_FR] = fr
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'capitale accentuée (0.9.5)')
            n[l[K.I_TYPE]] += 1
    self.cr['majuscules_accentuees'] = sum(n.values())
    K.journal('import : capitales accentuées : %d lignes (%s)' % (sum(n.values()), dict(n.most_common(6))))


Importeur.majuscules_accentuees = _majuscules_accentuees

TYPES_SPECIALISATION = ('coa_specialisation', 'coa_avancement_onglet', 'arbre_coa', 'arbre_talents', 'competence',
                        'coa_etiquette_sort')
CHOIX_SPECIALISATION = {'Farstrider': 'Pérégrin'}   # à égalité : le nom des Pérégrins de Quel'Thalas (officiel)


def _harmoniser_specialisations(self):
    """0.9.5 (version publique) : une spécialisation porte le même nom dans toutes les fenêtres (choix de la
    spécialisation, onglets de l'avancement, arbres de talents, compétences, étiquettes des sorts) et dans le nom du
    sort qui la représente : « Boltslinger » était « Tireur d'arbalète », « Tireur de carreaux » et « Lance-carreaux ».
    Forme officielle s'il y en a une, sinon la plus répandue entre les fenêtres ; jamais le nom d'une autre
    spécialisation (« Rime » ne devient pas « Givre », le nom de « Frost »)."""
    par_en = defaultdict(lambda: defaultdict(set))
    sures = defaultdict(set)
    sorts_sures = defaultdict(set)
    for l in self.lignes.values():
        if l[K.I_TYPE] in TYPES_SPECIALISATION and l[K.I_CHAMP] in ('name', 'Name', 'nom') and l[K.I_FR] \
                and l[K.I_ETAT] in ('machine', 'officiel', 'relu'):
            par_en[l[K.I_EN]][l[K.I_FR]].add(l[K.I_TYPE])
            if l[K.I_ETAT] in ('officiel', 'relu'):
                sures[l[K.I_EN]].add(l[K.I_FR])
        elif l[K.I_TYPE] == 'sort' and l[K.I_CHAMP] == 'Name' and l[K.I_ETAT] == 'officiel' and l[K.I_FR]:
            sorts_sures[l[K.I_EN]].add(l[K.I_FR])
    for en in par_en:               # « Rime » : talent officiel « Frimas » (chevalier de la mort)
        if not sures.get(en) and len(sorts_sures.get(en, ())) == 1:
            sures[en] = set(sorts_sures[en])
    pris = defaultdict(set)
    for en, d in par_en.items():
        for f in d:
            pris[_plat(f)].add(en)
    canon = {}
    for en, d in par_en.items():
        if len(d) < 2 and not (sures.get(en) and set(d) - sures[en]):
            continue
        if sures.get(en):
            canon[en] = sorted(sures[en])[0]
            continue
        if en in CHOIX_SPECIALISATION and CHOIX_SPECIALISATION[en] in d:
            canon[en] = CHOIX_SPECIALISATION[en]
            continue
        libres = [f for f in d if not (pris[_plat(f)] - {en})]
        if libres:
            canon[en] = min(libres, key=lambda f: (-len(d[f]), 'coa_specialisation' not in d[f], f))
    n = Counter()
    for l in self.lignes.values():
        if l[K.I_ETAT] != 'machine' or l[K.I_CHAMP] not in ('name', 'Name', 'nom') or l[K.I_EN] not in canon:
            continue
        if l[K.I_TYPE] not in TYPES_SPECIALISATION and l[K.I_TYPE] != 'sort':
            continue
        cn = canon[l[K.I_EN]]
        if l[K.I_FR] != cn and not self.controle(l[K.I_EN], cn, 'machine', l[K.I_TYPE]):
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'spécialisation harmonisée (0.9.5) : ancien « %s »' % l[K.I_FR])
            l[K.I_FR] = cn
            n[l[K.I_TYPE]] += 1
    self.cr['harmoniser_specialisations'] = sum(n.values())
    K.journal('import : noms de spécialisation harmonisés : %d noms anglais, %d lignes (%s)'
              % (len(canon), sum(n.values()), dict(n)))


Importeur.harmoniser_specialisations = _harmoniser_specialisations

RE_COULEUR = re.compile(r'\|c([0-9a-fA-F]{8})(.*?)\|r', re.S)


def _harmoniser_noms_sorts(self):
    """0.9.5 (version publique) : un sort doit porter le même nom partout. (1) Même nom anglais, traductions machine
    différentes (« Zealotry » : « Zèle » et « Zélotisme ») : la forme officielle ou relue, sinon la majoritaire (à
    égalité : la plus accentuée, puis l'ordre alphabétique). (2) Nom de sort cité en couleur dans une description ou une
    aura (« |cffffffffLava Shard|r ») : écrit comme le nom du sort (« Éclat de lave », pas « Eclat de lave »), si la
    citation est employée comme un nom (capitale initiale). Lignes machine seulement ; chaque correction passe le
    contrôle."""
    noms, sures = defaultdict(Counter), defaultdict(Counter)
    for l in self.lignes.values():
        if l[K.I_TYPE] == 'sort' and l[K.I_CHAMP] == 'Name' and l[K.I_FR] \
                and l[K.I_ETAT] in ('machine', 'officiel', 'relu') and l[K.I_FR] != l[K.I_EN]:
            noms[l[K.I_EN]][l[K.I_FR]] += 1
            if l[K.I_ETAT] in ('officiel', 'relu'):
                sures[l[K.I_EN]][l[K.I_FR]] += 1

    def accents(f):
        return sum(1 for c in f if c in 'ÉÈÊÂÀÎÔÛéèêâàîôûç')

    def capitales(f):          # capitales après la première lettre (« Flammes de Focalisation ») : à éviter
        return sum(1 for c in f[1:] if c.isupper())

    canon = {}
    for en, c in noms.items():
        if sures.get(en):
            canon[en] = min(sures[en].items(), key=lambda x: (-x[1], -accents(x[0]), x[0]))[0]
    # un nom français ne doit pas désigner deux sorts anglais différents (« Wildfire » ne devient pas « Brasier »,
    # le nom de « Blaze ») : sans forme officielle, on prend la meilleure forme qui n'est le nom d'aucun autre sort
    pris = defaultdict(set)
    for en, c in noms.items():
        for f in c:
            pris[_plat(f)].add(en)
    for en, c in noms.items():
        if en in canon:
            continue
        groupes = defaultdict(Counter)
        for f, k in c.items():
            groupes[_plat(f)][f] += k
        for g in sorted(groupes.values(), key=lambda x: (-sum(x.values()), min(x))):
            if pris[_plat(next(iter(g)))] - {en}:
                continue
            canon[en] = min(g.items(), key=lambda x: (-accents(x[0]), capitales(x[0]), -x[1], x[0]))[0]
            break
    n = Counter()
    for l in self.lignes.values():
        if l[K.I_ETAT] != 'machine' or not l[K.I_FR]:
            continue
        if l[K.I_TYPE] == 'sort' and l[K.I_CHAMP] == 'Name':
            cn = canon.get(l[K.I_EN])
            if cn and cn != l[K.I_FR] and not self.controle(l[K.I_EN], cn, 'machine', l[K.I_TYPE]):
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'nom harmonisé (0.9.5, même nom anglais) : ancien « %s »' % l[K.I_FR])
                l[K.I_FR] = cn
                n['nom'] += 1
            continue
        if not (l[K.I_TYPE] == 'sort' and l[K.I_CHAMP] in ('Description', 'ToolTip')
                or l[K.I_TYPE] == 'coa_description_sort_client') or '|c' not in l[K.I_EN]:
            continue
        se, sf = RE_COULEUR.findall(l[K.I_EN]), list(RE_COULEUR.finditer(l[K.I_FR]))
        if len(se) != len(sf):
            continue
        fr, decal = l[K.I_FR], 0
        for (_, te), m in zip(se, sf):
            cn, tf = canon.get(te), m.group(2)
            if not cn or tf == cn or not tf[:1].isupper() or not cn[:1].isupper():
                continue
            d, f = m.start(2) + decal, m.end(2) + decal
            fr = fr[:d] + cn + fr[f:]
            decal += len(cn) - len(tf)
        if fr != l[K.I_FR] and not self.controle(l[K.I_EN], fr, 'machine', l[K.I_TYPE]):
            l[K.I_FR] = fr
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'noms de sorts cités harmonisés (0.9.5)')
            n['citation'] += 1
    self.cr.update({'harmoniser_noms_sorts:' + a: b for a, b in n.items()})
    K.journal('import : noms de sorts harmonisés : %d noms, %d textes qui les citent' % (n['nom'], n['citation']))


Importeur.harmoniser_noms_sorts = _harmoniser_noms_sorts

RE_EXT = re.compile(r'(@ext:)(\s*)(.*?)(\s*)(:ext@)', re.S)


def _textes_ext(self):
    """0.9.5 (essai 8, captures du 09/11) : texte détaillé des sorts (« @ext: Can only have 1 Aegis up at a time.:ext@ »,
    montré quand le joueur maintient MAJ) resté en anglais dans le français : remplacé par sa traduction
    (glossaire/textes_ext.tsv, outils/textes_ext.py). Seul un texte resté identique à l'anglais est remplacé."""
    p = os.path.join(K.RACINE, 'glossaire', 'textes_ext.tsv')
    if not os.path.exists(p):
        return
    table = {}
    with open(p, encoding='utf-8') as f:
        for ligne in list(f)[1:]:
            c = ligne.rstrip('\n').split('\t')
            if len(c) >= 2 and c[1]:
                table[K.desechapper(c[0])] = K.desechapper(c[1])
    n = Counter()
    for l in self.lignes.values():
        if '@ext:' not in l[K.I_EN] or '@ext:' not in l[K.I_FR] or l[K.I_ETAT] in ('officiel', 'technique'):
            continue
        anglais = {x.group(3) for x in RE_EXT.finditer(l[K.I_EN])}

        def rempl(m):
            if m.group(3) in anglais and m.group(3) in table:
                n['blocs'] += 1
                return m.group(1) + m.group(2) + table[m.group(3)] + m.group(4) + m.group(5)
            return m.group(0)
        fr = RE_EXT.sub(rempl, l[K.I_FR])
        if fr == l[K.I_FR]:
            continue
        if self.controle(l[K.I_EN], fr, 'machine' if l[K.I_ETAT] != 'relu' else 'relu', l[K.I_TYPE]):
            n['refus_controle'] += 1
            continue
        l[K.I_FR] = fr
        n['lignes'] += 1
    self.cr.update({'textes_ext:' + a: b for a, b in n.items()})
    K.journal('import : textes détaillés @ext traduits : %s' % dict(n))


Importeur.textes_ext = _textes_ext


# libellés internes de CoA, seuls dans le champ (rang « UNUSED », nom « NYI », description « PLACEHOLDER »…)
BOUCHE_TROUS_SORTS = {'Placeholder Tooltip', 'Placeholder', 'placeholder', 'PLACEHOLDER', 'UNUSED', 'Unused', 'NYI',
                      'WIP', 'DEPRECATED', 'DEPRECTAED', 'null', 'TBD', 'TODO'}


def _bouche_trous_sorts(self):
    """0.9.5 (audit des sorts) : texte d'aura laissé vide par CoA (« Placeholder Tooltip », 47 talents) : technique,
    rien à traduire (l'aura du talent n'a pas de bulle propre)."""
    n = 0
    for l in self.lignes.values():
        if l[K.I_TYPE] == 'sort' and l[K.I_EN].strip() in BOUCHE_TROUS_SORTS and l[K.I_ETAT] in ('a_traduire', 'a_revoir'):
            l[K.I_ETAT], l[K.I_FR] = 'technique', ''
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'technique=bouche-trou de CoA (« Placeholder Tooltip »)')
            n += 1
    # textes de sorts que l'atelier a jugés à garder en anglais (doutes résolus, 0.9.5) : libellés internes de CoA
    # (« SLS », « WIP », « PassiveSLS », journal de débogage) et noms identiques en français (« Absolution »)
    pg = os.path.join(K.RACINE, 'glossaire', 'sorts_garder.tsv')
    g = 0
    if os.path.exists(pg):
        with open(pg, encoding='utf-8') as f:
            for c in (x.rstrip('\n').split('\t') for x in list(f)[1:]):
                l = self.lignes.get(tuple(c[:4])) if len(c) >= 6 else None
                if l and K.empreinte(l[K.I_EN]) == c[4] and l[K.I_ETAT] in ('a_traduire', 'a_revoir'):
                    l[K.I_ETAT], l[K.I_FR] = 'technique', ''
                    l[K.I_NOTE] = joindre(l[K.I_NOTE], 'technique=à garder en anglais (atelier, 0.9.5) : '
                                          + K.desechapper(c[5]))
                    g += 1
    self.cr['sorts_bouche_trous'] = n
    self.cr['sorts_garder'] = g


Importeur.bouche_trous_sorts = _bouche_trous_sorts


def main():
    ecrire = '--sans-ecrire' not in sys.argv
    imp = Importeur()
    imp.charger_relus()
    imp.importer_serveur()
    imp.mise_a_jour_coa()             # 08/11 : CoA b39aa861
    imp.verifier_quetes()
    imp.importer_client()
    imp.importer_sorts_standard()
    imp.importer_sorts_coa_puissance()
    imp.importer_sorts_interface()
    imp.importer_sorts_objets()       # essai 8
    imp.importer_dbc()
    imp.hauts_faits_officiels()       # 0.9.2
    imp.libelles_lua_coa()            # 0.9.2
    imp.categories_competences()      # 0.9.4
    imp.importer_interface()
    imp.noms_officiels_web()          # 0.9 : avant la couche (les lignes libérées reçoivent leur traduction)
    imp.appliquer_vocabulaire()
    imp.corriger_et_controler()
    imp.importer_enchantements_modele()
    imp.fusionner_relus()
    imp.appliquer_couche()
    imp.reprise_meme_anglais()        # essai 8
    imp.harmoniser_officiel()
    imp.limites_objets_par_nom()
    imp.focalisation_interface()
    imp.pierres_de_retraite()         # 0.9.4
    imp.noms_vanite()                 # essai 8
    imp.criteres_par_nom()            # 0.9.2
    imp.voie_ascension()              # 0.9.4 : décision 34
    imp.transcende()                  # 1.2.0 : décision 35
    imp.prems_niveau()                # 0.9.4 : décision 24 (modèle de niveau)
    imp.harmoniser_statique()         # 0.9.4
    imp.textes_ext()                  # 0.9.5
    imp.majuscules_accentuees()       # 0.9.5 (version publique)
    imp.harmoniser_specialisations()  # 0.9.5 (version publique)
    imp.harmoniser_noms_sorts()       # 0.9.5 (version publique)
    imp.bouche_trous_sorts()          # 0.9.5
    tailles = imp.ecrire(ecrire)
    imp.resume(tailles)


if __name__ == '__main__':
    main()
