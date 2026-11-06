# Doutes des agents de traduction

*Rassemblés par `python3 -I outils/lots.py doutes` le 2026-11-06 06:19 depuis `traductions/<famille>/<lot>.doutes.tsv`. Un texte en doute reste en anglais (état inchangé) ; « garder l'anglais » = choix délibéré de l'agent (nom propre, texte technique…). Pour lever un doute : trancher ici, puis réextraire le lot avec `--avec-doutes`.*

Total : 492 doute(s), 1887 « garder l'anglais ».

## broadcast_cris / broadcast_cris_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `texte_creature/23577/1-0/Text` | doute | coquille de CoA : une tabulation à la place de l'apostrophe (« can\t ») ; proposition : « Vous pouvez pas combattre la puissance ! » | You can	 fight da power! |
| `texte_creature/24144/1-0/Text` | doute | coquille de CoA : une tabulation à la place de l'apostrophe (« can\t ») ; proposition : « Vous pouvez pas combattre la puissance ! » | You can	 fight da power! |
| `texte_creature/27328/4-0/Text` | garder_anglais | mot technique de CoA (« Reset ») | Reset |

## competences / competences_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `competence/39//name` | garder_anglais | Felforged : nom de mode CoA sans décision (question 11l) | Felforged |
| `competence/130//name` | garder_anglais | nom du serveur (Conquest of Azeroth) | Conquest of Azeroth |

## competences / competences_002

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `competence/6000//name` | garder_anglais | nom propre inventé par CoA | Aroy |
| `competence/10038//name` | garder_anglais | nom de familier du Bricoleur (contient Scrap, question 20) | Scrapbot |
| `competence/10039//name` | garder_anglais | nom de familier du Bricoleur, gardé avec les autres | Rusthound |
| `competence/10040//name` | garder_anglais | nom propre de familier | Ziggy-6k |
| `competence/10041//name` | garder_anglais | nom de familier du Bricoleur (contient Scrap, question 20) | Scrapmaw |
| `competence/11799//name` | garder_anglais | entrée technique marquée DEPRECATED (inutilisée) | Pet - Dinomancy Devilsaur DEPRECATED |

## cpp_en_dur / cpp_en_dur_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `cpp_en_dur/modules/mod-cfbg/src/cs_cfbg.cpp/139/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clés de configuration |   Config:  System={}  WG={} |
| `cpp_en_dur/modules/mod-cfbg/src/cs_cfbg.cpp/144/SendSysMessage` | garder_anglais | identique en français (« Faction ») |   Faction |
| `cpp_en_dur/modules/mod-cfbg/src/cs_cfbg.cpp/169/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur |     Fake  team={:<8}  race={}  morph={} |
| `cpp_en_dur/modules/mod-cfbg/src/cs_cfbg.cpp/171/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur |     Real  team={:<8}  race={}  morph={}  nativeMorph={} |
| `cpp_en_dur/modules/mod-cfbg/src/cs_cfbg.cpp/209/PSendSysMessage` | garder_anglais | identique en français (en-tête « Alliance  Horde ») |                    Alliance  Horde |
| `cpp_en_dur/modules/mod-cfbg/src/cs_cfbg.cpp/338/SendSysMessage` | garder_anglais | sortie technique de débogage (MJ) ; arguments WAR/PEACE recollés par l'extraction | Battlefield {} ¦ {}WARPEACE |
| `cpp_en_dur/modules/mod-coa-challenges/src/CoA.Challenges.Scripts.cpp/3132/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) ; arguments yes/no recollés par l'extraction | Fatigue[{}] = {}/{} (resting={})yesno |
| `cpp_en_dur/modules/mod-coa-challenges/src/CoA.Challenges.Scripts.cpp/3153/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur |   item={} x{} ach={} special={} first={} |
| `cpp_en_dur/modules/mod-coa-challenges/src/CoA.Challenges.Scripts.cpp/3208/PSendSysMessage` | garder_anglais | marqueur de test automatique (MJ) | E2E PASS |
| `cpp_en_dur/modules/mod-coa-challenges/src/CoA.Challenges.Scripts.cpp/3233/PSendSysMessage` | garder_anglais | marqueur de test automatique (MJ) | E2E PASS |
| `cpp_en_dur/modules/mod-coa-challenges/src/CoA.Challenges.Scripts.cpp/3297/PSendSysMessage` | garder_anglais | marqueur de test automatique (MJ) | RULE GATES PASS |
| `cpp_en_dur/modules/mod-coa-challenges/src/CoA.Challenges.Scripts.cpp/3315/PSendSysMessage` | garder_anglais | marqueur de test automatique (MJ) | CONDITION GATES PASS |
| `cpp_en_dur/modules/mod-coa-challenges/src/CoA.Challenges.Scripts.cpp/3361/PSendSysMessage` | garder_anglais | marqueur de test automatique (MJ) | PARTY RULE GATES PASS |
| `cpp_en_dur/modules/mod-coa-challenges/src/CoA.Challenges.Scripts.cpp/3412/PSendSysMessage` | garder_anglais | marqueur de test automatique (MJ) | CACHE TOCTOU PASS |
| `cpp_en_dur/modules/mod-coa-challenges/src/CoA.Challenges.Scripts.cpp/3429/PSendSysMessage` | garder_anglais | marqueur de test automatique (MJ) | PET TRIAL AURAS PASS |
| `cpp_en_dur/modules/mod-coa-mythic-plus/src/MythicPlus.cpp/2125/AddGossipItemFor` | doute | icône « Spell_Shadow_Teleport » + libellé « Back » recollés par l'extraction : le contrôle lit le nom d'icône comme de l'anglais ; proposition « Spell_Shadow_TeleportRetour » | Spell_Shadow_TeleportBack |
| `cpp_en_dur/modules/mod-coa-mythic-plus/src/MythicPlus.cpp/2145/AddGossipItemFor` | doute | icône « Spell_Shadow_Teleport » + libellé « Back » recollés par l'extraction : le contrôle lit le nom d'icône comme de l'anglais ; proposition « Spell_Shadow_TeleportRetour » | Spell_Shadow_TeleportBack |
| `cpp_en_dur/modules/mod-coa-mythic-plus/src/MythicPlus.cpp/2171/AddGossipItemFor` | doute | icône « Spell_Shadow_Teleport » + libellé « Back » recollés par l'extraction : le contrôle lit le nom d'icône comme de l'anglais ; proposition « Spell_Shadow_TeleportRetour » | Spell_Shadow_TeleportBack |
| `cpp_en_dur/modules/mod-coa-mythic-plus/src/MythicPlus.cpp/2277/AddGossipItemFor` | doute | icône « Spell_Shadow_Teleport » + libellé « Back » recollés par l'extraction : le contrôle lit le nom d'icône comme de l'anglais ; proposition « Spell_Shadow_TeleportRetour » | Spell_Shadow_TeleportBack |
| `cpp_en_dur/modules/mod-coa-mythic-plus/src/MythicPlus.cpp/2793/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) ; arguments down/alive recollés par l'extraction | Mythic+ +{} lfg {} state {}: {} / {} s, forces {} / {}, encounters {} / {} (final {})downalive |
| `cpp_en_dur/modules/mod-ethereal-bazaar/src/GrootCoin.cpp/190/PSendSysMessage` | garder_anglais | sortie technique (MJ) : clés de configuration | Config: GrootCoin.Enable={} GrootCoin.ExchangeEnable={} TokensPerCoin={} MaxAward={}. |
| `cpp_en_dur/modules/mod-ethereal-bazaar/src/GrootCoinScripts.cpp/111/AddGossipItemFor` | doute | terme CoA sans décision : « Groot Coin » (monnaie du bazar éthéré, ~15 textes de ce lot, laissé en anglais dans les autres) ; proposition « Je voudrais échanger des pièces Groot. » | I want to exchange Groot Coins. |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormClientBridge.cpp/642/SendSystemMessage` | doute | le contrôle refuse le mot « Manastorm » des clés de configuration à garder ; proposition : « La Tempête de mana native nécessite Manastorm.Enable=1 et Manastorm.ClientMode=2 (redémarrage nécessaire). » | Native Manastorm requires Manastorm.Enable=1 and Manastorm.ClientMode=2 (restart required). |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/221/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur | Manastorm run {} ¦ state={} ¦ mode={} ¦ members={} ¦ depth={} ¦ creatureLevel={} ¦ seed={} |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/232/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur | Stage: segment={} map={} instance={} difficulty={} encounter={} objective={} tele={} weight={} reward={:.3f}x |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/245/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur | Effective scaling (depth x {} members): HP={:.3f}x GlobalDamage={:.3f}x Melee={:.3f}x Spell={:.3f}x |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/256/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur | Runtime: stageCreatures={} objectiveGuid={} counter={} chaoticLinks={} unusedLinkSpawns={} resurrections={}/{} complete={}yesno |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/520/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur | Manastorm checkpoints ¦ mode={} ¦ bestCompleted={} ¦ pendingUnlock={} ¦ pendingIntroDepth={} ¦ pendingSegment={} |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/725/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur | Manastorm spawn roles ¦ segment={} spawn={} entry={} flags=0x{:X} enabled={} route={} link={} randomslot={} poolsource={} affix={}yesnoyesnoyesnoyesno |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/777/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur |   spawn={} entry={} flags=0x{:X} enabled={}yesno |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/805/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur | Manastorm creature pool {} '{}' ¦ sourceSegments={} derivedCreatureEntries={} ¦ replacementRuntime=disabled |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/816/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur |   sourceSegment={} |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/828/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur |   creatureEntry={} name='{}'<missing template> |
| `cpp_en_dur/modules/mod-manastorm-endless/src/ManastormCommands.cpp/1214/PSendSysMessage` | garder_anglais | sortie technique de débogage (MJ) : clé=valeur |   spawn={} entry={} flags=0x{:X} enabled={}yesno |

