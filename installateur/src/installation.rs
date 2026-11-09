//! Ce que fait l'installateur, sans fenêtre : trouver le dossier du jeu, installer, désinstaller.
//!
//! Il ne touche qu'à ce qui appartient à Azeroth_FR : les dossiers `Interface\AddOns\Azeroth_FR…` et, dans
//! `Interface\PTRXML`, `AzerothFR_Interface.lua` et le `PTR.xml` qui le charge. Un `PTR.xml` qui n'est pas le nôtre est
//! mis de côté (`PTR.xml.avant-azeroth-fr`) avant l'installation et remis en place à la désinstallation.

use std::fs;
use std::io::{Cursor, Read};
use std::path::{Path, PathBuf};

pub const ZIP: &[u8] = include_bytes!(env!("AZFR_ZIP"));
pub const VERSION: &str = env!("AZFR_VERSION");
const EXECUTABLES: [&str; 3] = ["Ascension.exe", "Wow.exe", "WoW.exe"];
const PTR_SAUVEGARDE: &str = "PTR.xml.avant-azeroth-fr";

pub fn dossier_valide(p: &Path) -> bool {
    EXECUTABLES.iter().any(|e| p.join(e).is_file())
}

/// Le dossier du jeu : celui mémorisé par l'installateur, sinon celui du lanceur de CoA (`installPath` de
/// `%APPDATA%\Conquest of AzerothCore\settings.json`), sinon le dossier de l'installateur s'il est dans le jeu.
pub fn detecter() -> Option<PathBuf> {
    let mut candidats = Vec::new();
    if let Some(p) = lire_memoire() {
        candidats.push(p);
    }
    let mut reglages_lanceur = Vec::new();
    if let Ok(appdata) = std::env::var("APPDATA") {
        reglages_lanceur.push(Path::new(&appdata).join("Conquest of AzerothCore").join("settings.json"));
    }
    if let Ok(home) = std::env::var("HOME") {
        reglages_lanceur.push(Path::new(&home).join(".config").join("Conquest of AzerothCore").join("settings.json"));
    }
    for reglages in reglages_lanceur {
        if let Ok(t) = fs::read_to_string(reglages) {
            if let Ok(v) = serde_json::from_str::<serde_json::Value>(&t) {
                if let Some(p) = v.get("installPath").and_then(|x| x.as_str()) {
                    candidats.push(PathBuf::from(p));
                }
            }
        }
    }
    if let Ok(exe) = std::env::current_exe() {
        if let Some(d) = exe.parent() {
            candidats.push(d.to_path_buf());
        }
    }
    candidats.into_iter().find(|p| dossier_valide(p))
}

fn fichier_memoire() -> Option<PathBuf> {
    let base = std::env::var("APPDATA")
        .map(PathBuf::from)
        .or_else(|_| std::env::var("HOME").map(|h| Path::new(&h).join(".config")))
        .ok()?;
    Some(base.join("Azeroth_FR").join("installateur.json"))
}

fn lire_memoire() -> Option<PathBuf> {
    let t = fs::read_to_string(fichier_memoire()?).ok()?;
    let v: serde_json::Value = serde_json::from_str(&t).ok()?;
    v.get("dossier")?.as_str().map(PathBuf::from)
}

pub fn memoriser(dossier: &Path) {
    if let Some(f) = fichier_memoire() {
        let _ = fs::create_dir_all(f.parent().unwrap());
        let _ = fs::write(f, serde_json::json!({ "dossier": dossier.to_string_lossy() }).to_string());
    }
}

/// Version d'Azeroth_FR déjà installée (ligne `## Version:` du fichier .toc), s'il y en a une.
pub fn version_installee(dossier: &Path) -> Option<String> {
    let toc = dossier.join("Interface").join("AddOns").join("Azeroth_FR").join("Azeroth_FR.toc");
    let t = fs::read_to_string(toc).ok()?;
    t.lines().find_map(|l| l.strip_prefix("## Version:").map(|v| v.trim().to_string()))
}

/// Le jeu est-il ouvert ? (Ascension.exe dans la liste des processus)
#[cfg(windows)]
pub fn jeu_ouvert() -> bool {
    use std::os::windows::process::CommandExt;
    const SANS_FENETRE: u32 = 0x0800_0000;
    std::process::Command::new("tasklist")
        .args(["/FI", "IMAGENAME eq Ascension.exe", "/NH", "/FO", "CSV"])
        .creation_flags(SANS_FENETRE)
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).to_lowercase().contains("ascension.exe"))
        .unwrap_or(false)
}

/// Sous Linux (Wine, Lutris, Steam/Proton) : un processus dont la ligne de commande contient Ascension.exe
#[cfg(not(windows))]
pub fn jeu_ouvert() -> bool {
    let Ok(it) = fs::read_dir("/proc") else { return false };
    it.flatten().any(|e| {
        e.file_name().to_string_lossy().chars().all(|c| c.is_ascii_digit())
            && fs::read(e.path().join("cmdline"))
                .map(|c| {
                    // un argument qui EST le jeu (« wine …/Ascension.exe »), pas une commande qui en parle
                    c.split(|&o| o == 0).any(|a| {
                        let a = String::from_utf8_lossy(a).to_lowercase();
                        a.trim_end().ends_with("ascension.exe")
                    })
                })
                .unwrap_or(false)
    })
}

pub struct Rapport {
    pub fichiers: usize,
    pub octets: u64,
    pub version: String,
    pub ptr_mis_de_cote: bool,
}

