//! Installateur d'Azeroth_FR : un assistant en quatre étapes (Bienvenue, Dossier du jeu, Installation, C'est prêt)
//! qui trouve le dossier du jeu, installe ou met à jour la traduction, et peut la désinstaller. Le zip de l'add-on
//! est dans l'exécutable ; si GitHub annonce une version plus récente, c'est elle qui est téléchargée (maj.rs).
//!
//! Modes sans fenêtre, pour les essais : `--test-installer <dossier> <rapport>`, `--test-desinstaller <dossier>
//! <rapport>`, `--test-corriger <dossier> <rapport>`, `--test-chercher <rapport>`, `--test-maj <rapport> [<dossier>]` ; `--capture <png> [<dossier>
//! [<étape>]]` enregistre une image de la fenêtre puis la ferme (étapes : bienvenue, dossier, maj, introuvable, attente,
//! installation, erreur, fini).
#![windows_subsystem = "windows"]

mod installation;
mod maj;

use eframe::egui::{self, Color32, RichText};
use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

// couleurs du logo du Discord Azeroth_FR : bleu nuit, or du livre et de l'étoile, ruban bleu-blanc-rouge
const NUIT: Color32 = Color32::from_rgb(4, 16, 46);
const CARTE: Color32 = Color32::from_rgb(12, 31, 74);
const BORD: Color32 = Color32::from_rgb(44, 72, 132);
const TEXTE: Color32 = Color32::from_rgb(238, 242, 251);
const DOUX: Color32 = Color32::from_rgb(160, 176, 214);
const OR: Color32 = Color32::from_rgb(233, 182, 94);
const CRISTAL: Color32 = Color32::from_rgb(250, 232, 175);
const VERT: Color32 = Color32::from_rgb(132, 222, 168);
const ROUGE: Color32 = Color32::from_rgb(244, 120, 120);

const PAGE_PROJET: &str = "https://github.com/LePetitDan/Azeroth_FR";
const PAGE_SOUTIEN: &str = "https://buymeacoffee.com/LePetitDan";
const PAGE_DISCORD: &str = "https://discord.gg/kFJGDJbeay";

#[derive(Clone, Copy, PartialEq)]
enum Etape {
    Bienvenue,
    Dossier,
    Installation,
    Fini,
    Desinstalle,
}

#[derive(Clone, PartialEq)]
enum Etat {
    Attente,
    EnCours,
    Fini(String),
    Erreur(String),
}

/// Ce que GitHub a répondu sur la dernière version publiée.
#[derive(Clone, PartialEq)]
enum Maj {
    EnCours,
    Aucune,
    Disponible(maj::Disponible),
    Injoignable,
}

#[derive(Clone, PartialEq)]
enum Recherche {
    Non,
    EnCours(String),
    Finie(Vec<PathBuf>),
}

struct Partage {
    etat: Etat,
    fraction: f32,
    message: String,
    recherche: Recherche,
    maj: Maj,
}

struct App {
    etape: Etape,
    dossier: Option<PathBuf>,
    /// ce qu'on dit au joueur sur le dossier qu'il vient de choisir (texte, bonne nouvelle ?)
    note_dossier: Option<(String, bool)>,
    installee: Option<String>,
    jeu_ouvert: bool,
    dernier_controle: Instant,
    partage: Arc<Mutex<Partage>>,
    arret_recherche: Arc<AtomicBool>,
    confirmer_desinstallation: bool,
    erreur_desinstallation: Option<String>,
    capture: Option<(PathBuf, u32)>,
    figer: bool,
    logo: Option<egui::TextureHandle>,
}

