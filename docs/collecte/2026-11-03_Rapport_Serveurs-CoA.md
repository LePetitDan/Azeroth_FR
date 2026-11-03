# Les serveurs « Conquest of Azeroth » après la fermeture d'Ascension : état au 03/11/2026

Recherche web faite le 03/11/2026 pour la relance de la traduction française. Chaque fait est suivi de sa source et de sa date. Les citations sont reformulées.
Repères de fiabilité : **[sûr]** = source officielle ou plusieurs sources concordantes ; **[probable]** = une seule source sérieuse ; **[à vérifier]** = indice faible ou sources en désaccord.

Note sur les sources : les annuaires `wowprivateservers.vercel.app` et `privateserverhub.com` reprennent souvent ce que disent les serveurs eux-mêmes. Les sites `conquestofazerothwiki.wiki` et `conquestofazeroth.com` ont l'air générés automatiquement pour le référencement : ils n'ont **pas** été utilisés.

---

## 1. Tableau récapitulatif

### 1a. Serveurs qui reprennent les 21 classes de Conquest of Azeroth (CoA)

| Serveur | Site | État au 03/11 | Ouverture | Base technique | Client | Population (date, source) | Langue / FR | Discord affiché |
|---|---|---|---|---|---|---|---|---|
| **Conquest of AzerothCore** (« CoA Core ») | coa-development.org | **Ouvert, royaume permanent « Rexxar »** + royaumes de test (effaçables) | Test public dès le ~14/09 ; Rexxar le **22/10/2026** [probable] | **Code libre** : AzerothCore modifié, licence GPL-2.0 [sûr] | Lanceur Windows qui ajoute les fichiers CoA à un client 3.3.5a, en pratique une copie du client d'Ascension [sûr] | 27 à 29 en ligne, 2 442 personnages, 32 guildes (01/10, vercel) ; 27 en ligne sur CoA, 9 sur Warcraft Reborn, 1 sur Wildcard (21/10, vercel) ; **estimation de 60 à 140** (24/10, PSH) ; **Discord d'environ 5 500 membres** (24/10, PSH) | Anglais. Aucune communauté FR trouvée | discord.gg/2gmvcRXZTK (site + GitHub) |
| **GrimfallWoW, royaume « Conquest of Azeroth »** | grimfallwow.com | **Ouvert**, phase 1 limitée au **niveau 20** | **16/10/2026** [sûr] | **Inconnue**, code fermé. Aucune mention d'AzerothCore | Client 3.3.5a + lanceur Windows propre, téléchargé sur leur site [probable] | Non publiée. Un avis de joueur parle de 800 à 1 300 personnes sur la commande /who pour tout Grimfall, **invérifiable** (04/10, PSH) | Anglais | discord.gg/grimfallwow (vu sur PSH, pas sur leur site) |
| **ArdenWoW** | ardenwow.com | **Ouvert** (« Live », sans effacement prévu) | Alpha fermée en septembre (la date du 13/09 n'a pas été tenue), ouverture le **24/10/2026** [sûr] | Remercie AzerothCore et « le travail libre de la communauté Ascension/CoA ». **Très probablement CoA Core modifié** (voir section 2) | Lanceur à télécharger depuis le compte. Le client n'est pas précisé | Non publiée | Anglais (site en en_US) | discord.gg/mZJDMF7FRM |
| **Conquest Reborn** | conquestreborn.com | **Ouvert, en test**, mis à jour tous les jours | **09/09/2026** [sûr] | **TrinityCore**, autre code. Système de talents à lui (« Forging ») [probable] | Client 3.3.5a + lanceur Windows (~60 Mo, ~47 Go installé) | 7 à 8 joueurs (02/10) ; 14 à 24 (04/10, PSH) ; 35 (19/10, flux d'état du serveur, vercel) | Anglais | Lien donné après l'inscription seulement |

PSH = privateserverhub.com ; vercel = wowprivateservers.vercel.app.

### 1b. Outils liés (pas des serveurs publics)

| Outil | Ce que c'est | Faits |
|---|---|---|
| **CoA Server Manager** (Corfirean) | Appli Windows pour héberger un serveur CoA chez soi | Code serveur : `Corfirean/azerothcore-wotlk-coa`, une copie (fork) de `jealous-sound/azerothcore-wotlk-coa`. Les données du jeu viennent du client CoA d'Ascension (~43 Go). Royaumes CoA, Wildcard et Warcraft Reborn. Interface de l'appli traduite en 6 langues, **dont le français**. 54 étoiles, licence AGPL-3.0 ([GitHub](https://github.com/Corfirean/coa-server-manager), lu le 03/11/2026) |
| **CoA-Hosting-Guide** (BZRK / ScikuVRC) | Guide pour héberger soi-même | **Introuvable** par la recherche web le 03/11. À vérifier avec le lien d'origine |
| **DragonUI-CoA** (PentSec) | Interface de jeu (add-on) pour CoA Core | Traduite en anglais, espagnol, allemand, coréen, russe et chinois. **Pas de français**. Licence MIT, 3 étoiles ([GitHub](https://github.com/PentSec/DragonUI-CoA), lu le 03/11/2026) |
| **Add-ons « Exiles »** | ~25 add-ons connus (DBM, ElvUI, Leatrix…) adaptés au client CoA 3.3.5 | Guide de portage daté du 25/05/2026, aucune mention de langues ([git.sub-net.at](https://git.sub-net.at/Exiles/coa-mapster/src/branch/master/PORTING.md)) |

### 1c. Les autres anciens royaumes d'Ascension (à ne pas confondre)

| Royaume d'Ascension | Principe | Que reste-t-il ? |
|---|---|---|
| Area 52 | Sans classe, choix libre des sorts, Mystic Enchants, PvP à haut risque | Fermé le 04/09. CoA Core a une catégorie « Area 52 » dans son journal des changements mais aucun royaume public à ce nom ([vercel, 21/10](https://wowprivateservers.vercel.app/blog/coa-development-status-and-changelog-oct-21/)) |
| Elune | Saisonnier, sorts tirés au hasard (« Wildcard ») | Fermé le 04/09. **CoA Core** a un royaume de test Wildcard (en ligne depuis le 02/10, 1 joueur le 21/10). **GrimfallWoW « Whisperwind »** est un royaume sans classe avec tirages Wildcard, ouvert le 05/09 ([PSH](https://www.privateserverhub.com/servers/grimfallwow)) |
| Bronzebeard | « Warcraft Reborn » : les 9 classes d'origine retravaillées | Fermé le 04/09. **CoA Core** a un royaume de test Warcraft Reborn (en ligne depuis le 19/10, 9 joueurs le 21/10) |
| Conquest of Azeroth (royaume « Vol'jin ») | 21 classes maison | Fermé le 04/09 à 19 h, heure du Pacifique (le 05/09 vers 4 h en France). Copies : tableau 1a |

Les quatre royaumes ont fermé le 04/09/2026 ([vercel, 04/09](https://wowprivateservers.vercel.app/blog/ascension-shutdown-explained/)). D'après [Indie Kings (24/10)](https://www.indiekings.com/2026/10/conquest-of-azerothcore-launches-rexxar.html), Rexxar propose aussi un mode Wildcard et Warcraft Reborn.

Autres serveurs « sans classe » sans lien prouvé avec CoA : Wrathstorm (WotLK sans classe, très peu de joueurs), Rupture WoW, Azeroth Universe, Everwood WoW (pas de date de sortie), Lightborne et Torment WoW (projets annoncés) ([vercel](https://wowprivateservers.vercel.app/), [PSH](https://www.privateserverhub.com/new-wow-private-servers), lus le 03/11).

L'équipe d'Ascension prépare un **nouveau jeu sans lien avec WoW**. Il n'a pas de nom ni de date, et le retour des classes CoA n'est pas confirmé ([kami-labs, 31/08](https://kami-labs.fr/en/ascension/ascension-devient-mmo-original/)).

**Le « dernier serveur » cité par le joueur** est très probablement **Conquest Reborn**. C'est le seul autre projet qui reprend le nom et les classes de CoA [à vérifier].

---

## 2. Lien technique entre ces serveurs

### Conquest of AzerothCore : le seul projet libre
- L'organisation GitHub [Conquest-of-AzerothCore](https://github.com/Conquest-of-AzerothCore) (lue le 03/11) a :
  - un dépôt public `azerothcore-wotlk-coa` : licence GPL-2.0, 286 à 290 étoiles, 200 à 202 copies (forks), plus de 20 800 modifications, environ 1 900 tickets, mis à jour le 26/10 ;
  - un dépôt privé `coa-server-live`, qui contient la version exacte qui tourne sur le royaume.
- Le dépôt a été créé le 07/09/2026. Le 26/10, il comptait 51 contributeurs ([kami-labs, 29/10](https://kami-labs.fr/en/ascension/ascension-coa-apres-fermeture-proces/)).
- Dans notre copie locale du dépôt, la dernière modification date du **02/11/2026** (correctif n° 10885). Le projet est donc encore actif.
- Le projet se présente comme une reconstruction libre et indépendante du mode CoA, qui tourne sur le client 3.3.5a ([profil GitHub](https://raw.githubusercontent.com/Conquest-of-AzerothCore/.github/main/profile/README.md)).
- Le client utilisé est une **copie du client d'Ascension**, avec un module complémentaire (`Extensions.dll`) reconstruit par la communauté. Source : la documentation du dépôt (`docs/coa/client-dbc-stream.md` et d'autres fichiers), copie locale du 02/11/2026.
- Une autre copie du code existe chez `jealous-sound/azerothcore-wotlk-coa` (156 étoiles, 95 copies). La copie de Corfirean en descend. Le lien exact avec le dépôt officiel n'est pas clair [à vérifier].

### ArdenWoW : l'affirmation « ils reprennent CoA Core » est très probable, pas prouvée
Ce qui va dans ce sens :
1. Leur page « À propos » remercie AzerothCore et le travail libre de la communauté Ascension/CoA ([ardenwow.com/about](https://ardenwow.com/about), lue le 03/11).
2. Plusieurs réglages sont identiques à ceux de Rexxar (CoA Core) :
   - gain d'expérience ×1,5 et niveau maximum 60 ;
   - « Bazaar Tokens » gagnés en jouant ;
   - joueurs virtuels (« playerbots ») ;
   - système de parrainage.
   Sources : [FAQ ArdenWoW](https://ardenwow.com/faq) et [Indie Kings, 24/10](https://www.indiekings.com/2026/10/conquest-of-azerothcore-launches-rexxar.html).
3. Les noms de contenus qu'ArdenWoW met en avant se trouvent tous dans le code de CoA Core (copie locale du 02/11/2026) : Pale Reach, objets « Worldforged », Azzar Faire, Druk Thar, Red Mage Tower, « Warchest », la monture « Autumn Harvesthog ».

Ce qui limite la preuve :
- Une bonne partie de ces noms vient du CoA d'origine d'Ascension. N'importe quelle reconstruction fidèle les aurait aussi.
- ArdenWoW ne publie aucun code et ne nomme pas CoA Core. L'annuaire vercel dit lui aussi n'avoir vérifié aucun code commun ([vercel, 17/10](https://wowprivateservers.vercel.app/blog/conquest-of-azeroth-which-one/)).
- Pour être exact : la GPL-2.0 autorise à reprendre le code. Contrairement à la licence AGPL, elle n'oblige pas à publier ses modifications quand on fait seulement tourner un serveur. C'est la description de la licence, pas un avis juridique.

**Pour la traduction**, c'est une bonne nouvelle : si ArdenWoW repose sur CoA Core, la plupart des numéros d'identifiant (sorts, objets, quêtes) devraient être les mêmes. Cela reste à vérifier sur des exemples avant de le promettre.

### GrimfallWoW : code fermé, origine inconnue
- Le serveur existait avant la fermeture : bêta ouverte le 27/03/2026, puis sortie « sans classe » le 05/09 ([vercel](https://wowprivateservers.vercel.app/servers/grimfallwow/)).
- Son royaume CoA a les mêmes 21 classes, mais aucune source ne dit d'où viennent ses données ([PSH, 16/10](https://www.privateserverhub.com/news/grimfallwow-opens-a-conquest-of-azeroth-realm-with-21-custom)).
- Il ajoute des contenus à lui : plus de 10 races, donjons de Cataclysm adaptés, Kezan et Gilnéas retravaillés.
- **On ne peut rien dire sur la compatibilité** sans comparer en jeu.

### Conquest Reborn : un autre code
- Il est construit sur **TrinityCore** (un autre moteur de serveur), par un développeur seul. Le développeur précise lui-même que les autres projets utilisent AzerothCore ([PSH, 01/10](https://www.privateserverhub.com/news/one-month-in-conquest-reborn-keeps-conquest-of-azeroths)).
- Les talents sont remplacés par un réseau de nœuds (« Forging »). Les textes de talents seront donc différents.
- **La compatibilité sera probablement faible.**

---

## 3. Traductions qui existent déjà

| Quoi | État | Source |
|---|---|---|
| **AscensionFR** (LePetitDan, le projet de Dan) | Traduisait quêtes, sorts, talents (dont ceux des 21 classes), objets, zones et interface, soit environ 1,27 million de champs. Les textes de base reprennent les traductions françaises officielles de WotLK. Voix françaises en option. Fonctionnait **par-dessus le client anglais**, sans modifier les fichiers du jeu | [kami-labs, 28/07/2026](https://kami-labs.fr/ascension/guides-ascension/ascension-en-francais-addon-traduction-ascensionfr/) |
| Dépôt `LePetitDan/AscensionFR` | Public, **archivé le 10/09/2026**, 9 étoiles, 6 copies. Le README annonce la fin du projet | [GitHub](https://github.com/LePetitDan/AscensionFR), lu le 03/11 |
| Dépôt `LePetitDan/AscensionFR-Archive` | Public. Environ 643 000 textes FR, l'add-on, l'installeur et 66 documents de conception. Les données personnelles ont été retirées | [GitHub](https://github.com/LePetitDan/AscensionFR-Archive), lu le 03/11 |
| Ce que le web dit d'AscensionFR après la fermeture | **Rien** : aucun article n'en parle, et aucun ne le relie aux nouveaux serveurs | Recherches du 03/11 |
| Autre traduction FR pour CoA ou pour ses copies | **Aucune trouvée** | Recherches du 03/11 |
| Patchs de langue dans le lanceur d'Ascension | Un wiki de fans dit que l'onglet « Mods » du lanceur proposait des patchs **allemand et espagnol**. Pas de français | [conquest-of-azeroth.wiki/fr, sept. 2026](https://conquest-of-azeroth.wiki/fr/tools/addons-guide/) [à vérifier] |
| Wiki de fans en français | conquest-of-azeroth.wiki/fr. Seule la navigation est en français : les noms de classes, de spécialisations et de talents restent en anglais. Qualité de traduction moyenne | [conquest-of-azeroth.wiki/fr](https://conquest-of-azeroth.wiki/fr/classes/tier-list/) |
| **Textes français officiels de WotLK dans la base de CoA Core** | AzerothCore livre des tables de traduction qui contiennent le français. Dans la copie locale de CoA Core : 9 456 lignes FR pour les quêtes, 24 391 pour les créatures, 42 542 pour les objets. Ce sont les textes Blizzard d'origine. **Le contenu propre à CoA n'est presque pas traduit** : 16 fichiers sur 2 255 ajouts SQL mentionnent le français | [Wiki AzerothCore](https://azerothcore.org/wiki/quest_template_locale) + copie locale du 02/11/2026 |
| Add-ons pour CoA traduits dans d'autres langues | DragonUI-CoA existe en 7 langues, sans le français | [GitHub PentSec](https://github.com/PentSec/DragonUI-CoA) |

---

## 4. Langue du client

- **Le client d'Ascension était en anglais.** AscensionFR affichait le français par-dessus l'anglais, sans toucher aux fichiers du jeu ([kami-labs, 28/07](https://kami-labs.fr/ascension/guides-ascension/ascension-en-francais-addon-traduction-ascensionfr/)). Les notes de conception de l'archive AscensionFR parlent aussi d'un « client enUS », c'est-à-dire anglais américain (copie locale).
- **Les copies utilisent le même client anglais.**
  - CoA Core et le CoA Server Manager se servent d'une copie du client CoA d'Ascension ([GitHub Corfirean](https://github.com/Corfirean/coa-server-manager)).
  - Privateserverhub indique « anglais » pour CoA Core, Grimfall CoA et Conquest Reborn ([PSH](https://www.privateserverhub.com/best-wow-private-servers), lu le 03/11).
  - **Aucun de ces lanceurs ne propose le français**, d'après tout ce qui a été trouvé.
- **Côté serveur, CoA Core sait déjà envoyer la langue du joueur.**
  - Il envoie certaines données dans la langue du client quand elles existent, sinon en anglais (`docs/coa/client-dbc-stream.md`, copie locale).
  - AzerothCore choisit aussi les textes de quêtes selon la langue du client.
  - Un client réglé en français recevrait donc en français les quêtes Blizzard d'origine, mais pas le contenu propre à CoA. **C'est une déduction, pas un test.**
- **Passer le jeu en français (frFR) : rien de documenté.**
  - Sur un client 3.3.5a normal, la langue dépend d'un dossier de langue dans `Data` et de fichiers d'archives propres à chaque langue ([warcraft.wiki.gg, page marquée comme ancienne](https://warcraft.wiki.gg/wiki/European_Language_Pack)).
  - Rien n'indique qu'on puisse le faire sur le client modifié d'Ascension sans casser ses ajouts.
  - **À tester avant d'en faire une piste.** L'approche « add-on par-dessus le client anglais » reste celle qui a déjà marché.

---

## 5. Cadre juridique et risques (faits seulement, aucun avis juridique)

### L'affaire Ascension
| Date | Fait | Source |
|---|---|---|
| 12/06/2026 | Blizzard dépose plainte devant le tribunal fédéral du district central de Californie (dossier 8:26-cv-01506, *Blizzard v. Derek S. Powell et al.*). Neuf griefs : droit d'auteur, DMCA (loi américaine qui interdit notamment de contourner les protections), fausse indication d'origine, association de malfaiteurs (RICO), entente, atteinte à des contrats | [Aftermath, 13/06](https://aftermath.site/blizzard-project-ascension-lawsuit/) ; [kami-labs, 10/07](https://kami-labs.fr/en/gaming/blizzard-vs-serveurs-prives-wow/) |
| 25-26/06/2026 | Assignations. Blizzard demande des informations à 13 entreprises, dont **GitHub** et **Discord**, pour identifier les personnes qui gèrent et financent le serveur | [JudgeHype, 29/06](https://worldofwarcraft.judgehype.com/news/project-ascension-blizzard-veut-accelerer-la-procedure-et-identifier-tous-les-responsables-185435/) |
| Juillet 2026 | Blizzard retire cette demande anticipée | [vercel, 04/09](https://wowprivateservers.vercel.app/blog/ascension-shutdown-explained/) |
| 29/08/2026 | Ascension annonce sa fermeture « dans le cadre d'un accord » avec Blizzard | [kami-labs, 29/08](https://kami-labs.fr/en/ascension/project-ascension-fermeture-5-septembre/) |
| 01/09/2026 | Les deux parties signalent au tribunal qu'elles ont trouvé un accord. Les conditions sont confidentielles | [kami-labs, 29/10](https://kami-labs.fr/en/ascension/ascension-coa-apres-fermeture-proces/) |
| 04/09/2026, 19 h (heure du Pacifique) | Fermeture des royaumes | [JudgeHype, 01/09](https://worldofwarcraft.judgehype.com/news/project-ascension-fermera-ses-serveurs-prives-world-of-warcraft-le-4-septembre-185991/10/) |
| 06/10/2026 | Le juge John W. Holcomb clôt l'affaire. Le jugement ne dit rien sur l'argent, le code ni une interdiction future | [kami-labs, 29/10](https://kami-labs.fr/en/ascension/ascension-coa-apres-fermeture-proces/) |

### Le précédent Turtle WoW (pour comparer)
- Plainte déposée le 29/08/2025.
- Un accord confidentiel est suivi d'une **interdiction définitive** prononcée en avril 2026 : interdiction de faire tourner un serveur, de demander des dons et de transmettre le code à un « successeur » ([kami-labs, 10/07](https://kami-labs.fr/en/gaming/blizzard-vs-serveurs-prives-wow/) ; [PC Gamer, 12/04](https://www.pcgamer.com/games/world-of-warcraft/blizzard-wins-injunction-against-vanilla-world-of-warcraft-private-server)).
- Les dates précises varient selon les sources (12, 13 ou 15/04, et un jugement d'accord le 15/05).

### Ce qui vise (ou non) les copies
- **Aucune demande de retrait (DMCA) de Blizzard visant les dépôts CoA n'a été trouvée** dans le registre public des demandes de retrait de GitHub. Recherche limitée, faite le 03/11. Le dépôt CoA Core est toujours en ligne et actif au 02/11.
- Pour toute copie, le client, les cartes et les textes restent la propriété de Blizzard, même quand le code du serveur est libre. Héberger un serveur public expose à une plainte du même type, surtout s'il accepte des dons ([kami-labs, 29/10](https://kami-labs.fr/en/ascension/ascension-coa-apres-fermeture-proces/)).
- Monétisation des copies :
  - **ArdenWoW vend des points de don** par PayPal et Terminal3 (politique de remboursement du 25/10/2026, [ardenwow.com](https://ardenwow.com/refund-policy)) ;
  - **GrimfallWoW a une boutique** : objets cosmétiques, montures, services, déblocage d'une race ([PSH](https://www.privateserverhub.com/servers/grimfallwow)) ;
  - **CoA Core et Conquest Reborn ne vendent rien** (Indie Kings, 24/10 ; PSH, 01/10).
  - Dans la plainte contre Ascension, Blizzard mettait en avant les millions de dollars de points de don.

### Pour un add-on de traduction gratuit
- **Aucune action connue de Blizzard contre un add-on ou une traduction** dans les affaires de serveurs privés ([kami-labs, 10/07](https://kami-labs.fr/en/gaming/blizzard-vs-serveurs-prives-wow/)).
- Seul précédent proche trouvé : en 2018, Blizzard a **demandé poliment** à un fan d'arrêter un add-on qui ajoutait des voix aux quêtes, au nom de la propriété intellectuelle. Il n'y a pas eu de poursuite ([Mein-MMO, 15/03/2018](https://mein-mmo.de/en/wow-quest-blizzard-vertonen-ende,216116)).
- Points à connaître pour la relance (constats, pas des avis) :
  1. Les textes français de base d'AscensionFR étaient les **traductions officielles de Blizzard**, redistribuées.
  2. Les « voix françaises d'époque » (environ 14 000 fichiers, 1,4 Go) viennent du client officiel ([kami-labs, 28/07](https://kami-labs.fr/ascension/guides-ascension/ascension-en-francais-addon-traduction-ascensionfr/)). Ce sont les éléments les plus clairement « Blizzard ».
  3. Les textes propres à CoA ont été écrits par l'équipe d'Ascension. Leur statut après l'accord est inconnu.
  4. Ne vendre et ne monétiser rien éloigne le projet du profil que Blizzard a attaqué.

---

## 6. Solidité et durée de vie

| Serveur | Points solides (faits datés) | Points fragiles | Bilan |
|---|---|---|---|
| **CoA Core** | Code public avec plus de 20 800 modifications et 51 contributeurs (26/10). Modifications tous les jours, dernière le 02/11. Journal des changements généré automatiquement. Royaume permanent depuis le 22/10. Discord d'environ 5 500 membres (24/10). Rien à vendre | Les royaumes de test peuvent être effacés à tout moment. Disponibilité d'environ 96 % avec beaucoup de redémarrages (437 en octobre, au 21/10). Dépend d'une copie du client d'Ascension. L'adresse de connexion est diffusée par Discord | **Le plus solide** |
| **GrimfallWoW** | Existe depuis mars 2026. Deux royaumes. Une boutique qui le finance. Avis 4,5/5 (2 avis, 04/10) | Code fermé. CoA limité au niveau 20 pour l'instant, pas de calendrier des phases suivantes. Population non publiée. La boutique l'expose davantage sur le plan juridique | Solide mais opaque |
| **ArdenWoW** | Ouvert depuis le 24/10, sans effacement prévu, avec un Discord | Date du 13/09 ratée. Vend des points de don. Code fermé alors qu'il repose très probablement sur CoA Core. Population inconnue | Récent, à surveiller |
| **Conquest Reborn** | Mis à jour presque tous les jours. Gratuit. Coûts de serveur de 10 à 20 $ par mois | Un seul développeur. 10 à 35 joueurs. Système de talents différent | Fragile |

---

## Recommandation factuelle : par quel serveur commencer

**Cibler d'abord Conquest of AzerothCore.** Raisons :
1. C'est **le seul projet dont le code et les données sont publics**. On peut extraire les textes à traduire directement (sorts, quêtes, objets, créatures) au lieu de les relever en jeu.
2. **Les autres en profitent probablement.** ArdenWoW et les serveurs hébergés avec le CoA Server Manager semblent partir de la même base, donc des mêmes identifiants. Il faut vérifier par un échantillon d'identifiants avant de l'annoncer.
3. C'est **la plus grande communauté visible** : environ 5 500 personnes sur Discord et 60 à 140 joueurs estimés. Il a un royaume permanent et une activité quotidienne.
4. **Rien à vendre et licence libre** : c'est le profil le moins exposé des quatre.
5. **Le serveur gère déjà le français pour les textes Blizzard.** Il manque surtout le contenu propre à CoA, c'est-à-dire exactement ce qu'AscensionFR avait déjà traduit pour Ascension.

Ensuite : vérifier la compatibilité avec ArdenWoW, puis GrimfallWoW si des joueurs le demandent. Conquest Reborn en dernier, car son code et ses talents sont différents.

---

## Incertain / à vérifier

1. **Base technique d'ArdenWoW** : très probablement CoA Core, sans preuve formelle. Il faut comparer des identifiants (sorts, objets) en jeu ou dans une base de données publique d'ArdenWoW.
2. **Date d'ouverture de Rexxar** : 22/10 selon PSH, article d'Indie Kings daté du 24/10.
3. **Nombre de classes de CoA Core** : 21 ou 22 selon les sources.
4. **Origine du code et des données de GrimfallWoW** : inconnue.
5. **Population de GrimfallWoW** (800 à 1 300) : un seul avis de joueur, invérifiable.
6. **Passer en français (frFR)** sur un lanceur CoA : aucune source. À tester.
7. **Patchs allemand et espagnol dans l'ancien lanceur d'Ascension** : une seule source, un wiki de fans de qualité moyenne.
8. **Lien entre `jealous-sound/azerothcore-wotlk-coa` et le dépôt officiel** : pas clair.
9. **« CoA-Hosting-Guide » (BZRK / ScikuVRC)** : introuvable sur le web.
10. **Lettre de mise en demeure envoyée environ 12 jours avant la fermeture d'Ascension** : sans date ni source vérifiable (kami-labs le note aussi).
11. **Dates du jugement Turtle WoW** : elles varient selon les sources.
12. **Lien Discord de CoA Core** : celui du site et du profil GitHub (2gmvcRXZTK) diffère de celui affiché dans la case « About » du dépôt (k7qpSndvW).
13. **Aucune demande de retrait DMCA trouvée** : la recherche dans le registre GitHub était limitée. Ce n'est pas une preuve d'absence.
14. **Wrathstorm** : « jouable » selon vercel, « bientôt » selon PSH (« Tirisgarde - Wrathstorm »).
15. **Pages non lues** (bloquées ou en erreur) : vidéos YouTube sur ArdenWoW et la comparaison ArdenWoW / CoA Core (HVLN Plays, 10/10), page d'accueil d'ArdenWoW, pages internes de grimfallwow.com, état en direct de coa-development.org (chargé en JavaScript), article de MassivelyOP du 29/08.

---

## Sources principales (consultées le 03/11/2026)
- Organisation GitHub Conquest-of-AzerothCore : https://github.com/Conquest-of-AzerothCore ; dépôt : https://github.com/Conquest-of-AzerothCore/azerothcore-wotlk-coa ; site : https://coa-development.org
- Fiches privateserverhub : https://www.privateserverhub.com/servers/conquest-of-azerothcore · /servers/grimfallwow · /servers/grimfallwow-conquest-of-azeroth · /servers/conquest-reborn · /new-wow-private-servers · /news/grimfallwow-opens-a-conquest-of-azeroth-realm-with-21-custom · /news/one-month-in-conquest-reborn-keeps-conquest-of-azeroths
- Annuaire wowprivateservers.vercel.app : /servers/ardenwow/ · /servers/grimfallwow/ · /servers/conquest-reborn/ · /servers/conquest-of-azerothcore/ · /blog/conquest-of-azeroth-which-one/ · /blog/coa-development-status-and-changelog-oct-21/ · /blog/ascension-shutdown-explained/ · /blog/ardenwow-21-custom-classes-closed-alpha/
- ArdenWoW : https://ardenwow.com/about · /faq · /news/live-server-launch · /refund-policy
- Conquest Reborn : https://conquestreborn.com
- GrimfallWoW : https://www.grimfallwow.com/news/grimfallwow-release-announcement/37
- Indie Kings (Rexxar) : https://www.indiekings.com/2026/10/conquest-of-azerothcore-launches-rexxar.html
- Kami Labs : affaire et copies (29/10), fermeture (29/08), 20 ans de procès (10/07), AscensionFR (28/07), MMO d'Ascension (31/08)
- JudgeHype : 29/06 et 01/09 ; Aftermath : 13/06 ; PC Gamer : 12/04 ; Mein-MMO : 15/03/2018
- CoA Server Manager : https://github.com/Corfirean/coa-server-manager ; DragonUI-CoA : https://github.com/PentSec/DragonUI-CoA
- AscensionFR : https://github.com/LePetitDan/AscensionFR ; https://github.com/LePetitDan/AscensionFR-Archive
- Wiki AzerothCore : https://azerothcore.org/wiki/quest_template_locale ; warcraft.wiki.gg : European_Language_Pack
- Copie locale du dépôt CoA Core (`/home/claude/conquest-of-azerothcore/azerothcore-wotlk-coa`, dernière modification 042b38a du 02/11/2026) : comptage des textes français, présence des noms de contenus d'ArdenWoW, documentation sur le client
