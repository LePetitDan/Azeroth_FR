//! Les voix françaises, en option : le doublage français d'origine des personnages, posé en fichiers libres dans
//! `Sound\` (le jeu les lit à la place de ses voix anglaises, sans qu'aucun de ses fichiers soit modifié).
//!
//! Le pack n'est pas dans l'installateur : il est téléchargé depuis sa propre page (dépôt séparé de l'add-on), sa
//! taille et son empreinte sont vérifiées, et la liste de ce qui a été posé est gardée dans `Sound\Azeroth_FR_voix.txt`
//! pour pouvoir tout retirer. Un téléchargement interrompu reprend où il s'était arrêté.

use crate::installation::{dossier_valide, expliquer, jeu_ouvert};
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::fs;
use std::io::{BufReader, BufWriter, Read, Write};
use std::path::{Path, PathBuf};
use std::time::Duration;

pub const VERSION: &str = "voix-1.1";
const ADRESSE: &str = "https://github.com/LePetitDan/AscensionFR-Voix/releases/download/voix-1.1/AscensionFR_Voix.zip";
pub const TAILLE: u64 = 1_504_623_290;
const EMPREINTE: &str = "137ca233c790acd7ea01d543cd4d771bb6d47542a21819cff5cda053f07ca48e";
/// Place prise dans le jeu une fois les voix posées, et place nécessaire pendant l'installation (pack + voix).
pub const SUR_LE_DISQUE: u64 = 1_727_608_064;
const LISTE: &str = "Azeroth_FR_voix.txt";
const TELECHARGEMENT: &str = "Azeroth_FR_voix.telechargement";
const INCOMPLET: &str = " incomplet";

fn liste(dossier: &Path) -> PathBuf {
    sous_dossier_son(dossier).join(LISTE)
}

/// Le dossier `Sound` du jeu, sous le nom qu'il porte déjà (sous Linux, `sound` et `Sound` sont deux dossiers).
fn sous_dossier_son(dossier: &Path) -> PathBuf {
    existant(dossier, "Sound").unwrap_or_else(|| dossier.join("Sound"))
}

/// L'entrée de `parent` qui porte ce nom, sans tenir compte des majuscules.
fn existant(parent: &Path, nom: &str) -> Option<PathBuf> {
    let direct = parent.join(nom);
    if direct.exists() {
        return Some(direct);
    }
    if cfg!(windows) {
        return None;
    }
    fs::read_dir(parent).ok()?.flatten().find(|e| e.file_name().to_string_lossy().eq_ignore_ascii_case(nom)).map(|e| e.path())
}

/// La version des voix installées par cet assistant, s'il y en a une (et si l'installation est allée au bout).
pub fn installees(dossier: &Path) -> Option<String> {
    let t = fs::read_to_string(liste(dossier)).ok()?;
    let premiere = t.lines().next()?.trim();
    (!premiere.is_empty() && !premiere.ends_with(INCOMPLET.trim())).then(|| premiere.to_string())
}

/// Des voix posées par cet assistant sont-elles dans le jeu, même en partie ?
pub fn presentes(dossier: &Path) -> bool {
    liste(dossier).is_file()
}

fn agent() -> ureq::Agent {
    ureq::AgentBuilder::new()
        .try_proxy_from_env(true)
        .timeout_connect(Duration::from_secs(10))
        .timeout_read(Duration::from_secs(60))
        .user_agent(concat!("Azeroth_FR-Installateur/", env!("CARGO_PKG_VERSION")))
        .build()
}

/// Une taille en gigaoctets, écrite à la française (« 1,40 »).
pub fn go(n: u64, decimales: usize) -> String {
    format!("{:.*}", decimales, n as f64 / 1_073_741_824.0).replace('.', ",")
}

