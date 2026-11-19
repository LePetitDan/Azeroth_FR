//! Mises à jour : l'installateur demande à GitHub la dernière version publiée d'Azeroth_FR ; s'il en existe une plus
//! récente que celle qu'il transporte, il télécharge son zip, vérifie son empreinte, et c'est elle qu'il installe.
//! Rien d'autre ne passe par le réseau, et sans connexion l'installateur installe la version qu'il transporte.
//!
//! (1.2.0) L'installateur se met aussi à jour LUI-MÊME : si la version publiée a un installateur pour ce système, il
//! le télécharge, vérifie son empreinte, prend sa place et se relance. Le joueur garde le même fichier d'une version
//! à l'autre, avec les nouveautés de l'assistant (les voix françaises, par exemple).

use sha2::{Digest, Sha256};
use std::io::Read;
use std::time::Duration;

const DERNIERE: &str = "https://api.github.com/repos/LePetitDan/Azeroth_FR/releases/latest";
/// Les fichiers ne sont acceptés que depuis les versions publiées du dépôt d'Azeroth_FR.
const ORIGINE: &str = "https://github.com/LePetitDan/Azeroth_FR/releases/download/";
const TAILLE_MAX: u64 = 300 * 1024 * 1024;
/// Argument donné à l'installateur relancé après s'être mis à jour : il ne recommence pas.
pub const APRES_MAJ: &str = "--apres-maj";

#[derive(Clone, PartialEq, Debug)]
pub struct Disponible {
    pub version: String,
    pub url_zip: String,
    pub taille: u64,
    pub url_sommes: Option<String>,
    /// l'installateur de cette version pour ce système (adresse, taille), s'il est publié
    pub installateur: Option<(String, u64)>,
}

/// Le nom de l'installateur publié pour ce système.
pub fn nom_installateur(version: &str) -> String {
    if cfg!(windows) {
        format!("Azeroth_FR-Installateur-{}.exe", version)
    } else {
        format!("Azeroth_FR-Installateur-{}-linux", version)
    }
}

fn nombres(v: &str) -> Option<Vec<u32>> {
    let v = v.trim().trim_start_matches('v');
    let n: Vec<u32> = v.split('.').map(|x| x.parse().ok()).collect::<Option<_>>()?;
    if n.len() == 3 { Some(n) } else { None }
}

/// `a` est-elle une version plus récente que `b` ? (faux si l'une des deux n'a pas la forme 1.2.3)
pub fn plus_recente(a: &str, b: &str) -> bool {
    match (nombres(a), nombres(b)) {
        (Some(x), Some(y)) => x > y,
        _ => false,
    }
}

fn agent() -> ureq::Agent {
    // certificats du système (un antivirus qui inspecte le HTTPS y ajoute le sien) et proxy éventuel de l'ordinateur
    ureq::AgentBuilder::new()
        .try_proxy_from_env(true)
        .timeout_connect(Duration::from_secs(6))
        .timeout_read(Duration::from_secs(30))
        .user_agent(concat!("Azeroth_FR-Installateur/", env!("CARGO_PKG_VERSION")))
        .build()
}

/// La dernière version publiée, si elle est plus récente que `actuelle`. `Err` : GitHub injoignable.
pub fn verifier(actuelle: &str) -> Result<Option<Disponible>, String> {
    let texte = agent()
        .get(DERNIERE)
        .set("Accept", "application/vnd.github+json")
        .call()
        .map_err(|e| e.to_string())?
        .into_string()
        .map_err(|e| e.to_string())?;
    lire_reponse(&texte, actuelle)
}

pub fn lire_reponse(texte: &str, actuelle: &str) -> Result<Option<Disponible>, String> {
    let v: serde_json::Value = serde_json::from_str(texte).map_err(|e| e.to_string())?;
    let version = v.get("tag_name").and_then(|x| x.as_str()).unwrap_or("").trim_start_matches('v').to_string();
    if !plus_recente(&version, actuelle) {
        return Ok(None);
    }
    let attendu = format!("Azeroth_FR-{}.zip", version);
    let (mut url_zip, mut taille, mut url_sommes) = (None, 0u64, None);
    let (attendu_exe, mut installateur) = (nom_installateur(&version), None);
    for a in v.get("assets").and_then(|x| x.as_array()).map(|x| x.as_slice()).unwrap_or(&[]) {
        let nom = a.get("name").and_then(|x| x.as_str()).unwrap_or("");
        let url = a.get("browser_download_url").and_then(|x| x.as_str()).unwrap_or("");
        if !url.starts_with(ORIGINE) {
            continue;
        }
        if nom == attendu {
            url_zip = Some(url.to_string());
            taille = a.get("size").and_then(|x| x.as_u64()).unwrap_or(0);
        } else if nom == "SHA256SUMS.txt" {
            url_sommes = Some(url.to_string());
        } else if nom == attendu_exe {
            let t = a.get("size").and_then(|x| x.as_u64()).unwrap_or(0);
            if t > 0 && t <= TAILLE_MAX {
                installateur = Some((url.to_string(), t));
            }
        }
    }
    match url_zip {
        Some(url_zip) if taille > 0 && taille <= TAILLE_MAX => Ok(Some(Disponible { version, url_zip, taille, url_sommes, installateur })),
        _ => Ok(None), // version annoncée sans son zip : on s'en tient à la version transportée
    }
}