impl App {
    fn new(cc: &eframe::CreationContext<'_>, dossier: Option<PathBuf>, capture: Option<PathBuf>, etape: Option<String>) -> Self {
        polices(&cc.egui_ctx);
        apparence(&cc.egui_ctx);
        let essai = capture.is_some();
        let dossier = match dossier {
            Some(d) => installation::corriger(&d),
            None if essai => None,
            None => installation::detecter(),
        };
        let installee = dossier.as_deref().and_then(installation::version_installee);
        let mut app = App {
            etape: Etape::Bienvenue,
            dossier,
            note_dossier: None,
            installee,
            jeu_ouvert: installation::jeu_ouvert(),
            dernier_controle: Instant::now(),
            partage: Arc::new(Mutex::new(Partage { etat: Etat::Attente, fraction: 0.0, message: String::new(), recherche: Recherche::Non, maj: Maj::Aucune })),
            arret_recherche: Arc::new(AtomicBool::new(false)),
            confirmer_desinstallation: false,
            erreur_desinstallation: None,
            capture: capture.map(|p| (p, 0)),
            figer: false,
            logo: decoder_png(include_bytes!("../assets/logo192.png"))
                .map(|(rgba, l, h)| cc.egui_ctx.load_texture("logo", egui::ColorImage::from_rgba_unmultiplied([l as usize, h as usize], &rgba), Default::default())),
        };
        if !essai {
            app.partage.lock().unwrap().maj = Maj::EnCours;
            let (partage, ctx) = (app.partage.clone(), cc.egui_ctx.clone());
            std::thread::spawn(move || {
                let r = match maj::verifier(installation::VERSION) {
                    Ok(Some(d)) => Maj::Disponible(d),
                    Ok(None) => Maj::Aucune,
                    Err(_) => Maj::Injoignable,
                };
                partage.lock().unwrap().maj = r;
                ctx.request_repaint();
            });
        }
        // mode essai : montrer une étape précise, sans rien installer
        if let Some(e) = etape.as_deref() {
            app.figer = true;
            let mut p = app.partage.lock().unwrap();
            match e {
                "dossier" => app.etape = Etape::Dossier,
                "maj" => {
                    app.etape = Etape::Dossier;
                    app.installee = Some(installation::VERSION.to_string());
                    p.maj = Maj::Disponible(maj::Disponible { version: "9.9.9".into(), url_zip: String::new(), taille: 27 * 1024 * 1024, url_sommes: None });
                }
                "introuvable" => {
                    app.etape = Etape::Dossier;
                    app.dossier = None;
                    app.installee = None;
                }
                "attente" => {
                    app.etape = Etape::Installation;
                    app.jeu_ouvert = true;
                }
                "installation" => {
                    app.etape = Etape::Installation;
                    app.jeu_ouvert = false;
                    p.etat = Etat::EnCours;
                    p.fraction = 0.62;
                    p.message = "Copie : Azeroth_FR_Sorts03".into();
                }
                "erreur" => {
                    app.etape = Etape::Installation;
                    app.jeu_ouvert = false;
                    p.etat = Etat::Erreur("Impossible d'écrire dans le dossier du jeu.\nWindows refuse d'écrire dans ce dossier. Fermez le jeu et le lanceur, puis réessayez. Si cela ne suffit pas : fermez cet installateur, faites un clic droit dessus et choisissez « Exécuter en tant qu'administrateur ».\n(détail : Accès refusé. (os error 5))".into());
                }
                "fini" => {
                    app.etape = Etape::Fini;
                    p.etat = Etat::Fini(String::new());
                    app.installee = Some(installation::VERSION.to_string());
                }
                _ => {}
            }
            drop(p);
        }
        app
    }

    /// La version qui sera installée : la dernière publiée si GitHub en annonce une plus récente, sinon celle
    /// que l'installateur transporte.
    fn cible(&self) -> String {
        match &self.partage.lock().unwrap().maj {
            Maj::Disponible(d) => d.version.clone(),
            _ => installation::VERSION.to_string(),
        }
    }

    fn retenir_dossier(&mut self, p: PathBuf) {
        match installation::corriger(&p) {
            Some(c) => {
                self.note_dossier = if c != p {
                    Some((format!("Le jeu se trouve dans « {} » : nous avons pris ce dossier-là.", c.display()), true))
                } else {
                    None
                };
                self.installee = installation::version_installee(&c);
                self.dossier = Some(c);
            }
            None => {
                self.note_dossier = Some((
                    format!("« {} » n'est pas le dossier du jeu : il ne contient pas Ascension.exe. Choisissez le dossier où le lanceur a installé le jeu, ou lancez la recherche automatique.", p.display()),
                    false,
                ));
            }
        }
    }

    fn choisir_dossier(&mut self) {
        let mut d = rfd::FileDialog::new().set_title("Choisissez le dossier du jeu (celui qui contient Ascension.exe)");
        if let Some(p) = &self.dossier {
            d = d.set_directory(p);
        }
        if let Some(p) = d.pick_folder() {
            self.partage.lock().unwrap().recherche = Recherche::Non;
            self.retenir_dossier(p);
        }
    }

    fn lancer_recherche(&mut self, ctx: &egui::Context) {
        self.note_dossier = None;
        self.arret_recherche.store(false, Ordering::Relaxed);
        self.partage.lock().unwrap().recherche = Recherche::EnCours(String::new());
        let (partage, arret, ctx) = (self.partage.clone(), self.arret_recherche.clone(), ctx.clone());
        std::thread::spawn(move || {
            let (p2, c2) = (partage.clone(), ctx.clone());
            let dernier = Mutex::new(Instant::now());
            let vu = move |d: &std::path::Path| {
                let mut t = dernier.lock().unwrap();
                if t.elapsed() > Duration::from_millis(80) {
                    *t = Instant::now();
                    let mut p = p2.lock().unwrap();
                    if matches!(p.recherche, Recherche::EnCours(_)) {
                        p.recherche = Recherche::EnCours(d.to_string_lossy().to_string());
                    }
                    c2.request_repaint();
                }
            };
            let trouves = installation::chercher(&arret, &vu);
            let mut p = partage.lock().unwrap();
            if matches!(p.recherche, Recherche::EnCours(_)) {
                p.recherche = Recherche::Finie(trouves);
            }
            ctx.request_repaint();
        });
    }