/// Télécharge le pack dans le dossier du jeu (en reprenant un téléchargement interrompu), vérifie sa taille et son
/// empreinte. Renvoie le chemin du fichier.
fn telecharger(dossier: &Path, progres: &dyn Fn(f32, &str)) -> Result<PathBuf, String> {
    let chemin = dossier.join(TELECHARGEMENT);
    let mut somme = Sha256::new();
    let mut deja = fs::metadata(&chemin).map(|m| m.len()).unwrap_or(0);
    if deja > TAILLE {
        deja = 0;
    }
    let mut bloc = vec![0u8; 1024 * 1024];
    if deja > 0 {
        // ce qui est déjà là entre dans l'empreinte
        progres(0.0, "Reprise du téléchargement des voix…");
        let mut f = fs::File::open(&chemin).map_err(|e| expliquer("Impossible de relire le téléchargement des voix", &e))?;
        loop {
            let n = f.read(&mut bloc).map_err(|e| expliquer("Impossible de relire le téléchargement des voix", &e))?;
            if n == 0 {
                break;
            }
            somme.update(&bloc[..n]);
        }
    }
    if deja < TAILLE {
        let mut requete = agent().get(ADRESSE);
        if deja > 0 {
            requete = requete.set("Range", &format!("bytes={}-", deja));
        }
        let rep = requete.call().map_err(|e| format!("téléchargement impossible ({})", e))?;
        let reprise = rep.status() == 206;
        if deja > 0 && !reprise {
            // le serveur renvoie tout : on repart de zéro
            deja = 0;
            somme = Sha256::new();
        }
        let f = fs::OpenOptions::new()
            .create(true)
            .write(true)
            .append(reprise)
            .truncate(!reprise)
            .open(&chemin)
            .map_err(|e| expliquer("Impossible d'écrire le téléchargement des voix", &e))?;
        let mut f = BufWriter::new(f);
        let mut lecteur = rep.into_reader().take(TAILLE - deja);
        let mut recu = deja;
        loop {
            let n = lecteur.read(&mut bloc).map_err(|e| format!("téléchargement interrompu ({})", e))?;
            if n == 0 {
                break;
            }
            f.write_all(&bloc[..n]).map_err(|e| expliquer("Impossible d'écrire le téléchargement des voix", &e))?;
            somme.update(&bloc[..n]);
            recu += n as u64;
            progres(
                recu as f32 / TAILLE as f32,
                &format!("Téléchargement des voix françaises : {} Go sur {}", go(recu, 2), go(TAILLE, 2)),
            );
        }
        f.flush().map_err(|e| expliquer("Impossible d'écrire le téléchargement des voix", &e))?;
        if recu != TAILLE {
            return Err("téléchargement interrompu".into());
        }
    }
    let obtenue: String = somme.finalize().iter().map(|o| format!("{:02x}", o)).collect();
    if obtenue != EMPREINTE {
        let _ = fs::remove_file(&chemin);
        return Err("le fichier téléchargé ne correspond pas à son empreinte ; il a été effacé".into());
    }
    Ok(chemin)
}

/// Le chemin d'une entrée du pack, en morceaux, si elle va dans `Sound` (le reste du pack n'est pas posé).
fn morceaux(nom: &str) -> Option<Vec<String>> {
    let m: Vec<String> = nom.replace('\\', "/").split('/').filter(|x| !x.is_empty()).map(|x| x.to_string()).collect();
    if m.len() < 2 || !m[0].eq_ignore_ascii_case("sound") {
        return None;
    }
    // jamais de remontée ni de chemin absolu
    if m.iter().any(|x| x == "." || x == ".." || x.contains(':')) {
        return None;
    }
    Some(m[1..].to_vec())
}

/// Pose les voix depuis le pack `zip` : extrait ce qui va dans `Sound`, vérifie chaque fichier, tient la liste.
pub fn poser(dossier: &Path, zip: &Path, progres: &dyn Fn(f32, &str)) -> Result<usize, String> {
    let f = fs::File::open(zip).map_err(|e| expliquer("Impossible d'ouvrir le pack de voix", &e))?;
    let mut archive = zip::ZipArchive::new(BufReader::new(f)).map_err(|e| format!("Pack de voix illisible : {}", e))?;
    let son = sous_dossier_son(dossier);
    fs::create_dir_all(&son).map_err(|e| expliquer(&format!("Impossible de créer {}", son.display()), &e))?;
    // dossiers déjà rencontrés (chemin en minuscules → dossier réel) : « Creature » et « CREATURE » ne font qu'un
    let mut dossiers: HashMap<String, PathBuf> = HashMap::new();
    let mut poses: HashMap<String, String> = HashMap::new();
    let total = archive.len();
    let ecrire_liste = |poses: &HashMap<String, String>, fin: bool| -> Result<(), String> {
        let mut lignes: Vec<&String> = poses.values().collect();
        lignes.sort();
        let mut t = format!("{}{}\n", VERSION, if fin { "" } else { INCOMPLET });
        for l in lignes {
            t.push_str(l);
            t.push('\n');
        }
        fs::write(son.join(LISTE), t).map_err(|e| expliquer("Impossible d'écrire la liste des voix", &e))
    };
    ecrire_liste(&poses, false)?;
    for i in 0..total {
        let mut entree = archive.by_index(i).map_err(|e| format!("Pack de voix illisible : {}", e))?;
        if entree.is_dir() {
            continue;
        }
        let Some(m) = morceaux(entree.name()) else { continue };
        let (nom, chemin_dossier) = m.split_last().unwrap();
        let mut reel = son.clone();
        let mut cle = String::new();
        for d in chemin_dossier {
            cle.push_str(&d.to_lowercase());
            cle.push('/');
            reel = match dossiers.get(&cle) {
                Some(p) => p.clone(),
                None => {
                    let p = existant(&reel, d).unwrap_or_else(|| reel.join(d));
                    fs::create_dir_all(&p).map_err(|e| expliquer(&format!("Impossible de créer {}", p.display()), &e))?;
                    dossiers.insert(cle.clone(), p.clone());
                    p
                }
            };
        }
        let cle_fichier = format!("{}{}", cle, nom.to_lowercase());
        let cible = existant(&reel, nom).unwrap_or_else(|| reel.join(nom));
        let attendu = entree.size();
        {
            let sortie = fs::File::create(&cible).map_err(|e| expliquer(&format!("Impossible d'écrire {}", cible.display()), &e))?;
            let mut sortie = BufWriter::new(sortie);
            std::io::copy(&mut entree, &mut sortie).map_err(|e| expliquer(&format!("Impossible d'écrire {}", cible.display()), &e))?;
            sortie.flush().map_err(|e| expliquer(&format!("Impossible d'écrire {}", cible.display()), &e))?;
        }
        if fs::metadata(&cible).map(|x| x.len()).unwrap_or(0) != attendu {
            return Err(format!("Fichier de voix incomplet : {}", cible.display()));
        }
        let relatif = cible.strip_prefix(&son).unwrap_or(&cible).to_string_lossy().replace('\\', "/");
        poses.insert(cle_fichier, relatif);
        if poses.len() % 500 == 0 {
            ecrire_liste(&poses, false)?;
        }
        if i % 50 == 0 || i + 1 == total {
            progres((i + 1) as f32 / total as f32, &format!("Mise en place des voix : {} fichiers sur {}", i + 1, total));
        }
    }
    if poses.is_empty() {
        return Err("Le pack de voix ne contient aucun fichier pour le dossier Sound.".into());
    }
    ecrire_liste(&poses, true)?;
    Ok(poses.len())
}

