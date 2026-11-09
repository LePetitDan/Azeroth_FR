//! Installateur d'Azeroth_FR : une petite fenêtre qui trouve le dossier du jeu, installe ou met à jour la traduction,
//! et peut la désinstaller. Le zip de l'add-on est dans l'exécutable : rien n'est téléchargé.
//!
//! Modes sans fenêtre, pour les essais : `--test-installer <dossier> <rapport>`, `--test-desinstaller <dossier>
//! <rapport>` ; `--capture <png> [<dossier>]` enregistre une image de la fenêtre puis la ferme.
#![windows_subsystem = "windows"]

mod installation;

use eframe::egui::{self, Color32, RichText};
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

// couleurs du logo du Discord Azeroth_FR : brume vert-de-gris, or de la fleur de lys, cristal bleu-blanc-rouge
const NUIT: Color32 = Color32::from_rgb(18, 41, 47);
const CARTE: Color32 = Color32::from_rgb(28, 58, 65);
const BORD: Color32 = Color32::from_rgb(62, 112, 123);
const TEXTE: Color32 = Color32::from_rgb(233, 243, 242);
const DOUX: Color32 = Color32::from_rgb(143, 179, 180);
const OR: Color32 = Color32::from_rgb(222, 178, 74);
const CRISTAL: Color32 = Color32::from_rgb(161, 229, 240);
const VERT: Color32 = Color32::from_rgb(132, 222, 168);
const ROUGE: Color32 = Color32::from_rgb(238, 148, 160);

#[derive(Clone, PartialEq)]
enum Etat {
    Pret,
    EnCours,
    Fini(String),
    Erreur(String),
}

struct Partage {
    etat: Etat,
    fraction: f32,
    message: String,
}

struct App {
    dossier: Option<PathBuf>,
    installee: Option<String>,
    jeu_ouvert: bool,
    dernier_controle: Instant,
    partage: Arc<Mutex<Partage>>,
    confirmer_desinstallation: bool,
    capture: Option<(PathBuf, u32)>,
    logo: Option<egui::TextureHandle>,
}

impl App {
    fn new(cc: &eframe::CreationContext<'_>, dossier: Option<PathBuf>, capture: Option<PathBuf>) -> Self {
        polices(&cc.egui_ctx);
        apparence(&cc.egui_ctx);
        let dossier = dossier.or_else(installation::detecter);
        let installee = dossier.as_deref().and_then(installation::version_installee);
        App {
            dossier,
            installee,
            jeu_ouvert: installation::jeu_ouvert(),
            dernier_controle: Instant::now(),
            partage: Arc::new(Mutex::new(Partage { etat: Etat::Pret, fraction: 0.0, message: String::new() })),
            confirmer_desinstallation: false,
            capture: capture.map(|p| (p, 0)),
            logo: decoder_png(include_bytes!("../assets/logo192.png"))
                .map(|(rgba, l, h)| cc.egui_ctx.load_texture("logo", egui::ColorImage::from_rgba_unmultiplied([l as usize, h as usize], &rgba), Default::default())),
        }
    }

    fn choisir_dossier(&mut self) {
        let mut d = rfd::FileDialog::new().set_title("Choisissez le dossier du jeu (celui qui contient Ascension.exe)");
        if let Some(p) = &self.dossier {
            d = d.set_directory(p);
        }
        if let Some(p) = d.pick_folder() {
            self.installee = installation::version_installee(&p);
            self.dossier = Some(p);
            self.partage.lock().unwrap().etat = Etat::Pret;
        }
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
            let r = installation::installer(&dossier, &progres, true);
            let mut p = partage.lock().unwrap();
            p.etat = match r {
                Ok(r) => Etat::Fini(format!(
                    "Azeroth_FR {} est installé : {} fichiers, {:.1} Mo.{}",
                    r.version,
                    r.fichiers,
                    r.octets as f64 / 1_048_576.0,
                    if r.ptr_mis_de_cote { " L'ancien PTR.xml a été mis de côté." } else { "" }
                )),
                Err(e) => Etat::Erreur(e),
            };
            ctx.request_repaint();
        });
    }

    fn lancer_desinstallation(&mut self) {
        let Some(dossier) = self.dossier.clone() else { return };
        let mut p = self.partage.lock().unwrap();
        p.etat = match installation::desinstaller(&dossier) {
            Ok(_) => Etat::Fini("Azeroth_FR est désinstallé : le jeu est de nouveau en anglais.".into()),
            Err(e) => Etat::Erreur(e),
        };
        drop(p);
        self.installee = installation::version_installee(&dossier);
        self.confirmer_desinstallation = false;
    }
}