/// L'empreinte attendue du zip, lue dans SHA256SUMS.txt (« empreinte  nom »).
pub fn empreinte_attendue(sommes: &str, nom: &str) -> Option<String> {
    sommes.lines().find_map(|l| {
        let mut p = l.split_whitespace();
        let (e, n) = (p.next()?, p.next()?);
        (n == nom && e.len() == 64).then(|| e.to_lowercase())
    })
}

/// Télécharge un fichier de la version publiée, en vérifie la taille et l'empreinte (SHA256SUMS.txt).
fn telecharger_fichier(d: &Disponible, nom: &str, url: &str, taille: u64, quoi: &str, progres: &dyn Fn(f32, &str)) -> Result<Vec<u8>, String> {
    let attendue = match &d.url_sommes {
        Some(u) => {
            let t = agent().get(u).call().map_err(|e| e.to_string())?.into_string().map_err(|e| e.to_string())?;
            Some(empreinte_attendue(&t, nom).ok_or("empreinte absente de SHA256SUMS.txt")?)
        }
        None => return Err("la version publiée n'a pas de fichier d'empreintes".into()),
    };
    let rep = agent().get(url).call().map_err(|e| e.to_string())?;
    let mut lecteur = rep.into_reader().take(TAILLE_MAX);
    let mut octets = Vec::with_capacity(taille as usize);
    let mut bloc = vec![0u8; 256 * 1024];
    let mo = |n: usize| n as f32 / 1_048_576.0;
    loop {
        let n = lecteur.read(&mut bloc).map_err(|e| e.to_string())?;
        if n == 0 {
            break;
        }
        octets.extend_from_slice(&bloc[..n]);
        progres(
            (octets.len() as f32 / taille as f32).min(1.0),
            &format!("Téléchargement {} {} : {:.0} Mo sur {:.0}", quoi, d.version, mo(octets.len()), mo(taille as usize)),
        );
    }
    if octets.len() as u64 != taille {
        return Err("téléchargement incomplet".into());
    }
    let obtenue: String = Sha256::digest(&octets).iter().map(|o| format!("{:02x}", o)).collect();
    if Some(obtenue) != attendue {
        return Err("le fichier téléchargé ne correspond pas à son empreinte".into());
    }
    Ok(octets)
}

/// Télécharge le zip de la version, en vérifie la taille et l'empreinte.
pub fn telecharger(d: &Disponible, progres: &dyn Fn(f32, &str)) -> Result<Vec<u8>, String> {
    telecharger_fichier(d, &format!("Azeroth_FR-{}.zip", d.version), &d.url_zip, d.taille, "de la version", progres)
}

/// Télécharge l'installateur de la version pour ce système, vérifié de la même façon.
pub fn telecharger_installateur(d: &Disponible, progres: &dyn Fn(f32, &str)) -> Result<Vec<u8>, String> {
    let (url, taille) = d.installateur.clone().ok_or("pas d'installateur publié pour ce système")?;
    telecharger_fichier(d, &nom_installateur(&d.version), &url, taille, "de l'installateur", progres)
}

fn a_cote(cible: &std::path::Path, suffixe: &str) -> std::path::PathBuf {
    let mut nom = cible.file_name().map(|n| n.to_os_string()).unwrap_or_default();
    nom.push(suffixe);
    cible.with_file_name(nom)
}

