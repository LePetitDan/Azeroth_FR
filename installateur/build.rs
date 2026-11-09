// Installateur d'Azeroth_FR : le zip de l'add-on est embarqué dans l'exécutable (AZFR_ZIP), avec sa version
// (AZFR_VERSION) ; icône et informations de version Windows (winresource, windres de MinGW en compilation croisée).
use std::env;
use std::path::PathBuf;

fn main() {
    let racine = PathBuf::from(env::var("CARGO_MANIFEST_DIR").unwrap()).join("..");
    let version = env::var("AZFR_VERSION").unwrap_or_else(|_| {
        std::fs::read_to_string(racine.join("addon").join("VERSION")).unwrap().trim().to_string()
    });
    let zip = env::var("AZFR_ZIP").map(PathBuf::from).unwrap_or_else(|_| {
        racine.join("dist").join(format!("Azeroth_FR-{}.zip", version))
    });
    if !zip.exists() {
        panic!("zip de l'add-on absent : {} (lancer outils/fabriquer.py)", zip.display());
    }
    println!("cargo:rustc-env=AZFR_ZIP={}", zip.canonicalize().unwrap().display());
    println!("cargo:rustc-env=AZFR_VERSION={}", version);
    println!("cargo:rerun-if-env-changed=AZFR_ZIP");
    println!("cargo:rerun-if-env-changed=AZFR_VERSION");
    println!("cargo:rerun-if-changed={}", zip.display());

    if env::var("CARGO_CFG_TARGET_OS").as_deref() == Ok("windows") {
        let mut res = winresource::WindowsResource::new();
        res.set_icon("assets/icone.ico");
        res.set("ProductName", "Azeroth_FR");
        res.set("FileDescription", "Installateur d'Azeroth_FR (Conquest of Azeroth en français)");
        res.set("CompanyName", "Azeroth_FR (projet de joueurs)");
        res.set("LegalCopyright", "Dan (LePetitDan) et contributeurs");
        res.set("ProductVersion", &version);
        res.set("FileVersion", &version);
        res.set_language(0x040c); // français (France)
        if env::var("HOST").map(|h| !h.contains("windows")).unwrap_or(false) {
            res.set_windres_path("x86_64-w64-mingw32-windres");
            res.set_ar_path("x86_64-w64-mingw32-ar");
        }
        res.compile().expect("ressources Windows");
    }
}