    fn lancer_installation(&mut self, ctx: &egui::Context) {
        let Some(dossier) = self.dossier.clone() else { return };
        let partage = self.partage.clone();
        {
            let mut p = partage.lock().unwrap();
            p.etat = Etat::EnCours;
            p.fraction = 0.0;
            p.message = "Préparation…".into();
        }
        let ctx = ctx.clone();
        std::thread::spawn(move || {
            let p2 = partage.clone();
            let c2 = ctx.clone();
            let progres = move |f: f32, m: &str| {
                let mut p = p2.lock().unwrap();
                p.fraction = f;
                p.message = m.to_string();
                c2.request_repaint();
            };
            // une version plus récente est publiée : on la télécharge ; en cas d'échec, on installe celle
            // que l'installateur transporte et on le dit
            let dispo = match &partage.lock().unwrap().maj {
                Maj::Disponible(d) => Some(d.clone()),
                _ => None,
            };
            let mut notes: Vec<String> = Vec::new();
            let mut archive: Option<Vec<u8>> = None;
            if let Some(d) = &dispo {
                let moitie = |f: f32, m: &str| progres(f * 0.6, m);
                match maj::telecharger(d, &moitie) {
                    Ok(z) => archive = Some(z),
                    Err(e) => notes.push(format!(
                        "La version {} n'a pas pu être téléchargée ({}) : c'est la version {} de cet installateur qui est installée.",
                        d.version, e, installation::VERSION
                    )),
                }
            }
            let r = match &archive {
                Some(z) => {
                    let suite = |f: f32, m: &str| progres(0.6 + f * 0.4, m);
                    installation::installer_archive(&dossier, z, &suite, true)
                }
                None => installation::installer(&dossier, &progres, true),
            };
            let mut p = partage.lock().unwrap();
            p.etat = match r {
                Ok(r) => {
                    if r.ptr_mis_de_cote {
                        notes.push("Un ancien fichier PTR.xml a été mis de côté ; la désinstallation le remettra en place.".to_string());
                    }
                    Etat::Fini(notes.join(" "))
                }
                Err(e) => Etat::Erreur(e),
            };
            ctx.request_repaint();
        });
    }

    fn lancer_desinstallation(&mut self) {
        let Some(dossier) = self.dossier.clone() else { return };
        match installation::desinstaller(&dossier) {
            Ok(_) => {
                self.etape = Etape::Desinstalle;
                self.erreur_desinstallation = None;
            }
            Err(e) => self.erreur_desinstallation = Some(e),
        }
        self.installee = installation::version_installee(&dossier);
        self.confirmer_desinstallation = false;
    }

