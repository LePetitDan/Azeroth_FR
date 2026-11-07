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
    GROUPE_LIEU = ('AreaTable', 'WMOAreaTable', 'AreaPOI', 'Map', 'TaxiNodes')
    TECHNIQUE_DBC = re.compile(r'\b(?:DND|NYI|UNUSED|TEST|QA|DEBUG)\b|^zz|\[PH\]|\bunused\b', re.I)

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
            if b and b[1] and O.meme_anglais(en, b[0]):
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = b[1], 'officiel', 'blizzard_frFR'
                l[K.I_NOTE] = joindre(note, '%s.dbc frFR officiel (patch-frFR-3), même numéro et même anglais que Blizzard' % dbc)
                quoi = 'par_numero'
            elif len(frs) == 1:
                l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = next(iter(frs)), 'officiel', 'blizzard_frFR'
                l[K.I_NOTE] = joindre(note, '%s frFR officiel (patch-frFR-3) : même anglais, un seul français officiel pour ce texte'
                                      % ('DBC de lieux' if g == 'lieu' else dbc + '.dbc'))
                quoi = 'par_texte'
            elif self.TECHNIQUE_DBC.search(en):
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

    # ------------------------------------------------------------------
    # 6. Ecriture
    # ------------------------------------------------------------------
    def famille_de(self, k, l):
        f = self.famille.get(k)
        if f:
            return f
        t = l[K.I_TYPE]
        for fam, _, types, _ in K.FAMILLES:
            if t in types and fam not in ('sorts_classes', 'talents', 'sorts_standard', 'sorts_coa'):
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
    imp.verifier_quetes()
    imp.importer_client()
    imp.importer_sorts_standard()
    imp.importer_sorts_coa_puissance()
    imp.importer_sorts_interface()
    imp.importer_dbc()
    imp.importer_interface()
    imp.appliquer_vocabulaire()
    imp.corriger_et_controler()
    imp.importer_enchantements_modele()
    imp.fusionner_relus()
    imp.appliquer_couche()
    imp.harmoniser_officiel()
    tailles = imp.ecrire(ecrire)
    imp.resume(tailles)


if __name__ == '__main__':
    main()