impl eframe::App for App {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        if self.dernier_controle.elapsed() > Duration::from_secs(2) {
            self.jeu_ouvert = installation::jeu_ouvert();
            self.dernier_controle = Instant::now();
            if let Some(d) = &self.dossier {
                if !matches!(self.partage.lock().unwrap().etat, Etat::EnCours) {
                    self.installee = installation::version_installee(d);
                }
            }
        }
        ctx.request_repaint_after(Duration::from_secs(2));
        let (etat, fraction, message) = {
            let p = self.partage.lock().unwrap();
            (p.etat.clone(), p.fraction, p.message.clone())
        };
        let occupe = etat == Etat::EnCours;

        egui::CentralPanel::default()
            .frame(egui::Frame::new().fill(NUIT).inner_margin(egui::Margin::symmetric(28, 22)))
            .show(ctx, |ui| {
                ui.spacing_mut().item_spacing = egui::vec2(10.0, 10.0);
                ui.horizontal(|ui| {
                    if let Some(t) = &self.logo {
                        ui.add(egui::Image::new((t.id(), egui::vec2(92.0, 92.0))));
                    }
                    ui.add_space(6.0);
                    ui.vertical(|ui| {
                        ui.add_space(10.0);
                        ui.label(RichText::new("Azeroth_FR").family(egui::FontFamily::Name("titre".into())).size(40.0).color(OR));
                        ui.label(RichText::new("Conquest of Azeroth en français").size(17.0).color(CRISTAL));
                        ui.label(RichText::new(format!("version {}", installation::VERSION)).size(14.0).color(DOUX));
                    });
                });
                ui.add_space(4.0);

                carte(ui, |ui| {
                    ui.label(RichText::new("DOSSIER DU JEU").size(12.0).color(DOUX).strong());
                    match &self.dossier {
                        Some(d) => {
                            ui.label(RichText::new(d.to_string_lossy()).size(16.0).color(TEXTE));
                            if installation::dossier_valide(d) {
                                ui.label(RichText::new("✔ Jeu trouvé").color(VERT));
                            } else {
                                ui.label(RichText::new("✖ Ascension.exe introuvable dans ce dossier").color(ROUGE));
                            }
                        }
                        None => {
                            ui.label(RichText::new("Dossier du jeu introuvable : choisissez-le (celui qui contient Ascension.exe).").color(TEXTE));
                        }
                    }
                    if ui.add_enabled(!occupe, bouton_secondaire("Choisir un autre dossier…")).clicked() {
                        self.choisir_dossier();
                    }
                });

                carte(ui, |ui| {
                    ui.label(RichText::new("TRADUCTION").size(12.0).color(DOUX).strong());
                    let texte = match &self.installee {
                        Some(v) if v == installation::VERSION => format!("Azeroth_FR {} est installé (à jour).", v),
                        Some(v) => format!("Azeroth_FR {} est installé : la version {} peut le remplacer.", v, installation::VERSION),
                        None => "Azeroth_FR n'est pas encore installé.".to_string(),
                    };
                    ui.label(RichText::new(texte).size(16.0).color(TEXTE));
                    if self.jeu_ouvert {
                        ui.label(RichText::new("Le jeu est ouvert : fermez-le avant d'installer.").color(ROUGE));
                    }
                });

                let valide = self.dossier.as_deref().map(installation::dossier_valide).unwrap_or(false);
                let libelle = match &self.installee {
                    Some(v) if v == installation::VERSION => "Réinstaller",
                    Some(_) => "Mettre à jour",
                    None => "Installer",
                };
                ui.add_space(4.0);
                let principal = egui::Button::new(RichText::new(libelle).size(21.0).strong().color(NUIT)).fill(OR);
                let actif = valide && !occupe && !self.jeu_ouvert;
                let largeur = ui.available_width();
                if ui.add_enabled_ui(actif, |ui| ui.add_sized([largeur, 48.0], principal)).inner.clicked() {
                    self.confirmer_desinstallation = false;
                    self.lancer_installation(ctx);
                }

                match &etat {
                    Etat::EnCours => {
                        ui.add(egui::ProgressBar::new(fraction).desired_height(10.0).fill(OR));
                        ui.label(RichText::new(message).color(DOUX));
                    }
                    Etat::Fini(m) => {
                        ui.label(RichText::new(format!("✔ {}", m)).color(VERT));
                        ui.label(RichText::new("Lancez le jeu : à l'écran des personnages, le bouton AddOns doit montrer Azeroth_FR coché.").color(DOUX));
                    }
                    Etat::Erreur(m) => {
                        ui.label(RichText::new(format!("✖ {}", m)).color(ROUGE));
                    }
                    Etat::Pret => {}
                }

                ui.with_layout(egui::Layout::bottom_up(egui::Align::Min), |ui| {
                    ui.label(RichText::new("Projet de joueurs, sans lien avec Blizzard Entertainment ni avec l'équipe de Conquest of Azeroth.").size(13.0).color(DOUX));
                    if self.installee.is_some() && valide && !occupe {
                        ui.horizontal(|ui| {
                            if self.confirmer_desinstallation {
                                ui.label(RichText::new("Retirer la traduction ?").color(TEXTE));
                                if ui.add_enabled(!self.jeu_ouvert, bouton_secondaire("Oui, désinstaller")).clicked() {
                                    self.lancer_desinstallation();
                                }
                                if ui.add(bouton_secondaire("Annuler")).clicked() {
                                    self.confirmer_desinstallation = false;
                                }
                            } else if ui.add(egui::Button::new(RichText::new("Désinstaller").color(DOUX)).frame(false)).clicked() {
                                self.confirmer_desinstallation = true;
                            }
                        });
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
        s.text_styles.insert(egui::TextStyle::Body, egui::FontId::proportional(16.0));
        s.text_styles.insert(egui::TextStyle::Button, egui::FontId::proportional(16.0));
        s.spacing.button_padding = egui::vec2(12.0, 6.0);
    });
}

fn apparence(ctx: &egui::Context) {
    let mut v = egui::Visuals::dark();
    v.panel_fill = NUIT;
    v.window_fill = NUIT;
    v.override_text_color = None;
    v.selection.bg_fill = OR;
    v.widgets.hovered.weak_bg_fill = Color32::from_rgb(40, 78, 87);
    v.widgets.active.weak_bg_fill = Color32::from_rgb(52, 96, 106);
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
    let (mode, dossier, rapport) = match args {
        [m, d, r, ..] if m == "--test-installer" || m == "--test-desinstaller" => (m.as_str(), PathBuf::from(d), PathBuf::from(r)),
        _ => return false,
    };
    let texte = if mode == "--test-installer" {
        match installation::installer(&dossier, &|_, _| {}, false) {
            Ok(r) => format!("OK installé {} : {} fichiers, {} octets, PTR mis de côté : {}\n", r.version, r.fichiers, r.octets, r.ptr_mis_de_cote),
            Err(e) => format!("ERREUR {}\n", e),
        }
    } else {
        match installation::desinstaller(&dossier) {
            Ok(n) => format!("OK désinstallé : {} éléments retirés\n", n),
            Err(e) => format!("ERREUR {}\n", e),
        }
    };
    let _ = std::fs::write(rapport, texte);
    true
}

fn main() -> eframe::Result<()> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if essai(&args) {
        return Ok(());
    }
    let (capture, dossier) = match args.as_slice() {
        [c, png, rest @ ..] if c == "--capture" => (Some(PathBuf::from(png)), rest.first().map(PathBuf::from)),
        _ => (None, None),
    };
    let mut vp = egui::ViewportBuilder::default()
        .with_title(format!("Azeroth_FR {} : installation", installation::VERSION))
        .with_inner_size([580.0, 600.0])
        .with_resizable(false);
    if let Some(i) = icone() {
        vp = vp.with_icon(Arc::new(i));
    }
    let options = eframe::NativeOptions { viewport: vp, ..Default::default() };
    eframe::run_native(
        "Azeroth_FR",
        options,
        Box::new(move |cc| Ok(Box::new(App::new(cc, dossier, capture)))),
    )
}