    fn entete(&self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            if let Some(t) = &self.logo {
                ui.add(egui::Image::new((t.id(), egui::vec2(76.0, 76.0))));
            }
            ui.add_space(6.0);
            ui.vertical(|ui| {
                ui.add_space(6.0);
                ui.label(RichText::new("Azeroth_FR").family(egui::FontFamily::Name("titre".into())).size(36.0).color(OR));
                ui.label(RichText::new(format!("Conquest of Azeroth en français · version {}", self.cible())).size(15.0).color(CRISTAL));
            });
        });
        ui.add_space(2.0);
        // le fil des étapes
        let courant = match self.etape {
            Etape::Bienvenue => 0,
            Etape::Dossier => 1,
            Etape::Installation => 2,
            Etape::Fini | Etape::Desinstalle => 3,
        };
        ui.horizontal(|ui| {
            ui.spacing_mut().item_spacing.x = 7.0;
            let fin = if self.etape == Etape::Desinstalle { "Terminé" } else { "C'est prêt" };
            for (i, nom) in ["Bienvenue", "Dossier du jeu", "Installation", fin].iter().enumerate() {
                if i > 0 {
                    ui.label(RichText::new("›").size(14.0).color(BORD));
                }
                let (texte, couleur) = if i < courant {
                    (format!("✔ {}", nom), VERT)
                } else if i == courant {
                    (format!("{}. {}", i + 1, nom), OR)
                } else {
                    (format!("{}. {}", i + 1, nom), DOUX)
                };
                let mut r = RichText::new(texte).size(14.0).color(couleur);
                if i == courant {
                    r = r.strong();
                }
                ui.label(r);
            }
        });
        ui.add_space(2.0);
    }

    fn page_bienvenue(&mut self, ui: &mut egui::Ui) {
        carte(ui, |ui| {
            ui.label(RichText::new("Bienvenue !").family(egui::FontFamily::Name("titre".into())).size(24.0).color(TEXTE));
            ui.label(RichText::new("Cet assistant met Conquest of Azeroth en français, en trois clics.").size(17.0).color(TEXTE));
            ui.add_space(4.0);
            for l in [
                "Il trouve le dossier du jeu, ou vous aide à le trouver.",
                "Il n'ajoute que la traduction : les fichiers du jeu ne sont pas modifiés.",
                "Il regarde sur GitHub s'il existe une version plus récente. Aucun compte ni mot de passe n'est demandé.",
                "Vous pourrez tout retirer avec ce même assistant.",
            ] {
                ui.horizontal_top(|ui| {
                    ui.label(RichText::new("✔").color(VERT));
                    ui.add(egui::Label::new(RichText::new(l).color(TEXTE)).wrap());
                });
            }
        });
        carte(ui, |ui| {
            ui.label(RichText::new("AVANT DE COMMENCER").size(12.0).color(DOUX).strong());
            if self.jeu_ouvert {
                ui.label(RichText::new("Le jeu est ouvert : fermez-le, l'installation ne peut pas se faire pendant qu'il tourne.").color(ROUGE));
            } else {
                ui.label(RichText::new("Fermez le jeu s'il est ouvert. C'est tout.").color(TEXTE));
            }
        });
        ui.add_space(4.0);
        if bouton_principal(ui, "Commencer", true) {
            self.etape = Etape::Dossier;
        }
    }

    fn page_dossier(&mut self, ui: &mut egui::Ui, ctx: &egui::Context) {
        let (recherche, etat_maj) = {
            let p = self.partage.lock().unwrap();
            (p.recherche.clone(), p.maj.clone())
        };
        let cherche = matches!(recherche, Recherche::EnCours(_));
        let cible = self.cible();
        carte(ui, |ui| {
            ui.label(RichText::new("OÙ EST LE JEU ?").size(12.0).color(DOUX).strong());
            match &self.dossier {
                Some(d) => {
                    ui.label(RichText::new("✔ Nous avons trouvé votre jeu").size(18.0).color(VERT));
                    ui.add(egui::Label::new(RichText::new(d.to_string_lossy()).size(16.0).color(TEXTE)).wrap());
                    let texte = match &self.installee {
                        Some(v) if *v == cible => format!("Azeroth_FR {} y est déjà installé : vous êtes à jour.", v),
                        Some(v) => format!("Azeroth_FR {} y est installé : il sera remplacé par la version {}.", v, cible),
                        None => "Azeroth_FR n'y est pas encore installé.".to_string(),
                    };
                    ui.label(RichText::new(texte).color(DOUX));
                    if !installation::est_coa(d) {
                        ui.add(egui::Label::new(RichText::new(
                            "Vérifiez que c'est bien le jeu de Conquest of Azeroth : ce dossier ne porte pas la marque de son lanceur.",
                        ).size(14.0).color(CRISTAL)).wrap());
                    }
                }
                None => {
                    ui.label(RichText::new("Nous n'avons pas trouvé le jeu tout seuls").size(18.0).color(CRISTAL));
                    ui.add(egui::Label::new(RichText::new(
                        "Le dossier du jeu est celui où le lanceur de Conquest of Azeroth a installé le jeu. On le reconnaît à ce qu'il contient : le fichier Ascension.exe et un dossier Interface.",
                    ).color(TEXTE)).wrap());
                }
            }
            if let Some((texte, bonne)) = &self.note_dossier {
                ui.add(egui::Label::new(RichText::new(texte).color(if *bonne { VERT } else { ROUGE })).wrap());
            }
            match &recherche {
                Recherche::EnCours(ou) => {
                    ui.horizontal(|ui| {
                        ui.add(egui::Spinner::new().color(OR));
                        ui.label(RichText::new("Recherche du jeu sur vos disques…").color(TEXTE));
                    });
                    ui.add(egui::Label::new(RichText::new(ou).size(13.0).color(DOUX)).truncate());
                }
                Recherche::Finie(t) if t.is_empty() => {
                    ui.add(egui::Label::new(RichText::new(
                        "La recherche n'a rien trouvé. Le jeu est peut-être rangé très profond, ou sur un disque débranché : choisissez son dossier vous-même.",
                    ).color(ROUGE)).wrap());
                }
                Recherche::Finie(t) if t.len() > 1 => {
                    ui.label(RichText::new("Plusieurs jeux trouvés : choisissez le vôtre.").color(CRISTAL));
                    let mut choix = None;
                    for d in t {
                        let actuel = self.dossier.as_ref() == Some(d);
                        if ui.radio(actuel, RichText::new(d.to_string_lossy()).color(TEXTE)).clicked() {
                            choix = Some(d.clone());
                        }
                    }
                    if let Some(d) = choix {
                        self.retenir_dossier(d);
                    }
                }
                _ => {}
            }
            ui.add_space(2.0);
            ui.horizontal(|ui| {
                if cherche {
                    if ui.add(bouton_secondaire("Arrêter la recherche")).clicked() {
                        self.arret_recherche.store(true, Ordering::Relaxed);
                        self.partage.lock().unwrap().recherche = Recherche::Non;
                    }
                } else {
                    let libelle = if self.dossier.is_some() { "Choisir un autre dossier…" } else { "Choisir le dossier…" };
                    if ui.add(bouton_secondaire(libelle)).clicked() {
                        self.choisir_dossier();
                    }
                    if ui.add(bouton_secondaire("Chercher automatiquement")).clicked() {
                        self.lancer_recherche(ctx);
                    }
                }
            });
        });

        // ce que GitHub dit de la dernière version
        match &etat_maj {
            Maj::Disponible(d) => carte(ui, |ui| {
                ui.label(RichText::new("NOUVELLE VERSION").size(12.0).color(OR).strong());
                ui.add(egui::Label::new(RichText::new(format!(
                    "La version {} est disponible : elle sera téléchargée depuis GitHub ({:.0} Mo) puis installée.",
                    d.version, d.taille as f32 / 1_048_576.0
                )).color(TEXTE)).wrap());
            }),
            Maj::EnCours => {
                ui.label(RichText::new("Recherche d'une version plus récente…").size(13.0).color(DOUX));
            }
            Maj::Injoignable => {
                ui.add(egui::Label::new(RichText::new(format!(
                    "Pas de connexion à GitHub : c'est la version {} de cet installateur qui sera installée.", installation::VERSION
                )).size(13.0).color(DOUX)).wrap());
            }
            Maj::Aucune => {}
        }
        ui.add_space(4.0);
        let libelle = match &self.installee {
            Some(v) if *v == cible => "Réinstaller",
            Some(_) => "Mettre à jour",
            None => "Installer",
        };
        if bouton_principal(ui, libelle, self.dossier.is_some() && !cherche) {
            self.confirmer_desinstallation = false;
            self.partage.lock().unwrap().etat = Etat::Attente;
            self.etape = Etape::Installation;
        }
        if self.dossier.is_none() {
            ui.label(RichText::new("Le bouton s'allume dès que le dossier du jeu est trouvé.").size(13.0).color(DOUX));
        }

        // désinstallation, discrète
        if self.installee.is_some() && self.dossier.is_some() && !cherche {
            ui.add_space(2.0);
            ui.horizontal(|ui| {
                if self.confirmer_desinstallation {
                    ui.label(RichText::new("Retirer la traduction du jeu ?").color(TEXTE));
                    if ui.add_enabled(!self.jeu_ouvert, bouton_secondaire("Oui, désinstaller")).clicked() {
                        self.lancer_desinstallation();
                    }
                    if ui.add(bouton_secondaire("Annuler")).clicked() {
                        self.confirmer_desinstallation = false;
                    }
                } else if ui.add(egui::Button::new(RichText::new("Désinstaller la traduction").color(DOUX)).frame(false)).clicked() {
                    self.confirmer_desinstallation = true;
                    self.erreur_desinstallation = None;
                }
            });
            if self.confirmer_desinstallation && self.jeu_ouvert {
                ui.label(RichText::new("Fermez d'abord le jeu.").color(ROUGE));
            }
            if let Some(e) = &self.erreur_desinstallation {
                ui.add(egui::Label::new(RichText::new(format!("✖ {}", e)).color(ROUGE)).wrap());
            }
        }
    }

    fn page_installation(&mut self, ui: &mut egui::Ui, ctx: &egui::Context, etat: &Etat, fraction: f32, message: &str) {
        match etat {
            Etat::Attente if self.jeu_ouvert => {
                carte(ui, |ui| {
                    ui.label(RichText::new("LE JEU EST OUVERT").size(12.0).color(DOUX).strong());
                    ui.horizontal(|ui| {
                        ui.add(egui::Spinner::new().color(OR));
                        ui.label(RichText::new("Fermez le jeu").size(20.0).color(CRISTAL));
                    });
                    ui.add(egui::Label::new(RichText::new(
                        "La traduction ne peut pas s'installer pendant que le jeu tourne. Quittez le jeu : l'installation commencera toute seule, vous n'avez rien d'autre à faire.",
                    ).color(TEXTE)).wrap());
                });
                ui.add_space(4.0);
                if ui.add(bouton_secondaire("Retour")).clicked() {
                    self.etape = Etape::Dossier;
                }
            }
            Etat::Attente => {
                if !self.figer {
                    self.lancer_installation(ctx);
                }
            }
            Etat::EnCours => {
                carte(ui, |ui| {
                    ui.label(RichText::new("INSTALLATION EN COURS").size(12.0).color(DOUX).strong());
                    ui.label(RichText::new("Encore quelques secondes…").size(20.0).color(TEXTE));
                    ui.add_space(4.0);
                    ui.add(egui::ProgressBar::new(fraction).desired_height(14.0).fill(OR));
                    ui.label(RichText::new(message).color(DOUX));
                    ui.add_space(2.0);
                    ui.label(RichText::new("Ne fermez pas cette fenêtre.").size(13.0).color(DOUX));
                });
            }
            Etat::Erreur(m) => {
                carte(ui, |ui| {
                    ui.label(RichText::new("L'INSTALLATION N'A PAS ABOUTI").size(12.0).color(ROUGE).strong());
                    let mut lignes = m.lines();
                    if let Some(l) = lignes.next() {
                        ui.add(egui::Label::new(RichText::new(l).size(17.0).color(TEXTE)).wrap());
                    }
                    if let Some(l) = lignes.next() {
                        ui.add(egui::Label::new(RichText::new(l).color(CRISTAL)).wrap());
                    }
                    for l in lignes {
                        ui.add(egui::Label::new(RichText::new(l).size(13.0).color(DOUX)).wrap());
                    }
                    ui.add_space(2.0);
                    ui.label(RichText::new("Votre jeu n'est pas abîmé : il suffit de recommencer.").size(13.0).color(DOUX));
                });
                ui.add_space(4.0);
                if bouton_principal(ui, "Réessayer", true) {
                    self.partage.lock().unwrap().etat = Etat::Attente;
                }
                if ui.add(bouton_secondaire("Retour au choix du dossier")).clicked() {
                    self.partage.lock().unwrap().etat = Etat::Attente;
                    self.etape = Etape::Dossier;
                }
            }
            Etat::Fini(_) => {
                if let Some(d) = &self.dossier {
                    self.installee = installation::version_installee(d);
                }
                self.etape = Etape::Fini
            }
        }
    }

    fn page_fini(&mut self, ui: &mut egui::Ui, ctx: &egui::Context, note: &str) {
        carte(ui, |ui| {
            ui.label(RichText::new("C'est prêt !").family(egui::FontFamily::Name("titre".into())).size(26.0).color(VERT));
            let v = self.installee.clone().unwrap_or_else(|| installation::VERSION.to_string());
            ui.label(RichText::new(format!("Azeroth_FR {} est installé. Voici la suite :", v)).size(17.0).color(TEXTE));
            ui.add_space(4.0);
            for (n, l) in [
                "Lancez le jeu avec le lanceur, comme d'habitude. Si le lanceur propose un « nettoyage des add-ons », laissez-le décoché : sinon il retire la traduction.",
                "À l'écran des personnages, cliquez sur le bouton AddOns : Azeroth_FR et ses modules doivent être cochés.",
                "En jeu, tapez /azfr pour les options. Un texte faux ou resté en anglais ? Survolez-le et tapez /azfr signaler.",
            ].iter().enumerate() {
                ui.horizontal_top(|ui| {
                    ui.label(RichText::new(format!("{}.", n + 1)).size(17.0).strong().color(OR));
                    ui.add(egui::Label::new(RichText::new(*l).color(TEXTE)).wrap());
                });
            }
            if !note.is_empty() {
                ui.add(egui::Label::new(RichText::new(note).size(13.0).color(DOUX)).wrap());
            }
        });
        carte(ui, |ui| {
            ui.add(egui::Label::new(RichText::new(
                "Nouvelles versions, aide, texte resté en anglais : tout se passe sur le Discord Azeroth_FR. Pour les prochaines versions, relancez simplement cet installateur : il se met à jour tout seul.",
            ).color(DOUX)).wrap());
            ui.add(egui::Label::new(RichText::new(
                "Azeroth_FR est gratuit et le restera. Si la traduction vous plaît, vous pouvez offrir un café à Dan.",
            ).color(TEXTE)).wrap());
            ui.horizontal(|ui| {
                if ui.add(egui::Button::new(RichText::new("☕ Soutenir le créateur").color(NUIT).strong()).fill(CRISTAL)).clicked() {
                    ouvrir(PAGE_SOUTIEN);
                }
                if ui.add(bouton_secondaire("Rejoindre le Discord")).clicked() {
                    ouvrir(PAGE_DISCORD);
                }
                if ui.add(bouton_secondaire("Page du projet")).clicked() {
                    ouvrir(PAGE_PROJET);
                }
            });
        });
        ui.add_space(4.0);
        if bouton_principal(ui, "Fermer", true) {
            ctx.send_viewport_cmd(egui::ViewportCommand::Close);
        }
    }

    fn page_desinstalle(&mut self, ui: &mut egui::Ui, ctx: &egui::Context) {
        carte(ui, |ui| {
            ui.label(RichText::new("Traduction retirée").family(egui::FontFamily::Name("titre".into())).size(26.0).color(VERT));
            ui.add(egui::Label::new(RichText::new(
                "Azeroth_FR est désinstallé : le jeu est de nouveau en anglais. Rien d'autre n'a été touché. Pour remettre la traduction, relancez cet assistant.",
            ).size(17.0).color(TEXTE)).wrap());
        });
        ui.add_space(4.0);
        if bouton_principal(ui, "Fermer", true) {
            ctx.send_viewport_cmd(egui::ViewportCommand::Close);
        }
        if ui.add(bouton_secondaire("Réinstaller la traduction")).clicked() {
            self.etape = Etape::Dossier;
        }
    }
}