/// Installe les voix : téléchargement vérifié, mise en place, puis le pack téléchargé est effacé.
pub fn installer(dossier: &Path, progres: &dyn Fn(f32, &str)) -> Result<usize, String> {
    if !dossier_valide(dossier) {
        return Err("Ce dossier ne contient pas le jeu (Ascension.exe introuvable).".into());
    }
    if jeu_ouvert() {
        return Err("Le jeu est ouvert : fermez-le, puis recommencez.".into());
    }
    let zip = telecharger(dossier, &|f, m| progres(f * 0.8, m))?;
    let n = poser(dossier, &zip, &|f, m| progres(0.8 + f * 0.2, m))?;
    let _ = fs::remove_file(&zip);
    Ok(n)
}

/// Retire les voix posées par cet assistant (et seulement elles), les dossiers devenus vides, et un téléchargement
/// resté en plan. Renvoie le nombre de fichiers retirés.
pub fn retirer(dossier: &Path) -> Result<usize, String> {
    if jeu_ouvert() {
        return Err("Le jeu est ouvert : fermez-le, puis recommencez.".into());
    }
    let _ = fs::remove_file(dossier.join(TELECHARGEMENT));
    let son = sous_dossier_son(dossier);
    let Ok(t) = fs::read_to_string(son.join(LISTE)) else { return Ok(0) };
    let mut n = 0;
    let mut parents: Vec<PathBuf> = Vec::new();
    for l in t.lines().skip(1) {
        let l = l.trim();
        if l.is_empty() || l.split('/').any(|x| x == ".." || x == "." || x.contains(':')) || l.starts_with('/') {
            continue;
        }
        let p = son.join(l);
        if p.is_file() {
            fs::remove_file(&p).map_err(|e| expliquer(&format!("Impossible de retirer {}", p.display()), &e))?;
            n += 1;
        }
        let mut d = p.parent();
        while let Some(x) = d {
            if x == son || !x.starts_with(&son) {
                break;
            }
            if !parents.iter().any(|y| y == x) {
                parents.push(x.to_path_buf());
            }
            d = x.parent();
        }
    }
    fs::remove_file(son.join(LISTE)).map_err(|e| expliquer("Impossible de retirer la liste des voix", &e))?;
    // les dossiers les plus profonds d'abord ; remove_dir ne retire qu'un dossier vide
    parents.sort_by_key(|p| std::cmp::Reverse(p.components().count()));
    for d in parents {
        let _ = fs::remove_dir(&d);
    }
    let _ = fs::remove_dir(&son);
    Ok(n)
}

#[cfg(test)]
mod essais {
    use super::*;

    #[test]
    fn chemins_du_pack() {
        assert_eq!(morceaux("Sound/CREATURE/A/b.wav"), Some(vec!["CREATURE".to_string(), "A".to_string(), "b.wav".to_string()]));
        assert_eq!(morceaux("sound\\creature\\a\\b.wav").map(|m| m.len()), Some(3));
        assert_eq!(morceaux("Wow.ini"), None);
        assert_eq!(morceaux("Sound/../Wow.exe"), None);
        assert_eq!(morceaux("Interface/AddOns/x.lua"), None);
        assert_eq!(morceaux("Sound/"), None);
    }
}