## creatures / creatures_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `creature/1//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Waypoint (Only GM can see it) |
| `creature/1//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Visual |
| `creature/128//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Testing |
| `creature/275//name` | garder_anglais | nom propre inventé par CoA | Whit Wantmal |
| `creature/298//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | <Needs Texture> |
| `creature/384//name` | garder_anglais | nom propre inventé par CoA | Katie Hunter |
| `creature/795//name` | garder_anglais | nom propre inventé par CoA | Mark |
| `creature/797//name` | garder_anglais | nom propre inventé par CoA | Bo |
| `creature/953//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Spawn Test One |
| `creature/1266//name` | garder_anglais | nom propre inventé par CoA | Tundra MacGrann |
| `creature/1483//name` | garder_anglais | nom propre inventé par CoA | Murphy West |
| `creature/1649//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Reuse Me |
| `creature/1722//name` | garder_anglais | nom propre inventé par CoA | Andr'e |
| `creature/1991//name` | garder_anglais | nom propre inventé par CoA | Jaxil Rye |
| `creature/2756//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Reuse Me |
| `creature/2896//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Magic Skill Trainer *Temp* |
| `creature/2899//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Toughness/Resist Trainer *Temp* |
| `creature/3200//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Eric's AAA Special Vendor |
| `creature/3831//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | NEED MODEL |
| `creature/4896//name` | garder_anglais | nom propre inventé par CoA | Charity Mipsy |
| `creature/4950//name` | garder_anglais | nom propre inventé par CoA | Spot |
| `creature/5349//name` | garder_anglais | nom officiel identique (Arash-ethis) | Arash-ethis |
| `creature/8001//name` | garder_anglais | nom propre inventé par CoA | Corpus Ragatus |
| `creature/10189//name` | garder_anglais | nom propre inventé par CoA | Basalthane |
| `creature/10190//name` | garder_anglais | nom propre inventé par CoA | Basalthane |
| `creature/10191//name` | garder_anglais | nom propre inventé par CoA | Basalthane |
| `creature/10192//name` | garder_anglais | nom propre inventé par CoA | Basalthane |
| `creature/11111//name` | garder_anglais | nom propre inventé par CoA | Wynne Larsone |
| `creature/11826//name` | garder_anglais | nom propre inventé par CoA | Kristy Grant |
| `creature/11827//name` | garder_anglais | nom propre inventé par CoA | Kimberly Grant |
| `creature/11828//name` | garder_anglais | nom propre inventé par CoA | Kelly Grant |
| `creature/12537//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Morph Firemane Scalebane |
| `creature/13157//name` | garder_anglais | nom propre inventé par CoA | Makasgar |
| `creature/13514//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Fel Commutation Credit |
| `creature/14162//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | 100FR Arcane |
| `creature/14851//name` | garder_anglais | nom propre inventé par CoA | Bog |
| `creature/16853//name` | garder_anglais | nom propre inventé par CoA | Anterius Black |
| `creature/19430//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Test Elemental Totem |
| `creature/19431//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Test Elemental |
| `creature/19663//name` | garder_anglais | nom propre inventé par CoA ; « Madame » se lit déjà en français | Madame Ruby |
| `creature/20002//name` | garder_anglais | nom propre inventé par CoA | Hurlog Horde |
| `creature/21281//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Designer Island Gnome Spell Target |
| `creature/21412//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Designer Island Horde Leader |
| `creature/21444//name` | garder_anglais | nom propre inventé par CoA | Tempixx Finagler |
| `creature/21447//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Blade's Edge - Toshley's - Def Gun Attack Origin |
| `creature/22401//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Zeth'Gor Quest Credit Marker, They Must Burn, Tower North |
| `creature/22402//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Zeth'Gor Quest Credit Marker, They Must Burn, Tower Forge |
| `creature/22403//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Zeth'Gor Quest Credit Marker, They Must Burn, Tower Foothill |
| `creature/22411//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Ethereal Caster, Type A (Gold) |
| `creature/22412//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Ethereal Caster, Type A (Green) |
| `creature/22413//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Ethereal Caster, Type A (Purple) |
| `creature/22414//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Ethereal Caster, Type A (Red) |
| `creature/22415//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Ethereal Caster, Type B (Black) |
| `creature/22416//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Ethereal Caster, Type B (White) |
| `creature/22641//name` | garder_anglais | nom officiel identique (Drek'Thar) ; « (1) » est un repère technique | Drek'Thar (1) |
| `creature/23234//name` | garder_anglais | nom propre inventé par CoA | Bananas |
| `creature/23746//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Zul'Aman Exterior InvisMan |
| `creature/23807//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Zul'Aman - Bear God Invisman |
| `creature/23813//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Zul'Aman - Dragonhawk God Invisman |
| `creature/23814//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Zul'Aman - Eagle God Invisman |
| `creature/24012//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Ingvar Res Ground Visual |
| `creature/24324//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Crash Test Creature |
| `creature/24353//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Eric Maloof Test Forsaken Male |
| `creature/24354//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Eric Maloof Test Forsaken Female |
| `creature/24355//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Eric Maloof Test Human Male |
| `creature/24531//name` | garder_anglais | nom propre inventé par CoA | Gavin Ward |
| `creature/24532//name` | garder_anglais | nom propre inventé par CoA | Sabetta Ward |
| `creature/24705//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Rope Swing Invisible Vehicle Stalker |
| `creature/24939//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - BE Male Tier 2 |
| `creature/24940//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - BE Male Tier 3 |
| `creature/24941//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - BE Male Tier 4 |
| `creature/24942//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - BE Female Tier 1 |
| `creature/24943//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - BE Female Tier 2 |
| `creature/24944//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - BE Female Tier 3 |
| `creature/24945//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - BE Female Tier 4 |
| `creature/24946//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - Draenei Male Tier 1 |
| `creature/24947//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - Draenei Male Tier 2 |
| `creature/24948//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - Draenei Male Tier 3 |
| `creature/24949//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - Draenei Male Tier 4 |
| `creature/24950//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - Draenei Female Tier 1 |
| `creature/24951//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - Draenei Female Tier 2 |
| `creature/24952//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - Draenei Female Tier 3 |
| `creature/24953//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - Draenei Female Tier 4 |
| `creature/24963//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Marksman - BE Male Tier 1 |
| `creature/25116//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - BE Female Tier 1 |
| `creature/25117//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - BE Female Tier 2 |
| `creature/25118//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - BE Female Tier 3 |
| `creature/25119//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - BE Female Tier 4 |
| `creature/25120//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - BE Male Tier 1 |
| `creature/25121//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - BE Male Tier 2 |
| `creature/25122//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - BE Male Tier 3 |
| `creature/25123//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - BE Male Tier 4 |
| `creature/25124//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - Draenei Female Tier 1 |
| `creature/25125//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - Draenei Female Tier 2 |
| `creature/25126//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - Draenei Female Tier 3 |
| `creature/25127//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - Draenei Female Tier 4 |
| `creature/25128//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - Draenei Male Tier 1 |
| `creature/25129//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - Draenei Male Tier 2 |
| `creature/25130//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - Draenei Male Tier 3 |
| `creature/25131//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Shattered Sun Warrior - Draenei Male Tier 4 |
| `creature/25738//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Clayton J Dubin (1) |
| `creature/25738//subname` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Uber Quality Assured |
| `creature/26080//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Craig's Test Human B |
| `creature/26105//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest Invisman - Buying Time |
| `creature/26129//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest InvisMan - Buying Time - Effect Caster |
| `creature/26130//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest InvisMan - Buying Time - Effect Target |
| `creature/26155//name` | garder_anglais | nom propre inventé par CoA | Mark Hanes |
| `creature/26193//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Nexus 70 - Buying Time - Kill Credit |
| `creature/26248//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Northern Sinkhole Kill Credit |
| `creature/26249//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Southern Sinkhole Kill Credit |
| `creature/26373//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Coldarra Spell FX InvisMan |
| `creature/26376//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Test - Brutallus Craig |
| `creature/26444//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest Invisman - Filling the Cages |
| `creature/26612//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Burninate Kill Credit |
| `creature/26671//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Rabid Dire Bear *Unused* |
| `creature/26688//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Statis orb |
| `creature/26895//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Snowfall Elk Credit |
| `creature/27124//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | [TDB] Killcredit Quest XXXXX |
| `creature/27276//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Let Them Not Rise! Rat |
| `creature/27324//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Outhouse Invisible Man |
| `creature/27458//name` | garder_anglais | nom propre inventé par CoA | Flora |
| `creature/27474//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Captain Luc D'Merud Quest Credit |
| `creature/27625//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Plague Wagon Credit |
| `creature/27796//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Worg's Blood Elixir Credit |
| `creature/27879//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Frostmourne Cavern Quest Credit |
| `creature/27890//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Brewfest - Direbrew Mole Machine Loc bunny |
| `creature/27952//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Protector Visual (Red) |
| `creature/27954//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Protector Visual (Green) |
| `creature/27955//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Protector Visual (Bronze) |
| `creature/27956//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Dan's Test Turret |
| `creature/28019//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Escape from Silverbrook Credit |
| `creature/28130//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Invis Lightning Stalker |
| `creature/28250//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Protector Visual (Black) |
| `creature/28251//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Protector Visual (Blue) |
| `creature/28252//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Protector Visual (Nether) |
| `creature/28270//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Jintha'kalar Scourge (PROXY DO NOT SPAWN) |
| `creature/28482//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Avatar of Freya Conversation Credit |
| `creature/28501//name` | garder_anglais | nom propre inventé par CoA | Ronakada |
| `creature/28507//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Summon Vision Test - LAB |
| `creature/28664//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Seat Squatter - LAB |
| `creature/28696//name` | garder_anglais | nom propre inventé par CoA | Derik Marks |
| `creature/28722//name` | garder_anglais | nom propre inventé par CoA | Bryan Landers |
| `creature/28758//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Reconnaisaince Flight Kill Credit |
| `creature/28763//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | [Phase 1] Scarlet Crusade Proxy Creature |
| `creature/28764//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | [Phase 1] Citizen of Havenshire Proxy Creature |
| `creature/28767//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | [Phase 1] Havenshrie Horse Credit, Step 01 |
| `creature/28820//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Destructive Ward Kill Credit |
| `creature/28947//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Ionar Invis Stalker |
| `creature/28949//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Spell Performance Test Caster |
| `creature/28950//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Spell Performance Test Target |
| `creature/29027//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wild Growth Stalker |
| `creature/29052//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Outhouse Invisible Woman |
| `creature/29058//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Suntouched Pillar Credit |
| `creature/29069//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Skyreach Pillar Credit |
| `creature/29170//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | WotLK Apothecary Bat Rider Controller |
| `creature/29521//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Unworthy Initiate Anchor |
| `creature/29682//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Slad'ran Summon Target |
| `creature/29800//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Hyldsmeet Drake-Rider Credit |
| `creature/29816//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Eagle Feeding Kill Credit |
| `creature/29878//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Log Ride (Log A) |
| `creature/29879//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Log Ride (Log B) |
| `creature/30059//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Warden Visual (Bronze) |
| `creature/30072//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Warden Visual (Red) |
| `creature/30073//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Warden Visual (Green) |
| `creature/30076//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Warden Visual (Blue) |
| `creature/30077//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Wyrmrest Warden Visual (Black) |
| `creature/30138//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Frost Giant Ghost KC |
| `creature/30139//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Frost Dwarf Ghost KC |
| `creature/30515//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Witness the Reckoning Credit |
| `creature/30573//name` | garder_anglais | nom propre inventé par CoA | Duke |
| `creature/30802//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Rabid Dire Bear *Unused* (1) |
| `creature/31071//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - PvP Kill - Fire |
| `creature/31072//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - PvP Kill - Water |
| `creature/31073//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - PvP Kill - Shadow |
| `creature/31074//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - PvP Kill - Life |
| `creature/31077//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Safirdrang's Chill Target |
| `creature/31086//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - PvP Kill - Alliance |
| `creature/31093//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - PvP Kill - Vehicle |
| `creature/31128//name` | garder_anglais | nom propre inventé par CoA | Chilly |
| `creature/31138//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Tenebron Egg Controller |
| `creature/31156//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - Tower Kill |
| `creature/31244//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - Structure Kill |
| `creature/31284//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - Vehicle Protected |
| `creature/31286//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - Bridge Kill |
| `creature/31287//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - Wall Kill |
| `creature/31288//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - Workshop Kill |
| `creature/31289//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - Gate Kill |
| `creature/31481//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Scourge Fight Kill Credit |
| `creature/31517//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Dalaran Fountain Invis Stalker |
| `creature/31550//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Tenebron Egg Controller (1) |
| `creature/31641//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Icecrown - Pit Fall |
| `creature/31766//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | King of the Mountain Kill Credit |
| `creature/31773//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Plague Cauldron Target |
| `creature/32338//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Northrend BG - Gate Kill |
| `creature/32427//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Plague Cauldron Target 01 |
| `creature/32442//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Plague Cauldron Target 02 |
| `creature/32465//name` | garder_anglais | nom propre inventé par CoA | Skosiris |
| `creature/32508//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | David Test Creature 1235 |
| `creature/32654//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | SOTA Alliance Gun 1 |
| `creature/32655//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | SOTA Horde Gun 2 |
| `creature/32656//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | SOTA Horde Gun 1 |
| `creature/32661//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | SOTA Alliance Gun 2 |
| `creature/32694//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Vesperon Controller Clear Debuff |
| `creature/32768//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Invisible Stalker (Floating, Uninteractible, Large, Sessile, Custom Phase 2) |
| `creature/33123//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Scorched Ground |
| `creature/33192//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Icecrown Scourge Proxy |
| `creature/33351//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Morgan Test |
| `creature/33764//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | OCL Test Creature |
| `creature/34100//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Algalon Void Zone Visual Stalker |
| `creature/34533//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | ScottM Test Creature |
| `creature/34704//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Val'kyr Twins Bullet Stalker Dark |
| `creature/34720//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Val'kyr Twins Bullet Stalker Light |
| `creature/34743//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Val'kyr Twins Bullet Controller |
| `creature/34810//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | CoD Eye Proxy |
| `creature/34899//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Snowblind Follower Proxy |
| `creature/35015//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Burning Breath Koralon Stalker |
| `creature/35055//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Fallen Hero's Spirit Proxy |
| `creature/35062//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Furious Charge Stalker |
| `creature/35074//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - Southern Tower Kill |
| `creature/35089//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Black Knight Spell Proxy |
| `creature/35226//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Mobile Burrow Target |
| `creature/35227//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Sessile Burrow Target |
| `creature/35297//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Icecrown Cultist Proxy |
| `creature/35820//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Beasts Taplist |
| `creature/36495//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Forgemaster Putridus Invisible Stalker |
| `creature/36508//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Soulguard Beam Focus Target |
| `creature/36549//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Beasts Combat Stalker |
| `creature/36659//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Abomination Wing Orange Gas Stalker |
| `creature/36904//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Gryphon Hatchling 3.3.0 |
| `creature/36934//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Empowering Orb Controller Stalker |
| `creature/37013//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Puddle Stalker |
| `creature/37071//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Invisible Stalker (Icecrown Dungeon Trap Controller) |
| `creature/37231//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Rope Beam Stalker |
| `creature/37525//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Morgan Test (1) |
| `creature/37526//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Morgan Test (2) |
| `creature/37601//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Thalorien Dawnseeker Credit |
| `creature/37699//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | RN Test Honor Guard |
| `creature/37700//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | RN Test Royal Guard |
| `creature/37744//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Frost Freeze Trap |
| `creature/37824//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Abomination Wing Mad Scientist Stalker |
| `creature/37947//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Deathwhisper Spawn Stalker |
| `creature/37986//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Ooze Spray Stalker |
| `creature/38107//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Unstable Ooze Explosion Stalker |
| `creature/38317//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Tear Gas Target Stalker |
| `creature/38440//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Toravon Whiteout Ground Effect |
| `creature/38461//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Toravon Frozen Orb Stalker |
| `creature/38463//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Empowering Orb Visual Stalker |
| `creature/38546//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Frost Infusion Quest Credit |
| `creature/38548//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Vile Gas Stalker |
| `creature/38710//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Frostmourne Soul Transform Visual |
| `creature/38751//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Black Knight Shield Proxy |
| `creature/38903//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Queue trigger |
| `creature/39010//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Martyr Stalker (Reputation) |
| `creature/39011//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Martyr Stalker (Reputation) (1) |
| `creature/39012//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Martyr Stalker (Reputation) (2) |
| `creature/39013//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Martyr Stalker (Reputation) (3) |
| `creature/39019//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Quest - Wintergrasp - PvP Kill - Horde |
| `creature/39091//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Darnavan Kill Credit 10 |
| `creature/39092//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Darnavan Kill Credit 25 |
| `creature/39123//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Blood Quickening Credit 25 |
| `creature/39794//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Zarithrian Spawn Stalker |
| `creature/39821//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Cho'Gall Speech Credit |
| `creature/41273//name` | garder_anglais | nom propre inventé par CoA | Sunny K'arroc |
| `creature/43480//name` | garder_anglais | nom officiel identique (Arash-ethis) | Arash-ethis |
| `creature/50133//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive éventuelle : « Ver de fange » | Muckworm |
| `creature/50287//name` | garder_anglais | nom propre inventé par CoA | Norman Goldshire |
| `creature/52808//name` | doute | nom de créature CoA (forme de druide ?) sans officiel ; proposition : « Forme sauvage » | Wildshape |
| `creature/56332//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel, test ou variante interne), jamais vu sous ce nom | Tank Worgen Form |

## creatures / creatures_002

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `creature/64627//name` | garder_anglais | nom propre inventé par CoA | Korrim Snowgrave |
| `creature/66063//name` | doute | monture de Mists of Pandaria ; Shado-Pan = « Pandashan » chez Blizzard, non prouvé dans nos sources ; proposition : « Tigre de monte pandashan bleu » | Blue Shado-Pan Riding Tiger |
| `creature/80027//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Duel Victory Credit |
| `creature/80420//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Talk to Ameer Greatluck Credit |
| `creature/80421//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Talk to Tiraxis Credit |
| `creature/80652//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Mythic Dungeon Completion Credit |
| `creature/80879//name` | garder_anglais | nom propre inventé par CoA | Fix-o-Tron 5000 |
| `creature/81041//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Heroic Dungeon Completion Credit |
| `creature/81042//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Normal Dungeon Completion Credit |
| `creature/97920//name` | garder_anglais | nom propre inventé par CoA | Pol Hunter |
| `creature/100467//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Path to Ascension Flightmaster Credit |
| `creature/101000//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Raid Leader Credit |
| `creature/101001//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Dungeon Leader Credit |
| `creature/123228//name` | doute | monture ; « Dark Ranger General » (Sylvanas ?) et « Dreadwing » sans forme officielle sûre ; proposition : « Aile-d'effroi du général des Forestiers-sombres » | Dark Ranger General's Dreadwing |
| `creature/137439//name` | doute | anglais obscur (« Ruin Vile ») ; proposition : « Rôdeur ruine-vile » | Ruin Vile Prowler |
| `creature/160001//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Blooming Shot Flower spawner |
| `creature/162710//subname` | doute | sous-titre CoA (sort ?) sans contexte ; proposition : « Éruption du Vide » | Voidflare |
| `creature/164900//name` | doute | nom en espagnol dans les données de CoA (« pirate humaine épéiste ») ; proposition : « Pirate humaine bretteuse » | pirata humana espadachin |
| `creature/165622//name` | garder_anglais | nom propre inventé par CoA | Moer Stonefist |
| `creature/165623//name` | garder_anglais | nom propre inventé par CoA | Brenna Deeprock |
| `creature/165624//name` | garder_anglais | nom propre inventé par CoA | Tormund Deeprock |
| `creature/165625//name` | garder_anglais | nom propre inventé par CoA | Sigra Kazadmere |
| `creature/165626//name` | garder_anglais | nom propre inventé par CoA | Haldor Kazadmere |
| `creature/165627//name` | garder_anglais | nom propre inventé par CoA | Yrsa Embervial |
| `creature/165628//name` | garder_anglais | nom propre inventé par CoA | Brokk Embervial |
| `creature/165629//name` | garder_anglais | nom propre inventé par CoA | Hagren Forgeheart |
| `creature/165630//name` | garder_anglais | nom propre inventé par CoA | Bodvar Forgeheart |
| `creature/165631//name` | garder_anglais | nom propre inventé par CoA | Gimrik Stonedelve |
| `creature/165632//name` | garder_anglais | nom propre inventé par CoA | Ulfgar Kazadbrew |
| `creature/165633//name` | garder_anglais | nom propre inventé par CoA | Callum Titanus |
| `creature/178081//subname` | garder_anglais | « Prestige » est déjà français | Prestige |
| `creature/180238//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Buster Call Marker |
| `creature/216377//name` | doute | « Frogduck » sans forme officielle ; proposition : « Canard-grenouille métamorphosé » | Polymorphed Frogduck |
| `creature/229921//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Build:Mechsuit |
| `creature/254575//name` | garder_anglais | nom propre inventé par CoA | Takan Velor |
| `creature/254941//name` | garder_anglais | nom propre inventé par CoA | Lowfang |
| `creature/254945//name` | garder_anglais | nom propre inventé par CoA | Deathscreech |
| `creature/254947//name` | doute | nom de créature rare ; proposition : « Le Broyeur » | The Masher |
| `creature/299238//name` | garder_anglais | nom propre inventé par CoA | Onacona Warheart |
| `creature/299325//name` | garder_anglais | nom propre inventé par CoA | Gerald |
| `creature/299326//name` | garder_anglais | nom propre inventé par CoA | Kali |
| `creature/299327//name` | garder_anglais | nom propre inventé par CoA | Alanor |
| `creature/299328//name` | garder_anglais | nom propre inventé par CoA | Gok |
| `creature/299329//name` | garder_anglais | nom propre inventé par CoA | Jediyah |
| `creature/371661//name` | doute | couleur « Insignia Red » obscure ; proposition : « Wonka rouge insigne » | Insignia Red Wonka |
| `creature/377942//name` | garder_anglais | « Conduit » est déjà français | Conduit |
| `creature/379411//name` | garder_anglais | nom propre inventé par CoA | Sparky |
| `creature/399300//name` | doute | nom composé « Spiritreaver » sans forme officielle ; proposition : « Ravageur d'esprits ombreux » | Shadowed Spiritreaver |
| `creature/399301//name` | doute | nom composé « Spiritreaver » sans forme officielle ; proposition : « Ravageur d'esprits mortel » | Deathly Spiritreaver |
| `creature/399302//name` | doute | nom composé « Spiritreaver » sans forme officielle ; proposition : « Ravageur d'esprits courroucé » | Wrathful Spiritreaver |
| `creature/445303//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Learn Novice Riding Credit |
| `creature/445304//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Furious Gilded Treant Pacified Credit |
| `creature/453247//name` | doute | « Rockling » sans forme officielle ; proposition : « Rocaillon » | Rockling |
| `creature/502924//name` | garder_anglais | nom propre inventé par CoA | Ophana Gloom |
| `creature/502951//name` | garder_anglais | nom propre inventé par CoA | Alessia |
| `creature/602951//name` | garder_anglais | nom propre inventé par CoA | Ray'chelle Greenhill |
| `creature/642829//name` | garder_anglais | nom propre inventé par CoA | Pete Arr |
| `creature/642829//subname` | garder_anglais | jeu de mots de CoA sur « PTR » (royaume de test) | Plunder Trade Representative (PTR) |
| `creature/840031//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Shadow Trickster Summon |
| `creature/840081//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Binding Shot dummy spawn |
| `creature/840100//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Shadow Trickster Summon |
| `creature/841103//name` | garder_anglais | PNJ technique (déclencheur, crédit de quête, visuel ou invocation interne), jamais vu sous ce nom | Eye beam aoe |
| `creature/996114//name` | garder_anglais | nom identique en français (Agent Serina Vale) | Agent Serina Vale |
| `creature/996115//name` | garder_anglais | nom identique en français (Agent Serina Vale) | Agent Serina Vale |
| `creature/9300102//name` | garder_anglais | nom propre inventé par CoA | Jo |
| `creature/9300151//name` | garder_anglais | nom propre inventé par CoA | Zipak Cogweight |
| `creature/9300152//name` | garder_anglais | nom propre inventé par CoA | Talos |
| `creature/9300154//name` | garder_anglais | nom propre inventé par CoA | Gyrothor Turbospark |
| `creature/9300155//name` | garder_anglais | nom propre inventé par CoA | Hulda Frostwhisper |
| `creature/9300201//name` | garder_anglais | nom propre inventé par CoA | Pangajo Sunseer |
| `creature/9300202//name` | garder_anglais | nom propre inventé par CoA | Beaky |
| `creature/9300203//name` | garder_anglais | nom propre inventé par CoA | Hi'bi Ja'min |
| `creature/9300250//name` | garder_anglais | nom propre inventé par CoA | Brallmular |
| `creature/9300251//name` | doute | titre « Shadow-Walker » sans forme officielle ; proposition : « Marche-ombre Voss » | Shadow-Walker Voss |
| `creature/9300253//name` | garder_anglais | nom propre inventé par CoA | Felo |
| `creature/9300255//name` | garder_anglais | nom propre inventé par CoA | Dalin Soft |
| `creature/9300256//name` | garder_anglais | nom propre inventé par CoA | Agatha Harlow |
| `creature/9300257//name` | garder_anglais | nom propre inventé par CoA | Mortimer |
| `creature/9300300//name` | garder_anglais | nom propre inventé par CoA | Jax Dawnsoar |
| `creature/9300301//name` | garder_anglais | nom propre inventé par CoA | Nawat Windhorn |
| `creature/9300302//name` | garder_anglais | nom propre inventé par CoA | Keed |
| `creature/9300350//name` | garder_anglais | nom propre inventé par CoA ; « Exodite » : titre de CoA | Exodite Telusaara |
| `creature/9300352//name` | garder_anglais | nom propre inventé par CoA | Brim |
| `creature/9300353//name` | garder_anglais | nom propre inventé par CoA | Thalador |
| `creature/9300414//name` | garder_anglais | nom propre inventé par CoA | Seraath |
| `creature/9300416//name` | garder_anglais | nom propre inventé par CoA | Asheer Skyvoice |
| `creature/9300424//name` | garder_anglais | nom propre inventé par CoA | Pyraal |
| `creature/9300425//name` | garder_anglais | nom propre inventé par CoA | Mazhaara |
| `creature/9300426//name` | garder_anglais | nom propre inventé par CoA | Astraan |
| `creature/9300430//name` | doute | genre inconnu pour l'épithète ; proposition : « Sorashii le Silencieux » ou « la Silencieuse » | Sorashii the Silent |
| `creature/9300431//name` | garder_anglais | nom propre inventé par CoA | Elduur |
| `creature/9300432//name` | garder_anglais | nom identique en français (Scribe Taalan) | Scribe Taalan |
| `creature/9300464//name` | garder_anglais | nom propre inventé par CoA | Seldrath Duskblind |
| `creature/9300466//name` | garder_anglais | nom propre inventé par CoA | Aerisa Stormlace |
| `creature/9300467//name` | garder_anglais | nom propre inventé par CoA | Dravinor Ashbrand |
| `creature/9300468//name` | garder_anglais | nom propre inventé par CoA | Therandis Sunshield |
| `creature/9300469//name` | garder_anglais | nom propre inventé par CoA | Aeloris Lightbrand |
| `creature/9300470//name` | garder_anglais | nom propre inventé par CoA | Sanreia Crimsonvein |
| `creature/9300471//name` | garder_anglais | nom propre inventé par CoA | Lyssia Leafstride |
| `creature/9300472//name` | garder_anglais | nom propre inventé par CoA | Taelenna Sandweaver |
| `creature/9300473//name` | garder_anglais | nom propre inventé par CoA | Morthalis Gravewhisper |
| `creature/9300474//name` | garder_anglais | nom propre inventé par CoA | Caelor Emberhand |
| `creature/9300475//name` | garder_anglais | nom propre inventé par CoA | Zaelith Shadowmoor |
| `creature/9300476//name` | garder_anglais | nom propre inventé par CoA | Isolen Starweaver |
| `creature/9300477//name` | garder_anglais | nom propre inventé par CoA | Saleria Sunvow |
| `creature/9300478//name` | garder_anglais | nom propre inventé par CoA | Brelan Arcspindle |
| `creature/9300480//name` | garder_anglais | nom propre inventé par CoA | Solwyn Ashenveil |
| `creature/9300482//name` | garder_anglais | nom propre inventé par CoA | Quelnar Runescribe |
| `creature/9300514//name` | garder_anglais | nom propre inventé par CoA | Haraaz Felscar |
| `creature/9300516//name` | garder_anglais | nom propre inventé par CoA | Kuraax Stormspeaker |
| `creature/9300517//name` | garder_anglais | nom propre inventé par CoA | Vorathaan Ashmantle |
| `creature/9300518//name` | doute | genre inconnu pour le titre ; proposition : « Gardien Iruvaa » ou « Gardienne Iruvaa » | Warden Iruvaa |
| `creature/9300523//name` | doute | titre « Soulbinder » sans forme officielle ; proposition : « Lieur d'âmes Kaarun » | Soulbinder Kaarun |
| `creature/9300524//name` | garder_anglais | nom propre inventé par CoA | Ilaara Cindervow |
| `creature/9300525//name` | doute | genre inconnu pour l'épithète ; proposition : « Nyrosha la Voilée » | Nyrosha the Veiled |
| `creature/9300526//name` | doute | titre « Starseer » sans forme officielle, genre inconnu ; proposition : « Voyante des étoiles Naliima » | Starseer Naliima |
| `creature/9300531//name` | doute | titre « Wildkeeper » sans forme officielle, genre inconnu ; proposition : « Gardienne des terres sauvages Oraana » | Wildkeeper Oraana |
| `creature/9300532//name` | doute | titre « Runecarver » sans forme officielle ; proposition : « Graveur de runes Iskaar » | Runecarver Iskaar |
| `creature/9300564//name` | garder_anglais | nom propre inventé par CoA | Veyrin Felshroud |
| `creature/9300566//name` | garder_anglais | nom propre inventé par CoA | Ilythara Skyrender |
| `creature/9300567//name` | garder_anglais | nom propre inventé par CoA | Tarenar Blackflame |
| `creature/9300568//name` | garder_anglais | nom propre inventé par CoA | Lorthiel Brightward |
| `creature/9300569//name` | garder_anglais | nom propre inventé par CoA | Kaeleth Dawnbrand |
| `creature/9300570//name` | garder_anglais | nom propre inventé par CoA | Velanna Redthorn |
| `creature/9300571//name` | garder_anglais | nom propre inventé par CoA | Nyssa Swiftbough |
| `creature/9300572//name` | garder_anglais | nom propre inventé par CoA | Aeduin Hourward |
| `creature/9300573//name` | garder_anglais | nom propre inventé par CoA | Velrith Scarwatch |
| `creature/9300574//name` | garder_anglais | nom propre inventé par CoA | Ilsara Flamecrest |
| `creature/9300575//name` | garder_anglais | nom propre inventé par CoA | Nerethil Voidwhisper |

## creatures / creatures_003

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `creature/9300576//name` | garder_anglais | nom propre inventé par CoA | Caleste Nightglow |
| `creature/9300577//name` | garder_anglais | nom propre inventé par CoA | Liraen Dawnlight |
| `creature/9300578//name` | garder_anglais | nom propre inventé par CoA | Keldan Sparkwright |
| `creature/9300580//name` | garder_anglais | nom propre inventé par CoA | Dathren Duskmourn |
| `creature/9300582//name` | garder_anglais | nom propre inventé par CoA | Ithrien Glyphwarden |
| `creature/9303637//name` | garder_anglais | jeu de mots de CoA (« Orcamania », catch) : nom de ring à garder | Orcamania Ring |
| `creature/9312001//name` | garder_anglais | nom propre inventé par CoA | Fizzlebolt Gearwhistle |
| `creature/9312002//name` | garder_anglais | nom propre inventé par CoA | Grizzik Scrapsnatch |
| `creature/9780029//name` | garder_anglais | nom propre inventé par CoA | Trut-K'hahn |
| `creature/9780600//name` | garder_anglais | PNJ technique (cible), jamais vu sous ce nom | Cannonball Target |
| `creature/9916113//name` | garder_anglais | nom propre inventé par CoA | Torvald Greyfeather |
| `creature/9916114//name` | garder_anglais | nom propre inventé par CoA | Zul'khar |
| `creature/9916212//name` | garder_anglais | nom propre inventé par CoA | Stormfang |
| `creature/9916213//name` | garder_anglais | nom propre inventé par CoA | Vaelthara |
| `creature/9916214//name` | garder_anglais | nom propre inventé par CoA | Nytharos |
| `creature/9916222//name` | garder_anglais | nom propre inventé par CoA | Stormfang |
| `creature/9916223//name` | garder_anglais | nom propre inventé par CoA | Vaelthara |
| `creature/9916224//name` | garder_anglais | nom propre inventé par CoA | Nytharos |
| `creature/9920211//name` | garder_anglais | PNJ technique (offre de quête), jamais vu sous ce nom | Ealdmaine Caverns Quest Offer |
| `creature/10157257//name` | garder_anglais | nom propre inventé par CoA | Stony Tark |
| `creature/10157258//name` | garder_anglais | nom propre inventé par CoA | Stony Tark |
| `creature/10157356//name` | garder_anglais | « Challenger » se lit en français ; nom propre CoA (Darien) | Challenger Darien |
| `creature/10157358//name` | garder_anglais | « Challenger » se lit en français ; nom propre CoA (Vilria) | Challenger Vilria |
| `creature/11000187//name` | garder_anglais | nom propre inventé par CoA | Lucky-Dee |

## dialogues / dialogues_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `dialogue_pnj/5940/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/6520/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/7868/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/8322/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/8494/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/9516/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/9842/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/10231/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/10955/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/11596/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/11694/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/11696/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/12404/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/12588/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/12970/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/12972/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/14330/0/text0_1` | garder_anglais | texte manquant côté CoA (« Missing US text »), technique | Missing US text |
| `dialogue_pnj/14451/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/14452/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/14569/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/15299/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/15427/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/15546/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/15619/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/15682/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/15904/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/16271/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/17701/0/text0_0` | garder_anglais | texte manquant côté CoA (« MISSING TEXT »), technique | MISSING TEXT |
| `dialogue_pnj/20551/1/text1_1` | doute | coquille de CoA (« gro8und ») : le contrôle exige le chiffre 8 ; proposition : « Araxes ! Envoyez de l'aide ! Je suis coincé dans les mines, je... je ne sais pas exactement où je suis, mais j'ai eu la présence d'esprit de semer des marqueurs sur le sol derrière moi » | Arxes! Send help! Im pinned down in the mines, I...Im not sure where iam exactly but i had the presence of mind to drop tracers on the gro8und behind me |

## enchantements / enchantements_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `enchantement/946//name` | garder_anglais | texte provisoire de CoA (Visual PH), pas un nom de jeu | Fire/Frost Visual PH |
| `enchantement/947//name` | garder_anglais | texte provisoire de CoA (Visual PH), pas un nom de jeu | Purple Visual PH |
| `enchantement/948//name` | garder_anglais | texte provisoire de CoA (Visual PH), pas un nom de jeu | Butterflies Visual PH meme |
| `enchantement/949//name` | garder_anglais | texte provisoire de CoA (Visual PH), pas un nom de jeu | Eldritch Visual PH |
| `enchantement/950//name` | garder_anglais | texte provisoire de CoA (Visual PH), pas un nom de jeu | Arcane Visual PH |
| `enchantement/1008//name` | doute | préfixe CoA « Weapon Craft: » sans décision (sous-classe « Weapon Crafts » = « Artisanat d'armes », traduction de Claude non validée) ; proposition « Artisanat d'armes : Tranchant dentelé » | Weapon Craft: Jagged Edge |
| `enchantement/1009//name` | doute | préfixe CoA « Weapon Craft: » sans décision ; proposition « Artisanat d'armes : Bain d'huile » | Weapon Craft: Oil Dip |
| `enchantement/1010//name` | doute | préfixe CoA « Weapon Craft: » sans décision ; proposition « Artisanat d'armes : Venin neurotoxique » | Weapon Craft: Nerve Venom |
| `enchantement/1011//name` | doute | préfixe CoA « Weapon Craft: » sans décision ; proposition « Artisanat d'armes : Toxine brûlante » | Weapon Craft: Burning Toxin |
| `enchantement/1012//name` | doute | préfixe CoA « Weapon Craft: » sans décision ; proposition « Artisanat d'armes : Toxine glaçante » | Weapon Craft: Freezing Toxin |
| `enchantement/1790//name` | doute | nom CoA « Everdark » : nom propre ou descriptif ? proposition « Ténèbres éternelles » | ¦cff0066ffEverdark¦r |
| `enchantement/1905//name` | doute | « Strider » seul : sens incertain (trotteur, la créature, ou marcheur) ; proposition « Trotteur » | ¦cff0066ffStrider¦r |

## ensembles_objets_client / ensembles_objets_client_003

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `ensemble_objets_client/60062//name` | doute | anglais incomplet ou fautif (« Gladiator's » sans nom après) ; proposition : « Ensemble de gladiateur de devin aquombre » | Aquashadow Diviner's Gladiator's |
| `ensemble_objets_client/60096//name` | doute | jeu de mots sur Frostmourne (Deuillegivre) et lobster (homard) ; aucune forme française sans invention ; proposition : « Homardeuillegivres » ou garder l'anglais | Lobstmournes |

## ensembles_objets_client / ensembles_objets_client_004

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `ensemble_objets_client/61188//name` | doute | nom-plaisanterie (« Kobe » : PNJ de CoA, Firelord Kobe, maître des pyromanciens ; argot « Based » ; « Tier » gardé, décision 13) ; garder l'anglais ou traduire, au choix de Dan ; proposition : « Ensemble Tier de Kobe de la vérité absolue, totale, honnête et suprêmement based » | Kobe's Tier Set of Absolute and Utter Honest and Utmost Based Truth |
| `ensemble_objets_client/61783//name` | doute | anglais incomplet (« Triumphant Raider's » sans nom après) ; proposition, sur le modèle de 61766 : « Costume de pillard triomphant » | Triumphant Raider's  |

## factions / factions_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `faction/1173//name` | garder_anglais | nom propre identique en français (Ramkahen) | Ramkahen |
| `faction/1373//name` | garder_anglais | nom propre inventé par CoA | Eladmine Ealdir |
| `faction/1376//name` | garder_anglais | nom propre inventé par CoA | GraySky |
| `faction/1377//name` | garder_anglais | nom propre (lieu nain) | Dun Kazad |
| `faction/1378//name` | garder_anglais | nom propre inventé par CoA | Thundrakar |
| `faction/1600//name` | garder_anglais | nom propre identique en français (Stromgarde) | Stromgarde |
| `faction/2246//description` | garder_anglais | description interne (faction de test de CoA) | Mystic Coin people |
| `faction/2246//name` | garder_anglais | nom interne (faction de test de CoA) | Mystic Guys |
| `faction/2247//name` | garder_anglais | nom propre inventé par CoA | Vardrheim |

## hauts_faits / hauts_faits_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `haut_fait/5023//name` | garder_anglais | cri sans mot (« REEEEEEEEEEEE! ») : rien à traduire | REEEEEEEEEEEE! |

## hauts_faits / hauts_faits_012

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `haut_fait/39005//name` | garder_anglais | Felforged (sans décision) et Tier (décision 13) restent en anglais : rien à traduire | Felforged Tier: 16 |
| `haut_fait/39007//name` | garder_anglais | Felforged (sans décision) et Tier (décision 13) restent en anglais : rien à traduire | Felforged Tier: 18 |
| `haut_fait/39011//name` | garder_anglais | Felforged (sans décision) et Tier (décision 13) restent en anglais : rien à traduire | Felforged Tier: 22 |
| `haut_fait/39012//name` | garder_anglais | Felforged (sans décision) et Tier (décision 13) restent en anglais : rien à traduire | Felforged Tier: 23 |
| `haut_fait/39014//name` | garder_anglais | Felforged (sans décision) et Tier (décision 13) restent en anglais : rien à traduire | Felforged Tier: 25 |

## hauts_faits / hauts_faits_015

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `haut_fait/80013//name` | garder_anglais | nom officiel de l'extension, identique en français (The Burning Crusade) | The Burning Crusade |
| `haut_fait/80014//name` | garder_anglais | nom officiel de l'extension, identique en français (The Burning Crusade) | The Burning Crusade |
| `haut_fait_categorie/14805//name` | garder_anglais | nom officiel de l'extension, identique en français (The Burning Crusade) | The Burning Crusade |
| `haut_fait_categorie/14822//name` | garder_anglais | nom officiel de l'extension, identique en français (The Burning Crusade) | The Burning Crusade |
| `haut_fait_categorie/14862//name` | garder_anglais | nom officiel de l'extension, identique en français (The Burning Crusade) | The Burning Crusade |
| `haut_fait_categorie/14865//name` | garder_anglais | nom officiel de l'extension, identique en français (The Burning Crusade) | The Burning Crusade |

## hauts_faits / hauts_faits_018

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `haut_fait/254010//name` | garder_anglais | nom propre inventé par CoA (boss), rien à traduire | Pyrava |
| `haut_fait/254011//name` | garder_anglais | nom propre CoA (boss), identique en français | Cascade |
| `haut_fait/254013//name` | garder_anglais | nom propre inventé par CoA (boss) | Raijuu |
| `haut_fait/254018//name` | garder_anglais | nom propre inventé par CoA (boss) | Adranus |
| `haut_fait/254020//name` | garder_anglais | nom propre inventé par CoA (boss) | Corla |
| `haut_fait/254021//name` | garder_anglais | nom propre inventé par CoA (boss) | G'huurak |
| `haut_fait/254024//name` | garder_anglais | nom propre inventé par CoA (boss) | Gorg'ak |
| `haut_fait/254026//name` | garder_anglais | nom propre inventé par CoA (boss) | Akour Qel |

## hauts_faits / hauts_faits_020

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `haut_fait/321878//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Warrior. |
| `haut_fait/321878//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Warrior] Testing - Test Trial |
| `haut_fait/321879//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Paladin. |
| `haut_fait/321879//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Paladin] Testing - Test Trial |
| `haut_fait/321880//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Hunter. |
| `haut_fait/321880//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Hunter] Testing - Test Trial |
| `haut_fait/321881//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Rogue. |
| `haut_fait/321881//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Rogue] Testing - Test Trial |
| `haut_fait/321882//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Priest. |
| `haut_fait/321882//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Priest] Testing - Test Trial |
| `haut_fait/321883//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Death Knight. |
| `haut_fait/321883//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Death Knight] Testing - Test Trial |
| `haut_fait/321884//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Shaman. |
| `haut_fait/321884//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Shaman] Testing - Test Trial |
| `haut_fait/321885//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Mage. |
| `haut_fait/321885//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Mage] Testing - Test Trial |
| `haut_fait/321886//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Warlock. |
| `haut_fait/321886//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Warlock] Testing - Test Trial |
| `haut_fait/321887//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Hero. |
| `haut_fait/321887//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Hero] Testing - Test Trial |
| `haut_fait/321888//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Druid. |
| `haut_fait/321888//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Druid] Testing - Test Trial |
| `haut_fait/321889//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Barbarian. |
| `haut_fait/321889//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Barbarian] Testing - Test Trial |
| `haut_fait/321890//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Witch Doctor. |
| `haut_fait/321890//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Witch Doctor] Testing - Test Trial |
| `haut_fait/321891//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Felsworn. |
| `haut_fait/321891//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Felsworn] Testing - Test Trial |
| `haut_fait/321892//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Witch Hunter. |
| `haut_fait/321892//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Witch Hunter] Testing - Test Trial |
| `haut_fait/321893//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Stormbringer. |
| `haut_fait/321893//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Stormbringer] Testing - Test Trial |
| `haut_fait/321894//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Knight of Xoroth. |
| `haut_fait/321894//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Knight of Xoroth] Testing - Test Trial |
| `haut_fait/321895//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Guardian. |
| `haut_fait/321895//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Guardian] Testing - Test Trial |
| `haut_fait/321896//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Templar. |
| `haut_fait/321896//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Templar] Testing - Test Trial |
| `haut_fait/321897//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Bloodmage. |
| `haut_fait/321897//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Bloodmage] Testing - Test Trial |
| `haut_fait/321898//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Ranger. |
| `haut_fait/321898//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Ranger] Testing - Test Trial |
| `haut_fait/321899//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Chronomancer. |
| `haut_fait/321899//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Chronomancer] Testing - Test Trial |
| `haut_fait/321900//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Necromancer. |
| `haut_fait/321900//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Necromancer] Testing - Test Trial |
| `haut_fait/321901//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Pyromancer. |
| `haut_fait/321901//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Pyromancer] Testing - Test Trial |
| `haut_fait/321902//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Cultist. |
| `haut_fait/321902//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Cultist] Testing - Test Trial |
| `haut_fait/321903//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Starcaller. |
| `haut_fait/321903//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Starcaller] Testing - Test Trial |
| `haut_fait/321904//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Sun Cleric. |
| `haut_fait/321904//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Sun Cleric] Testing - Test Trial |
| `haut_fait/321905//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Tinker. |
| `haut_fait/321905//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Tinker] Testing - Test Trial |
| `haut_fait/321906//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Venomancer. |
| `haut_fait/321906//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Venomancer] Testing - Test Trial |
| `haut_fait/321907//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Reaper. |
| `haut_fait/321907//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Reaper] Testing - Test Trial |
| `haut_fait/321908//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Primalist. |
| `haut_fait/321908//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Primalist] Testing - Test Trial |
| `haut_fait/321909//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Runemaster. |
| `haut_fait/321909//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Runemaster] Testing - Test Trial |
| `haut_fait/321910//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as a Hero and all standard classes. |
| `haut_fait/321910//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Mastery] Testing - Test Trial |
| `haut_fait/321911//description` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | Complete the "Testing - Test Trial" challenge as all Conquest of Azeroth classes. |
| `haut_fait/321911//name` | garder_anglais | défi de test de CoA (« Testing - Test Trial »), texte technique | [Conquest] Testing - Test Trial |
| `haut_fait_categorie/50//name` | garder_anglais | catégorie interne de CoA (« Sinstalis… Temp »), texte technique | Sinstalis Achievements Temp |
| `haut_fait_categorie/51//name` | garder_anglais | catégorie interne de CoA (« Sinstalis… Temp »), texte technique | Sinstalis Achievements Temp |
| `haut_fait_categorie/52//name` | garder_anglais | catégorie interne de CoA (« Sinstalis… »), texte technique | Sinstalis Achievements Feats Of Strength |
| `haut_fait_categorie/53//name` | garder_anglais | catégorie interne de CoA (« Sinstalis… Bench »), texte technique | Sinstalis Achievements Bench |
| `haut_fait_categorie/14817//name` | garder_anglais | identique en français (Naxxramas, Vanilla gardé) | Naxxramas (Vanilla) |
| `haut_fait_categorie/14823//name` | garder_anglais | nom officiel de l'extension, identique en français | Wrath of the Lich King |
| `haut_fait_categorie/14863//name` | garder_anglais | nom officiel de l'extension, identique en français | Wrath of the Lich King |
| `haut_fait_categorie/14866//name` | garder_anglais | nom officiel de l'extension, identique en français | Wrath of the Lich King |
| `haut_fait_categorie/15132//name` | garder_anglais | nom de la plateforme Ascension (pas le sort « Sublimation ») | Ascension |
| `haut_fait_categorie/17009//name` | garder_anglais | identique en français (« Collections ») | Collections |
| `haut_fait_categorie/17015//name` | garder_anglais | Hardcore : épreuve CoA, gardée en anglais (sans décision) | Hardcore |
| `haut_fait_categorie/64922//name` | garder_anglais | Ascended reste en anglais (décision 3) | Ascended |
| `haut_fait_categorie/64923//name` | garder_anglais | Ascended reste en anglais (décision 3) | Ascended |
| `haut_fait_categorie/64924//name` | garder_anglais | Ascended reste en anglais (décision 3) | Ascended |
| `haut_fait_categorie/65099//name` | garder_anglais | Ascended reste en anglais (décision 3) | Ascended |
| `haut_fait_categorie/65106//name` | garder_anglais | Ascended reste en anglais (décision 3) | Ascended |
| `haut_fait_categorie/65109//name` | garder_anglais | Ascended reste en anglais (décision 3) | Ascended |
| `haut_fait_categorie/65112//name` | garder_anglais | Ascended reste en anglais (décision 3) | Ascended |
| `haut_fait_categorie/80000//name` | garder_anglais | Felforged : mode CoA sans décision, gardé en anglais | Felforged |
| `haut_fait_categorie/80001//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 1 |
| `haut_fait_categorie/80002//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 2 |
| `haut_fait_categorie/80003//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 3 |
| `haut_fait_categorie/80004//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 4 |
| `haut_fait_categorie/80005//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 5 |
| `haut_fait_categorie/80006//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 6 |
| `haut_fait_categorie/80007//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 7 |
| `haut_fait_categorie/80008//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 8 |
| `haut_fait_categorie/80009//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 9 |
| `haut_fait_categorie/80010//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 10 |
| `haut_fait_categorie/80011//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 11 |
| `haut_fait_categorie/80012//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 12 |
| `haut_fait_categorie/80013//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 13 |
| `haut_fait_categorie/80014//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 14 |
| `haut_fait_categorie/80015//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 15 |
| `haut_fait_categorie/80016//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 16 |
| `haut_fait_categorie/80017//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 17 |
| `haut_fait_categorie/80018//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 18 |
| `haut_fait_categorie/80019//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 19 |
| `haut_fait_categorie/80020//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 20 |
| `haut_fait_categorie/80021//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 21 |
| `haut_fait_categorie/80022//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 22 |
| `haut_fait_categorie/80023//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 23 |
| `haut_fait_categorie/80024//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 24 |
| `haut_fait_categorie/80025//name` | garder_anglais | Tier N reste en anglais (décision 13) | Tier 25 |

## interface / interface_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `chaine_interface/BATTLENET_OPTIONS_LABEL//texte` | garder_anglais | nom de marque et icône, identique à l'officiel | Battle.net¦TInterface\OptionsFrame\UI-OptionsFrame-NewFeatureIcon:0:0:0:-1¦t |
| `chaine_interface/BIND_TRADE_TIME_REMAINING//texte` | garder_anglais | texte technique (nom de la clé suivi de %s), pas un texte du jeu | BIND_TRADE_TIME_REMAINING:%s |
| `chaine_interface/BUG_REPORT_LABEL_RAID//texte` | garder_anglais | identique à l'officiel français (« Raid ») | Raid |
| `chaine_interface/BUILDCREATOR_CATEGORYBUTTON_BUILDDRAFTENDGAMEPVE//texte` | doute | « Draft de build » refusé par le contrôle (majoritairement anglais) ; proposition : « Draft de build » (nom du mode CoA, comme « Draft ») | Build Draft |
| `chaine_interface/BUILDCREATOR_CATEGORYBUTTON_BUILDDRAFTENDGAMEPVP//texte` | doute | « Draft de build » refusé par le contrôle (majoritairement anglais) ; proposition : « Draft de build » (nom du mode CoA, comme « Draft ») | Build Draft |
| `chaine_interface/BUILDDRAFT_MODE//texte` | doute | « Draft de build » refusé par le contrôle (majoritairement anglais) ; proposition : « Draft de build » (nom du mode CoA, comme « Draft ») | Build Draft |
| `chaine_interface/BUILD_URL_COPIED_TO_CLIPBOARD//texte` | doute | exclu par le contrôle (presse-papiers) ; proposition : « Lien de partage du build copié dans le presse-papiers ! » | Shareable Build URL Copied to Clipboard! |
| `chaine_interface/BURNING_CRUSADE//texte` | garder_anglais | nom officiel de l'extension, identique en français | The Burning Crusade |
| `chaine_interface/CALENDAR_TYPE_RAID//texte` | garder_anglais | identique à l'officiel français (« Raid ») | Raid |
| `chaine_interface/CHARACTER_FRIEND//texte` | garder_anglais | nom du jeu, identique à l'officiel | World of Warcraft |
| `chaine_interface/CHAT_MSG_RAID//texte` | garder_anglais | identique à l'officiel français (« Raid ») | Raid |
| `chaine_interface/CHAT_RAID_GET//texte` | garder_anglais | lien de canal, identique à l'officiel français | ¦Hchannel:RAID¦h[Raid]¦h %s:  |
| `chaine_interface/CRIT_ABBR//texte` | garder_anglais | abréviation identique à l'officiel français (« Crit ») | Crit |
| `chaine_interface/DRAFT_MODE//texte` | garder_anglais | Draft reste en anglais (glossaire : nom de la mécanique) | Draft |
| `chaine_interface/ENCHANT_COLLECTION_WORLDFORGED//texte` | garder_anglais | Worldforged reste en anglais (décision 2) | ¦cff00CCFFWorldforged¦r |
| `chaine_interface/ERR_APPROACHING_NO_PLAY_TIME_2//texte` | doute | le contrôle de format lit « % o » dans « 50% of » (anglais) et exige le même code ; message anti-addiction chinois, sans doute jamais affiché ; proposition : « Vous êtes en état fatigué et vous ne recevez plus que 50% des bénéfices normaux. Dans l'intérêt de votre santé, nous vous prions de vous déconnecter pour vous reposer, faire de l'exercice et gérer correctement votre emploi du temps. » | You are in tired time, and your benefits have been reduced to 50% of normal. For the sake of your own health, please go offline and rest, do some exercise, and  |
| `chaine_interface/ERR_BG_PLAYER_JOINED_SS//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition (officiel) : « ¦Hplayer:%s¦h[%s]¦h se joint à la bataille » | ¦Hplayer:%s¦h[%s]¦h has joined the battle |
| `chaine_interface/ERR_FRIEND_ONLINE_SS//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition (officiel) : « ¦Hplayer:%s¦h[%s]¦h vient de se connecter. » | ¦Hplayer:%s¦h[%s]¦h has come online. |
| `chaine_interface/ERR_INVITED_ALREADY_IN_GROUP_SS//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition (officiel) : « ¦Hplayer:%s¦h[%s]¦h vous a invité à rejoindre un groupe, mais vous ne pouviez pas accepter car vous êtes déjà dans un groupe. » | ¦Hplayer:%s¦h[%s]¦h invited you to a group, but you could not accept because you are already in a group. |
| `chaine_interface/ERR_INVITED_TO_GROUP_SS//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition (officiel) : « ¦Hplayer:%s¦h[%s]¦h vous a invité à rejoindre un groupe. » | ¦Hplayer:%s¦h[%s]¦h has invited you to join a group. |
| `chaine_interface/ERR_INVITED_TO_GUILD_SSS//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition (officiel) : « ¦Hplayer:%s¦h[%s]¦h vous invite à rejoindre %s. » | ¦Hplayer:%s¦h[%s]¦h invites you to join %s. |
| `chaine_interface/EXPANSION_NAME1//texte` | garder_anglais | nom officiel de l'extension, identique en français | The Burning Crusade |
| `chaine_interface/GAMEMODE10//texte` | doute | « Draft de build » refusé par le contrôle (majoritairement anglais) ; proposition : « Draft de build » (nom du mode CoA, comme « Draft ») | Build Draft |
| `chaine_interface/GAMEMODE4//texte` | garder_anglais | Draft reste en anglais (glossaire : nom de la mécanique) | Draft |
| `chaine_interface/LFG_TYPE_RAID//texte` | garder_anglais | identique à l'officiel français (« Raid ») | Raid |
| `chaine_interface/RAID//texte` | garder_anglais | identique à l'officiel français (« Raid ») | Raid |
| `chaine_interface/RAID_MESSAGE//texte` | garder_anglais | identique à l'officiel français (« Raid ») | Raid |

## interface / interface_002

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `chaine_interface/EXPANSION_NAME2//texte` | garder_anglais | nom officiel de l'extension, identique en français | Wrath of the Lich King |
| `chaine_interface/GENERIC_DIFFICULTY4//texte` | garder_anglais | Ascended reste en anglais (décision 3) | Ascended |
| `chaine_interface/INT//texte` | garder_anglais | abréviation identique en français (Int = Intelligence) | Int |
| `chaine_interface/ITEM_SUBCLASS_4_7//texte` | garder_anglais | mot identique en français (officiel : « Librams ») | Librams |
| `chaine_interface/KEY_TAB//texte` | garder_anglais | touche identique à l'officiel (« Tab ») | Tab |
| `chaine_interface/MELEE_CRIT//texte` | garder_anglais | identique à l'officiel français (« CRIT %.2f ») | CRIT %.2f |
| `chaine_interface/MINIMAP_TRACKING_DREAM_LIKE_AZGA//texte` | garder_anglais | nom propre inventé par CoA | Azga |
| `chaine_interface/MINIMAP_TRACKING_DREAM_LIKE_KEKEER//texte` | garder_anglais | nom propre inventé par CoA | Kekeer |
| `chaine_interface/MINIMAP_TRACKING_DREAM_LIKE_MIKOLON//texte` | garder_anglais | nom propre inventé par CoA | Mikolon |
| `chaine_interface/MINIMAP_TRACKING_DREAM_LIKE_SVELTA//texte` | garder_anglais | nom propre inventé par CoA | Svelta |
| `chaine_interface/MINIMAP_TRACKING_DREAM_LIKE_ZALAKKAR//texte` | garder_anglais | nom propre inventé par CoA | Zalakkar |
| `chaine_interface/MINIMAP_TRACKING_STONYTARK//texte` | garder_anglais | suivi de la minicarte, sens incertain (« Challenger » se dit aussi en français) | Challenger |
| `chaine_interface/MOVIE_RECORDING_MJPEG//texte` | garder_anglais | nom de codec, identique à l'officiel | Motion JPEG |
| `chaine_interface/MSG_REQUESTED_INVITE//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition : « Vous avez demandé à rejoindre le groupe de ¦cffffffff¦Hplayer:%1$s¦h[%1$s]¦h¦r. » | You requested to join ¦cffffffff¦Hplayer:%1$s¦h[%1$s]¦h¦r's group. |
| `chaine_interface/MSG_REQUESTED_INVITE_TO_GROUP//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition : « ¦cffffffff¦Hplayer:%1$s¦h[%1$s]¦h¦r a demandé à rejoindre votre groupe. » | ¦cffffffff¦Hplayer:%1$s¦h[%1$s]¦h¦r has requested to join your group. |
| `chaine_interface/MSG_SUGGESTED_INVITE//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition : « Vous avez proposé à ¦cffffffff¦Hplayer:%1$s¦h[%1$s]¦h¦r de rejoindre votre groupe. » | You suggested ¦cffffffff¦Hplayer:%1$s¦h[%1$s]¦h¦r join your group. |
| `chaine_interface/NEWS//texte` | garder_anglais | identique à l'officiel français (« News ») | News |
| `chaine_interface/PVP_TIER_CHALLENGER//texte` | garder_anglais | suivi de la minicarte, sens incertain (« Challenger » se dit aussi en français) | Challenger |
| `chaine_interface/WRATH_OF_THE_LICH_KING//texte` | garder_anglais | nom officiel de l'extension, identique en français | Wrath of the Lich King |

## interface / interface_003

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `chaine_interface/OPTIMAL//texte` | garder_anglais | mot identique en français (« Optimal ») | Optimal |
| `chaine_interface/PLAYER_SERVER_FIRST_ACHIEVEMENT//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition (officiel) : « ¦Hplayer:%s¦h[%s]¦h a accompli le haut fait $a ! » | ¦Hplayer:%s¦h[%s]¦h has earned the achievement $a! |
| `chaine_interface/RAID_PROFILE_COPIED//texte` | doute | exclu par le contrôle (presse-papiers) ; proposition : « Profil de raid ¦cffffffff[%s]¦r copié dans le presse-papiers ! » | Raid Profile ¦cffffffff[%s]¦r Copied to Clipboard! |
| `chaine_interface/SPELL_USE_ALL_ENERGY//texte` | doute | le contrôle de format lit « % E » (« 100% Energy ») comme un code %E et l'exige dans le français ; proposition : « Utilise 100% de l'Énergie » | Uses 100% Energy |
| `chaine_interface/S_COPIED_TO_CLIPBOARD//texte` | doute | exclu par le contrôle (presse-papiers) ; proposition : « "%s" copié dans le presse-papiers ! » | "%s" Copied to Clipboard! |
| `chaine_interface/TARGET_ICON_SET//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition (officiel) : « ¦Hplayer:%s¦h[%s]¦h place la cible ¦TInterface\TargetingFrame\UI-RaidTargetingIcon_%d:0¦t sur %s. » | ¦Hplayer:%s¦h[%s]¦h sets ¦TInterface\TargetingFrame\UI-RaidTargetingIcon_%d:0¦t on %s. |
| `chaine_interface/TEXT_MODE_A_STRING_RESULT//texte` | garder_anglais | variable seule, identique à l'officiel | ($resultString) |
| `chaine_interface/TOO_MANY_LUA_ERRORS//texte` | doute | le contrôle des nombres lit « 3rd party » comme le nombre 3 et l'exige dans le français (le double retour à la ligne est désormais accepté) ; proposition : « Vos add-ons rencontrent un grand nombre d'erreurs et ralentissent peut-être le jeu. \n\nLes add-ons tiers peuvent causer des baisses d'IPS, de la latence et des plantages. Utilisez si possible les add-ons du lanceur d'Ascension. » | Your AddOns are experiencing a large number of errors and may be slowing down the game.   3rd party AddOns can cause FPS, lag, and crashing issues. Please try t |

## interface / interface_004

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `chaine_interface/VOICEMACRO_LABEL_SILLY1//texte` | garder_anglais | étiquette technique de macro vocale, gardée en anglais par l officiel français | silly |
| `chaine_interface/WHO_LIST_FORMAT//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition (officiel) : « ¦Hplayer:%s¦h[%s]¦h : Niveau %d %s %s - %s » | ¦Hplayer:%s¦h[%s]¦h: Level %d %s %s - %s |
| `chaine_interface/WHO_LIST_GUILD_FORMAT//texte` | doute | exclu par le contrôle (lien de joueur ¦Hplayer) ; proposition (officiel) : « ¦Hplayer:%s¦h[%s]¦h : Niveau %d %s %s <%s> - %s » | ¦Hplayer:%s¦h[%s]¦h: Level %d %s %s <%s> - %s |

## messages_serveur / messages_serveur_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `message_serveur/34//content_default` | garder_anglais | identique en français (« [talent] ») |  [talent] |
| `message_serveur/41//content_default` | garder_anglais | identique en français (« visible ») | visible |
| `message_serveur/42//content_default` | garder_anglais | identique en français (« invisible ») | invisible |
| `message_serveur/87//content_default` | garder_anglais | code d'erreur technique | UNKNOWN_ERROR |
| `message_serveur/101//content_default` | garder_anglais | sortie technique de la commande .gps (MJ) | Map: {} ({}) Zone: {} ({}) Area: {} ({}) Phase: {} X: {} Y: {} Z: {} Orientation: {} grid[{},{}]cell[{},{}] InstanceID: {}  ZoneX: {} ZoneY: {} GroundZ: {} Floo |
| `message_serveur/152//content_default` | garder_anglais | sortie technique de débogage (MJ) | USER1: {}, ADD: {}, DIF: {}  |
| `message_serveur/160//content_default` | garder_anglais | sortie technique de débogage (MJ) | USER2: {}, ADD: {}, RESULT: {}  |
| `message_serveur/178//content_default` | garder_anglais | sortie technique de la commande .gps (MJ) | grid[{},{}]cell[{},{}] InstanceID: {}  ZoneX: {} ZoneY: {} GroundZ: {} FloorZ: {} Have height data (Map: {} VMap: {} MMap: {}) |
| `message_serveur/179//content_default` | garder_anglais | libellé technique (MJ) | ¦ AccountFlags: |
| `message_serveur/186//content_default` | garder_anglais | sortie technique de débogage (MJ) | TransMapID: {} TransOffsetX: {} TransOffsetY: {} TransOffsetZ: {} TransOffsetO: {} (Transport ID: {} {}) |
| `message_serveur/312//content_default` | garder_anglais | identique en français (« [visible] ») |  [visible] |

## messages_serveur / messages_serveur_002

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `message_serveur/319//content_default` | garder_anglais | identique en français (rang de réputation « Hostile ») | Hostile |
| `message_serveur/329//content_default` | garder_anglais | format technique sans texte |   {} (GUID {}) |
| `message_serveur/349//content_default` | garder_anglais | format technique de la liste des titres (MJ) | {} (idx:{}) - ¦cffffffff¦Htitle:{}¦h[{} {}]¦h¦r {} {}  |
| `message_serveur/350//content_default` | garder_anglais | format technique de la liste des titres (MJ) | {} (idx:{}) - [{} {}] {} {}  |
| `message_serveur/457//content_default` | garder_anglais | identique en français (« alliance ») | alliance |
| `message_serveur/458//content_default` | garder_anglais | identique en français (« horde ») | horde |
| `message_serveur/468//content_default` | garder_anglais | sortie technique de débogage des auras (MJ) | id: {} {} effmask: {} charges: {} stack: {} slot {} duration: {} maxduration: {} {} {} caster: {} guid: {} |
| `message_serveur/470//content_default` | garder_anglais | sortie technique de débogage des auras (MJ) | id: {} eff: {} amount: {} |
| `message_serveur/515//content_default` | garder_anglais | format technique de lien (MJ) | {} - (entry: {}) ¦cffffffff¦Hcreature:{}¦h[{} X:{} Y:{} Z:{} MapId:{}]¦h¦r |
| `message_serveur/517//content_default` | garder_anglais | format technique de lien (MJ) | {} (Entry: {}) - ¦cffffffff¦Hgameobject:{}¦h[{} X:{} Y:{} Z:{} MapId:{}]¦h¦r  |
| `message_serveur/555//content_default` | garder_anglais | sortie technique de débogage (MJ) | SetData performed on [GUID: {}, entry: {}, name: {}] Field: {}, Data: {}, with {} |
| `message_serveur/562//content_default` | garder_anglais | sortie technique de débogage (MJ) | GUID={} 's updateIndex: {}, value:  {}. |
| `message_serveur/563//content_default` | garder_anglais | sortie technique de débogage (MJ) | You change GUID={} 's UpdateIndex: {} value to {}. |
| `message_serveur/564//content_default` | garder_anglais | sortie technique de débogage (MJ) | The value index {} is too big to {}(count: {}). |
| `message_serveur/565//content_default` | garder_anglais | sortie technique de débogage (MJ) | Set {} uint32 Value:[OPCODE]:{} [VALUE]:{} |
| `message_serveur/566//content_default` | garder_anglais | sortie technique de débogage (MJ) | You Set {} Field:{} to uint32 Value: {} |
| `message_serveur/567//content_default` | garder_anglais | sortie technique de débogage (MJ) | Set {} float Value:[OPCODE]:{} [VALUE]:{} |
| `message_serveur/568//content_default` | garder_anglais | sortie technique de débogage (MJ) | You Set {} Field:{} to float Value: {} |
| `message_serveur/569//content_default` | garder_anglais | sortie technique de débogage (MJ) | Get {} uint32 Value:[OPCODE]:{} [VALUE]:{} |
| `message_serveur/570//content_default` | garder_anglais | sortie technique de débogage (MJ) | The uint32 value of {} in {} is: {} |
| `message_serveur/571//content_default` | garder_anglais | sortie technique de débogage (MJ) | Get {} float Value:[OPCODE]:{} [VALUE]:{} |
| `message_serveur/572//content_default` | garder_anglais | sortie technique de débogage (MJ) | The float of {} value in {} is: {} |
| `message_serveur/573//content_default` | garder_anglais | sortie technique de débogage (MJ) | .Set32Bit:[OPCODE]:{} [VALUE]:{} |
| `message_serveur/574//content_default` | garder_anglais | sortie technique de débogage (MJ) | You set Bit of Field:{} to Value: {} |
| `message_serveur/575//content_default` | garder_anglais | sortie technique de débogage (MJ) | .Mod32Value:[OPCODE]:{} [VALUE]:{} |
| `message_serveur/576//content_default` | garder_anglais | sortie technique de débogage (MJ) | You modified the value of Field:{} to Value: {} |
| `message_serveur/594//content_default` | garder_anglais | en-tête de tableau aligné (MJ) | ¦    Account    ¦   BanDate    ¦   UnbanDate  ¦  Banned By    ¦   Ban Reason  ¦ |
| `message_serveur/596//content_default` | garder_anglais | en-tête de tableau aligné (MJ) | ¦      IP       ¦   BanDate    ¦   UnbanDate  ¦  Banned By    ¦   Ban Reason  ¦ |
| `message_serveur/598//content_default` | garder_anglais | en-tête de tableau aligné (MJ) | ¦    Account    ¦  GM  ¦ |
| `message_serveur/603//content_default` | garder_anglais | sortie technique de débogage (MJ) | Do Action performed on [GUID: {}, entry: {}, name: {}] Action: {} |

## messages_serveur / messages_serveur_003

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `message_serveur/870//content_default` | garder_anglais | format technique sans texte | ¦"{}"[ID:{}]({}x{})¦ |
| `message_serveur/1010//content_default` | garder_anglais | en-tête de tableau aligné (MJ) | -[         Account][   Character][             IP][Map][Zone][Exp][GMLev]- |
| `message_serveur/1011//content_default` | garder_anglais | ligne de tableau alignée (MJ) | ¦<Error>        ¦ {} ¦<Error>          ¦<Er>¦ <Error>   ¦ |
| `message_serveur/1016//content_default` | garder_anglais | en-tête de tableau aligné (MJ) | ¦ GUID       ¦ Name                 ¦ Level ¦ Account                      ¦ Delete Date         ¦ |
| `message_serveur/1110//content_default` | garder_anglais | format technique sans texte | {} - {} X:{} Y:{} Z:{} MapId:{} |
| `message_serveur/1111//content_default` | garder_anglais | format technique sans texte | {} - {} X:{} Y:{} Z:{} MapId:{} |
| `message_serveur/1122//content_default` | garder_anglais | format technique sans texte | ({}/{} +perm {} +temp {}) |
| `message_serveur/1128//content_default` | garder_anglais | format technique de lien (MJ) | {} - ¦cffffffff¦Htaxinode:{}¦h[{} {}]¦h¦r (Map:{} X:{} Y:{} Z:{}) |
| `message_serveur/1129//content_default` | garder_anglais | format technique sans texte | {} - {} {} (Map:{} X:{} Y:{} Z:{}) |
| `message_serveur/1133//content_default` | garder_anglais | en-tête de tableau aligné (MJ) | ¦   Character   ¦   BanDate    ¦   UnbanDate  ¦  Banned By    ¦   Ban Reason  ¦ |
| `message_serveur/1143//content_default` | garder_anglais | sortie technique de débogage (MJ) | Target's moveFlags: {}, moveFlagsExtra: {}. |
| `message_serveur/1144//content_default` | garder_anglais | sortie technique de débogage (MJ) | Target's moveFlags set to: {}, moveFlagsExtra to: {} |
| `message_serveur/1160//content_default` | garder_anglais | en-tête de tableau aligné (MJ) | ¦            ¦ Alliance ¦  Horde   ¦ Neutral  ¦  Total   ¦ |
| `message_serveur/1161//content_default` | garder_anglais | en-tête de tableau aligné (MJ) |           Alliance/Horde/Neutral/Total |
| `message_serveur/1166//content_default` | garder_anglais | en-tête de tableau aligné (MJ) | ¦            ¦ Alliance ¦   Horde  ¦ Neutral  ¦  Amount  ¦ |
| `message_serveur/1167//content_default` | garder_anglais | en-tête de tableau aligné (MJ) |           Alliance/Horde/Neutral/Amount |
| `message_serveur/1173//content_default` | garder_anglais | identique en français (« Orange ») | Orange |
| `message_serveur/5010//content_default` | garder_anglais | sortie technique de débogage (MJ) | linkGUID: {}, Entry: {} ({}) |
| `message_serveur/5013//content_default` | garder_anglais | identique en français (« [Continent] ») | [Continent] |
| `message_serveur/5014//content_default` | garder_anglais | identique en français (« [Instance] ») | [Instance] |
| `message_serveur/5017//content_default` | garder_anglais | identique en français (« [Raid] ») | [Raid] |
| `message_serveur/5031//content_default` | garder_anglais | sortie technique de débogage (MJ) | AIName: {} ScriptName: {} |
| `message_serveur/5036//content_default` | garder_anglais | sortie technique de débogage (MJ) | EquipmentId: {} (Original: {}). |
| `message_serveur/5037//content_default` | garder_anglais | sortie technique de débogage (MJ) | MechanicImmuneMask: {} |
| `message_serveur/5039//content_default` | garder_anglais | identique en français (« Console ») | Console |
| `message_serveur/5045//content_default` | garder_anglais | sortie technique de débogage (MJ) | Map: {} ¦ ID: {} ¦ perm: {} ¦ extended: {} ¦ diff: {} ¦ canReset: {} ¦ TTR: {} |
| `message_serveur/5048//content_default` | garder_anglais | sortie technique de débogage (MJ) | Unbinding map: {} inst: {} perm: {} diff: {} canReset: {} TTR: {} |
| `message_serveur/5062//content_default` | garder_anglais | sortie technique de débogage (MJ) | SpellSchoolImmuneMask: {} |

## messages_serveur / messages_serveur_004

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `message_serveur/11009//content_default` | garder_anglais | sortie technique de débogage (MJ) : nom du champ flags_extra | Flags Extra: {} |
| `message_serveur/991475//content_default` | garder_anglais | cri d'un nom propre (« Jasper »), rien à traduire | JASPERRRRR!!! |

## objets / objets_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/5732//name` | garder_anglais | nom technique (explosif NG-5), identique en français | NG-5 |
| `objet/11271//name` | garder_anglais | nom propre inventé, identique en français | Eles'finel |
| `objet/11331//name` | garder_anglais | nom de travail des développeurs (« lw mail gloves caster »), technique | lw mail gloves caster (int,sp,hit,crit) |
| `objet/11332//name` | garder_anglais | nom de travail des développeurs (« lw mail gloves caster »), technique | lw mail gloves caster (int,sp,hit,crit) |
| `objet/11333//name` | garder_anglais | nom de travail des développeurs (« lw mail gloves caster »), technique | lw mail gloves caster (int,sp,hit,crit) |
| `objet/11334//name` | garder_anglais | nom de travail des développeurs (« lw mail gloves caster »), technique | lw mail gloves caster (int,sp,hit,crit) |
| `objet/11447//name` | garder_anglais | nom de travail des développeurs (« bs plate gloves str »), technique | bs plate gloves str (str,hit,haste,stam) |
| `objet/11448//name` | garder_anglais | nom de travail des développeurs (« bs plate gloves str »), technique | bs plate gloves str (str,hit,haste,stam) |
| `objet/11449//name` | garder_anglais | nom de travail des développeurs (« bs plate gloves str »), technique | bs plate gloves str (str,hit,haste,stam) |
| `objet/11450//name` | garder_anglais | nom de travail des développeurs (« bs plate gloves str »), technique | bs plate gloves str (str,hit,haste,stam) |
| `objet/11451//name` | garder_anglais | nom de travail des développeurs (« Plans: bs plate gloves str »), technique | Plans: bs plate gloves str (str,hit,haste,stam) |
| `objet/12284//name` | garder_anglais | nom propre d'appareil gnome, identique en français | Draco-Incarcinatrix 900 |

## objets / objets_002

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/16171//name` | garder_anglais | nom propre inventé par CoA | Shinsollo |
| `objet/19000//name` | garder_anglais | nom de travail des développeurs (« Combat Rogue 1.5 Speed Wep »), technique | Combat Rogue 1.5 Speed Wep |
| `objet/20577//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDNightmare Blade |
| `objet/20578//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDEmerald Dragonfang |
| `objet/20579//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDGreen Dragonskin Cloak |
| `objet/20580//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDHammer of Bestial Fury |
| `objet/20581//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDStaff of Rampant Growth |
| `objet/20582//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDTrance Stone |
| `objet/20599//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDPolished Ironwood Crossbow |
| `objet/20615//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDDragonspur Wraps |
| `objet/20616//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDDragonbone Wristguards |
| `objet/20617//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDAncient Corroded Leggings |
| `objet/20618//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDGloves of Delusional Power |
| `objet/20619//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDAcid Inscribed Greaves |
| `objet/20621//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDBoots of the Endless Moor |
| `objet/20622//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDDragonheart Necklace |
| `objet/20623//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDCirclet of Restless Dreams |
| `objet/20624//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDRing of the Unliving |
| `objet/20625//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDBelt of the Dark Bog |
| `objet/20626//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDBlack Bark Wristbands |
| `objet/20627//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDDark Heart Pants |
| `objet/20628//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDDeviate Growth Cap |
| `objet/20629//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDMalignant Footguards |
| `objet/20630//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDGauntlets of the Shining Light |
| `objet/20631//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDMendicant's Slippers |
| `objet/20632//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDMindtear Band |
| `objet/20633//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDUnnatural Leather Spaulders |
| `objet/20634//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDBoots of Fright |
| `objet/20635//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDJade Inlaid Vestments |
| `objet/20636//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDHibernation Crystal |
| `objet/20637//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDAcid Inscribed Pauldrons |
| `objet/20638//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDLeggings of the Demented Mind |
| `objet/20639//name` | garder_anglais | objet marqué UNUSED (inutilisé) par les développeurs, technique | UNUSEDStrangely Glyphed Legplates |
| `objet/27002//description` | garder_anglais | texte de test des développeurs (pseudonyme), rien à traduire | Spojka 4ever |
| `objet/27007//description` | garder_anglais | texte de test des développeurs (pseudonyme), rien à traduire | Spojka 4ever |
| `objet/30648//name` | garder_anglais | jeu de mots sur l'anglais (« Re'ahl Ni-pwn »), intraduisible | Re'ahl Ni-pwn Steel |

## objets / objets_003

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/37295//name` | garder_anglais | nom de travail technique des développeurs | HF28 Cloth Spell Head4 |
| `objet/37536//name` | garder_anglais | nom de travail technique des développeurs | BT57 Fast Mace2 |
| `objet/37974//name` | garder_anglais | nom de travail technique des développeurs | DB52 Spell Cloak2  |
| `objet/37978//name` | garder_anglais | nom de travail technique des développeurs | DB57 Cloth Spell Chest3 |
| `objet/38140//name` | garder_anglais | nom de travail technique des développeurs | DB50 Spell Staff4 |
| `objet/38204//name` | garder_anglais | nom de travail technique des développeurs | DB38 Spell Wand2 |
| `objet/41911//name` | garder_anglais | nom de travail technique des développeurs | LK Honor 5 Caster DPS Bracers |
| `objet/42083//name` | garder_anglais | nom de travail technique des développeurs | LK Honor 5 Caster DPS Crit Cloak |
| `objet/44662//name` | garder_anglais | nom de travail technique des développeurs (« HEAL 25P ») | HEAL 25P Life-Binder's Locket |
| `objet/44831//name` | garder_anglais | langue murloc, intraduisible | Mmrgrg glm Nuubs |
| `objet/46325//name` | garder_anglais | nom de mascotte propre à CoA, gardé | Withers |
| `objet/46522//name` | garder_anglais | nom technique (apparence numérotée) | Descension Appearance 46522 |
| `objet/46523//name` | garder_anglais | nom technique (apparence numérotée) | Descension Appearance 46523 |
| `objet/46524//name` | garder_anglais | nom technique (apparence numérotée) | Descension Appearance 46524 |
| `objet/46525//name` | garder_anglais | nom technique (apparence numérotée) | Descension Appearance 46525 |
| `objet/46526//name` | garder_anglais | nom technique (apparence numérotée) | Descension Appearance 46526 |
| `objet/46527//name` | garder_anglais | nom technique (apparence numérotée) | Descension Appearance 46527 |
| `objet/46654//name` | garder_anglais | nom de mascotte propre à CoA, gardé | Quillby |
| `objet/46655//name` | garder_anglais | nom de mascotte propre à CoA, gardé | Quilliana |
| `objet/46656//name` | garder_anglais | nom de mascotte propre à CoA, gardé | Pricklepuff |
| `objet/46657//name` | garder_anglais | nom de mascotte propre à CoA, gardé | Quillbert |
| `objet/46659//name` | garder_anglais | nom de mascotte propre à CoA, gardé | Bouncer |
| `objet/46660//name` | garder_anglais | nom de mascotte propre à CoA, gardé | Jump Jump |
| `objet/46661//name` | garder_anglais | nom de mascotte propre à CoA, gardé | Fuzzy |
| `objet/46662//name` | garder_anglais | nom de mascotte propre à CoA, gardé | Fringe |
| `objet/46851//name` | garder_anglais | nom de mascotte en langage bébé (jeu de mots), intraduisible | Wittle Waptor |
| `objet/46853//name` | garder_anglais | nom en langage bébé (jeu de mots), intraduisible | Waptor Twap |
| `objet/49040//name` | garder_anglais | nom propre, identique en français | Jeeves |
| `objet/50733//description` | garder_anglais | langue thalassienne après l'étiquette, rien à traduire | @Ascended Raid@Thalas'din belore. |
| `objet/244831//name` | garder_anglais | langue murloc, intraduisible | Mmrgrg glm Nuubs |
| `objet/320416//name` | garder_anglais | nom de travail technique des développeurs | HF28 Cloth Spell Head4 |
| `objet/322771//name` | garder_anglais | nom de travail technique des développeurs | BT57 Fast Mace2 |
| `objet/327937//name` | garder_anglais | nom de travail technique des développeurs | DB50 Spell Staff4 |
| `objet/327939//name` | garder_anglais | nom de travail technique des développeurs | DB50 Spell Staff4 |
| `objet/328430//name` | garder_anglais | nom de travail technique des développeurs | DB38 Spell Wand2 |
| `objet/328432//name` | garder_anglais | nom de travail technique des développeurs | DB38 Spell Wand2 |
| `objet/344831//name` | garder_anglais | langue murloc, intraduisible | Mmrgrg glm Nuubs |
| `objet/352591//name` | garder_anglais | nom de travail technique des développeurs | LK Honor 5 Caster DPS Bracers |
| `objet/354272//name` | garder_anglais | nom de travail technique des développeurs | LK Honor 5 Caster DPS Crit Cloak |
| `objet/507330//description` | garder_anglais | langue thalassienne après l'étiquette, rien à traduire | @Ascended Raid@Thalas'din belore. |
| `objet/1344831//name` | garder_anglais | langue murloc, intraduisible | Mmrgrg glm Nuubs |

## objets / objets_004

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/54862//name` | garder_anglais | nom technique des développeurs | SquirrelGirl_1 |
| `objet/54863//name` | garder_anglais | nom technique des développeurs | SquirrelGirl_2 |
| `objet/54864//name` | garder_anglais | nom technique des développeurs | SquirrelGirl_3 |
| `objet/56910//name` | garder_anglais | nom technique des développeurs | Monster Axe 1H Cataclysm B02 Blue |
| `objet/56911//name` | garder_anglais | nom technique des développeurs | Monster Axe 1H Cataclysm B02 Green |
| `objet/56912//name` | garder_anglais | nom technique des développeurs | Monster Axe 1H Cataclysm B02 Red |

## objets / objets_005

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/57005//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Sword 1H Cataclysm B02 Blue |
| `objet/57006//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Sword 1H Cataclysm B02 Brown |
| `objet/57007//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Sword 1H Cataclysm B02 Purple |
| `objet/57008//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Sword 1H Cataclysm B02 Red |
| `objet/57009//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Axe 2H Cataclysm B01 Black |
| `objet/57011//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Axe 2H Cataclysm B02 Blue |
| `objet/57012//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Axe 2H Cataclysm B02 Brown |
| `objet/57013//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Axe 2H Cataclysm B02 Red |
| `objet/57014//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Axe 2H Cataclysm B01 Blue |
| `objet/57015//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Axe 2H Cataclysm B01 Green |
| `objet/57023//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Gun Cataclysm B01 Green |
| `objet/57024//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Gun Cataclysm B01 Silver |
| `objet/57027//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Polearm Cataclysm B01 Gold |
| `objet/57028//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Polearm Cataclysm B01 Purple |
| `objet/57029//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Polearm Cataclysm B01 Red |
| `objet/57030//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Polearm Cataclysm B02 Green |
| `objet/57031//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Polearm Cataclysm B02 Purple |
| `objet/57032//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Polearm Cataclysm B02 Red |
| `objet/57033//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Shield Cataclysm B01 Red |
| `objet/57038//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Sword 2H Cataclysm B01 Blue |
| `objet/57039//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Sword 2H Cataclysm B01 Brown |
| `objet/58173//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Gun Cataclysm B02 Brown |
| `objet/58174//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Gun Cataclysm B02 Green |
| `objet/58175//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Gun Cataclysm B02 Yellow |
| `objet/58470//name` | garder_anglais | nom technique des développeurs | Monster Staff Grimbatolraid D 01 |
| `objet/58794//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Bow Cataclysm B01 Blue |
| `objet/58795//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Bow Cataclysm B01 Brown |
| `objet/58796//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Bow Cataclysm B01 Yellow |
| `objet/58797//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Bow Cataclysm B02 Blue |
| `objet/58799//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Bow Cataclysm B02 Purple |
| `objet/58800//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Bow Cataclysm B02 Red |
| `objet/58801//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Bow Cataclysm B02 Yellow |
| `objet/58816//name` | garder_anglais | objet de test (QA), technique | Qa Test Finger 250 Hit |
| `objet/58817//name` | garder_anglais | objet de test (QA), technique | Qa Test Finger 500 Hit |
| `objet/58818//name` | garder_anglais | objet de test (QA), technique | Qa Test Finger 1000 Hit |
| `objet/58819//name` | garder_anglais | objet de test (QA), technique | Qa Test Finger 1500 Hit |
| `objet/58940//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Shield Cataclysm B02 Purple |
| `objet/58941//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Shield Cataclysm B02 White |
| `objet/58942//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Shield Cataclysm B02 Yellow |
| `objet/59563//name` | garder_anglais | nom en langage bébé (jeu de mots), intraduisible | Waptor Thwapper |
| `objet/59565//name` | garder_anglais | nom en langage bébé (jeu de mots), intraduisible | Waptor Scale Bweastpwate |

## objets / objets_006

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/60641//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Fist Cataclysm B02 Green |
| `objet/60642//name` | garder_anglais | nom technique des développeurs (« Monster … Cataclysm ») | Monster Fist Cataclysm B02 Red |

## objets / objets_007

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/60723//name` | doute | « Monnions » obscur (coquille de « Minions » ?) ; proposition : « Sbires de la compagnie Bravo » | Bravo Company Monnions |
| `objet/60968//name` | garder_anglais | nom technique des développeurs (« Monster … ») | Monster Sword 2H Bwdraid D01 |
| `objet/60969//name` | garder_anglais | nom technique des développeurs (« Monster … ») | Monster Sword 2H Grim Batol Raid D01 |
| `objet/60972//name` | garder_anglais | nom technique des développeurs (« Monster … ») | Monster Axe 2H Grim Batol Raid D01 |
| `objet/61295//name` | garder_anglais | nom technique des développeurs (« Monster … ») | Monster Item Ulduar Raid D03 Red offhand |
| `objet/61305//name` | garder_anglais | nom technique des développeurs (« Monster … ») | Monster Troll Polearm Drak Tharon D1 |
| `objet/62930//name` | garder_anglais | nom technique des développeurs (« Monster … ») | Monster Bow Cataclysm C 01 Green |

## objets / objets_008

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/68600//description` | garder_anglais | langue de C'Thun après l'étiquette, rien à traduire | @Ascended Raid@Uulwi gag erh'ongg w'ssht. |
| `objet/68702//name` | garder_anglais | jeu de mots sur « EVIdence » (évidence / EVI), intraduisible tel quel | Twilight EVIdence |
| `objet/72134//name` | doute | le nom « Grell Moss » ne correspond pas à la description (« Gregarious Grell ») : objet ou compagnon ? ; proposition : « Mousse de grell » | Grell Moss |

## objets / objets_009

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/79232//name` | garder_anglais | nom technique des développeurs (« Ardenweald Raid Offhand ») | Ardenweald Raid Offhand |
| `objet/80689//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Bassinet de Glass Lake » | Glass Lake Headcover |
| `objet/80692//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Heaume de Fox Grove » | Fox Grove Helm |
| `objet/80698//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Spallières de Glass Lake » | Glass Lake Spaulders |
| `objet/80701//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Spallières de Fox Grove » | Fox Grove Spaulders |
| `objet/80707//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Corselet de Glass Lake » | Glass Lake Chestguard |
| `objet/80710//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Armure de Fox Grove » | Fox Grove Armor |
| `objet/80716//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Cuissards de Glass Lake » | Glass Lake Legplates |
| `objet/80719//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Garde-jambes de Fox Grove » | Fox Grove Legguards |
| `objet/80725//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Grèves de Glass Lake » | Glass Lake Greaves |
| `objet/80728//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Solerets de Fox Grove » | Fox Grove Sabatons |
| `objet/80737//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Ceinture de Fox Grove » | Fox Grove Belt |
| `objet/80746//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Gantelets de Fox Grove » | Fox Grove Gauntlets |
| `objet/80752//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Brassards de Glass Lake » | Glass Lake Bracers |
| `objet/80755//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Garde-poignets de Fox Grove » | Fox Grove Wristguards |
| `objet/81960//name` | garder_anglais | nom technique (variante « Red-TopOnly ») | Robes of the Cycle (Red-TopOnly) |
| `objet/83878//name` | doute | gemme de Pandarie sans nom officiel dans la source (« Keen Tiger Opal ») ; proposition : « Dessin : Opale tigrée affûtée » | Design: Keen Tiger Opal |
| `objet/84249//name` | doute | lieu de Pandarie (« Glass Lake », « Fox Grove ») sans nom officiel dans la source ; proposition : « Garde-mains de Fox Grove » | Fox Grove Handguards |

## objets / objets_010

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/87986//name` | garder_anglais | nom technique (variante « Purple-TopOnly ») | Robes of the Betrayer (Purple-TopOnly) |
| `objet/87995//name` | garder_anglais | nom technique (variante « Red-TopOnly ») | Robes of the Betrayer (Red-TopOnly) |
| `objet/88692//name` | doute | lieu de Pandarie (« Fox Grove ») sans nom officiel dans la source ; proposition : « Brassards de Fox Grove » | Fox Grove Bracers |
| `objet/88798//name` | garder_anglais | nom technique (variante de couleur « DkMagenta ») | Kilrak, Jaws of Terror (DkMagenta) |
| `objet/92553//name` | garder_anglais | texte technique (« dupplicate appearance ») | dupplicate appearance |
| `objet/97330//name` | garder_anglais | nom propre de mascotte | Fix-o-Tron 5000 |
| `objet/97351//name` | garder_anglais | gabarit technique (« BUILD_NAME ») | Build Draft Deck: BUILD_NAME |
| `objet/97355//name` | doute | nom de build CoA et terme « Deck » sans décision ; à trancher avec l'interface des builds | Build Draft Deck: Scarlet Juggernaut (2H Tank) |
| `objet/97367//name` | doute | nom de build CoA et terme « Deck » sans décision ; à trancher avec l'interface des builds | Build Draft Deck: Fire Craft |
| `objet/97370//name` | doute | nom de build CoA et terme « Deck » sans décision ; à trancher avec l'interface des builds | Build Draft Deck: Booming Thunder |
| `objet/97377//name` | doute | nom de build CoA et terme « Deck » sans décision ; à trancher avec l'interface des builds | Build Draft Deck: Storm Blademaster (2H tank) |
| `objet/97766//name` | doute | « Build Card » (mécanique CoA des builds) sans décision ; proposition : « Carte de maître des builds » | Build Master's Card |

## objets / objets_011

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/98325//name` | doute | emplacement de l'objet inconnu : « Wraps » se traduit Cafetan (torse), Couvre-bras ou Protège-mains selon l'emplacement ; proposition : « Cafetan de néophyte bordeaux » | Burgundy Neophyte Wraps |
| `objet/98337//name` | doute | emplacement de l'objet inconnu : « Wraps » se traduit Cafetan (torse), Couvre-bras ou Protège-mains selon l'emplacement ; proposition : « Cafetan d'aspirant rustique » | Rustic Aspirant Wraps |
| `objet/99479//name` | doute | monture de Légion (Highmountain Elderhorn) sans nom officiel dans la source ; proposition : « Rênes de grand-corne de Haut-Roc » | Reins of the Highmountain Elderhorn |
| `objet/101400//name` | doute | terme CoA sans décision : Fel Power, monnaie d'amélioration de la classe Héros ; proposition : « Puissance gangrenée » | Fel Power |
| `objet/104310//name` | garder_anglais | objet de test des développeurs, technique | Jeremy's Test Item |
| `objet/168279//name` | garder_anglais | objet de test des développeurs, technique | Jeremy's Test Item |

## objets / objets_012

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/108598//name` | garder_anglais | objet de test des développeurs, technique | Maldo's Test Gun |
| `objet/109281//name` | garder_anglais | marque technique (« retired » : objet retiré) | retired |
| `objet/111023//name` | garder_anglais | objet de test des développeurs, technique | Paul's Test Item |
| `objet/111405//name` | garder_anglais | objet de test des développeurs, technique | Test Invisible Axe 002 |
| `objet/112574//name` | garder_anglais | objet de test des développeurs, technique | Test Weapon |
| `objet/112575//name` | garder_anglais | objet de test des développeurs, technique | Test Weapon |
| `objet/173752//name` | garder_anglais | objet de test des développeurs, technique | Test Weapon |
| `objet/3456432//name` | garder_anglais | objet de test des développeurs, technique | Test Weapon |

## objets / objets_013

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/118397//name` | garder_anglais | nom propre (latin), identique en français | Equus |
| `objet/120427//name` | garder_anglais | objet de test des développeurs, technique | Owen Test 2H Sword |
| `objet/122151//name` | garder_anglais | objet de test des développeurs, technique | Test Tier 2 Headmaster's Charge |
| `objet/127656//name` | doute | emplacement de l'objet inconnu : « Wraps » se traduit Cafetan (torse), Couvre-bras ou Protège-mains selon l'emplacement ; proposition : « Cafetan roussi par la gangrène » | Fel Singed Wraps |
| `objet/127857//name` | garder_anglais | nom propre (arme prodigieuse), identique en français | Aluneth |
| `objet/129305//name` | garder_anglais | objet marqué inutilisé (« Unused »), technique | Wildsky's Unused Helmet |
| `objet/129718//name` | garder_anglais | objet de test des développeurs, technique | Test Warglaive |
| `objet/129763//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129764//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129765//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129766//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129771//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129772//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129773//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129774//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129775//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129776//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129777//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129778//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129779//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129780//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129781//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129782//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129783//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129784//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129785//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129786//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129787//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129788//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129789//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129790//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129791//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129792//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129793//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129794//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129795//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129796//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129797//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129805//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129806//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129807//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129844//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129859//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/129887//name` | garder_anglais | marque technique (« Unused ») | Unused |
| `objet/131332//name` | doute | nom en langage bébé (jeu de mots), intraduisible | Waptor Tweads |

## objets / objets_014

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/132485//name` | garder_anglais | objet de test des développeurs, technique | Darren's Test DH Leather Chest |
| `objet/132707//name` | doute | nom technique (apparence numérotée) | Descension Appearance 132707 |
| `objet/132719//name` | doute | nom technique (apparence numérotée) | Descension Appearance 132719 |
| `objet/132822//name` | garder_anglais | objet de test des développeurs, technique | Doug Test - Axe |
| `objet/133327//name` | garder_anglais | objet de test des développeurs, technique | GBerger Test Glaive MH |
| `objet/134946//name` | garder_anglais | objet de test des développeurs, technique | test bow |
| `objet/135567//name` | garder_anglais | objet de test des développeurs, technique | Doug Test - Axe2 |
| `objet/136270//name` | garder_anglais | objet de test des développeurs, technique | Doug Test - Bow |
| `objet/136327//name` | garder_anglais | objet de test des développeurs, technique | Doug Test - Warglaive |
| `objet/136837//name` | garder_anglais | objet de test des développeurs, technique | Doug Test - Offhand Glaive |
| `objet/137013//name` | garder_anglais | objet de test des développeurs, technique | GBerger Test Glaive OH |
| `objet/137581//name` | garder_anglais | objet de test des développeurs, technique | Test Artifact 1 |
| `objet/137629//name` | garder_anglais | objet de test des développeurs, technique | Charles Test Plate Chest |
| `objet/142205//name` | doute | jeu de mots ou argot obscur (« Jabber Grookin' »), sens incertain | Jabber Grookin' Gauntlets |
| `objet/142299//name` | doute | argot obscur (« Horkin' »), sens incertain ; proposition : « Lance-trucs crachoteurs » | Horkin' Stuff-Lobbers |

## objets / objets_015

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/143766//name` | garder_anglais | objet de test des développeurs, technique | Bret Test |
| `objet/147902//name` | garder_anglais | objet de test des développeurs, technique | Transmog Set Test - Ranger's Chain of Unending Summer |
| `objet/150415//name` | doute | emplacement de l'objet inconnu : « Wraps » se traduit Cafetan (torse), Couvre-bras ou Protège-mains selon l'emplacement ; proposition : « Couvre-bras éperon-de-dragon » | Dragonspur Wraps |
| `objet/151105//name` | garder_anglais | objet de test des développeurs, technique | BDow's Test Shield |
| `objet/151827//name` | garder_anglais | objet de test des développeurs, technique | Serban Test Transmog |
| `objet/152189//name` | garder_anglais | nom de mascotte propre à CoA (jeu de mots), gardé | Pooftalon |
| `objet/152190//name` | garder_anglais | nom de mascotte propre à CoA (jeu de mots), gardé | Gooftalon |
| `objet/152230//name` | garder_anglais | objet de test des développeurs, technique | _JKL - Test Data |
| `objet/152502//name` | garder_anglais | objet de test des développeurs, technique | Darren's Test 7.3 Robe |
| `objet/153698//name` | garder_anglais | objet de test des développeurs, technique | _JKL - Junk Test |
| `objet/155658//name` | garder_anglais | objet de test des développeurs, technique | Bret Test 3 |
| `objet/156547//name` | garder_anglais | objet de test des développeurs, technique | Bret Test Monster Item |
| `objet/157557//name` | garder_anglais | objet de test des développeurs, technique | CWK Test Item |
| `objet/160697//name` | garder_anglais | objet de test des développeurs, technique | Darren's Test Priority Robes |
| `objet/160749//name` | garder_anglais | objet de test des développeurs, technique | Darren's Test Armor 2 Kilt |
| `objet/160903//name` | garder_anglais | objet de test des développeurs, technique | Darren's Test Priority Robes - arm upper hidden |
| `objet/170464//name` | garder_anglais | objet de test des développeurs, technique | CWK Test Item |
| `objet/217425//name` | doute | emplacement de l'objet inconnu : « Wraps » se traduit Cafetan (torse), Couvre-bras ou Protège-mains selon l'emplacement ; proposition : « Couvre-bras éperon-de-dragon » | Dragonspur Wraps |
| `objet/256146//name` | doute | emplacement de l'objet inconnu : « Wraps » se traduit Cafetan (torse), Couvre-bras ou Protège-mains selon l'emplacement ; proposition : « Couvre-bras éperon-de-dragon » | Dragonspur Wraps |
| `objet/317425//name` | doute | emplacement de l'objet inconnu : « Wraps » se traduit Cafetan (torse), Couvre-bras ou Protège-mains selon l'emplacement ; proposition : « Couvre-bras éperon-de-dragon » | Dragonspur Wraps |
| `objet/1317425//name` | doute | emplacement de l'objet inconnu : « Wraps » se traduit Cafetan (torse), Couvre-bras ou Protège-mains selon l'emplacement ; proposition : « Couvre-bras éperon-de-dragon » | Dragonspur Wraps |

## objets / objets_016

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/164255//name` | garder_anglais | objet de test des développeurs, technique | PRK Test |
| `objet/166546//name` | garder_anglais | objet de test des développeurs, technique | Darren's Test Timewalking Robes |
| `objet/168805//name` | garder_anglais | objet de test des développeurs, technique | MKelada Test Mace |
| `objet/169050//name` | garder_anglais | nom propre, identique en français | Logg |
| `objet/169476//name` | garder_anglais | objet de test des développeurs, technique | Valyri's Fire-Proof Bracers Test |
| `objet/171191//name` | garder_anglais | objet de test des développeurs, technique | Owen Test |
| `objet/171192//name` | garder_anglais | objet de test des développeurs, technique | Owen Test |
| `objet/172191//name` | garder_anglais | nom propre (langue de N'Zoth), identique en français | An'zig Vra |
| `objet/172196//name` | garder_anglais | nom propre (langue de N'Zoth), identique en français | Vorzz Yoq'al |
| `objet/173755//name` | garder_anglais | objet de test des développeurs, technique | Test Head |
| `objet/173758//name` | garder_anglais | objet de test des développeurs, technique | Test Shoulder |
| `objet/173763//name` | garder_anglais | objet de test des développeurs, technique | Test Chest |
| `objet/173765//name` | garder_anglais | objet de test des développeurs, technique | Test Wrist |
| `objet/173766//name` | garder_anglais | objet de test des développeurs, technique | Test Hand |
| `objet/173767//name` | garder_anglais | objet de test des développeurs, technique | Test Waist |
| `objet/173769//name` | garder_anglais | objet de test des développeurs, technique | Test Legs |
| `objet/173770//name` | garder_anglais | objet de test des développeurs, technique | Test Feet |
| `objet/173772//name` | garder_anglais | objet de test des développeurs, technique | Test Cloak |
| `objet/173904//name` | garder_anglais | objet de test des développeurs, technique | Test Shield |
| `objet/174453//name` | garder_anglais | objet de test des développeurs, technique | Paden's Test Item |
| `objet/175819//name` | garder_anglais | objet de test des développeurs, technique | Byron's Test Bracer |

## objets / objets_017

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet/176037//name` | garder_anglais | nom technique des développeurs (« Ardenweald Quest Shield »), comme « Ardenweald Raid Offhand » | Ardenweald Quest Shield |
| `objet/176333//name` | doute | sens ambigu : « Melody » peut être un nom propre ou « mélodie » ; proposition : « Rempart du défenseur de la mélodie » | Melody Defender's Bulwark |
| `objet/176399//name` | garder_anglais | objet de test des développeurs, technique | Bret Test Helm |
| `objet/176844//name` | garder_anglais | nom technique des développeurs (« Ardenweald Quest Staff »), comme « Ardenweald Raid Offhand » | Ardenweald Quest Staff |
| `objet/177567//name` | doute | nom de monture CoA (« Deathcycle », moto) sans forme établie ; proposition : « Clés de la motomort ravage-ciel » | Skyreaver Deathcycle's Keys |
| `objet/177568//name` | doute | nom de monture CoA (« Deathcycle », moto) sans forme établie ; proposition : « Clés de la motomort ravage-monde » | Worldreaver Deathcycle's Keys |
| `objet/177636//name` | doute | lieu de Shadowlands (« Sinfall », sanctuaire venthyr) sans français officiel vérifié (décision 23) ; proposition : « Bâton barbelé de légionnaire de Sinfall » | Sinfall Legionaire's Barbed Staff |
| `objet/177637//name` | doute | lieu de Shadowlands (« Sinfall ») sans français officiel vérifié (décision 23) ; proposition : « Arquebuse de Sinfall » | Sinfall Arquebus |
| `objet/177642//name` | doute | lieu de Shadowlands (« Sinfall ») sans français officiel vérifié (décision 23) ; proposition : « Lame noire de Sinfall » | Sinfall Darkblade |
| `objet/177643//name` | doute | lieu de Shadowlands (« Sinfall ») sans français officiel vérifié (décision 23) ; proposition : « Rapière de duelliste de Sinfall » | Sinfall Duelist's Rapier |
| `objet/177694//name` | garder_anglais | objet de test des développeurs, technique | Bret Test Quest - Uncommon Helm |
| `objet/177695//name` | garder_anglais | objet de test des développeurs, technique | Bret Test Quest - Rare Helm |
| `objet/177696//name` | garder_anglais | objet de test des développeurs, technique | Bret Test Quest - Epic Helm |
| `objet/177706//name` | garder_anglais | objet de test des développeurs, technique | Bret Test Quest - Uncommon Upgrade Helm |
| `objet/177729//name` | garder_anglais | nom technique des développeurs (« Ardenweald Covenant Offhand »), comme « Ardenweald Raid Offhand » | Ardenweald Covenant Offhand |
| `objet/177731//name` | garder_anglais | objet de test des développeurs, technique | Paden Test Armor |
| `objet/179381//name` | garder_anglais | objet de test des développeurs, technique | Non-Wand Shoot Test |
| `objet/179391//name` | garder_anglais | nom propre (épée de Shadowlands), identique en français | Remornia |
| `objet/179724//name` | garder_anglais | nom technique des développeurs (« Maw 2H Staff ») | Maw 2H Staff |
| `objet/181105//name` | doute | sens ambigu : « Haunting Maw » peut être l'Antre (Shadowlands) ou une créature ; proposition : « Trésors de l'Antre obsédant » | Haunting Maw's Treasures |
| `objet/181207//name` | doute | lieu de Shadowlands (« Dominance Keep ») sans français officiel vérifié (décision 23) ; proposition : « Barrière du donjon de la Domination » | Dominance Keep Barrier |
| `objet/181224//name` | doute | faction de Shadowlands (« the Avowed ») sans français officiel vérifié (décision 23) ; proposition : « Bâton d'arcaniste avoué » | Avowed Arcanist's Staff |
| `objet/181525//name` | garder_anglais | objet de test des développeurs, technique | Doug Test - Str Axe |
| `objet/181526//name` | garder_anglais | objet de test des développeurs, technique | Doug Test - Str Polearm |
| `objet/181527//name` | garder_anglais | objet de test des développeurs, technique | Doug Test - Str Sword |
| `objet/182105//name` | doute | sens ambigu : « Haunting Maw » peut être l'Antre (Shadowlands) ou une créature ; proposition : « Trésors de l'Antre obsédant » | Haunting Maw's Treasures |

## objets_monde / objets_monde_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet_monde/30//name` | garder_anglais | objet technique (focalisateur de sort), jamais vu sous ce nom | Dalaran Forge Spell Focus |
| `objet_monde/129//name` | garder_anglais | objet technique (piège de téléportation de Naxxramas) | Naxx Teleporter trap |
| `objet_monde/19097//name` | garder_anglais | nom officiel identique (Maraudon) | Maraudon |
| `objet_monde/19110//name` | garder_anglais | nom officiel identique (Gnomeregan, mal orthographié par CoA) | Gnomeragan |
| `objet_monde/19235//name` | garder_anglais | nom de modèle obscur de CoA (« Spidermane ») | Spidermane |

## objets_monde / objets_monde_002

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet_monde/19374//name` | doute | « Netherguard » sans forme officielle prouvée ; proposition : « Murs de la Garde-néant » | Netherguard Walls |
| `objet_monde/21653//name` | garder_anglais | marque technique (« unk ») | unk |
| `objet_monde/21654//name` | garder_anglais | marque technique (« unk ») | unk |
| `objet_monde/21655//name` | garder_anglais | marque technique (« unk ») | unk |
| `objet_monde/21656//name` | garder_anglais | marque technique (« unk ») | unk |
| `objet_monde/90605//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG PROP ») | Grunt Axe RPG PROP |
| `objet_monde/97392//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Mage Tower Floating Book RPG Prop |
| `objet_monde/97396//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Blue Rune Circle Large RPG Prop |
| `objet_monde/97403//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Human Inn Food Plate 4 RPG Prop |
| `objet_monde/97404//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Human Townhall Commander Shelf 3 RPG Prop |
| `objet_monde/97431//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Human Townhall Commander Desk 0 RPG Prop |
| `objet_monde/97437//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Ley Crystal RPG Prop |
| `objet_monde/97493//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Hellfire Supplies 5 RPG Prop |
| `objet_monde/97494//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Hellfire Supplies 6 RPG Prop |
| `objet_monde/97495//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Human Storehouse Cratestack 2 RPG Prop |
| `objet_monde/97496//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Hellfire Supplies 4 RPG Prop |
| `objet_monde/97499//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Rogue Lockpicking Junk 1 RPG Prop |
| `objet_monde/97502//name` | garder_anglais | accessoire technique de jeu de rôle (« RPG Prop ») | Rogue Poison Vial RPG Prop |
| `objet_monde/128972//name` | garder_anglais | objet technique (piège) | Shallow Grave TRAP |
| `objet_monde/151992//name` | garder_anglais | nom technique (« auctionhouse ») | auctionhouse |
| `objet_monde/176996//name` | garder_anglais | nom technique (« CavernDoor01 ») | CavernDoor01 |
| `objet_monde/177493//name` | garder_anglais | objet technique (piège) | Fire of Elune (Trap |
| `objet_monde/177529//name` | garder_anglais | objet technique (piège) | Altar of Elune (Trap |
| `objet_monde/178644//name` | garder_anglais | objet technique (piège) | Ryson's All Seeing Eye Trap |
| `objet_monde/179588//name` | garder_anglais | nom technique (« CavernDoor01 ») | CavernDoor01 |
| `objet_monde/179597//name` | garder_anglais | nom technique (« Meetingstone01 ») | Meetingstone01 |
| `objet_monde/180525//name` | garder_anglais | objet technique (piège) | Tonk Control Console Trap |

## objets_monde / objets_monde_003

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet_monde/181214//name` | garder_anglais | objet technique (générateur de bestioles) | Necropolis critter spawner |
| `objet_monde/181290//name` | garder_anglais | objet technique (piège) | Midsummer Bonfire Spawn Trap |
| `objet_monde/183282//name` | garder_anglais | objet technique (piège) | Infernaling Summoner Damage Trap |
| `objet_monde/184981//name` | garder_anglais | objet technique (piège) | Poodad Trap |
| `objet_monde/185305//name` | garder_anglais | objet technique (piège) | Fumper Trap |
| `objet_monde/186471//name` | garder_anglais | objet technique (piège) | Holiday - Brewfest - Dark Iron - Mug Trap |
| `objet_monde/188459//name` | garder_anglais | objet technique (piège) | Thor Modan Mole Machine Trap |
| `objet_monde/194645//name` | garder_anglais | objet technique (piège) | Stone Block Trap |
| `objet_monde/195061//name` | garder_anglais | objet technique (piège) | Glittering Shell Trap |
| `objet_monde/195304//name` | garder_anglais | objet technique (piège) | Stormforged Mole Machine Trap |
| `objet_monde/196829//name` | garder_anglais | objet technique (piège) | Living Ire Thyme Linked Trap |
| `objet_monde/200000//name` | garder_anglais | objet technique (zone personnalisée) | Fel Orc Encampment Custom Area |
| `objet_monde/202208//name` | garder_anglais | objet technique (piège) | Discarded Supplies (Trap |
| `objet_monde/202361//name` | garder_anglais | objet technique (visuel) | Rockin' Powder Visual |
| `objet_monde/203044//name` | garder_anglais | objet technique (piège) | Steamwheedle Supplies - Pirate Trap |
| `objet_monde/203971//name` | garder_anglais | objet technique (piège) | Prickly Pear Fruit Trap |
| `objet_monde/204289//name` | garder_anglais | objet technique (déclencheur de piège) | Rock Lobster Trap Activator |
| `objet_monde/204385//name` | garder_anglais | objet technique (déclencheur de piège) | Monstrous Clam Trap Activator |
| `objet_monde/204434//name` | garder_anglais | objet technique (piège) | Lime Crate Trap |
| `objet_monde/204968//name` | garder_anglais | objet technique (piège) | Glow Trap |
| `objet_monde/205547//name` | garder_anglais | objet technique (mine armée) | Stray Land Mine (Armed |
| `objet_monde/205581//name` | garder_anglais | objet technique (piège) | Suspended Starlight - TRAP |
| `objet_monde/206322//name` | garder_anglais | objet technique (piège) | Wild Black Dragon Egg Trap |
| `objet_monde/207418//name` | garder_anglais | objet technique (piège) | Chillwind Egg Trap |
| `objet_monde/208426//name` | garder_anglais | objet technique (piège) | Cinderweb Egg Sac - Spiderling Trap |
| `objet_monde/208596//name` | garder_anglais | objet technique (piège) | Flame Druid Idol Trap |
| `objet_monde/209282//name` | garder_anglais | objet technique (piège) | Paper Pile Trap |
| `objet_monde/210339//name` | garder_anglais | objet technique (piège) | Ahn'Qiraj Sand Trap |
| `objet_monde/210946//name` | garder_anglais | objet technique (piège) | Mite Trap |
| `objet_monde/212348//name` | garder_anglais | objet technique (déclencheur) | Ancient Haunt Trigger |
| `objet_monde/213351//name` | garder_anglais | objet technique (piège) | Lushroom Linked Trap |
| `objet_monde/244605//name` | garder_anglais | objet technique (piège) | Underbelly Hoard Trap |
| `objet_monde/300077//name` | garder_anglais | objet temporaire de CoA (« TEMP ») | TEMP Windyreed Hut |
| `objet_monde/300085//name` | garder_anglais | objet temporaire de CoA (« TEMP ») | TEMP Legion Antenna |
| `objet_monde/1326662//name` | garder_anglais | objet technique (brasero décoratif) | Druids of the flame- Root Brazier 2 (Tall Burning) |
| `objet_monde/2300625//name` | garder_anglais | objet technique (effet visuel de rune) | Rune FX 01 |
| `objet_monde/2300626//name` | garder_anglais | objet technique (effet visuel de rune) | Rune FX 02 |
| `objet_monde/2300627//name` | garder_anglais | objet technique (effet visuel de rune) | Rune FX 03 |
| `objet_monde/2300628//name` | garder_anglais | objet technique (effet visuel de rune) | Rune FX 04 |

## objets_monde / objets_monde_004

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `objet_monde/2310444//name` | garder_anglais | objet technique (barrière de donjon) | templeofembers 1st boss barrier |
| `objet_monde/2310445//name` | garder_anglais | objet technique (porte de donjon) | templeofembers 1st boss door |
| `objet_monde/2310461//name` | garder_anglais | objet technique (« SWS door ») | SWS door |
| `objet_monde/9000149//name` | doute | « Dark Whisper Gorge » sans forme officielle prouvée ; proposition : « Faille gangrenée : Gorge du Sombre murmure » | Fel Rift: Dark Whisper Gorge |

## pages_courriers / pages_courriers_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `page/5011//Text` | doute | signature « Norman Goldshire » : nom de PNJ CoA (créature 50287) dont le nom de famille est aussi le lieu officiel Goldshire = Comté-de-l'Or ; le contrôle refuse l'anglais ; garder « Norman Goldshire » ou écrire « Norman Comté-de-l'Or » ? Traduction prête avec « Goldshire » : « Salut, $N ! Si vous lisez ceci, c'est que le bricolage vous démange, et y a qu'un remède : bricoler encore plus.$B$BDes engrenages, des ressorts, une pincée de poudre explosive et une bonne dose d'entêtement : c'est tout ce qu'il faut à un bricoleur. Enfin, ça, et quelqu'un sur qui tester les prototypes. Vous en faites pas, la plupart explosent pas.$B$BVenez me trouver près des chariots à l'ouest de l'Abbaye de Comté-du-Nord. Apportez vos propres lunettes.$B$B-Norman Goldshire, maître des bricoleurs » | Howdy, $N! If you're reading this, you've got the tinkerin' itch, and there's only one cure: more tinkerin'.$B$BGears, springs, a pinch of blasting powder and a |

## quetes / quetes_053

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `quete/11934//QuestCompletionLog` | garder_anglais | quête de test [PH] de Blizzard (Île des concepteurs), texte technique passé au travers | Return to Jonathan LeCraft in Designer Island. |
| `quete/11934//QuestDescription` | garder_anglais | quête de test [PH] de Blizzard (Île des concepteurs), texte technique passé au travers | Today you unlock a page in your spellbook, one you may not have realized it was there.  Bring me something, and I'll open it up for you. |
| `quete/12179//LogDescription` | garder_anglais | quête de test [PH] de Blizzard (Specialization 1, Jonathan LeCraft), texte technique passé au travers | LOG: Complete this quest for Specialization 1. |
| `quete/12179//QuestDescription` | garder_anglais | quête de test [PH] de Blizzard (Specialization 1, Jonathan LeCraft), texte technique passé au travers | DESCRIPTION: Complete this quest for Specialization 1. |

## quetes / quetes_055

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `quete/12911//ObjectiveText1` | garder_anglais | quête de test interne (« Kill Credit Test »), texte technique passé au travers | Working |

## quetes / quetes_060

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `quete/25055//LogDescription` | garder_anglais | texte provisoire « [ph] » de Blizzard (bouche-trou), rien à traduire | [ph] log description |
| `quete/25055//QuestDescription` | garder_anglais | texte provisoire « [ph] » de Blizzard (bouche-trou), rien à traduire | [ph] I'll give you a sack of shaman stuff.  Use the elemental sapta to enter the spirit and use the totem on the Agitated Earth Elementals. |
| `quete/25092//LogDescription` | garder_anglais | texte provisoire « [ph] » de Blizzard (bouche-trou), rien à traduire | [ph] log description |
| `quete/25092//QuestDescription` | garder_anglais | texte provisoire « [ph] » de Blizzard (bouche-trou), rien à traduire | [ph] I'll give you a sack of shaman stuff.  Use the elemental sapta to enter the spirit and use the totem on the Agitated Fire Elementals. |

## quetes / quetes_061

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `quete/49985//LogDescription` | doute | nom de PNJ CoA « Norman Goldshire » (gardé en anglais au chantier des créatures) : le contrôle exige Comté-de-l'or pour « Goldshire » (faux positif, c'est un nom de famille) ; traduction proposée : Lisez le Manuel d'ingénierie et allez trouver Norman Goldshire dans la Vallée de Comté-du-nord. | Read the Engineering Manual and seek out Norman Goldshire in Northshire Valley. |
| `quete/49985//ObjectiveText1` | doute | nom de PNJ CoA « Norman Goldshire » (gardé en anglais au chantier des créatures) : le contrôle exige Comté-de-l'or pour « Goldshire » (faux positif, c'est un nom de famille) ; traduction proposée : Lisez le Manuel d'ingénierie et allez trouver Norman Goldshire dans la Vallée de Comté-du-nord. | Read the Engineering Manual and seek out Norman Goldshire in Northshire Valley. |
| `quete/49985//QuestCompletionLog` | doute | nom de PNJ CoA « Norman Goldshire » (gardé en anglais au chantier des créatures) : le contrôle exige Comté-de-l'or pour « Goldshire » (faux positif, c'est un nom de famille) ; traduction proposée : Allez trouver Norman Goldshire dans la Vallée de Comté-du-nord. | Seek out Norman Goldshire in Northshire Valley. |

## rencontres_donjon / rencontres_donjon_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `rencontre_donjon/120//name` | garder_anglais | nom propre, rien à traduire | Vex'tal |
| `rencontre_donjon/122//name` | garder_anglais | nom propre, rien à traduire | Zul'garok |
| `rencontre_donjon/124//name` | garder_anglais | nom propre, rien à traduire | Korrim Snowgrave (PvE) |
| `rencontre_donjon/125//name` | garder_anglais | nom propre, rien à traduire | Korrim Snowgrave (PvE) |
| `rencontre_donjon/126//name` | garder_anglais | nom propre, rien à traduire | Korrim Snowgrave (PvE) |
| `rencontre_donjon/127//name` | garder_anglais | nom propre, rien à traduire | Korrim Snowgrave (PvE) |
| `rencontre_donjon/149//name` | doute | Spirestone : nom officiel introuvable ; proposition « Seigneur magus de Pierre-du-pic » | Spirestone Lord Magus |
| `rencontre_donjon/150//name` | doute | Spirestone : nom officiel introuvable ; proposition « Seigneur de bataille de Pierre-du-pic » | Spirestone Battle Lord |
| `rencontre_donjon/151//name` | doute | Spirestone : nom officiel introuvable ; proposition « Boucher de Pierre-du-pic » | Spirestone Butcher |
| `rencontre_donjon/152//name` | doute | Stonespine : nom officiel introuvable (boss rare de Strathholme) ; proposition « Échine-de-pierre » | Stonespine |
| `rencontre_donjon/153//name` | garder_anglais | nom propre, rien à traduire | Fras Siabi |
| `rencontre_donjon/154//name` | garder_anglais | nom propre, rien à traduire | Skul |
| `rencontre_donjon/155//name` | garder_anglais | nom propre, rien à traduire | Isalien |
| `rencontre_donjon/157//name` | garder_anglais | nom propre, rien à traduire | Tsu'zee |
| `rencontre_donjon/880//name` | garder_anglais | nom propre, rien à traduire | Setis (PvE) |
| `rencontre_donjon/881//name` | garder_anglais | nom propre, rien à traduire | Setis (PvE) |
| `rencontre_donjon/882//name` | garder_anglais | nom propre, rien à traduire | Setis (PvE) |
| `rencontre_donjon/884//name` | garder_anglais | nom propre, rien à traduire | Setis (PvE) |
| `rencontre_donjon/885//name` | garder_anglais | nom propre, rien à traduire | Azuregos (PvE) |
| `rencontre_donjon/886//name` | garder_anglais | nom propre, rien à traduire | Azuregos (PvE) |
| `rencontre_donjon/887//name` | garder_anglais | nom propre, rien à traduire | Azuregos (PvE) |
| `rencontre_donjon/889//name` | garder_anglais | nom propre, rien à traduire | Azuregos (PvE) |
| `rencontre_donjon/901//name` | garder_anglais | nom propre, rien à traduire | Kazzak (PvE) |
| `rencontre_donjon/902//name` | garder_anglais | nom propre, rien à traduire | Kazzak (PvE) |
| `rencontre_donjon/903//name` | garder_anglais | nom propre, rien à traduire | Kazzak (PvE) |
| `rencontre_donjon/905//name` | garder_anglais | nom propre, rien à traduire | Kazzak (PvE) |
| `rencontre_donjon/906//name` | garder_anglais | nom propre, rien à traduire | Will of Soggoth (PvE) |
| `rencontre_donjon/907//name` | garder_anglais | nom propre, rien à traduire | Will of Soggoth (PvE) |
| `rencontre_donjon/908//name` | garder_anglais | nom propre, rien à traduire | Will of Soggoth (PvE) |
| `rencontre_donjon/910//name` | garder_anglais | nom propre, rien à traduire | Will of Soggoth (PvE) |
| `rencontre_donjon/973//name` | garder_anglais | nom propre, rien à traduire | Emeriss (PvE) |
| `rencontre_donjon/974//name` | garder_anglais | nom propre, rien à traduire | Emeriss (PvE) |
| `rencontre_donjon/975//name` | garder_anglais | nom propre, rien à traduire | Emeriss (PvE) |
| `rencontre_donjon/976//name` | garder_anglais | nom propre, rien à traduire | Emeriss (PvE) |
| `rencontre_donjon/980//name` | garder_anglais | nom propre, rien à traduire | Kormok |
| `rencontre_donjon/981//name` | garder_anglais | nom propre, rien à traduire | Hyakiss |
| `rencontre_donjon/982//name` | garder_anglais | nom propre, rien à traduire | Shadikith |
| `rencontre_donjon/983//name` | garder_anglais | nom propre, rien à traduire | Rokad |
| `rencontre_donjon/986//name` | garder_anglais | nom propre, rien à traduire | Taerar (PvE) |
| `rencontre_donjon/987//name` | garder_anglais | nom propre, rien à traduire | Taerar (PvE) |
| `rencontre_donjon/988//name` | garder_anglais | nom propre, rien à traduire | Taerar (PvE) |
| `rencontre_donjon/989//name` | garder_anglais | nom propre, rien à traduire | Taerar (PvE) |
| `rencontre_donjon/990//name` | garder_anglais | nom propre, rien à traduire | Ysondre (PvE) |
| `rencontre_donjon/991//name` | garder_anglais | nom propre, rien à traduire | Ysondre (PvE) |
| `rencontre_donjon/992//name` | garder_anglais | nom propre, rien à traduire | Ysondre (PvE) |
| `rencontre_donjon/993//name` | garder_anglais | nom propre, rien à traduire | Ysondre (PvE) |
| `rencontre_donjon/994//name` | garder_anglais | nom propre, rien à traduire | Lethon (PvE) |
| `rencontre_donjon/995//name` | garder_anglais | nom propre, rien à traduire | Lethon (PvE) |
| `rencontre_donjon/996//name` | garder_anglais | nom propre, rien à traduire | Lethon (PvE) |
| `rencontre_donjon/997//name` | garder_anglais | nom propre, rien à traduire | Lethon (PvE) |
| `rencontre_donjon/1006//name` | garder_anglais | nom propre, rien à traduire | Raijuu |
| `rencontre_donjon/1010//name` | garder_anglais | nom propre, rien à traduire | Varedis |
| `rencontre_donjon/1012//name` | garder_anglais | nom propre, rien à traduire | Sironas  |
| `rencontre_donjon/1120//name` | garder_anglais | nom propre, rien à traduire | Vex'tal |
| `rencontre_donjon/1122//name` | garder_anglais | nom propre, rien à traduire | Zul'garok |
| `rencontre_donjon/1149//name` | doute | Spirestone : nom officiel introuvable ; proposition « Seigneur magus de Pierre-du-pic » | Spirestone Lord Magus |
| `rencontre_donjon/1150//name` | doute | Spirestone : nom officiel introuvable ; proposition « Seigneur de bataille de Pierre-du-pic » | Spirestone Battle Lord |
| `rencontre_donjon/1151//name` | doute | Spirestone : nom officiel introuvable ; proposition « Boucher de Pierre-du-pic » | Spirestone Butcher |
| `rencontre_donjon/1152//name` | doute | Stonespine : nom officiel introuvable (boss rare de Strathholme) ; proposition « Échine-de-pierre » | Stonespine |
| `rencontre_donjon/1153//name` | garder_anglais | nom propre, rien à traduire | Fras Siabi |
| `rencontre_donjon/1154//name` | garder_anglais | nom propre, rien à traduire | Skul |
| `rencontre_donjon/1155//name` | garder_anglais | nom propre, rien à traduire | Isalien |
| `rencontre_donjon/1157//name` | garder_anglais | nom propre, rien à traduire | Tsu'zee |
| `rencontre_donjon/1254//name` | garder_anglais | nom propre, rien à traduire | Raijuu |
| `rencontre_donjon/1257//name` | garder_anglais | nom propre, rien à traduire | Varedis |
| `rencontre_donjon/1980//name` | garder_anglais | nom propre, rien à traduire | Kormok |
| `rencontre_donjon/1981//name` | garder_anglais | nom propre, rien à traduire | Hyakiss |
| `rencontre_donjon/1982//name` | garder_anglais | nom propre, rien à traduire | Shadikith |
| `rencontre_donjon/1983//name` | garder_anglais | nom propre, rien à traduire | Rokad |
| `rencontre_donjon/2120//name` | garder_anglais | nom propre, rien à traduire | Vex'tal |
| `rencontre_donjon/2122//name` | garder_anglais | nom propre, rien à traduire | Zul'garok |
| `rencontre_donjon/2149//name` | doute | Spirestone : nom officiel introuvable ; proposition « Seigneur magus de Pierre-du-pic » | Spirestone Lord Magus |
| `rencontre_donjon/2150//name` | doute | Spirestone : nom officiel introuvable ; proposition « Seigneur de bataille de Pierre-du-pic » | Spirestone Battle Lord |
| `rencontre_donjon/2151//name` | doute | Spirestone : nom officiel introuvable ; proposition « Boucher de Pierre-du-pic » | Spirestone Butcher |
| `rencontre_donjon/2152//name` | doute | Stonespine : nom officiel introuvable (boss rare de Strathholme) ; proposition « Échine-de-pierre » | Stonespine |
| `rencontre_donjon/2153//name` | garder_anglais | nom propre, rien à traduire | Fras Siabi |
| `rencontre_donjon/2154//name` | garder_anglais | nom propre, rien à traduire | Skul |
| `rencontre_donjon/2157//name` | garder_anglais | nom propre, rien à traduire | Tsu'zee |
| `rencontre_donjon/2168//name` | garder_anglais | nom propre, rien à traduire | Alva |
| `rencontre_donjon/2169//name` | garder_anglais | nom propre, rien à traduire | Alva |
| `rencontre_donjon/2170//name` | garder_anglais | nom propre, rien à traduire | Alva |
| `rencontre_donjon/2611//name` | garder_anglais | nom propre, rien à traduire | Veng |
| `rencontre_donjon/2612//name` | garder_anglais | nom propre, rien à traduire | Maraudos |
| `rencontre_donjon/2613//name` | garder_anglais | nom propre, rien à traduire | Zerillis |
| `rencontre_donjon/2980//name` | garder_anglais | nom propre, rien à traduire | Kormok |
| `rencontre_donjon/2985//name` | garder_anglais | nom propre, rien à traduire | Anub'shiah |
| `rencontre_donjon/3321//name` | garder_anglais | nom propre, rien à traduire | Mutanus |
| `rencontre_donjon/3981//name` | garder_anglais | nom propre, rien à traduire | Hyakiss |
| `rencontre_donjon/3982//name` | garder_anglais | nom propre, rien à traduire | Shadikith |
| `rencontre_donjon/3983//name` | garder_anglais | nom propre, rien à traduire | Rokad |
| `rencontre_donjon/4981//name` | garder_anglais | nom propre, rien à traduire | Hyakiss |
| `rencontre_donjon/4982//name` | garder_anglais | nom propre, rien à traduire | Shadikith |
| `rencontre_donjon/4983//name` | garder_anglais | nom propre, rien à traduire | Rokad |
| `rencontre_donjon/4985//name` | garder_anglais | nom propre, rien à traduire | Gath'Ilzogg |
| `rencontre_donjon/4986//name` | garder_anglais | nom propre, rien à traduire | Gath'Ilzogg |
| `rencontre_donjon/4987//name` | garder_anglais | nom propre, rien à traduire | Gath'Ilzogg |
| `rencontre_donjon/5018//name` | garder_anglais | nom propre, rien à traduire | Marisa du'Paige |
| `rencontre_donjon/5019//name` | garder_anglais | nom propre, rien à traduire | Marisa du'Paige |
| `rencontre_donjon/5020//name` | garder_anglais | nom propre, rien à traduire | Marisa du'Paige |
| `rencontre_donjon/5024//name` | garder_anglais | nom propre, rien à traduire | Ilifar |
| `rencontre_donjon/5025//name` | garder_anglais | nom propre, rien à traduire | Ilifar |
| `rencontre_donjon/5026//name` | garder_anglais | nom propre, rien à traduire | Ilifar |
| `rencontre_donjon/5027//name` | garder_anglais | nom propre, rien à traduire | Felcular |
| `rencontre_donjon/5028//name` | garder_anglais | nom propre, rien à traduire | Felcular |
| `rencontre_donjon/5029//name` | garder_anglais | nom propre, rien à traduire | Felcular |
| `rencontre_donjon/5042//name` | garder_anglais | nom propre, rien à traduire | Vai Sakir |
| `rencontre_donjon/5043//name` | garder_anglais | nom propre, rien à traduire | Vai Sakir |
| `rencontre_donjon/5044//name` | garder_anglais | nom propre, rien à traduire | Vai Sakir |
| `rencontre_donjon/5066//name` | garder_anglais | nom propre, rien à traduire | Njernthir |
| `rencontre_donjon/5067//name` | garder_anglais | nom propre, rien à traduire | Njernthir |
| `rencontre_donjon/5068//name` | garder_anglais | nom propre, rien à traduire | Njernthir |
| `rencontre_donjon/5075//name` | garder_anglais | nom propre, rien à traduire | Iorian |
| `rencontre_donjon/5076//name` | garder_anglais | nom propre, rien à traduire | Iorian |
| `rencontre_donjon/5077//name` | garder_anglais | nom propre, rien à traduire | Iorian |
| `rencontre_donjon/5078//name` | garder_anglais | nom propre, rien à traduire | Kolmos |
| `rencontre_donjon/5079//name` | garder_anglais | nom propre, rien à traduire | Kolmos |
| `rencontre_donjon/5080//name` | garder_anglais | nom propre, rien à traduire | Kolmos |
| `rencontre_donjon/5081//name` | garder_anglais | nom propre, rien à traduire | Solfir |
| `rencontre_donjon/5082//name` | garder_anglais | nom propre, rien à traduire | Solfir |
| `rencontre_donjon/5083//name` | garder_anglais | nom propre, rien à traduire | Solfir |
| `rencontre_donjon/5096//name` | garder_anglais | nom propre, rien à traduire | Cynfael |
| `rencontre_donjon/5097//name` | garder_anglais | nom propre, rien à traduire | Cynfael |
| `rencontre_donjon/5098//name` | garder_anglais | nom propre, rien à traduire | Cynfael |
| `rencontre_donjon/5105//name` | garder_anglais | nom propre, rien à traduire | Dryn Miel |
| `rencontre_donjon/5106//name` | garder_anglais | nom propre, rien à traduire | Dryn Miel |
| `rencontre_donjon/5107//name` | garder_anglais | nom propre, rien à traduire | Dryn Miel |
| `rencontre_donjon/5108//name` | garder_anglais | nom propre, rien à traduire | Takan Velor |
| `rencontre_donjon/5109//name` | garder_anglais | nom propre, rien à traduire | Takan Velor |
| `rencontre_donjon/5110//name` | garder_anglais | nom propre, rien à traduire | Takan Velor |
| `rencontre_donjon/5111//name` | garder_anglais | nom propre, rien à traduire | Dryn Miel |
| `rencontre_donjon/5112//name` | garder_anglais | nom propre, rien à traduire | Dryn Miel |
| `rencontre_donjon/5113//name` | garder_anglais | nom propre, rien à traduire | Dryn Miel |
| `rencontre_donjon/6666//name` | garder_anglais | nom propre, rien à traduire | Gorshok |
| `rencontre_donjon/6669//name` | garder_anglais | nom propre, rien à traduire | Morana |
| `rencontre_donjon/6670//name` | garder_anglais | nom propre, rien à traduire | Varra |
| `rencontre_donjon/6678//name` | garder_anglais | nom propre, rien à traduire | Gorshok |
| `rencontre_donjon/6681//name` | garder_anglais | nom propre, rien à traduire | Morana |
| `rencontre_donjon/6682//name` | garder_anglais | nom propre, rien à traduire | Varra |
| `rencontre_donjon/6690//name` | garder_anglais | nom propre, rien à traduire | Gorshok |
| `rencontre_donjon/6693//name` | garder_anglais | nom propre, rien à traduire | Morana |
| `rencontre_donjon/6694//name` | garder_anglais | nom propre, rien à traduire | Varra |
| `rencontre_donjon/9012//name` | garder_anglais | nom propre, rien à traduire | Mechatron |
| `rencontre_donjon/9013//name` | garder_anglais | nom propre, rien à traduire | Mechatron |
| `rencontre_donjon/9014//name` | garder_anglais | nom propre, rien à traduire | Mechatron |
| `rencontre_donjon/9072//name` | garder_anglais | nom propre, rien à traduire | Arynyes |
| `rencontre_donjon/9073//name` | garder_anglais | nom propre, rien à traduire | Basalthane |
| `rencontre_donjon/9074//name` | garder_anglais | nom propre, rien à traduire | Basalthane |
| `rencontre_donjon/9075//name` | garder_anglais | nom propre, rien à traduire | Basalthane |
| `rencontre_donjon/9076//name` | garder_anglais | nom propre, rien à traduire | Basalthane |
| `rencontre_donjon/9167//name` | garder_anglais | nom propre, rien à traduire | Arynyes |
| `rencontre_donjon/9262//name` | garder_anglais | nom propre, rien à traduire | Arynyes |
| `rencontre_donjon/9357//name` | garder_anglais | nom propre, rien à traduire | Arynyes |
| `rencontre_donjon/10000//name` | garder_anglais | nom propre, rien à traduire | Emeriss (PvE) |
| `rencontre_donjon/10001//name` | garder_anglais | nom propre, rien à traduire | Taerar (PvE) |
| `rencontre_donjon/10002//name` | garder_anglais | nom propre, rien à traduire | Ysondre (PvE) |
| `rencontre_donjon/10003//name` | garder_anglais | nom propre, rien à traduire | Lethon (PvE) |
| `rencontre_donjon/10006//name` | garder_anglais | nom propre, rien à traduire | Azuregos (PvE) |
| `rencontre_donjon/10010//name` | garder_anglais | nom propre, rien à traduire | Atal'Zul (PvE) |
| `rencontre_donjon/11000//name` | garder_anglais | nom propre, rien à traduire | Emeriss (PvE) |
| `rencontre_donjon/11001//name` | garder_anglais | nom propre, rien à traduire | Taerar (PvE) |
| `rencontre_donjon/11002//name` | garder_anglais | nom propre, rien à traduire | Ysondre (PvE) |
| `rencontre_donjon/11003//name` | garder_anglais | nom propre, rien à traduire | Lethon (PvE) |
| `rencontre_donjon/11006//name` | garder_anglais | nom propre, rien à traduire | Azuregos (PvE) |
| `rencontre_donjon/11010//name` | garder_anglais | nom propre, rien à traduire | Atal'Zul (PvE) |
| `rencontre_donjon/12000//name` | garder_anglais | nom propre, rien à traduire | Emeriss (PvE) |
| `rencontre_donjon/12001//name` | garder_anglais | nom propre, rien à traduire | Taerar (PvE) |
| `rencontre_donjon/12002//name` | garder_anglais | nom propre, rien à traduire | Ysondre (PvE) |
| `rencontre_donjon/12003//name` | garder_anglais | nom propre, rien à traduire | Lethon (PvE) |
| `rencontre_donjon/12006//name` | garder_anglais | nom propre, rien à traduire | Azuregos (PvE) |
| `rencontre_donjon/12010//name` | garder_anglais | nom propre, rien à traduire | Atal'Zul (PvE) |
| `rencontre_donjon/13000//name` | garder_anglais | nom propre, rien à traduire | Emeriss (PvE) |
| `rencontre_donjon/13001//name` | garder_anglais | nom propre, rien à traduire | Taerar (PvE) |
| `rencontre_donjon/13002//name` | garder_anglais | nom propre, rien à traduire | Ysondre (PvE) |
| `rencontre_donjon/13003//name` | garder_anglais | nom propre, rien à traduire | Lethon (PvE) |
| `rencontre_donjon/13006//name` | garder_anglais | nom propre, rien à traduire | Azuregos (PvE) |
| `rencontre_donjon/13010//name` | garder_anglais | nom propre, rien à traduire | Atal'Zul (PvE) |
| `rencontre_donjon/14012//name` | garder_anglais | nom propre, rien à traduire | Xarthos |
| `rencontre_donjon/14013//name` | garder_anglais | nom propre, rien à traduire | Xarthos |
| `rencontre_donjon/14014//name` | garder_anglais | nom propre, rien à traduire | Xarthos |
| `rencontre_donjon/14015//name` | garder_anglais | nom propre, rien à traduire | Xarthos |

## sorts_standard / sorts_standard_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/136//Description` | doute | majoritairement anglais à cause des longues étiquettes @ext@ gardées en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d. » + étiquettes telles quelles | Heals your Tamed Pet for $<total> health over $d.  @ext:This ability is usable while shapeshifted.:ext@  @ext:Tamed Pet includes Summoned Demon, Enslave Demon,  |

## sorts_standard / sorts_standard_002

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/3111//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d.\n\nCette technique est utilisable en étant transformé. » + étiquette telle quelle | Heals your Tamed Pet for $<total> health over $d.  This ability is usable while shapeshifted.  @ext:Tamed Pet includes Summoned Demon, Enslave Demon, Dominate U |
| `sort/3661//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d.\n\nCette technique est utilisable en étant transformé. » + étiquette telle quelle | Heals your Tamed Pet for $<total> health over $d.  This ability is usable while shapeshifted.  @ext:Tamed Pet includes Summoned Demon, Enslave Demon, Dominate U |
| `sort/3662//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d.\n\nCette technique est utilisable en étant transformé. » + étiquette telle quelle | Heals your Tamed Pet for $<total> health over $d.  This ability is usable while shapeshifted.  @ext:Tamed Pet includes Summoned Demon, Enslave Demon, Dominate U |
| `sort/13542//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d.\n\nCette technique est utilisable en étant transformé. » + étiquette telle quelle | Heals your Tamed Pet for $<total> health over $d.  This ability is usable while shapeshifted.  @ext:Tamed Pet includes Summoned Demon, Enslave Demon, Dominate U |
| `sort/13543//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d.\n\nCette technique est utilisable en étant transformé. » + étiquette telle quelle | Heals your Tamed Pet for $<total> health over $d.  This ability is usable while shapeshifted.  @ext:Tamed Pet includes Summoned Demon, Enslave Demon, Dominate U |
| `sort/13544//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d.\n\nCette technique est utilisable en étant transformé. » + étiquette telle quelle | Heals your Tamed Pet for $<total> health over $d.  This ability is usable while shapeshifted.  @ext:Tamed Pet includes Summoned Demon, Enslave Demon, Dominate U |
| `sort/27046//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d.\n\nCette technique est utilisable en étant transformé. » + étiquette telle quelle | Heals your Tamed Pet for $<total> health over $d.  This ability is usable while shapeshifted.  @ext:Tamed Pet includes Summoned Demon, Enslave Demon, Dominate U |
| `sort/48989//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d.\n\nCette technique est utilisable en étant transformé. » + étiquette telle quelle | Heals your Tamed Pet for $<total> health over $d.  This ability is usable while shapeshifted.  @ext:Tamed Pet includes Summoned Demon, Enslave Demon, Dominate U |
| `sort/48990//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Rend à votre familier apprivoisé $<total> points de vie en $d.\n\nCette technique est utilisable en étant transformé. » + étiquette telle quelle | Heals your Tamed Pet for $<total> health over $d.  This ability is usable while shapeshifted.  @ext:Tamed Pet includes Summoned Demon, Enslave Demon, Dominate U |

## sorts_standard / sorts_standard_005

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/11180//Description` | doute | conflit : l'étiquette @ext@ (à recopier telle quelle) contient « Frozen Orb », que le contrôle exige en « Orbe gelé » ; texte prêt sinon (« Augmente vos chances de coup critique de $s2%. … Cumulable jusqu'à $12579u fois. » + étiquette) | Increases your critical strike chance by $s2%.   Direct Frost damage has a $h% chance to apply the Winter's Chill effect, increasing the chance spells will cr |

## sorts_standard / sorts_standard_010

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/16332//Name` | garder_anglais | marqueur de développement CoA (« ASDF FOUND IT ») devant un nom officiel : texte technique, à laisser tel quel | ASDF FOUND IT Divine Touch of Vaelastrasz |
| `sort/16354//Name` | garder_anglais | marqueur de développement CoA (« ASDF FOUND IT ») : texte technique, à laisser tel quel | ASDF FOUND IT Vaelastrasz Spawn |
| `sort/16421//Name` | garder_anglais | marqueur de développement CoA (« ASDF FOUND IT ») : texte technique, à laisser tel quel | ASDF FOUND IT Vaelastrasz Dragon Form |

## sorts_standard / sorts_standard_011

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/17877//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Frappe instantanément la cible et lui inflige ${$m1+$sp*0.3748+$ap*0.2436} points de dégâts d'Ombreflamme. » + étiquette telle quelle | Instantly blasts the target for ${$m1+$sp*0.3748+$ap*0.2436} Shadowflame damage.   @ext:If the target dies within $1129341d of Shadowburn, and yields experien |
| `sort/18867//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Frappe instantanément la cible et lui inflige ${$m1+$sp*0.3748+$ap*0.2436} points de dégâts d'Ombreflamme. » + étiquette telle quelle | Instantly blasts the target for ${$m1+$sp*0.3748+$ap*0.2436} Shadowflame damage.    @ext:If the target dies within $1129341d of Shadowburn, and yields experie |
| `sort/18868//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Frappe instantanément la cible et lui inflige ${$m1+$sp*0.3748+$ap*0.2436} points de dégâts d'Ombreflamme. » + étiquette telle quelle | Instantly blasts the target for ${$m1+$sp*0.3748+$ap*0.2436} Shadowflame damage.    @ext:If the target dies within $1129341d of Shadowburn, and yields experie |
| `sort/18869//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Frappe instantanément la cible et lui inflige ${$m1+$sp*0.3748+$ap*0.2436} points de dégâts d'Ombreflamme. » + étiquette telle quelle | Instantly blasts the target for ${$m1+$sp*0.3748+$ap*0.2436} Shadowflame damage.    @ext:If the target dies within $1129341d of Shadowburn, and yields experie |
| `sort/18870//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Frappe instantanément la cible et lui inflige ${$m1+$sp*0.3748+$ap*0.2436} points de dégâts d'Ombreflamme. » + étiquette telle quelle | Instantly blasts the target for ${$m1+$sp*0.3748+$ap*0.2436} Shadowflame damage.    @ext:If the target dies within $1129341d of Shadowburn, and yields experie |
| `sort/18871//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Frappe instantanément la cible et lui inflige ${$m1+$sp*0.3748+$ap*0.2436} points de dégâts d'Ombreflamme. » + étiquette telle quelle | Instantly blasts the target for ${$m1+$sp*0.3748+$ap*0.2436} Shadowflame damage.    @ext:If the target dies within $1129341d of Shadowburn, and yields experie |
| `sort/18944//Rank` | garder_anglais | rang technique de CoA (« Asc D0 20 ») : marqueur interne, à laisser tel quel | Asc D0 20 |
| `sort/27263//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Frappe instantanément la cible et lui inflige ${$m1+$sp*0.3748+$ap*0.2436} points de dégâts d'Ombreflamme. » + étiquette telle quelle | Instantly blasts the target for ${$m1+$sp*0.3748+$ap*0.2436} Shadowflame damage.    @ext:If the target dies within $1129341d of Shadowburn, and yields experie |
| `sort/30546//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Frappe instantanément la cible et lui inflige ${$m1+$sp*0.3748+$ap*0.2436} points de dégâts d'Ombreflamme. » + étiquette telle quelle | Instantly blasts the target for ${$m1+$sp*0.3748+$ap*0.2436} Shadowflame damage.    @ext:If the target dies within $1129341d of Shadowburn, and yields experie |
| `sort/47826//Description` | doute | majoritairement anglais à cause de la longue étiquette @ext@ gardée en anglais ; proposition : « Frappe instantanément la cible et lui inflige ${$m1+$sp*0.3748+$ap*0.2436} points de dégâts d'Ombreflamme. » + étiquette telle quelle | Instantly blasts the target for ${$m1+$sp*0.3748+$ap*0.2436} Shadowflame damage.    @ext:If the target dies within $1129341d of Shadowburn, and yields experie |

## talents / essai_talents

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/92086//ToolTip` | doute | infobulle tronquée par CoA : elle commence par « cause your next… » sans sujet ; sens incomplet, à voir avec le texte complet du sort 92086 |  cause your next ¦cffffffffMalefic Wrath¦r within $802623d to become instant cast, incur no global cooldown, and become free of cost. |

## talents / talents_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/92086//ToolTip` | doute | infobulle tronquée par CoA : elle commence par « cause your next… » sans sujet ; sens incomplet, à voir avec le texte complet du sort 92086 |  cause your next ¦cffffffffMalefic Wrath¦r within $802623d to become instant cast, incur no global cooldown, and become free of cost. |

## talents / talents_012

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/572213//Description` | doute | blocage du contrôle : l'étiquette @ext:…:ext@ (moins de 80 caractères) doit rester identique à l'anglais (codes_couleur_liens), mais elle contient « Reaper's », refusé comme classe CoA restée en anglais ; traduction prête : Lancer ¦cffffffffPorteur de fin¦r marque désormais le sol sous vous comme votre ¦cffffffffSépulture¦r pendant $804722d.\r\n\r\nLes coups critiques directs portés aux ennemis dans une ¦cffffffffSépulture¦r infligent désormais ${$300979m1*$<scalingbp>+$AP*0.36} points de dégâts d'Ombre.\r\n\r\n@ext:This effect is still active while in another Reaper's ¦cffffffffGravesite¦r.:ext@ | Casting ¦cffffffffEndbringer¦r now marks the ground beneath you as your ¦cffffffffGravesite¦r for $804722d.  Direct critical strikes made against enemies with |

## talents / talents_013

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/574153//ToolTip` | garder_anglais | texte de travail des développeurs (horodatage, identifiant interne et deux versions de la description), pas une infobulle à traduire | 6/19/2026 8:13:46 PM keedarasWShfdmftsJKGFx spell SpellDescription0 ¦cFF66DDFFLevel 30 Passive¦r Increases your dodge and critical strike rating by $s1% of you |

## talents / talents_014

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `sort/680369//Name` | garder_anglais | nom de fantaisie en latin (« Ignis Ultimatus »), identique en français | Ignis Ultimatus |
| `sort/680544//ToolTip` | garder_anglais | bouche-trou technique (« placeholder »), pas un texte du jeu | placeholder |

## zones / zones_001

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `carte/35//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Prison de Hurlevent » | Stormwind Prison |
| `carte/400//name` | garder_anglais | nom propre inventé par CoA | Siltithus Setis |
| `carte/714//name` | garder_anglais | nom interne d'une carte de transport (navire), jamais affiché comme lieu | Transport: The Royal Breaker (Battle Royal) |
| `carte/754//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Trône des Quatre vents » | Throne of the Four Winds |
| `carte/755//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cité perdue des Tol'vir » | Lost City of the Tol'vir |
| `carte/801//name` | garder_anglais | nom propre inventé par CoA | Ortus Mallum |
| `carte/807//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | MageArtifact |
| `carte/809//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | InstanceName |
| `carte/860//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | AzerothHDDev |
| `carte/861//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | KalimdorHDDev |
| `carte/862//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | PandariaDev |
| `carte/863//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | DraenorDev |
| `carte/864//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | BrokenIslesDev |
| `carte/865//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | KultirasMapDev |
| `carte/866//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | ZandalarDev |
| `carte/867//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | TheShadowlandsDev |
| `carte/868//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | DragonIslesDev |
| `carte/869//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | KhazAlgarSurfaceDev |
| `carte/870//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | KhazAlgarDev |
| `carte/871//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | SEtest01 |
| `carte/873//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | SEtest03 |
| `carte/874//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | SEtest04 |
| `carte/875//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | SEtest05 |
| `carte/880//name` | garder_anglais | nom propre inventé par CoA ; PvE reste en anglais (glossaire) | Setis (PvE) |
| `carte/881//name` | garder_anglais | nom officiel identique (Azuregos), PvE reste en anglais (glossaire) | Azuregos (PvE) |
| `carte/883//name` | garder_anglais | nom propre inventé par CoA ; PvE reste en anglais (glossaire) | Soggoth (PvE) |
| `carte/884//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Creux de Depthbreaker » | Depthbreaker's Hollow |
| `carte/885//name` | garder_anglais | nom officiel identique (Emeriss), PvE reste en anglais (glossaire) | Emeriss (PvE) |
| `carte/886//name` | garder_anglais | nom officiel identique (Taerar), PvE reste en anglais (glossaire) | Taerar (PvE) |
| `carte/887//name` | garder_anglais | nom officiel identique (Ysondre), PvE reste en anglais (glossaire) | Ysondre (PvE) |
| `carte/889//name` | garder_anglais | nom propre inventé par CoA ; PvE reste en anglais (glossaire) | Snowgrave (PvE) |
| `carte/890//name` | garder_anglais | nom propre inventé par CoA ; PvE reste en anglais (glossaire) | Atal'zull (PvE) |
| `carte/891//name` | garder_anglais | nom propre inventé par CoA ; PvE reste en anglais (glossaire) | Kaldros Depthbreaker (PvE) |
| `carte/900//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Norfendre du futur » | Future Northrend |
| `carte/901//name` | garder_anglais | nom propre inventé par CoA ; jeu de mots sur Nerub | Newnerub |
| `carte/905//name` | garder_anglais | nom propre inventé par CoA | Mish Faramos |
| `carte/907//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Île évanescente » | Fading Island |
| `carte/910//name` | garder_anglais | nom propre inventé par CoA ; jeu de mots sur Nerub | Newnerub |
| `carte/920//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | SpellDevMap |
| `carte/921//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | BlackDevMap |
| `carte/922//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | DungeonDevMap |
| `carte/923//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | RaidDevMap |
| `carte/926//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | RobinDevMap |
| `carte/927//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Azerothdev |
| `carte/928//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Kalimdordev |
| `carte/929//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | AdtDevMap |
| `carte/931//name` | garder_anglais | nom propre inventé par CoA | Astaroth |
| `carte/933//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Gouffre du Regret » | Regret's Chasm |
| `carte/934//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | AzerothDev BB |
| `carte/936//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Caveaux de l'Inquisition » | Vaults of the Inquisition |
| `carte/937//name` | garder_anglais | parler troll de CoA (« De Other Side ») ; proposition : « La route d'l'Autre Côté » | Road to De Other Side |
| `carte/938//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon des nécromanciens d'Azga » | Azga Necromancer Dungeon |
| `carte/939//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Donjon du sanctuaire du culte du Vautour » | Vulture Cult Sanctuary Dungeon |
| `carte/940//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Profondeurs de Shadowbone » (même lieu que « Shadowbone Depths ») | Shadow Bone Depths |
| `carte/941//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « Temple des Braises » | Temple Of Embers |
| `carte/951//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Vengeance d'Helya » | Helya Revenge |
| `carte/959//name` | garder_anglais | nom propre inventé par CoA | Druk'Thar |
| `carte/960//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Mini-jeux » | Mini Games |
| `carte/968//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « L'Abysse » | The Abbys |
| `carte/970//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Taverne de l'Écho ombragé » | Shaded Echo Tavern |
| `carte/971//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Salle des égouts de Hurlevent » | Stormwind Sewer Room |
| `carte/1009//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | CoA PvP |
| `carte/1010//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | CoaSpellVisuals |
| `carte/1043//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Arène de Castagn'ar » | Brawl'gar Arena |
| `carte/1171//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | custom_marsh |
| `carte/1177//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | SpellVisualMap |
| `carte/1200//name` | garder_anglais | nom officiel identique en français (Lordaeron) | Lordaeron |
| `carte/1383//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | UldumNew |
| `carte/1404//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | pvp5v5map1 |
| `carte/1681//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bassin Arathi (hiver) » | Arathi Basin Winter |
| `carte/1682//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Goulet des Chanteguerres (hiver) » | Warsong Gulch Winter |
| `carte/1686//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Assaut sur l'île d'Alcaz » | Assault on Alcaz Island |
| `carte/1690//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Assaut d'Alterac » | Alterac Assault |
| `carte/1731//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Guilde des bagarreurs de Grizlo » | Grizlo's Brawlers Guild |
| `carte/1776//name` | garder_anglais | nom propre inventé par CoA | Vardrheim |
| `carte/1789//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Arène de Castagn'ar » | Brawl'gar Arena |
| `carte/1908//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Île de Zanza » | Zanza's Isle |
| `carte/1911//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ruines de la cité d'Akhen » | Akhen City Ruins |
| `carte_monde/2000//area_name` | garder_anglais | nom technique (carte de développement, de test ou interne) | SpellDevMap |
| `carte_monde/2031//area_name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Xorthal » | Xorthal's Lair |
| `carte_monde/3040//area_name` | garder_anglais | nom technique (carte de développement, de test ou interne) | CoaSpellVisuals |
| `carte_monde/3042//area_name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ruines de la cité d'Akhen » | Akhen City Ruins |
| `point_carte/2842//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Camp Coldhewn » | Coldhewn Camp |
| `point_carte/2843//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Poste du bosquet cénarien » | Cenarion Grovepost |
| `point_carte/2844//name` | garder_anglais | jeu de mots de CoA sur « Jurassic Park » et Un'Goro : à garder tel quel | Un'Gorassic Park |
| `point_carte/2850//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Creuset de sang » | The Blood Crucible |
| `point_carte/2852//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Jardin de Malorne » | Garden Of Malorne |
| `point_carte/2854//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Garde de nuit » | The Night's Watch |
| `point_carte/2855//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Camp Noirbois » | Camp Blackwood |
| `point_carte/2856//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Ranch des béliers » | Ram Ranch |
| `point_carte/2857//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Bastion de Highwind » | Highwind Hold |
| `point_carte/2862//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Les Terres de Warborn » | The Warborn Grounds |
| `point_carte/2864//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Chapelle de la Grâce finale » | Chapel of Final Grace |
| `point_carte/2866//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Poste de Mosshorn » | Mosshorn Post |
| `point_carte/2867//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Refuge de Whispergleam » | Whispergleam Refuge |
| `point_carte/2868//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Donjon verdoyant » | The Verdant Keep |
| `point_carte/2869//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cercle de Stonefather » | Stonefather's Circle |
| `point_carte/2873//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cœur de Thel'dralor » | Thel'dralor's Heart |
| `point_carte/2877//name` | garder_anglais | nom propre inventé par CoA | Graysky |
| `point_carte/2878//name` | garder_anglais | nom propre inventé par CoA | Dun Kazad |
| `zone/1804//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Camp Coldhewn » | Coldhewn Camp |
| `zone/1805//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Bastion de Morvath » | Morvath’s Hold |
| `zone/1806//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Camp Dusthorn » | Dusthorn Camp |
| `zone/1807//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Avant-poste de Winterdelve » | Winterdelve Outpost  |
| `zone/1808//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bosquet silencieux » | Silent Grove |
| `zone/1809//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Crête de Gearspark » | Gearspark Ridge |
| `zone/1810//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Avant-poste de Felmantle » | Felmantle Outpost |
| `zone/1811//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Poste d'exorcisme des croisés » | Crusader’s Exorcism Post |
| `zone/1812//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Refuge du collectionneur » | The Collector’s Refuge |
| `zone/1813//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Creuset de sang » | The Blood Crucible |
| `zone/1814//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Bastion d'Everburn » | Everburn Hold  |
| `zone/1815//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Jardin de Malorne » | Garden Of Malorne |
| `zone/1816//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Garde de nuit » | The Night's Watch |
| `zone/1818//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Camp Noirbois » | Camp Blackwood |
| `zone/1819//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Ranch des béliers » | Ram Ranch |
| `zone/1820//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Bastion de Highwind » | Highwind Hold |
| `zone/1821//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Sanctuaire des plaines » | Sanctuary of the Plains |
| `zone/1822//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Sanctuaire de Moonrest » | Moonrest Sanctuary  |
| `zone/1823//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Bastion du bandit » | The Bandit’s Bastion |
| `zone/1824//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Les Terres de Warborn » | The Warborn Grounds |
| `zone/1825//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cercle de Stonefather » | Stonefather's Circle |
| `zone/1826//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory  |
| `zone/1827//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Chapelle de la Grâce finale » | Chapel of Final Grace |
| `zone/1828//name` | garder_anglais | nom propre inventé par CoA | Shal’Athil  |
| `zone/1829//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Poste de Mosshorn » | Mosshorn Post |
| `zone/1830//name` | garder_anglais | nom propre inventé par CoA ; « Camp Krag'zul » se lit déjà en français | Camp Krag’zul |
| `zone/1831//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Refuge de Whispergleam » | Whispergleam Refuge |
| `zone/1832//name` | garder_anglais | jeu de mots de CoA sur « Jurassic Park » et Un'Goro : à garder tel quel | Un'Gorassic Park |
| `zone/1833//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Poste du bosquet cénarien » | Cenarion Grovepost |
| `zone/1834//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Perchoir du braconnier » | Poacher’s Perch |
| `zone/1835//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Donjon verdoyant » | The Verdant Keep |
| `zone/2804//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cœur de Thel'dralor » | Thel'dralor's Heart |
| `zone/2810//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Lamentation de la Désolation » | Desolation's Lament |
| `zone/4991//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Marais supérieurs » | Upper Marshes |
| `zone/4992//name` | garder_anglais | nom propre inventé par CoA | Dun Guldar |
| `zone/4993//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Caverne de Silverwind » (Silverwind = Vent-argent chez Blizzard, à confirmer) | Silverwind Cavern |
| `zone/4994//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ranch Crambers » | Crambers Ranch |
| `zone/4995//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Recoin des Hautes-terres » | Highlands Nook |
| `zone/4996//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Avant-poste de Longview » | Longview Outpost |
| `zone/4997//name` | garder_anglais | nom propre inventé par CoA | Zulumar |
| `zone/4998//name` | garder_anglais | nom propre inventé par CoA | Burndural |
| `zone/5002//name` | garder_anglais | nom propre inventé par CoA | Sty'La |
| `zone/5006//name` | garder_anglais | nom propre inventé par CoA | Sty'La |
| `zone/5019//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Collines ardentes » | The Blazing Hills |
| `zone/5020//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Domaine d'Alestone » | Alestone Estate |
| `zone/5021//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Croissant calciné » | The Charred Crescent |
| `zone/5159//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des zeppelins » | Zeppelin Tower |
| `zone/5366//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Xorthal » | Xorthal's Lair |
| `zone/5449//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Profondeurs du Crépuscule » | Twilight Depths |
| `zone/5497//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des zeppelins » | Zeppelin Tower |
| `zone/5520//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Vestiges de Thel'dralor » | Remnants of Thel’dralor |
| `zone/6206//name` | garder_anglais | nom propre inventé par CoA | Fort Airheart |
| `zone/7000//name` | garder_anglais | nom officiel identique en français (Lordaeron) | Lordaeron |
| `zone/7009//name` | garder_anglais | nom propre inventé par CoA | Akghelm |
| `zone/7717//name` | garder_anglais | nom propre inventé par CoA | Vardrheim |
| `zone/8464//name` | garder_anglais | nom propre inventé par CoA ; officiel du Brawlpub de Bizmo non prouvé ; partie descriptive : « Arène du Brawlpup de Bizmo » | Bizmo's Brawlpup Arena |
| `zone/8465//name` | garder_anglais | nom propre inventé par CoA ; officiel du Brawlpub de Bizmo non prouvé | Bizmo's Brawlpup |
| `zone/8466//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Salle Boum » | Boom Room |
| `zone/10002//name` | garder_anglais | nom propre inventé par CoA | Astaroth |
| `zone/10013//name` | garder_anglais | nom propre inventé par CoA | Mish Faramos |
| `zone/10018//name` | garder_anglais | nom propre inventé par CoA ; jeu de mots sur Nerub | Newnerub |
| `zone/10019//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Mer d'Azzar » | Sea of Azzar |
| `zone/10032//name` | garder_anglais | nom officiel identique en français (Maldraxxus) | Maldraxxus |
| `zone/10053//name` | garder_anglais | nom officiel identique en français (Val'sharah) | Val'sharah |
| `zone/10068//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | AzzarEvent |
| `zone/10078//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Île de Dawnrise » | Dawnrise Island |
| `zone/10088//name` | garder_anglais | nom propre inventé par CoA | Ala'Taclar |
| `zone/10097//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | RobinDevMap |
| `zone/10110//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Île de Dawnrise » | Dawnrise Island |
| `zone/10112//name` | garder_anglais | nom de fantaisie de CoA (Wonka) | Wonka Wonka! |
| `zone/10148//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Gorge » | The Gorge |
| `zone/10151//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Suite de la duchesse » | Duchess' Suite |
| `zone/10152//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Grotte des Patriarches » | Patriarchs' Grotto |
| `zone/10153//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Taverne de l'Écho ombragé » | Shaded Echo Tavern |
| `zone/10156//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | ADT Dev Map |
| `zone/10161//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Camp d'infiltration de la Horde » | Horde Infiltration Camp |
| `zone/10163//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Île évanescente » | Fading Island |
| `zone/10164//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Côte murmurante » | Whispering Coast |
| `zone/10165//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Crique des Pèlerins » | Pilgrims’ Cove |
| `zone/10166//name` | garder_anglais | nom propre inventé par CoA | Eyirhold |
| `zone/10167//name` | garder_anglais | nom propre inventé par CoA | Runeheap |
| `zone/10168//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Phare d'Eyiren » | Eyiren Lighthouse |
| `zone/10169//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Sommet de la gondole » | Gondola Highpoint |
| `zone/10170//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Falaises des Aspirants » | Aspirants’ Cliffs |
| `zone/10171//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cimetière de Gharna » | Gharna Graveyard |
| `zone/10172//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Plage de Mistcoast » | Mistcoast Beach |
| `zone/10173//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Vieux Salthillyen » | Old Salthillyen |
| `zone/10174//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ruines englouties de Salthillyen » | Sunken Ruins of Salthillyen |
| `zone/10175//name` | garder_anglais | nom propre inventé par CoA | Zin-N’zothi |
| `zone/10176//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Hameau de Whim » | Whim’s Hamlet |
| `zone/10177//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Prairies abyssales » | Abyssal Meadows |
| `zone/10178//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Gorge fumante » | Smoldering Gorge |
| `zone/10179//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Abysse luminescent » | Luminescent Abyss |
| `zone/10180//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Forêt de Duskglen » | Duskglen Forest |
| `zone/10181//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour du Kirin Tor » | Kirin Tor Tower |
| `zone/10182//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Grand terrier de Darkandle » | Darkandle Grand Burrow |
| `zone/10183//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Terrier de Benttoe » | Benttoe Burrow |
| `zone/10184//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Terrier de Coughsnort » | Coughsnort Burrow |
| `zone/10185//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Terrier de Wiggleteeth » | Wiggleteeth Burrow |
| `zone/10186//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Ville de la Faveur » | Favor Town |
| `zone/10187//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Mine à ciel ouvert de Fastfuse » | Fastfuse Open-Pit Mine |
| `zone/10188//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Floraison aurique » | Aureic Bloom |
| `zone/10189//name` | garder_anglais | nom propre inventé par CoA | Hardluck |
| `zone/10190//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Faubourgs de la Compagnie Fastfure » (Fastfure : coquille de CoA pour Fastfuse ?) | Fastfure Company Outskirts |
| `zone/10191//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Compagnie Fastfuse » | Fastfuse Company |
| `zone/10192//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Côte déchiquetée » | Jagged Coast |
| `zone/10193//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ruines d'Alzar'din » | Alzar’din Ruins |
| `zone/10194//name` | garder_anglais | nom propre inventé par CoA ; proposition éventuelle : « Concorde » | Concord |
| `zone/10204//name` | garder_anglais | nom propre inventé par CoA | Zeb'Goro |
| `zone/10213//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Sanctuaire de Theren-Dion » | Theren-Dion Sanctuary |
| `zone/10214//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Sommet du Sanctuaire d'Iris » | Iris Sanctuary Summit  |
| `zone/10216//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Docks de Brightwater » | Brightwater Docks |
| `zone/10217//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Manoir de la famille Spada » | Spada Family Manor |
| `zone/10218//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Caveaux de l'Inquisition » | Vaults of the Inquisition |
| `zone/10219//name` | garder_anglais | parler troll de CoA (« De Other Side ») ; proposition : « La route d'l'Autre Côté » | Road to De Other Side |
| `zone/10220//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Temple de la Matrice blessée » | Temple of the Wounded Womb |
| `zone/10233//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon des nécromanciens d'Azga » | Azga Necromancer Dungeon |
| `zone/10234//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Donjon du sanctuaire du culte du Vautour » | Vulture Cult Sanctuary Dungeon |
| `zone/10236//name` | garder_anglais | nom officiel identique (Azuregos), PvE reste en anglais (glossaire) | Azuregos (PvE) |
| `zone/10237//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Trône du seigneur funeste » | Throne of the Doom Lord |
| `zone/10238//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse gastrique du Maître » | Master’s Gastric Pit |
| `zone/10239//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Creux de Depthbreaker » | Depthbreaker's Hollow |
| `zone/10240//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Creux de Depthbreaker » | Depthbreaker's Hollow |
| `zone/10241//name` | garder_anglais | nom propre inventé par CoA | Dunshire |
| `zone/10242//name` | garder_anglais | nom propre inventé par CoA | Cresthairn |
| `zone/10243//name` | garder_anglais | nom propre inventé par CoA | Graysky |
| `zone/10244//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Manoir Darengar » | Darengar Manor |
| `zone/10245//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cavernes d'Ealdmaine » | Ealdmaine Caverns |
| `zone/10246//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Village de Scaidern » | Scaidern Village |
| `zone/10247//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Village de Galdaern » | Galdaern Village |
| `zone/10248//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Pic de Daumor » | Daumor Peak |
| `zone/10249//name` | garder_anglais | nom propre inventé par CoA | Rockrend |
| `zone/10250//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Bourg de Shadewell » | Shadewell Town |
| `zone/10251//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Sanctuaire de Namarien » | Namarien Sanctuary |
| `zone/10252//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Vallon doré » | Guilded Vale |
| `zone/10253//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Forêt d'Oldmist » | Oldmist Forest |
| `zone/10254//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Vallée de Snowsong » | Snowsong Valley |
| `zone/10255//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Tertres de Scadeald » | Scadeald Barrows |
| `zone/10256//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Rivage évanescent » | Fading Shore |
| `zone/10257//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Abbaye suspendue du Vent sacré » | Hallow Wind Hanging Abbey |
| `zone/10258//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Embuscade des Crins-de-givre » | Frostmane Ambush |
| `zone/10259//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Avant-poste de Graysky » | Graysky Outpost |
| `zone/10260//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ruines de Zuramunda » | Zuramunda Ruins |
| `zone/10261//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Pont de Kharadol » | Kharadol Bridge |
| `zone/10262//name` | garder_anglais | nom propre inventé par CoA | Kheled-Zaram |
| `zone/10263//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Avant-poste de Denathel » | Denathel Outpost |
| `zone/10264//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cimetière de Snowveil » | Snowveil Cemetery |
| `zone/10265//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Blessure de Thaurgrim » | Thaurgrim’s Wound |
| `zone/10266//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Forteresse d'Andraste » | Andraste’s Fortress |
| `zone/10267//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Sommet battu par les vents » | Windswept Summit |
| `zone/10268//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Falaises inclinées » | Tilted Cliffs |
| `zone/10269//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Fort Kerebor » | Kerebor Fort |
| `zone/10270//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Nord d'Elwynn » | Northern Elwynn |
| `zone/10276//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cimetière de Hurlevent » | Stormwind City Cemetery |
| `zone/10277//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Lac de Hurlevent » | Stormwind Lake |
| `zone/10279//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Caverne de Snowgrave » | Snowgrave's Cavern |
| `zone/10280//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Caverne de Snowgrave » | Snowgrave's Cavern |
| `zone/10282//name` | garder_anglais | nom propre inventé par CoA | Baile Escada |
| `zone/10283//name` | garder_anglais | nom propre inventé par CoA | Cair Cragg |
| `zone/10284//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Hauts de Braicag » | Braicag Heights |
| `zone/10285//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Route sinueuse » | Winding Road |
| `zone/10286//name` | garder_anglais | nom propre inventé par CoA | Nivelarn |
| `zone/10287//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Avant-poste de Metantenna » | Metantenna Outpost |
| `zone/10288//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Station de Metantenna » | Metantenna Station |
| `zone/10289//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Chaîne d'Ealdfrost » | Ealdfrost Range |
| `zone/10290//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Contreforts d'Ealdfrost » | Ealdfrost Foothills |
| `zone/10291//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Chemin de l'hiver » | The Winter Path |
| `zone/10292//name` | garder_anglais | nom propre inventé par CoA | Druk'Thar |
| `zone/10293//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Pic de Moroduin » | Moroduin Peak |
| `zone/10294//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Pic de Helgen » | Helgen Peak |
| `zone/10295//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Brasero de l'Unité » | Brazier of Unity |
| `zone/10296//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cavernes d'Anzurak » | Anzurak Caverns |
| `zone/10297//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Lac Kazadmere » | Lake Kazadmere |
| `zone/10298//name` | garder_anglais | nom propre inventé par CoA | Ada-Gumbad |
| `zone/10299//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Plateaux ternis » | Tarnished Plateaus |
| `zone/10300//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Bois mort » | The Deadwood |
| `zone/10301//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Un endroit sombre » | A Dark Place |
| `zone/10302//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Étendue pâle » | Pale Reach |
| `zone/10303//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Mer de l'Étendue pâle » | Pale Reach Sea |
| `zone/10304//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Mer de Druk'Thar » | Druk'Thar Sea |
| `zone/10305//name` | garder_anglais | nom propre inventé par CoA | Shadewell |
| `zone/10306//name` | garder_anglais | nom propre inventé par CoA | Dun Kazad |
| `zone/10307//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Village de Zandor » | Zandor Village |
| `zone/10308//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Côte ensemencée » | Sown Coast |
| `zone/10309//name` | garder_anglais | nom propre inventé par CoA | Thundrakar |
| `zone/10310//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Forêt de Frostbark » | Frostbark Forest |
| `zone/10311//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Autel du Bourgeon sacré » | Altar of the Sacred Bud |
| `zone/10312//name` | garder_anglais | nom propre inventé par CoA | Dun Argan |
| `zone/10313//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Village de Faz'Faron » | Faz’Faron Village |
| `zone/10314//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Palais hiératique » | Hieratic Palace |
| `zone/10315//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Le Grand Snowfang » | The Great Snowfang |
| `zone/10316//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Côte de Mistridge » | Mistridge Coast |
| `zone/10317//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Falaises d'Icefang » | Icefang Cliffs |
| `zone/10318//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Village de Zorazon » | Zorazon Village |
| `zone/10319//name` | garder_anglais | nom propre inventé par CoA | Darkcove |
| `zone/10320//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Village d'Ar'akin » | Ar’akin Village |
| `zone/10321//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ruines d'Arandrak » | Arandrak Ruins |
| `zone/10322//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cavernes de Frostbirth » | Frostbirth Caverns |
| `zone/10323//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Ville pirate » | Pirate Town |
| `zone/10324//name` | doute | nom en espagnol dans les données de CoA (« village côtier ») ; proposition : « Village côtier » | Aldea costera |
| `zone/10325//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Vallée de la Rivière malade » | Sickened River Valley |
| `zone/10326//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Collines de Fan'dor » | Fan’dor Hills |
| `zone/10327//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Rivage évanescent » | Fading Shore |
| `zone/10328//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Profondeurs de Shadowbone » | Shadowbone Depths |
| `zone/10329//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Un endroit sombre » | A Dark Place |
| `zone/10330//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Norfendre du futur » | Future Northrend |
| `zone/10331//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « Temple des Braises » | Temple of Embers |
| `zone/12000//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Taverne de Moulin-de-Tarren » | Tarren Mill Tavern |
| `zone/12108//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Guilde des bagarreurs de Grizlo » | Grizlo's Brawlers Guild |
| `zone/13023//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Cryptes du Sépulcre » | The Sepulcher Crypts |
| `zone/14001//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Camp Dusthorn » | Dusthorn Camp |
| `zone/15011//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Île de Zanza » | Zanza's Isle |
| `zone/15012//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ruines d'Atali » | Ruins of Atali |
| `zone/15013//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Baie de l'Envahisseur » | Invader's Bay |
| `zone/15014//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Surplomb de Jin'Vile » | Jin'Vile Overlook |
| `zone/15015//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ruines de la cité d'Akhen » | Akhen City Ruins |
| `zone/15016//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Terrains rituels » | Ritual Grounds |
| `zone/15017//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « L'Attrition de rubis » | The Ruby Attrition |
| `zone/15018//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Caverne du Murmure de poussière » | Dust Whisper Cavern |
| `zone_interieure/24102//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Caverne du Murmure de poussière » | Dust Whisper Cavern |
| `zone_interieure/49492//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Xorthal » | Xorthal's Lair |
| `zone_interieure/49496//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Profondeurs du Crépuscule » | Twilight Depths |
| `zone_interieure/52477//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Gorge » | The Gorge |
| `zone_interieure/52478//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Gorge » | The Gorge |
| `zone_interieure/52502//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Grotte des Patriarches » | Patriarchs' Grotto |
| `zone_interieure/52503//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Grotte des Patriarches » | Patriarchs' Grotto |
| `zone_interieure/52515//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Suite de la duchesse » | Duchess' Suite |
| `zone_interieure/52558//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Gorge » | The Gorge |
| `zone_interieure/52559//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Gorge » | The Gorge |
| `zone_interieure/52583//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Grotte des Patriarches » | Patriarchs' Grotto |
| `zone_interieure/52584//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Grotte des Patriarches » | Patriarchs' Grotto |
| `zone_interieure/52596//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Suite de la duchesse » | Duchess' Suite |
| `zone_interieure/52668//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Caveaux de l'Inquisition » | Vaults of the Inquisition |
| `zone_interieure/52705//name` | garder_anglais | parler troll de CoA (« De Other Side ») ; proposition : « La route d'l'Autre Côté » | Road to De Other Side |
| `zone_interieure/52713//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Temple de la Matrice blessée » | Temple of the Wounded Womb |
| `zone_interieure/52714//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Temple de la Matrice blessée » | Temple of the Wounded Womb |
| `zone_interieure/52715//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon des nécromanciens d'Azga » | Azga Necromancer Dungeon |
| `zone_interieure/52731//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse gastrique du Maître » | Master’s Gastric Pit |
| `zone_interieure/53300//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Creux de Depthbreaker » | Depthbreaker's Hollow |
| `zone_interieure/53303//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Creux de Depthbreaker » | Depthbreaker's Hollow |
| `zone_interieure/53306//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Caverne de Snowgrave » | Snowgrave's Cavern |
| `zone_interieure/53311//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Caverne de Snowgrave » | Snowgrave's Cavern |
| `zone_interieure/53445//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cavernes d'Ealdmaine » | Ealdmaine Caverns |
| `zone_interieure/53553//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Cavernes d'Anzurak » | Anzurak Caverns |
| `zone_interieure/53568//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Station de Metantenna » | Metantenna Station |
| `zone_interieure/53596//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Salle Boum » | Boom Room |
| `zone_interieure/53642//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « L'Attrition de rubis » | The Ruby Attrition |
| `zone_interieure/53856//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Profondeurs de Shadowbone » | Shadowbone Depths |
| `zone_interieure/65691//name` | garder_anglais | nom propre inventé par CoA | Zulumar |
| `zone_interieure/65718//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Profondeurs de Shadowbone » | Shadowbone Depths |

## zones / zones_002

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `carte/1693//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Attaque d'Andorhal » | Andorhal Attack |
| `carte/1696//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Guerre contre Zin-Malor » | War on Zin-Malor |
| `carte/1700//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bataille du Bastion de Flèchelame » | Battle of Bladespire Hold |
| `carte/1703//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bataille de Baie-du-Butin » | Battle of Booty Bay |
| `carte/1706//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Escarmouche dans les Steppes » | Skirmish in the Steppes |
| `carte/1709//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Affrontement au Chaudron » | Clash in The Cauldron |
| `carte/1713//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Match à mort à Mortholme » | Deatholme Deathmatch |
| `carte/1716//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bataille de Hache-tripes » | Battle of Dire Maul |
| `carte/1718//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Affrontement à Pennelune » | Feathermoon Clash |
| `carte/1720//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Retombées du Blanc murmure » | Frostwhisper Fallout |
| `carte/1722//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Duel aux Pins-Argentés » | Silverpine Showdown |
| `carte/1725//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bataille pour Nagrand » | Battle for Nagrand |
| `carte/1727//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Chaos aux Flammes infernales » | Hellfire Havoc |
| `carte/1730//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Guerre de l'Arbre-Monde » | War of the World Tree |
| `carte/1733//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Assaut sur la piste d'atterrissage » | Airstrip Assault |
| `carte/1735//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bain de sang dans les Tarides » | Bloodshed in The Barrens |
| `carte/1737//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bataille du Passage de la porte Nord » | Battle of North Gate Pass |
| `carte/1740//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fouilles d'Ahn'Qiraj » | Excavation of Ahn'Qiraj |
| `carte/1741//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Massacre à Guet-de-pierre » | Stonewatch Slaughter |
| `carte/1748//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Massacre à Stromgarde » | Slaughter in Stromgarde |
| `carte/1751//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bataille pour Theramore » | Battle for Theramore |
| `carte/1754//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Carnage dans le cratère » | Carnage in the Crater |
| `carte/1755//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Guerre du camp de bûcherons chanteguerre » | Warsong Lumber War |
| `carte/1757//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Guerre de la Combe des Cisailles » | War of Windshear Crag |
| `carte/1758//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; carte « (Staging) » de préparation | The Crucible (Staging) |
| `carte/1772//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Snow Crate |
| `carte/1773//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | custom_troll |
| `carte/1775//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Village d'Iskarr » | Iskarr Village |
| `carte/1777//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | custom_vrykul2 |
| `carte/1807//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cryptes de Karazhan » | Karazhan Crypts |
| `carte/1810//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | EldaraTower |
| `carte/1811//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | GronnMapTest |
| `carte/1900//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Île des Rois » | Isle of Kings |
| `carte/1901//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | cu_LD_beast |
| `carte/1902//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | cu_LD_demon |
| `carte/1903//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | cu_LD_demon2 |
| `carte/1904//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | cu_LD_draenei |
| `carte/1905//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | cu_LD_living |
| `carte/1906//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | cu_LD_nightborne |
| `carte/1907//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | 5ppl_snow_bg |
| `carte/1909//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | 5ppl_tropical_bg |
| `carte/1910//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | 5ppl_twillight_bg |
| `carte/1912//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | TorWatha |
| `carte/1995//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Odyssée » | Odyssey |
| `carte/2000//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | intemporel_test |
| `carte/2001//description_alliance` | garder_anglais | nom technique (carte de développement, de test ou interne) ; description d'une carte de test | ...... Pathetic |
| `carte/2001//description_horde` | garder_anglais | nom technique (carte de développement, de test ou interne) ; description d'une carte de test | For the alliance ! |
| `carte/2001//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; carte de test | This is a REAL map |
| `carte/2003//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | intemporel_test4 |
| `carte/2004//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | MyInternalTest4 |
| `carte/3001//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | IntemporelTest14 |
| `carte/3690//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Bastonneurs » | Brawler's Guild |
| `carte/4000//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | TESTDONTTOUCH |
| `carte_monde/4//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Durotar |
| `carte_monde/9//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Mulgore |
| `carte_monde/11//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Barrens |
| `carte_monde/13//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Kalimdor |
| `carte_monde/14//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Azeroth |
| `carte_monde/15//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Alterac |
| `carte_monde/16//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Arathi |
| `carte_monde/19//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BlastedLands |
| `carte_monde/20//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Tirisfal |
| `carte_monde/21//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Silverpine |
| `carte_monde/22//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | WesternPlaguelands |
| `carte_monde/23//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | EasternPlaguelands |
| `carte_monde/24//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Hilsbrad |
| `carte_monde/26//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Hinterlands |
| `carte_monde/27//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | DunMorogh |
| `carte_monde/28//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | SearingGorge |
| `carte_monde/29//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BurningSteppes |
| `carte_monde/30//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Elwynn |
| `carte_monde/32//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | DeadwindPass |
| `carte_monde/35//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | LochModan |
| `carte_monde/38//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | SwampOfSorrows |
| `carte_monde/41//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Teldrassil |
| `carte_monde/61//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ThousandNeedles |
| `carte_monde/81//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | StonetalonMountains |
| `carte_monde/141//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Dustwallow |
| `carte_monde/161//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Tanaris |
| `carte_monde/181//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Aszhara |
| `carte_monde/201//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | UngoroCrater |
| `carte_monde/261//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Silithus |
| `carte_monde/321//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Ogrimmar |
| `carte_monde/362//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ThunderBluff |
| `carte_monde/381//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Darnassis |
| `carte_monde/401//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AlteracValley |
| `carte_monde/443//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | WarsongGulch |
| `carte_monde/461//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ArathiBasin |
| `carte_monde/462//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | EversongWoods |
| `carte_monde/464//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AzuremystIsle |
| `carte_monde/465//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Hellfire |
| `carte_monde/466//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Expansion01 |
| `carte_monde/471//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheExodar |
| `carte_monde/473//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ShadowmoonValley |
| `carte_monde/475//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BladesEdgeMountains |
| `carte_monde/476//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BloodmystIsle |
| `carte_monde/477//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Nagrand |
| `carte_monde/478//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TerokkarForest |
| `carte_monde/480//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | SilvermoonCity |
| `carte_monde/481//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ShattrathCity |
| `carte_monde/482//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | NetherstormArena |
| `carte_monde/486//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BoreanTundra |
| `carte_monde/490//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | GrizzlyHills |
| `carte_monde/491//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | HowlingFjord |
| `carte_monde/492//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | IcecrownGlacier |
| `carte_monde/493//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | SholazarBasin |
| `carte_monde/495//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheStormPeaks |
| `carte_monde/496//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ZulDrak |
| `carte_monde/499//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Sunwell |
| `carte_monde/500//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Silithus |
| `carte_monde/501//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | LakeWintergrasp |
| `carte_monde/502//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ScarletEnclave |
| `carte_monde/503//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Nexus |
| `carte_monde/504//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Dalaran |
| `carte_monde/505//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | WailingCaverns |
| `carte_monde/510//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | CrystalsongForest |
| `carte_monde/512//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | StrandoftheAncients |
| `carte_monde/520//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheNexus |
| `carte_monde/521//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | CoTStratholme |
| `carte_monde/522//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Ahnkahet |
| `carte_monde/523//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | UtgardeKeep |
| `carte_monde/524//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | UtgardePinnacle |
| `carte_monde/525//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | HallsofLightning |
| `carte_monde/526//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Ulduar77 |
| `carte_monde/527//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheEyeofEternity |
| `carte_monde/528//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Nexus80 |
| `carte_monde/529//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Ulduar |
| `carte_monde/530//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Gundrak |
| `carte_monde/531//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheObsidianSanctum |
| `carte_monde/532//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | VaultofArchavon |
| `carte_monde/533//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AzjolNerub |
| `carte_monde/534//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | DrakTharonKeep |
| `carte_monde/535//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Naxxramas |
| `carte_monde/536//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | VioletHold |
| `carte_monde/537//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Naxxramas |
| `carte_monde/540//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | IsleofConquest |
| `carte_monde/541//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | HrothgarsLanding |
| `carte_monde/542//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheArgentColiseum |
| `carte_monde/543//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheArgentColiseum |
| `carte_monde/601//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheForgeofSouls |
| `carte_monde/602//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | PitofSaron |
| `carte_monde/603//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | HallsofReflection |
| `carte_monde/604//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | IcecrownCitadel |
| `carte_monde/609//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheRubySanctum |
| `carte_monde/625//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TwistingNetherMap |
| `carte_monde/626//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TwinPeaks |
| `carte_monde/666//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ShadowfangKeep |
| `carte_monde/680//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Ragefire |
| `carte_monde/686//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ZulFarrak |
| `carte_monde/688//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BlackfathomDeeps |
| `carte_monde/690//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheStockade |
| `carte_monde/691//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Gnomeregan |
| `carte_monde/692//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Uldaman |
| `carte_monde/696//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MoltenCore |
| `carte_monde/697//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ZulGurub |
| `carte_monde/699//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | DireMaul |
| `carte_monde/704//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BlackrockDepths |
| `carte_monde/710//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheShatteredHalls |
| `carte_monde/717//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | RuinsofAhnQiraj |
| `carte_monde/718//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | OnyxiasLair |
| `carte_monde/720//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Uldum |
| `carte_monde/721//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BlackrockSpire |
| `carte_monde/722//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AuchenaiCrypts |
| `carte_monde/723//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | SethekkHalls |
| `carte_monde/724//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ShadowLabyrinth |
| `carte_monde/725//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheBloodFurnace |
| `carte_monde/726//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheUnderbog |
| `carte_monde/727//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheSteamvault |
| `carte_monde/728//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheSlavePens |
| `carte_monde/729//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheBotanica |
| `carte_monde/730//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheMechanar |
| `carte_monde/731//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheArcatraz |
| `carte_monde/732//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ManaTombs |
| `carte_monde/733//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | CoTTheBlackMorass |
| `carte_monde/734//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | CoTHillsbradFoothills |
| `carte_monde/749//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | WailingCaverns |
| `carte_monde/750//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Maraudon |
| `carte_monde/753//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BlackrockCaverns |
| `carte_monde/755//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BlackwingLair |
| `carte_monde/756//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TheDeadmines |
| `carte_monde/760//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | RazorfenDowns |
| `carte_monde/761//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | RazorfenKraul |
| `carte_monde/762//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ScarletMonastery |
| `carte_monde/763//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Scholomance |
| `carte_monde/764//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ShadowfangKeep |
| `carte_monde/765//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Stratholme |
| `carte_monde/766//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AhnQiraj |
| `carte_monde/775//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | CoTMountHyjal |
| `carte_monde/776//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | GruulsLair |
| `carte_monde/779//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MagtheridonsLair |
| `carte_monde/780//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | CoilfangReservoir |
| `carte_monde/781//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ZulAman |
| `carte_monde/782//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TempestKeep |
| `carte_monde/789//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | SunwellPlateau |
| `carte_monde/793//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ZulGurub |
| `carte_monde/796//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BlackTemple |
| `carte_monde/797//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | HellfireRamparts |
| `carte_monde/798//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MagistersTerrace |
| `carte_monde/799//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Karazhan |
| `carte_monde/801//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Ogrimmar |
| `carte_monde/820//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | HillsbradFoothillsBG |
| `carte_monde/856//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TempleofKotmogu |
| `carte_monde/1000//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | RedridgeMountainsManastorm |
| `carte_monde/1001//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AlteracMountainsManastorm |
| `carte_monde/1002//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BlastedLandsManastorm |
| `carte_monde/1003//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | EasternPlaguelandsManastorm |
| `carte_monde/1004//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | FeralasManastorm |
| `carte_monde/1005//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | HillsbradFoothillsManastorm |
| `carte_monde/1006//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | SilverpineForestManastorm |
| `carte_monde/1007//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TanarisManastorm |
| `carte_monde/1008//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | WesternPlaguelandsManastorm |
| `carte_monde/1009//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | WestfallManastorm |
| `carte_monde/1010//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | WinterSpringManastorm |
| `carte_monde/1139//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ArathiBasinWinter |
| `carte_monde/1140//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | WarsongGulchWinter |
| `carte_monde/1141//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TwistingNetherMap |
| `carte_monde/1142//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TwistingNetherMap |
| `carte_monde/1143//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TwistingNetherMap |
| `carte_monde/1144//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ForgottenMine |
| `carte_monde/1200//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | wailingcavernsbarrens |
| `carte_monde/1201//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | scarletmonasteryentrance |
| `carte_monde/1202//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | cavernsoftimein |
| `carte_monde/1203//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | cavernsoftime |
| `carte_monde/1204//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | blackrockmountain |
| `carte_monde/1205//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | upperblackrockmountain |
| `carte_monde/1206//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | lowerblackrockmountain |
| `carte_monde/1207//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | maraudonorange |
| `carte_monde/1208//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | maraudonpurple |
| `carte_monde/1209//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Uldamanin |
| `carte_monde/1210//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | stillpinehold |
| `carte_monde/1211//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | tideshollow |
| `carte_monde/1212//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | nightwebshollow |
| `carte_monde/1213//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | golbolarquarry |
| `carte_monde/1214//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | coldridgepass |
| `carte_monde/1215//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | thegrizzledden |
| `carte_monde/1216//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | burningbladecoven |
| `carte_monde/1217//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | dustwindcave |
| `carte_monde/1218//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | skullrock |
| `carte_monde/1219//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Upperfargodeepmine |
| `carte_monde/1220//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Lowerfargodeepmine |
| `carte_monde/1221//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | jasperlodemine |
| `carte_monde/1222//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | amanicatacombs |
| `carte_monde/1223//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | palemanerock |
| `carte_monde/1224//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | theventurecomine |
| `carte_monde/1225//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | echoridgemine |
| `carte_monde/1226//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | twilightsrun |
| `carte_monde/1227//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | thenoxiouslair |
| `carte_monde/1228//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | thegapingchasm |
| `carte_monde/1229//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Upperbanethilbarrowden |
| `carte_monde/1230//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Lowerbanethilbarrowden |
| `carte_monde/1231//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | felrock |
| `carte_monde/1232//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | shadowthreadcave |
| `carte_monde/1233//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | theslitheringscar |
| `carte_monde/1234//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | deadmineswestfall |
| `carte_monde/1235//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | goldcoastquarry |
| `carte_monde/1236//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | jangolodemine |
| `carte_monde/1237//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | northshire |
| `carte_monde/1238//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | coldridgevalley |
| `carte_monde/1239//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | deathknellstart |
| `carte_monde/1240//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | sunstriderislestart |
| `carte_monde/1241//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ammenvalestart |
| `carte_monde/1242//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | shadowglenstart |
| `carte_monde/1243//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | valleyoftrialsstart |
| `carte_monde/1244//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | campnarachestart |
| `carte_monde/2001//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AlvaEncounter |
| `carte_monde/2002//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | warsonggulchupdate |
| `carte_monde/2003//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | arathibasinupdate |
| `carte_monde/2004//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | StormwindSewers |
| `carte_monde/2005//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | osrs4 |
| `carte_monde/2006//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AzzarFaire |
| `carte_monde/2007//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TirisFortress |
| `carte_monde/2008//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | zamasucombat |
| `carte_monde/2009//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AzzarFaire |
| `carte_monde/2010//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | AzzarFaire2 |
| `carte_monde/2011//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | tolbarad |
| `carte_monde/2012//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | KarazhanCrypts |
| `carte_monde/2013//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | TwistingNetherMap |
| `carte_monde/2014//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | BloodmystIsleManastorm |
| `carte_monde/2015//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | GhostlandsManastorm |
| `carte_monde/2016//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | HellfirePeninsulaManastorm |
| `carte_monde/2017//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | NagrandManastorm |
| `carte_monde/2018//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ShadowmoonValleyManastorm |
| `carte_monde/2019//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ZangarmarshManastorm |
| `carte_monde/2020//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | OrgrimmarDepths |
| `carte_monde/2021//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | thetempleofatalhakkar |
| `carte_monde/2022//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Northrend2 |
| `carte_monde/2023//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | deepruntram |
| `carte_monde/2024//area_name` | garder_anglais | nom technique (carte de développement, de test ou interne) | TorWatha |
| `carte_monde/2025//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | OrgrimmarDepthsUnderroof |
| `carte_monde/2026//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | StormwindSewersShade |
| `carte_monde/2027//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | ShadewellSpring |
| `carte_monde/2028//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | SecretInquisitorialDungeon |
| `carte_monde/2029//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | SinisterLair |
| `carte_monde/2030//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MoonlitOssuary |
| `carte_monde/2032//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | DeepInquisitorialVaults |
| `carte_monde/2033//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | VoodooRoadToDeOtherSide |
| `carte_monde/2034//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Silithusboss |
| `carte_monde/2035//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Aszharaboss |
| `carte_monde/2036//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | kazzakbossmap |
| `carte_monde/2037//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | soggothbossmap |
| `carte_monde/2038//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | DepthbreakerHollow |
| `carte_monde/2039//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | DepthbreakerHollow |
| `carte_monde/2040//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Emerissbossmap |
| `carte_monde/2041//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Taerarbossmap |
| `carte_monde/2042//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Ysondrebossmap |
| `carte_monde/2043//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Lethonbossmap |
| `carte_monde/2044//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Minigamesmap |
| `carte_monde/2045//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Rainbowrace |
| `carte_monde/2046//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesWonka |
| `carte_monde/2047//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Minigamesvoid |
| `carte_monde/2048//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesDuckHunt |
| `carte_monde/2049//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesBulletRomper |
| `carte_monde/2050//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesVerticalAscend |
| `carte_monde/2051//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesKulTiranAscent |
| `carte_monde/3039//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | DepthbreakerHollow |
| `carte_monde/3043//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | DepthbreakerHollow |
| `zone_interieure/34589//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cryptes de Karazhan » | Karazhan Crypts |

## zones / zones_003

| Clé | Genre | Raison | Anglais |
|---|---|---|---|
| `canal/2//name` | doute | nom de canal de discussion de CoA, sans forme officielle dans nos sources ; proposition : « Nouveaux venus » (à vérifier : le nom de canal sert aussi à /join) | Newcomers |
| `canal/2//shortcut` | doute | nom de canal de discussion de CoA, sans forme officielle dans nos sources ; proposition : « Nouveaux venus » (à vérifier : le nom de canal sert aussi à /join) | Newcomers |
| `canal/3//name` | garder_anglais | « Zone » est déjà français ; nom de canal | Zone - %s |
| `canal/3//shortcut` | garder_anglais | « Zone » est déjà français ; raccourci de canal | Zone |
| `canal/5//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; abréviation de canal inconnue | pol |
| `canal/5//shortcut` | garder_anglais | nom technique (carte de développement, de test ou interne) ; abréviation de canal inconnue | pol |
| `carte_monde/2052//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesMechagnomicAscent |
| `carte_monde/2053//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesVolcanicAscent |
| `carte_monde/2054//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesNagaAscent |
| `carte_monde/2055//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesZandalariAscent |
| `carte_monde/2056//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesLegionAscent |
| `carte_monde/2057//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesDarkIronAscent |
| `carte_monde/2058//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesEmeraldAscent |
| `carte_monde/2059//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | MinigamesTitanicAscent |
| `carte_monde/2060//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Frostgiantnbossmap |
| `carte_monde/2061//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | EasternPlaguelandsboss |
| `carte_monde/3041//area_name` | garder_anglais | nom interne de WorldMapArea (dossier des textures de la carte), jamais affiché en jeu | Zanzasisle |
| `point_carte/2762//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2763//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2764//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2765//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2766//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2767//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2768//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2769//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2770//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2771//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2772//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2773//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2774//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2775//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2776//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2777//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Porte démoniaque » | Demonic Gateway |
| `point_carte/2786//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Portail de commutation gangrené » | Fel Commutation Portal |
| `point_carte/2787//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Portail de commutation gangrené » | Fel Commutation Portal |
| `point_carte/2788//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Portail de commutation gangrené » | Fel Commutation Portal |
| `point_carte/2789//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Portail de commutation gangrené » | Fel Commutation Portal |
| `point_carte/2790//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Portail de commutation gangrené » | Fel Commutation Portal |
| `point_carte/2791//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Portail de commutation gangrené » | Fel Commutation Portal |
| `point_carte/2845//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Perchoir du braconnier » | Poacher's Perch |
| `point_carte/2846//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Bastion de Morvath » | Morvath's Hold |
| `point_carte/2847//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Miljak » | Miljak's Laboratory |
| `point_carte/2848//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Poste d'exorcisme des croisés » | Crusader's Exorcism Post |
| `point_carte/2849//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Refuge du collectionneur » | Collectors Refuge |
| `point_carte/2851//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Bastion d'Everburn » | Everburn Hold |
| `point_carte/2853//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des Défias » | Defias Tower |
| `point_carte/2858//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour du mage rouge » | Red Mage Tower |
| `point_carte/2859//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Sanctuaire de Moonrest » | Moonrest Sanctuary |
| `point_carte/2860//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Brasserie du Frère » | Brother's Tapworks |
| `point_carte/2861//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bastion du bandit » | Bandit's Bastion |
| `point_carte/2863//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `point_carte/2865//name` | garder_anglais | nom propre inventé par CoA | Shal'Athil |
| `point_carte/2870//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Charstone » ; attention, noms_officiels.tsv donne à tort « Chemin de l'Aile de la terreur » (archive, zone 10421) | Charstone Keep |
| `point_carte/2871//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Charstone » ; attention, noms_officiels.tsv donne à tort « Chemin de l'Aile de la terreur » (archive, zone 10421) | Charstone Keep |
| `point_carte/2872//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Charstone » ; attention, noms_officiels.tsv donne à tort « Chemin de l'Aile de la terreur » (archive, zone 10421) | Charstone Keep |
| `point_carte/2874//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Vestiges de Thel'dralor » | Remnants of Thel'dralor |
| `point_carte/2875//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Vestiges de Thel'dralor » | Remnants of Thel'dralor |
| `point_vol/378//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; point de vol d'une carte de transport | Battle Royal Map - The Royal Breaker |
| `point_vol/397//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Sargeras - Warfare Battle Scenario - Enemy Ship1 |
| `point_vol/398//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Sargeras - Warfare Battle Scenario - Enemy Ship2 |
| `point_vol/399//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Sargeras - Warfare Battle Scenario - Player Ship |
| `point_vol/409//name` | garder_anglais | noms officiels identiques en français (Kharanos, Dun Morogh) | Kharanos, Dun Morogh |
| `point_vol/411//name` | garder_anglais | noms officiels identiques en français (Dolanaar, Teldrassil) | Dolanaar, Teldrassil |
| `point_vol/418//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; point de vol de transport de quête | Quest Upon Daarns - Scadeald - Start |
| `point_vol/419//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; point de vol de transport de quête | Quest Upon Daarns - Scadeald - End |
| `point_vol/420//name` | garder_anglais | nom propre inventé par CoA | Graysky, Scadeald |
| `point_vol/421//name` | garder_anglais | nom propre inventé par CoA | Dun Kazad, Scadeald |
| `point_vol/442//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; point de vol de transport interne au donjon | Black Temple - Transport after Teron - Start |
| `point_vol/443//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; point de vol de transport interne au donjon | Black Temple - Transport after Teron - End |
| `point_vol/444//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; point de vol de transport interne au donjon | Black Temple - Transport after Reliquary - Start |
| `point_vol/445//name` | garder_anglais | nom technique (carte de développement, de test ou interne) ; point de vol de transport interne au donjon | Black Temple - Transport after Reliquary - End |
| `point_vol/448//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | MAX VALUE - NEVER GO ABOVE 448 Sargeras - Warfare Battle Scenario |
| `zone_interieure/33568//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Miljak » | Miljak's Laboratory |
| `zone_interieure/34913//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tombe des Impénitents » | Tomb of the Unrepentant |
| `zone_interieure/48103//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Chambre d'incinération » | Chamber of Incineration |
| `zone_interieure/48105//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Salles de l'Éveil » | Halls of Awakening |
| `zone_interieure/48106//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Forge du Crépuscule » | Twilight Forge |
| `zone_interieure/48107//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cicatrice du Brise-monde » | Scar of the Worldbreaker |
| `zone_interieure/49500//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49501//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49502//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49503//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49504//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49505//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49506//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49507//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour du mage rouge » | Red Mage Tower |
| `zone_interieure/49508//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour du mage rouge » | Red Mage Tower |
| `zone_interieure/49509//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour du mage rouge » | Red Mage Tower |
| `zone_interieure/49510//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour du mage rouge » | Red Mage Tower |
| `zone_interieure/49511//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour du mage rouge » | Red Mage Tower |
| `zone_interieure/49512//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour du mage rouge » | Red Mage Tower |
| `zone_interieure/49513//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour du mage rouge » | Red Mage Tower |
| `zone_interieure/49514//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49515//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49516//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49517//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49518//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Tombshade » | Tombshade Laboratory |
| `zone_interieure/49519//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Brasserie du Frère » | Brother’s Tapworks |
| `zone_interieure/49531//name` | garder_anglais | nom propre inventé par CoA | Vardeheim |
| `zone_interieure/49532//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Couloir » | Hallway |
| `zone_interieure/49533//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Refuge du collectionneur » | The Collectors Refuge |
| `zone_interieure/49534//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Refuge du collectionneur » | The Collectors Refuge |
| `zone_interieure/49535//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Refuge du collectionneur » | The Collectors Refuge |
| `zone_interieure/49536//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Miljak » | Miljak's Laboratory |
| `zone_interieure/49537//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Miljak » | Miljak's Laboratory |
| `zone_interieure/49538//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Miljak » | Miljak's Laboratory |
| `zone_interieure/49539//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Miljak » | Miljak's Laboratory |
| `zone_interieure/49540//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Miljak » | Miljak's Laboratory |
| `zone_interieure/49541//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Miljak » | Miljak's Laboratory |
| `zone_interieure/49542//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Miljak » | Miljak's Laboratory |
| `zone_interieure/49543//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des Défias » | Defias Tower |
| `zone_interieure/49544//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des Défias » | Defias Tower |
| `zone_interieure/49545//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des Défias » | Defias Tower |
| `zone_interieure/49546//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des Défias » | Defias Tower |
| `zone_interieure/49547//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des Défias » | Defias Tower |
| `zone_interieure/49548//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des Défias » | Defias Tower |
| `zone_interieure/49549//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour des Défias » | Defias Tower |
| `zone_interieure/50668//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Antre de Beauté » | Beauty's Lair |
| `zone_interieure/51174//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Forge Gueule-de-dragon » | Dragonmaw Forge |
| `zone_interieure/52271//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Passage clandestin » | Clandestine Passage |
| `zone_interieure/52274//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Palissade des fugitifs » | Fugitives' Stockade |
| `zone_interieure/52275//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Taverne de Stormwater » | Stormwater Tavern |
| `zone_interieure/52276//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Salle « Le Schisme » » | "The Schism" Room |
| `zone_interieure/52282//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Entrée du port » | Harbor Entrance |
| `zone_interieure/52283//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52284//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Gorges noyées » | Drowned Gorges |
| `zone_interieure/52285//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Maisons sèches » | The Dry Homes |
| `zone_interieure/52286//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Maisons sèches » | The Dry Homes |
| `zone_interieure/52287//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Cereza » | Cereza's Den |
| `zone_interieure/52291//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cimetière des trams » | Trams Graveyard |
| `zone_interieure/52292//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Salle de pause » | Break Lounge |
| `zone_interieure/52293//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Couloir de l'usine » | Factory Corridor |
| `zone_interieure/52294//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Couloir de l'usine » | Factory Corridor |
| `zone_interieure/52295//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Couloir de l'usine » | Factory Corridor |
| `zone_interieure/52296//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Couloir de l'usine » | Factory Corridor |
| `zone_interieure/52297//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Usine Bulletsmith » | Bulletsmith Factory |
| `zone_interieure/52298//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Usine Bulletsmith » | Bulletsmith Factory |
| `zone_interieure/52299//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Allée des Étincelles » | Sparks Alley |
| `zone_interieure/52300//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Usine Bulletsmith » | Bulletsmith Factory |
| `zone_interieure/52301//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Couloir de l'usine » | Factory Corridor |
| `zone_interieure/52302//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Maisons sèches » | The Dry Homes |
| `zone_interieure/52303//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cimetière des trams » | Trams Graveyard |
| `zone_interieure/52304//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Anciennes cryptes de Hurlevent » | Ancient Crypts of Stormwind |
| `zone_interieure/52305//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Anciennes cryptes de Hurlevent » | Ancient Crypts of Stormwind |
| `zone_interieure/52306//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Anciennes cryptes de Hurlevent » | Ancient Crypts of Stormwind |
| `zone_interieure/52307//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Anciennes cryptes de Hurlevent » | Ancient Crypts of Stormwind |
| `zone_interieure/52308//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Anciennes cryptes de Hurlevent » | Ancient Crypts of Stormwind |
| `zone_interieure/52309//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Anciennes cryptes de Hurlevent » | Ancient Crypts of Stormwind |
| `zone_interieure/52310//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Anciennes cryptes de Hurlevent » | Ancient Crypts of Stormwind |
| `zone_interieure/52311//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Anciennes cryptes de Hurlevent » | Ancient Crypts of Stormwind |
| `zone_interieure/52312//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Anciennes cryptes de Hurlevent » | Ancient Crypts of Stormwind |
| `zone_interieure/52314//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Palissade des fugitifs » | Fugitives' Stockade |
| `zone_interieure/52315//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52316//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Gorges noyées » | Drowned Gorges |
| `zone_interieure/52317//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Usine Bulletsmith » | Bulletsmith Factory |
| `zone_interieure/52319//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Gorges noyées » | Drowned Gorges |
| `zone_interieure/52321//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52322//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Maisons sèches » | The Dry Homes |
| `zone_interieure/52323//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Maisons sèches » | The Dry Homes |
| `zone_interieure/52324//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52325//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52326//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52327//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52328//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52329//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52330//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Fosse septique de Hurlevent » | Stormwind Septic Tank |
| `zone_interieure/52357//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Allée de la course d'escargots » | Snail Race Alley |
| `zone_interieure/52358//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Allée de la course d'escargots » | Snail Race Alley |
| `zone_interieure/52359//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Allée de la course d'escargots » | Snail Race Alley |
| `zone_interieure/52360//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Allée de la course d'escargots » | Snail Race Alley |
| `zone_interieure/52408//name` | doute | lieu CoA (mini-jeu) ; l'archive donne « Ascension Kul Tiran » (zone CoA, état machine) ; proposition : « Ascension kultirassienne » | Kul Tiran Ascent |
| `zone_interieure/52409//name` | doute | lieu CoA (mini-jeu) ; l'archive donne « Ascension Kul Tiran » (zone CoA, état machine) ; proposition : « Ascension kultirassienne » | Kul Tiran Ascent |
| `zone_interieure/52410//name` | doute | lieu CoA (mini-jeu) ; l'archive donne « Ascension Kul Tiran » (zone CoA, état machine) ; proposition : « Ascension kultirassienne » | Kul Tiran Ascent |
| `zone_interieure/52411//name` | doute | lieu CoA (mini-jeu) ; l'archive donne « Ascension Mécagnomique » (zone CoA, état machine) ; proposition : « Ascension mécagnome » | Mechagnomic Ascent |
| `zone_interieure/52412//name` | doute | lieu CoA (mini-jeu) ; l'archive donne « Ascension Mécagnomique » (zone CoA, état machine) ; proposition : « Ascension mécagnome » | Mechagnomic Ascent |
| `zone_interieure/52413//name` | doute | lieu CoA (mini-jeu) ; l'archive donne « Ascension Mécagnomique » (zone CoA, état machine) ; proposition : « Ascension mécagnome » | Mechagnomic Ascent |
| `zone_interieure/52414//name` | doute | lieu CoA (mini-jeu) ; l'archive donne à tort « Ascension du Titanic » (zone CoA, état machine) ; proposition : « Ascension titanesque » | Titanic Ascent |
| `zone_interieure/52415//name` | doute | lieu CoA (mini-jeu) ; l'archive donne à tort « Ascension du Titanic » (zone CoA, état machine) ; proposition : « Ascension titanesque » | Titanic Ascent |
| `zone_interieure/52416//name` | doute | lieu CoA (mini-jeu) ; l'archive donne à tort « Ascension du Titanic » (zone CoA, état machine) ; proposition : « Ascension titanesque » | Titanic Ascent |
| `zone_interieure/52435//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Lava Pools |
| `zone_interieure/52436//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Magma 3 |
| `zone_interieure/52437//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Slow Magma 7 |
| `zone_interieure/52438//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Fast Magma 11 |
| `zone_interieure/52439//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Green lava 15 |
| `zone_interieure/52440//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | wmo lava 19 |
| `zone_interieure/52441//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | CoA Black-Magma 121 |
| `zone_interieure/52442//name` | garder_anglais | nom technique (carte de développement, de test ou interne) | Chamber Magma 141 |
| `zone_interieure/52485//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Vil the Squint » | Vil the Squint’s Den |
| `zone_interieure/52486//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Vil the Squint » | Vil the Squint’s Den |
| `zone_interieure/52487//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Passage vers les docks » | Passage to the Docks |
| `zone_interieure/52488//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Passage vers les docks » | Passage to the Docks |
| `zone_interieure/52489//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Escalier de la suite de la duchesse » | Stairway to the Duchess' Suite |
| `zone_interieure/52490//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Lucranta » | Lucranta's Den |
| `zone_interieure/52493//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Quartier général de Darts » | Darts' Headquarters |
| `zone_interieure/52494//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « L'Auberge des Braises » | The Embers Inn |
| `zone_interieure/52499//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « L'Auberge des Braises » | The Embers Inn |
| `zone_interieure/52500//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « L'Auberge des Braises » | The Embers Inn |
| `zone_interieure/52504//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Passe creusée » | Hollowed Pass |
| `zone_interieure/52505//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Fondations » | The Foundation |
| `zone_interieure/52508//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Docks d'Orgrimmar » | Orgrimmar Docks |
| `zone_interieure/52510//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « L'Auberge des Braises » | The Embers Inn |
| `zone_interieure/52511//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Banque Latch » | Latch Bank |
| `zone_interieure/52512//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Banque Latch » | Latch Bank |
| `zone_interieure/52514//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Grenier de Gillsplitter » | Gillsplitter Attic |
| `zone_interieure/52516//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Lucranta » | Lucranta's Den |
| `zone_interieure/52541//name` | garder_anglais | nom officiel identique (SI:7) | SI: 7 |
| `zone_interieure/52544//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour de garde » | Guard's Tower |
| `zone_interieure/52545//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour de garde » | Guard's Tower |
| `zone_interieure/52546//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour de garde » | Guard's Tower |
| `zone_interieure/52566//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Vil the Squint » | Vil the Squint’s Den |
| `zone_interieure/52567//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Vil the Squint » | Vil the Squint’s Den |
| `zone_interieure/52568//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Passage vers les docks » | Passage to the Docks |
| `zone_interieure/52569//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Passage vers les docks » | Passage to the Docks |
| `zone_interieure/52570//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Escalier de la suite de la duchesse » | Stairway to the Duchess' Suite |
| `zone_interieure/52571//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Lucranta » | Lucranta's Den |
| `zone_interieure/52574//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Quartier général de Darts » | Darts' Headquarters |
| `zone_interieure/52575//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « L'Auberge des Braises » | The Embers Inn |
| `zone_interieure/52580//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « L'Auberge des Braises » | The Embers Inn |
| `zone_interieure/52581//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « L'Auberge des Braises » | The Embers Inn |
| `zone_interieure/52585//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Passe creusée » | Hollowed Pass |
| `zone_interieure/52586//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Fondations » | The Foundation |
| `zone_interieure/52589//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Docks d'Orgrimmar » | Orgrimmar Docks |
| `zone_interieure/52591//name` | doute | lieu CoA descriptif, et « Ember » est la question ouverte 20 (A_TRANCHER) ; proposition : « L'Auberge des Braises » | The Embers Inn |
| `zone_interieure/52592//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Banque Latch » | Latch Bank |
| `zone_interieure/52593//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Banque Latch » | Latch Bank |
| `zone_interieure/52595//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Grenier de Gillsplitter » | Gillsplitter Attic |
| `zone_interieure/52597//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Antre de Lucranta » | Lucranta's Den |
| `zone_interieure/52663//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Laboratoire de Priscilla » | Priscilla's Laboratory |
| `zone_interieure/52669//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52670//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52671//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52672//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52673//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52674//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52675//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52676//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52677//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52678//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52679//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52680//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cellules du Saint-Office » | Holy Office Cells |
| `zone_interieure/52681//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Galeries de Darkcandle » | Darkcandle Galleries |
| `zone_interieure/52682//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Galeries de Darkcandle » | Darkcandle Galleries |
| `zone_interieure/52683//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Galeries de Darkcandle » | Darkcandle Galleries |
| `zone_interieure/52684//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Galeries de Darkcandle » | Darkcandle Galleries |
| `zone_interieure/52685//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Galeries de Darkcandle » | Darkcandle Galleries |
| `zone_interieure/52686//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Galeries de Darkcandle » | Darkcandle Galleries |
| `zone_interieure/52687//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Galeries de Darkcandle » | Darkcandle Galleries |
| `zone_interieure/52688//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Galeries de Darkcandle » | Darkcandle Galleries |
| `zone_interieure/52689//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Galeries de Darkcandle » | Darkcandle Galleries |
| `zone_interieure/52690//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Quartiers de l'Inquisition » | Inquisition Quarters |
| `zone_interieure/52691//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Quartiers de l'Inquisition » | Inquisition Quarters |
| `zone_interieure/52692//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Cage du Trompeur » | The Deceiver’s Cage |
| `zone_interieure/52706//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Grotte de l'Anticipation » | Cave of Anticipation |
| `zone_interieure/52707//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Toits ruisselants » | The Dripping Roofs |
| `zone_interieure/52708//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Les Toits ruisselants » | The Dripping Roofs |
| `zone_interieure/52709//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Nid » |  The Nest |
| `zone_interieure/52710//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Garennes d'Underroot » | Underroot Warrens |
| `zone_interieure/52711//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Terrier » | The Burrow |
| `zone_interieure/52712//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Dernier sépulcre » | The Last Sepulcher |
| `zone_interieure/53332//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « La Caldeira vivante » | The Living Caldera |
| `zone_interieure/53389//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Salles d'expérimentation » | Halls of Experimentation |
| `zone_interieure/53390//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Salles d'expérimentation » | Halls of Experimentation |
| `zone_interieure/53391//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Salles d'expérimentation » | Halls of Experimentation |
| `zone_interieure/53392//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Repaire du Sujet zéro » | Subject Zero's Lair |
| `zone_interieure/53393//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Repaire du Sujet zéro » | Subject Zero's Lair |
| `zone_interieure/53394//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Repaire du Sujet zéro » | Subject Zero's Lair |
| `zone_interieure/53397//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bastion d'élevage de griffons » | Gryphon Breeding Bastion |
| `zone_interieure/53400//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Moulin de Dunshire » | Dunshire Windmill |
| `zone_interieure/53407//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Ancienne église de Cresthairn » | Cresthairn Ancient Church |
| `zone_interieure/53432//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Grotte de Nightweave » | Nightweave Cave |
| `zone_interieure/53436//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Grotte déchiquetée » | Jagged Cave |
| `zone_interieure/53467//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Chemin du Chant doré » | Gilded Song Path |
| `zone_interieure/53472//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Chambres d'Erdaya » | Chambers of Erdaya |
| `zone_interieure/53481//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Caverne d'Eldigh » | Cavern of Eldigh |
| `zone_interieure/53496//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Passe d'Ealdfrost » | Ealdfrost Pass |
| `zone_interieure/53500//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Mine d'Ironbough » | Ironbough Mine |
| `zone_interieure/53526//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Entrée de Comté-de-l'Or » | Goldshire Entrance |
| `zone_interieure/53535//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Grotte de Shadewell » | Shadewell Cave |
| `zone_interieure/53544//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Grottes de Zuramunda » | Zuramunda Caves |
| `zone_interieure/53562//name` | garder_anglais | nom propre inventé par CoA | Grimepit |
| `zone_interieure/53594//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Bar-Tabasse de Bizmo » | Bizmo's Brawlpub |
| `zone_interieure/53595//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Arène du Bar-Tabasse de Bizmo » | Bizmo's Brawlpub Arena |
| `zone_interieure/53597//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Mine de Rockrend » | Rockrend Mine |
| `zone_interieure/53627//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Tour de garde battue par les vents » | Windswept Guardtower |
| `zone_interieure/53651//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Abbaye du Vent sacré » | Hallow Wind Abbey |
| `zone_interieure/53697//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53698//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53699//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53700//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53701//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53702//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53703//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53704//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53705//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53706//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53707//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53708//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53709//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53710//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Donjon de Coldmere » | Coldmere Keep |
| `zone_interieure/53711//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Chapelle de la Lumière » | Chapel of Light |
| `zone_interieure/53714//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Auberge du Freux plumé » | The Plucked Rook Inn |
| `zone_interieure/53715//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Remède de grand-mère » | Grandmother's Remedy |
| `zone_interieure/53716//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Remède de grand-mère » | Grandmother's Remedy |
| `zone_interieure/53717//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Remède de grand-mère » | Grandmother's Remedy |
| `zone_interieure/53718//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Remède de grand-mère » | Grandmother's Remedy |
| `zone_interieure/53720//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cryptes du Vent sacré » | Hallow Wind Crypts |
| `zone_interieure/53768//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Grotte des bandits » | Bandit Cave |
| `zone_interieure/53779//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Creux des Trois Sœurs » | Three Sisters Hollow |
| `zone_interieure/53788//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Temple d'Anzuldin » | Temple of Anzuldin |
| `zone_interieure/53837//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Grotte de Flamehowl » | Flamehowl Cave |
| `zone_interieure/53844//name` | garder_anglais | nom propre inventé par CoA ; partie descriptive : « Repaire de Skulltaken » | Skulltaken Lair |
| `zone_interieure/53847//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Le Repaire douillet » | The Cozy Den |
| `zone_interieure/65677//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Cryptes du Sépulcre » | Sepulcher Crypts |
| `zone_interieure/65713//name` | doute | lieu CoA descriptif, sans nom officiel prouvé ; proposition : « Temple du pont » | Bridge Temple |