impl eframe::App for App {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        if !self.figer && self.dernier_controle.elapsed() > Duration::from_secs(1) {
            self.jeu_ouvert = installation::jeu_ouvert();
            self.dernier_controle = Instant::now();
            if let Some(d) = &self.dossier {
                if !matches!(self.partage.lock().unwrap().etat, Etat::EnCours) {
                    self.installee = installation::version_installee(d);
                }
            }
        }
        ctx.request_repaint_after(Duration::from_secs(1));
        let (etat, fraction, message) = {
            let mut p = self.partage.lock().unwrap();
            // une recherche qui ne trouve qu'un jeu : on le prend
            if let Recherche::Finie(t) = &p.recherche {
                if t.len() == 1 {
                    let d = t[0].clone();
                    p.recherche = Recherche::Non;
                    drop(p);
                    self.retenir_dossier(d);
                    p = self.partage.lock().unwrap();
                }
            }
            (p.etat.clone(), p.fraction, p.message.clone())
        };

        egui::CentralPanel::default()
            .frame(egui::Frame::new().fill(NUIT).inner_margin(egui::Margin::symmetric(28, 20)))
            .show(ctx, |ui| {
                ui.spacing_mut().item_spacing = egui::vec2(10.0, 10.0);
                self.entete(ui);
                egui::TopBottomPanel::bottom("pied").frame(egui::Frame::new().fill(NUIT)).show_separator_line(false).show_inside(ui, |ui| {
                    ui.add(egui::Label::new(RichText::new(
                        "Projet de joueurs, sans lien avec Blizzard Entertainment ni avec l'équipe de Conquest of Azeroth.",
                    ).size(12.5).color(DOUX)).wrap());
                });
                egui::ScrollArea::vertical().auto_shrink([false, false]).show(ui, |ui| {
                    ui.spacing_mut().item_spacing = egui::vec2(10.0, 10.0);
                    match self.etape {
                        Etape::Bienvenue => self.page_bienvenue(ui),
                        Etape::Dossier => self.page_dossier(ui, ctx),
                        Etape::Installation => self.page_installation(ui, ctx, &etat, fraction, &message),
                        Etape::Fini => {
                            let note = if let Etat::Fini(n) = &etat { n.clone() } else { String::new() };
                            self.page_fini(ui, ctx, &note)
                        }
                        Etape::Desinstalle => self.page_desinstalle(ui, ctx),
                    }
                });
            });