fn nos_dossiers(dossier: &Path) -> Vec<PathBuf> {
    let addons = dossier.join("Interface").join("AddOns");
    let mut v = Vec::new();
    if let Ok(it) = fs::read_dir(&addons) {
        for e in it.flatten() {
            let nom = e.file_name().to_string_lossy().to_string();
            if nom.starts_with("Azeroth_FR") && e.path().is_dir() {
                v.push(e.path());
            }
        }
    }
    v
}

fn ptr_est_le_notre(p: &Path) -> bool {
    fs::read_to_string(p).map(|t| t.contains("AzerothFR")).unwrap_or(false)
}

/// Installe (ou met à jour) : retire l'ancienne version, extrait le zip embarqué, vérifie chaque fichier.
pub fn installer(dossier: &Path, progres: &dyn Fn(f32, &str), retenir: bool) -> Result<Rapport, String> {
    if !dossier_valide(dossier) {
        return Err("Ce dossier ne contient pas le jeu (Ascension.exe introuvable).".into());
    }
    if jeu_ouvert() {
        return Err("Le jeu est ouvert : fermez-le, puis recommencez.".into());
    }
    progres(0.0, "Retrait de l'ancienne version…");
    for d in nos_dossiers(dossier) {
        fs::remove_dir_all(&d).map_err(|e| format!("Impossible de retirer {} : {}", d.display(), e))?;
    }
    let ptrxml = dossier.join("Interface").join("PTRXML");
    fs::create_dir_all(&ptrxml).map_err(|e| format!("Impossible de créer {} : {}", ptrxml.display(), e))?;
    let ptr = ptrxml.join("PTR.xml");
    let mut mis_de_cote = false;
    if ptr.is_file() && !ptr_est_le_notre(&ptr) {
        let sauvegarde = ptrxml.join(PTR_SAUVEGARDE);
        if !sauvegarde.exists() {
            fs::rename(&ptr, &sauvegarde).map_err(|e| format!("Impossible de mettre de côté PTR.xml : {}", e))?;
            mis_de_cote = true;
        }
    }
    let mut archive = zip::ZipArchive::new(Cursor::new(ZIP)).map_err(|e| format!("Archive illisible : {}", e))?;
    let total = archive.len();
    let (mut fichiers, mut octets) = (0usize, 0u64);
    for i in 0..total {
        let mut entree = archive.by_index(i).map_err(|e| format!("Archive illisible : {}", e))?;
        let relatif = match entree.enclosed_name() {
            Some(r) => r,
            None => return Err(format!("Chemin refusé dans l'archive : {}", entree.name())),
        };
        let cible = dossier.join(&relatif);
        if entree.is_dir() {
            fs::create_dir_all(&cible).map_err(|e| format!("{} : {}", cible.display(), e))?;
            continue;
        }
        if let Some(p) = cible.parent() {
            fs::create_dir_all(p).map_err(|e| format!("{} : {}", p.display(), e))?;
        }
        let mut contenu = Vec::with_capacity(entree.size() as usize);
        entree.read_to_end(&mut contenu).map_err(|e| format!("Archive illisible : {}", e))?;
        fs::write(&cible, &contenu).map_err(|e| format!("Impossible d'écrire {} : {}", cible.display(), e))?;
        let ecrit = fs::metadata(&cible).map(|m| m.len()).unwrap_or(0);
        if ecrit != contenu.len() as u64 {
            return Err(format!("Fichier incomplet : {}", cible.display()));
        }
        fichiers += 1;
        octets += ecrit;
        if i % 4 == 0 || i + 1 == total {
            let nom = relatif.components().nth(2).map(|c| c.as_os_str().to_string_lossy().to_string()).unwrap_or_default();
            progres((i + 1) as f32 / total as f32, &format!("Copie : {}", nom));
        }
    }
    let version = version_installee(dossier).ok_or("Installation incomplète : Azeroth_FR.toc introuvable.")?;
    if retenir {
        memoriser(dossier);
    }
    progres(1.0, "Terminé.");
    Ok(Rapport { fichiers, octets, version, ptr_mis_de_cote: mis_de_cote })
}

/// Désinstalle : retire nos dossiers et nos fichiers d'avant-jeu ; remet en place un PTR.xml mis de côté.
pub fn desinstaller(dossier: &Path) -> Result<usize, String> {
    if jeu_ouvert() {
        return Err("Le jeu est ouvert : fermez-le, puis recommencez.".into());
    }
    let mut n = 0;
    for d in nos_dossiers(dossier) {
        fs::remove_dir_all(&d).map_err(|e| format!("Impossible de retirer {} : {}", d.display(), e))?;
        n += 1;
    }
    let ptrxml = dossier.join("Interface").join("PTRXML");
    let lua = ptrxml.join("AzerothFR_Interface.lua");
    if lua.is_file() {
        fs::remove_file(&lua).map_err(|e| e.to_string())?;
        n += 1;
    }
    let ptr = ptrxml.join("PTR.xml");
    if ptr.is_file() && ptr_est_le_notre(&ptr) {
        fs::remove_file(&ptr).map_err(|e| e.to_string())?;
        n += 1;
    }
    let sauvegarde = ptrxml.join(PTR_SAUVEGARDE);
    if sauvegarde.is_file() && !ptr.exists() {
        fs::rename(&sauvegarde, &ptr).map_err(|e| e.to_string())?;
    }
    Ok(n)
}