/// Met le nouvel installateur à la place de `cible` (l'installateur en cours). Sous Windows, un programme qui tourne
/// ne peut pas être écrasé mais peut être renommé : l'ancien devient `<nom>.ancien` (effacé au lancement suivant).
/// En cas d'échec, l'ancien est remis en place.
pub fn remplacer(octets: &[u8], cible: &std::path::Path) -> Result<(), String> {
    let (nouveau, ancien) = (a_cote(cible, ".nouveau"), a_cote(cible, ".ancien"));
    std::fs::write(&nouveau, octets).map_err(|e| e.to_string())?;
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let _ = std::fs::set_permissions(&nouveau, std::fs::Permissions::from_mode(0o755));
    }
    if std::fs::metadata(&nouveau).map(|m| m.len()).unwrap_or(0) != octets.len() as u64 {
        let _ = std::fs::remove_file(&nouveau);
        return Err("écriture incomplète".into());
    }
    let _ = std::fs::remove_file(&ancien);
    if let Err(e) = std::fs::rename(cible, &ancien) {
        let _ = std::fs::remove_file(&nouveau);
        return Err(e.to_string());
    }
    if let Err(e) = std::fs::rename(&nouveau, cible) {
        let _ = std::fs::rename(&ancien, cible);
        let _ = std::fs::remove_file(&nouveau);
        return Err(e.to_string());
    }
    Ok(())
}

/// Efface l'ancien installateur laissé par une mise à jour (et un téléchargement resté en plan).
pub fn nettoyer(cible: &std::path::Path) {
    let _ = std::fs::remove_file(a_cote(cible, ".ancien"));
    let _ = std::fs::remove_file(a_cote(cible, ".nouveau"));
}

#[cfg(test)]
mod essais {
    use super::*;

    #[test]
    fn versions() {
        assert!(plus_recente("1.1.0", "1.0.1"));
        assert!(plus_recente("v1.10.0", "1.9.9"));
        assert!(!plus_recente("1.0.1", "1.0.1"));
        assert!(!plus_recente("1.0.0", "1.0.1"));
        assert!(!plus_recente("n'importe quoi", "1.0.1"));
        assert!(!plus_recente("2.0", "1.0.1"));
    }

    #[test]
    fn reponse_de_github() {
        let j = r#"{"tag_name":"v1.2.0","assets":[
            {"name":"Azeroth_FR-1.2.0.zip","size":1000,"browser_download_url":"https://github.com/LePetitDan/Azeroth_FR/releases/download/v1.2.0/Azeroth_FR-1.2.0.zip"},
            {"name":"SHA256SUMS.txt","size":10,"browser_download_url":"https://github.com/LePetitDan/Azeroth_FR/releases/download/v1.2.0/SHA256SUMS.txt"}]}"#;
        let d = lire_reponse(j, "1.1.0").unwrap().unwrap();
        assert_eq!(d.version, "1.2.0");
        assert_eq!(d.taille, 1000);
        assert!(d.url_sommes.is_some());
        assert_eq!(d.installateur, None);
        // avec l'installateur de ce système dans la version publiée
        let nom = nom_installateur("1.2.0");
        let avec = j.replace(
            r#"{"name":"SHA256SUMS.txt""#,
            &format!(r#"{{"name":"{}","size":3000,"browser_download_url":"https://github.com/LePetitDan/Azeroth_FR/releases/download/v1.2.0/{}"}},{{"name":"SHA256SUMS.txt""#, nom, nom),
        );
        let d2 = lire_reponse(&avec, "1.1.0").unwrap().unwrap();
        assert_eq!(d2.installateur.as_ref().map(|x| x.1), Some(3000));
        assert_eq!(lire_reponse(j, "1.2.0").unwrap(), None);
        // un zip hébergé ailleurs est refusé
        let ailleurs = j.replace("https://github.com/LePetitDan/Azeroth_FR/releases/download/v1.2.0/Azeroth_FR-1.2.0.zip", "https://exemple.invalid/Azeroth_FR-1.2.0.zip");
        assert_eq!(lire_reponse(&ailleurs, "1.1.0").unwrap(), None);
    }

    #[test]
    fn remplacement() {
        let d = std::env::temp_dir().join(format!("azfr_essai_{}", std::process::id()));
        std::fs::create_dir_all(&d).unwrap();
        let cible = d.join("Installateur.exe");
        std::fs::write(&cible, b"ancien").unwrap();
        remplacer(b"nouveau programme", &cible).unwrap();
        assert_eq!(std::fs::read(&cible).unwrap(), b"nouveau programme");
        assert_eq!(std::fs::read(d.join("Installateur.exe.ancien")).unwrap(), b"ancien");
        nettoyer(&cible);
        assert!(!d.join("Installateur.exe.ancien").exists());
        let _ = std::fs::remove_dir_all(&d);
    }

    #[test]
    fn empreintes() {
        let e = "a".repeat(64);
        let t = format!("{}  Azeroth_FR-1.2.0.zip\n{}  autre.exe\n", e, "b".repeat(64));
        assert_eq!(empreinte_attendue(&t, "Azeroth_FR-1.2.0.zip"), Some(e));
        assert_eq!(empreinte_attendue(&t, "absent.zip"), None);
    }
}