        // mode essai : image de la fenêtre après quelques images, puis fermeture
        if let Some((chemin, n)) = &mut self.capture {
            *n += 1;
            if *n == 8 {
                ctx.send_viewport_cmd(egui::ViewportCommand::Screenshot(Default::default()));
            }
            let chemin = chemin.clone();
            let images: Vec<Arc<egui::ColorImage>> = ctx.input(|i| {
                i.raw.events.iter().filter_map(|e| match e {
                    egui::Event::Screenshot { image, .. } => Some(image.clone()),
                    _ => None,
                }).collect()
            });
            if let Some(img) = images.first() {
                let _ = enregistrer_png(&chemin, img);
                ctx.send_viewport_cmd(egui::ViewportCommand::Close);
            }
            ctx.request_repaint();
        }
    }
}

/// Le grand bouton doré de l'étape : une seule action évidente par écran.
fn bouton_principal(ui: &mut egui::Ui, libelle: &str, actif: bool) -> bool {
    let b = egui::Button::new(RichText::new(libelle).size(21.0).strong().color(NUIT)).fill(OR);
    let largeur = ui.available_width();
    ui.add_enabled_ui(actif, |ui| ui.add_sized([largeur, 48.0], b)).inner.clicked()
}

/// Ouvre une adresse dans le navigateur du joueur.
fn ouvrir(adresse: &str) {
    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        let _ = std::process::Command::new("cmd").args(["/C", "start", "", adresse]).creation_flags(0x0800_0000).spawn();
    }
    #[cfg(not(windows))]
    {
        let _ = std::process::Command::new("xdg-open").arg(adresse).spawn();
    }
}

fn carte(ui: &mut egui::Ui, contenu: impl FnOnce(&mut egui::Ui)) {
    egui::Frame::new()
        .fill(CARTE)
        .stroke(egui::Stroke::new(1.0_f32, BORD))
        .corner_radius(8.0)
        .inner_margin(egui::Margin::same(14))
        .show(ui, |ui| {
            ui.set_width(ui.available_width());
            ui.spacing_mut().item_spacing = egui::vec2(8.0, 6.0);
            contenu(ui);
        });
}

fn bouton_secondaire(t: &str) -> egui::Button<'static> {
    egui::Button::new(RichText::new(t.to_string()).color(TEXTE)).fill(CARTE).stroke(egui::Stroke::new(1.0_f32, BORD))
}

fn polices(ctx: &egui::Context) {
    let mut f = egui::FontDefinitions::default();
    f.font_data.insert("corps".into(), Arc::new(egui::FontData::from_static(include_bytes!("../assets/AlegreyaSans-Regular.ttf"))));
    f.font_data.insert("titre".into(), Arc::new(egui::FontData::from_static(include_bytes!("../assets/Alegreya-ExtraBold.ttf"))));
    f.families.get_mut(&egui::FontFamily::Proportional).unwrap().insert(0, "corps".into());
    f.families.insert(egui::FontFamily::Name("titre".into()), vec!["titre".into(), "corps".into()]);
    ctx.set_fonts(f);
    ctx.style_mut(|s| {
        s.text_styles.insert(egui::TextStyle::Body, egui::FontId::proportional(17.0));
        s.text_styles.insert(egui::TextStyle::Button, egui::FontId::proportional(17.0));
        s.spacing.button_padding = egui::vec2(12.0, 6.0);
    });
}

fn apparence(ctx: &egui::Context) {
    let mut v = egui::Visuals::dark();
    v.panel_fill = NUIT;
    v.window_fill = NUIT;
    v.override_text_color = None;
    v.selection.bg_fill = OR;
    v.widgets.hovered.weak_bg_fill = Color32::from_rgb(24, 48, 104);
    v.widgets.active.weak_bg_fill = Color32::from_rgb(34, 62, 126);
    for w in [&mut v.widgets.inactive, &mut v.widgets.hovered, &mut v.widgets.active, &mut v.widgets.noninteractive] {
        w.corner_radius = egui::CornerRadius::same(6);
    }
    ctx.set_visuals(v);
}

fn enregistrer_png(chemin: &std::path::Path, img: &egui::ColorImage) -> std::io::Result<()> {
    let f = std::fs::File::create(chemin)?;
    let mut e = png::Encoder::new(std::io::BufWriter::new(f), img.size[0] as u32, img.size[1] as u32);
    e.set_color(png::ColorType::Rgba);
    e.set_depth(png::BitDepth::Eight);
    let mut w = e.write_header().map_err(std::io::Error::other)?;
    let octets: Vec<u8> = img.pixels.iter().flat_map(|c| c.to_array()).collect();
    w.write_image_data(&octets).map_err(std::io::Error::other)
}

fn decoder_png(octets: &[u8]) -> Option<(Vec<u8>, u32, u32)> {
    let mut d = png::Decoder::new(std::io::Cursor::new(octets));
    d.set_transformations(png::Transformations::EXPAND);
    let mut r = d.read_info().ok()?;
    let mut buf = vec![0; r.output_buffer_size()];
    let info = r.next_frame(&mut buf).ok()?;
    buf.truncate(info.buffer_size());
    if info.color_type != png::ColorType::Rgba {
        return None;
    }
    Some((buf, info.width, info.height))
}

fn icone() -> Option<egui::IconData> {
    let (rgba, width, height) = decoder_png(include_bytes!("../assets/icone64.png"))?;
    Some(egui::IconData { rgba, width, height })
}

fn essai(args: &[String]) -> bool {
    let texte_et_rapport = match args {
        [m, d, r, ..] if m == "--test-installer" => {
            let t = match installation::installer(&PathBuf::from(d), &|_, _| {}, false) {
                Ok(r) => format!("OK installé {} : {} fichiers, {} octets, PTR mis de côté : {}\n", r.version, r.fichiers, r.octets, r.ptr_mis_de_cote),
                Err(e) => format!("ERREUR {}\n", e),
            };
            (t, PathBuf::from(r))
        }
        [m, d, r, ..] if m == "--test-desinstaller" => {
            let t = match installation::desinstaller(&PathBuf::from(d)) {
                Ok(n) => format!("OK désinstallé : {} éléments retirés\n", n),
                Err(e) => format!("ERREUR {}\n", e),
            };
            (t, PathBuf::from(r))
        }
        [m, d, r, ..] if m == "--test-corriger" => {
            let t = match installation::corriger(&PathBuf::from(d)) {
                Some(p) => format!("OK {}\n", p.display()),
                None => "RIEN\n".to_string(),
            };
            (t, PathBuf::from(r))
        }
        [m, r, ..] if m == "--test-maj" => {
            // ce que répond GitHub pour un installateur qui transporterait la version 0.0.1, puis téléchargement vérifié
            let t = match maj::verifier("0.0.1") {
                Ok(Some(d)) => match maj::telecharger(&d, &|_, _| {}) {
                    Ok(z) => {
                        let mut t = format!("OK version {} : {} octets, empreinte vérifiée ; pour {} : {:?}\n", d.version, z.len(), installation::VERSION, maj::verifier(installation::VERSION).map(|x| x.map(|d| d.version)));
                        // avec un dossier : la version téléchargée y est installée
                        if let Some(dossier) = args.get(2) {
                            t.push_str(&match installation::installer_archive(&PathBuf::from(dossier), &z, &|_, _| {}, false) {
                                Ok(r) => format!("OK installé {} depuis le téléchargement : {} fichiers\n", r.version, r.fichiers),
                                Err(e) => format!("ERREUR {}\n", e),
                            });
                        }
                        t
                    }
                    Err(e) => format!("ERREUR téléchargement {} : {}\n", d.version, e),
                },
                Ok(None) => "RIEN\n".to_string(),
                Err(e) => format!("INJOIGNABLE {}\n", e),
            };
            (t, PathBuf::from(r))
        }
        [m, r, ..] if m == "--test-chercher" => {
            let debut = Instant::now();
            let v = installation::chercher(&AtomicBool::new(false), &|_| {});
            let mut t = format!("OK {} jeu(x) en {:.1} s\n", v.len(), debut.elapsed().as_secs_f32());
            for p in v {
                t.push_str(&format!("{}\n", p.display()));
            }
            (t, PathBuf::from(r))
        }
        _ => return false,
    };
    let _ = std::fs::write(texte_et_rapport.1, texte_et_rapport.0);
    true
}

fn main() -> eframe::Result<()> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if essai(&args) {
        return Ok(());
    }
    let (capture, dossier, etape) = match args.as_slice() {
        [c, png, rest @ ..] if c == "--capture" => (Some(PathBuf::from(png)), rest.first().map(PathBuf::from), rest.get(1).cloned()),
        _ => (None, None, None),
    };
    let mut vp = egui::ViewportBuilder::default()
        .with_title(format!("Azeroth_FR {} : installation", installation::VERSION))
        .with_inner_size([600.0, 690.0])
        .with_resizable(false);
    if let Some(i) = icone() {
        vp = vp.with_icon(Arc::new(i));
    }
    let options = eframe::NativeOptions { viewport: vp, ..Default::default() };
    eframe::run_native(
        "Azeroth_FR",
        options,
        Box::new(move |cc| Ok(Box::new(App::new(cc, dossier, capture, etape)))),
    )
}
