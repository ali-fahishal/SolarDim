# Raana UI Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactoring complet de l'interface Raana (ex-SolarDim) — renommage, wizard navigation, cartes visuelles résultats, formulaires améliorés, polish mobile — sans modifier `core/`, `agent/`, `storage.py`, `sizing.py`, `config.py`.

**Architecture:** Approche B — uniquement `app.py`, `ui/*.py`, `export/pdf_generator.py`, `style.py` sont modifiés. Les 59 tests `tests/test_sizing.py` passent sans changement. Streamlit session_state orchestre le routing wizard.

**Tech Stack:** Streamlit 1.54.0, Python 3.12, CSS inline + style.py, LangGraph (agent existant — pas modifié)

---

## Fichiers modifiés

| Fichier | Rôle dans ce plan |
|---------|------------------|
| `app.py` | Routing wizard, sidebar Raana, checklist → wizard bar |
| `ui/style.py` | CSS wizard bar, kpi-card, component-card, mobile |
| `ui/results_display.py` | Layout cartes résultats, Analyse IA fonctionnelle |
| `ui/input_forms.py` | Tableau inline équipements, compteur live, factures cards |
| `ui/localisation_composants.py` | Enter pour recherche, indicateurs onglets |
| `export/pdf_generator.py` | En-tête Raana, nom fichier horodaté |
| `README.md` | Titre Raana |

---

## Task 1 : Renommage SolarDim → Raana + bug fixes rapides

**Files:**
- Modify: `app.py:7,26-30,42`
- Modify: `ui/style.py` (commentaires)
- Modify: `export/pdf_generator.py`
- Modify: `README.md`

- [ ] **Step 1 : Vérifier que les 59 tests passent avant de commencer**

```bash
cd /home/ali/Projects/solar/SolarDim
source .venv/bin/activate
pytest tests/test_sizing.py -v --tb=short
```
Expected : 59 passed

- [ ] **Step 2 : Corriger le bug CSS `color:vert` dans app.py ligne 29**

Dans `app.py`, remplacer :
```python
            <div style='font-size:16px; color:vert;'>Fahishal</div>
```
Par :
```python
            <div style='font-size:13px; color:#aaa;'>Fahishal</div>
```

- [ ] **Step 3 : Mettre à jour le page_title et le logo sidebar dans app.py**

Remplacer le bloc `st.set_page_config` et le bloc `st.markdown` du logo sidebar :
```python
st.set_page_config(
    page_title="Raana",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="auto"
)
```

Remplacer le markdown logo sidebar :
```python
    st.markdown("""
        <div style='text-align:center; padding: 20px 0 20px 0;'>
            <div style='font-size:48px;'>☀️</div>
            <div style='font-size:28px; font-weight:bold; color:white; letter-spacing:2px;'>Raana</div>
            <div style='font-size:13px; color:#aaa;'>Fahishal</div>
        </div>
    """, unsafe_allow_html=True)
```

- [ ] **Step 4 : Supprimer la double initialisation de `st.session_state.page_active` dans app.py**

Supprimer les lignes 41-43 (le second bloc `if "page_active" not in st.session_state:` dans la sidebar) — garder uniquement l'initialisation ligne 17.

Supprimer aussi le bloc de validation `noms_valides` (lignes 46-48) — il devient inutile avec le wizard.

- [ ] **Step 5 : Mettre à jour l'en-tête PDF dans export/pdf_generator.py**

Chercher toute occurrence de "SolarDim" dans `export/pdf_generator.py` et la remplacer par "Raana". Chercher avec :
```bash
grep -n "SolarDim\|solardim\|solar_dim" export/pdf_generator.py
```
Remplacer chaque occurrence.

- [ ] **Step 6 : Mettre à jour le nom du fichier PDF exporté dans `ui/results_display.py`**

Remplacer la ligne du `file_name` dans `st.download_button` :
```python
# Ancien
file_name=f"dimensionnement_{ville}_{datetime.now().strftime('%Y%m%d')}.pdf",
# Nouveau
file_name=f"raana_{ville}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
```

- [ ] **Step 7 : Mettre à jour README.md**

Remplacer "SolarDim Pro" / "SolarDim" par "Raana" dans les titres et descriptions du README.

- [ ] **Step 8 : Corriger la font-size des en-têtes de tableau dans ui/style.py**

Remplacer :
```css
        .result-table thead th {
            padding: 12px 16px;
            text-align: left;
            font-size: 24px;
```
Par :
```css
        .result-table thead th {
            padding: 12px 16px;
            text-align: left;
            font-size: 14px;
```

- [ ] **Step 9 : Vérifier les tests et commiter**

```bash
pytest tests/test_sizing.py -v --tb=short
```
Expected : 59 passed

```bash
git add app.py ui/style.py ui/results_display.py export/pdf_generator.py README.md
git commit -m "feat: renommer SolarDim en Raana, corriger bugs CSS"
```

---

## Task 2 : CSS — Nouvelles classes (style.py)

**Files:**
- Modify: `ui/style.py`

- [ ] **Step 1 : Ajouter les classes CSS du wizard bar**

À la fin de la fonction `get_css()`, avant la balise de fermeture `</style>`, ajouter :

```css
    /* =================== WIZARD BAR ====================== */
        .wizard-bar {
            display: flex;
            align-items: center;
            background: #0e1f3a;
            padding: 12px 24px;
            border-radius: 12px;
            margin-bottom: 24px;
            gap: 0;
        }
        .wizard-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            position: relative;
            cursor: pointer;
        }
        .wizard-step-circle {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: bold;
            z-index: 1;
            transition: all 0.2s;
        }
        .wizard-step-circle.done { background: #27AE60; color: white; }
        .wizard-step-circle.active { background: #F4A300; color: white; box-shadow: 0 0 0 3px rgba(244,163,0,0.3); }
        .wizard-step-circle.pending { background: #333; color: #888; }
        .wizard-step-label {
            font-size: 10px;
            margin-top: 4px;
            white-space: nowrap;
        }
        .wizard-step-label.done { color: #27AE60; }
        .wizard-step-label.active { color: #F4A300; font-weight: bold; }
        .wizard-step-label.pending { color: #666; }
        .wizard-connector {
            flex: 1;
            height: 2px;
            margin-bottom: 14px;
        }
        .wizard-connector.done { background: #27AE60; }
        .wizard-connector.pending { background: #333; }
        .wizard-nav {
            display: flex;
            justify-content: space-between;
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid #e0e0e0;
        }
        .wizard-nav-btn {
            padding: 8px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
        }

    /* =================== KPI CARDS (résultats) =================== */
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }
        .kpi-card {
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        .kpi-card.dark { background: #1B2A4A; }
        .kpi-card.light { background: white; border-left: 3px solid #F4A300; }
        .kpi-card.green { background: #27AE60; }
        .kpi-card.gray { background: #f0f0f0; }
        .kpi-card .kpi-label {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .kpi-card.dark .kpi-label { color: #F4A300; }
        .kpi-card.light .kpi-label { color: #F4A300; }
        .kpi-card.green .kpi-label { color: #c8f5d8; }
        .kpi-card.gray .kpi-label { color: #888; }
        .kpi-card .kpi-value {
            font-size: 24px;
            font-weight: bold;
            line-height: 1.1;
        }
        .kpi-card.dark .kpi-value { color: white; }
        .kpi-card.light .kpi-value { color: #1B2A4A; }
        .kpi-card.green .kpi-value { color: white; }
        .kpi-card.gray .kpi-value { color: #555; }
        .kpi-card .kpi-sub {
            font-size: 11px;
            margin-top: 4px;
        }
        .kpi-card.dark .kpi-sub { color: #aaa; }
        .kpi-card.light .kpi-sub { color: #888; }
        .kpi-card.green .kpi-sub { color: #c8f5d8; }
        .kpi-card.gray .kpi-sub { color: #aaa; }

    /* =================== COMPONENT CARDS (résultats) =================== */
        .component-cards-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }
        .component-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }
        .component-card .cc-title {
            font-size: 12px;
            font-weight: bold;
            color: #1B2A4A;
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 2px solid #F4A300;
        }
        .component-card .cc-row {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            padding: 3px 0;
            border-bottom: 1px solid #f5f5f5;
        }
        .component-card .cc-row span:first-child { color: #888; }
        .component-card .cc-row span:last-child { color: #1B2A4A; font-weight: 600; }

    /* =================== CONSUMPTION COUNTER =================== */
        .consumption-counter {
            background: #1B2A4A;
            border-radius: 12px;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .consumption-counter .cc-left .cc-label {
            font-size: 10px;
            color: #F4A300;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .consumption-counter .cc-left .cc-total {
            font-size: 28px;
            font-weight: bold;
            color: white;
        }
        .consumption-counter .cc-right { text-align: right; }
        .consumption-counter .cc-right .cc-kwh {
            font-size: 18px;
            font-weight: bold;
            color: #F4A300;
        }
        .consumption-counter .cc-right .cc-count {
            font-size: 11px;
            color: #27AE60;
        }

    /* =================== DISTRIBUTION BARS =================== */
        .distrib-bar-container { margin-bottom: 4px; }
        .distrib-bar-header {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #666;
            margin-bottom: 3px;
        }
        .distrib-bar-track {
            height: 8px;
            background: #eee;
            border-radius: 4px;
            overflow: hidden;
        }
        .distrib-bar-fill {
            height: 100%;
            border-radius: 4px;
            background: #1B2A4A;
        }
        .distrib-bar-fill.secondary { background: #F4A300; }

    /* =================== PULSE BOUTON ANALYSE =================== */
        @keyframes pulse-orange {
            0% { box-shadow: 0 0 0 0 rgba(244,163,0,0.5); }
            70% { box-shadow: 0 0 0 10px rgba(244,163,0,0); }
            100% { box-shadow: 0 0 0 0 rgba(244,163,0,0); }
        }
        .btn-pulse > button {
            animation: pulse-orange 1.5s infinite !important;
        }

    /* =================== RESPONSIVE WIZARD MOBILE =================== */
        @media (max-width: 768px) {
            .wizard-bar { padding: 8px 12px; }
            .wizard-step-label { display: none; }
            .kpi-row { grid-template-columns: repeat(2, 1fr); }
            .component-cards-row { grid-template-columns: 1fr; }
        }
```

- [ ] **Step 2 : Vérifier visuellement que le CSS est valide (pas d'erreur Python)**

```bash
python -c "from ui.style import get_css; css = get_css(); print('CSS OK, longueur:', len(css))"
```
Expected : `CSS OK, longueur: NNNNN` (pas d'erreur)

- [ ] **Step 3 : Commiter**

```bash
git add ui/style.py
git commit -m "style: ajouter classes CSS wizard, kpi-card, component-card, consumption-counter"
```

---

## Task 3 : app.py — Navigation wizard 5 étapes

**Files:**
- Modify: `app.py`

- [ ] **Step 1 : Définir les constantes et helpers du wizard en haut de app.py (après les imports)**

Ajouter après les imports et `st.set_page_config` :

```python
# ==============================
# WIZARD CONFIG
# ==============================
WIZARD_STEPS = [
    ("📄", "Factures"),
    ("🔌", "Équipements"),
    ("📍", "Localisation"),
    ("🔧", "Configurations"),
    ("⚡", "Analyse"),
]
WIZARD_STEP_NAMES = [nom for _, nom in WIZARD_STEPS]
SIDEBAR_PAGES = ["Guide & Notions", "Analyse IA"]


def _get_step_status(step_nom: str, data: dict) -> str:
    """Retourne 'done', 'active' ou 'pending' pour une étape du wizard."""
    if step_nom == st.session_state.page_active:
        return "active"
    if step_nom == "Factures" and data.get("factures"):
        return "done"
    if step_nom == "Équipements" and data.get("equipements"):
        return "done"
    if step_nom == "Localisation" and data.get("localisation"):
        return "done"
    if step_nom == "Configurations" and any([data.get("module"), data.get("onduleur"), data.get("batterie")]):
        return "done"
    if step_nom == "Analyse" and "dim" in st.session_state:
        return "done"
    return "pending"


def _afficher_wizard_bar(data: dict) -> None:
    """Affiche la barre de progression wizard en HTML."""
    html = "<div class='wizard-bar'>"
    for i, (icone, nom) in enumerate(WIZARD_STEPS):
        statut = _get_step_status(nom, data)
        label_circle = "✓" if statut == "done" else str(i + 1)
        html += f"""
        <div class='wizard-step' onclick="''">
            <div class='wizard-step-circle {statut}'>{label_circle}</div>
            <div class='wizard-step-label {statut}'>{icone} {nom}</div>
        </div>"""
        if i < len(WIZARD_STEPS) - 1:
            connector_class = "done" if statut == "done" else "pending"
            html += f"<div class='wizard-connector {connector_class}'></div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
```

- [ ] **Step 2 : Remplacer la sidebar par la version simplifiée (logo Raana + 2 boutons)**

Remplacer tout le bloc `with st.sidebar:` par :

```python
# ==============================
# SIDEBAR SIMPLIFIÉE
# ==============================
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 20px 0 16px 0;'>
            <div style='font-size:44px;'>☀️</div>
            <div style='font-size:26px; font-weight:bold; color:white; letter-spacing:2px;'>Raana</div>
            <div style='font-size:12px; color:#aaa;'>Fahishal</div>
        </div>
        <div style='height:1px; background:#1a2a4a; margin:0 8px 12px 8px;'></div>
    """, unsafe_allow_html=True)

    for icone, nom in [("📖", "Guide & Notions"), ("🤖", "Analyse IA")]:
        is_active = st.session_state.page_active == nom
        btn_style = "background:#F4A300 !important; color:white !important; font-weight:bold !important;"
        if is_active:
            st.markdown(f"<style>[data-testid='stSidebar'] [data-testid='stBaseButton-secondary']:has(p:contains('{nom}')) {{ {btn_style} }}</style>", unsafe_allow_html=True)
        if st.button(f"{icone}  {nom}", key=f"nav_{nom}", use_container_width=True):
            st.session_state.page_active = nom
            st.rerun()

    st.markdown("<div style='height:1px; background:#1a2a4a; margin:12px 8px 0 8px;'></div>", unsafe_allow_html=True)

    # Boutons étapes wizard dans la sidebar aussi (accès rapide)
    st.markdown("<div style='font-size:10px; color:#555; padding: 8px 16px; text-transform:uppercase; letter-spacing:0.5px;'>Étapes</div>", unsafe_allow_html=True)
    for icone, nom in WIZARD_STEPS:
        if st.button(f"{icone} {nom}", key=f"nav_wizard_{nom}", use_container_width=True):
            st.session_state.page_active = nom
            st.rerun()
```

- [ ] **Step 3 : Remplacer le bloc de routage principal par le nouveau routing wizard**

Remplacer tout le bloc de routage (depuis `page = st.session_state.page_active` jusqu'à la fin du fichier) par :

```python
# ==============================
# DONNÉES POUR WIZARD BAR
# ==============================
page = st.session_state.page_active

from core.storage import (
    get_factures, get_equipements, get_localisation,
    get_consommation_moyenne, get_module_pv,
    get_onduleur, get_batterie, get_strings, get_parametres
)
from core.sizing import calculer_dimensionnement_complet, calculer_consommation_journaliere

factures = get_factures()
equipements = get_equipements()
localisation = get_localisation()
module = get_module_pv()
onduleur_data = get_onduleur()
batterie_u = get_batterie()
strings = get_strings()
moyenne = get_consommation_moyenne()

_wizard_data = {
    "factures": factures,
    "equipements": equipements,
    "localisation": localisation,
    "module": module,
    "onduleur": onduleur_data,
    "batterie": batterie_u,
}

# ==============================
# PAGES SIDEBAR (hors wizard)
# ==============================
if page == "Guide & Notions":
    st.markdown("<div class='page-title'>📖 Guide & Notions</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Comprendre les concepts et utiliser l'outil efficacement</div>", unsafe_allow_html=True)
    from ui.guide import afficher_guide
    afficher_guide()

elif page == "Analyse IA":
    st.markdown("<div class='page-title'>🤖 Analyse IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Posez une question à l'agent solaire</div>", unsafe_allow_html=True)
    from ui.results_display import afficher_rapport_agent
    afficher_rapport_agent()

# ==============================
# PAGES WIZARD
# ==============================
else:
    # S'assurer que la page est valide
    if page not in WIZARD_STEP_NAMES:
        st.session_state.page_active = "Factures"
        st.rerun()

    _afficher_wizard_bar(_wizard_data)
    step_index = WIZARD_STEP_NAMES.index(page)

    # ----------------------------
    # ÉTAPE 1 — FACTURES
    # ----------------------------
    if page == "Factures":
        st.markdown("<div class='page-title'>📄 Factures d'électricité</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-subtitle'>Uploadez vos factures pour estimer votre consommation</div>", unsafe_allow_html=True)
        from ui.input_forms import afficher_formulaire_factures
        afficher_formulaire_factures()

    # ----------------------------
    # ÉTAPE 2 — ÉQUIPEMENTS
    # ----------------------------
    elif page == "Équipements":
        st.markdown("<div class='page-title'>🔌 Équipements électriques</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-subtitle'>Listez vos appareils pour estimer votre consommation</div>", unsafe_allow_html=True)
        from ui.input_forms import afficher_formulaire_equipements
        afficher_formulaire_equipements()

    # ----------------------------
    # ÉTAPE 3 — LOCALISATION
    # ----------------------------
    elif page == "Localisation":
        st.markdown("<div class='page-title'>📍 Localisation du site</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-subtitle'>Données d'ensoleillement via PVGIS</div>", unsafe_allow_html=True)
        from ui.localisation_composants import afficher_localisation
        afficher_localisation()

    # ----------------------------
    # ÉTAPE 4 — CONFIGURATIONS
    # ----------------------------
    elif page == "Configurations":
        st.markdown("<div class='page-title'>🔧 Configurations</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-subtitle'>Renseignez vos composants et les paramètres économiques</div>", unsafe_allow_html=True)
        from ui.localisation_composants import afficher_composants
        afficher_composants()

    # ----------------------------
    # ÉTAPE 5 — ANALYSE
    # ----------------------------
    elif page == "Analyse":
        st.markdown("<div class='page-title'>⚡ Analyse & Résultats</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-subtitle'>Dimensionnement complet de votre installation</div>", unsafe_allow_html=True)
        from ui.results_display import afficher_metriques_dimensionnement

        peut_analyser = (len(factures) >= 1 or len(equipements) >= 1) and localisation is not None

        if not peut_analyser:
            st.warning("⚠️ Complétez au minimum les étapes **Consommation** (Factures ou Équipements) et **Localisation** avant de lancer l'analyse.")
        else:
            # Bouton pulse quand toutes les conditions sont réunies
        if peut_analyser and "dim" not in st.session_state:
            st.markdown("<div class='btn-pulse'>", unsafe_allow_html=True)
        if st.button("⚡ Lancer l'analyse", type="primary", use_container_width=True):
            with st.spinner("Calcul en cours..."):
                try:
                    if equipements:
                        dim = calculer_dimensionnement_complet(
                            hsp=localisation["hsp_moyen"],
                            equipements=equipements,
                            module=module,
                            onduleur=onduleur_data,
                            strings=strings,
                            batterie_unitaire=batterie_u
                        )
                    else:
                        dim = calculer_dimensionnement_complet(
                            hsp=localisation["hsp_moyen"],
                            conso_journaliere_kwh=moyenne["consommation_journaliere_moyenne_kwh"],
                            module=module,
                            onduleur=onduleur_data,
                            strings=strings,
                            batterie_unitaire=batterie_u
                        )
                    st.session_state.dim = dim
                    st.success("✅ Analyse terminée !")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur : {e}")
        if peut_analyser and "dim" not in st.session_state:
            st.markdown("</div>", unsafe_allow_html=True)

        afficher_metriques_dimensionnement()

    # ----------------------------
    # NAVIGATION PRÉCÉDENT / SUIVANT
    # ----------------------------
    st.markdown("<div class='wizard-nav'>", unsafe_allow_html=True)
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if step_index > 0:
            if st.button(f"← {WIZARD_STEPS[step_index - 1][1]}", use_container_width=True):
                st.session_state.page_active = WIZARD_STEP_NAMES[step_index - 1]
                st.rerun()
    with col_next:
        if step_index < len(WIZARD_STEPS) - 1:
            if st.button(f"{WIZARD_STEPS[step_index + 1][1]} →", type="primary", use_container_width=True):
                st.session_state.page_active = WIZARD_STEP_NAMES[step_index + 1]
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
```

- [ ] **Step 4 : Initialisation session_state — s'assurer que page_active démarre sur "Factures"**

Vérifier ligne 17 de app.py :
```python
if "page_active" not in st.session_state:
    st.session_state.page_active = "Factures"
```

- [ ] **Step 5 : Lancer l'app et vérifier visuellement**

```bash
streamlit run app.py
```
Vérifier :
- La sidebar affiche le logo Raana avec couleur `#aaa` pour "Fahishal"
- La barre wizard 5 étapes apparaît dans le contenu principal
- Les boutons Précédent/Suivant naviguent entre étapes
- Guide & Notions et Analyse IA s'ouvrent depuis la sidebar

- [ ] **Step 6 : Commiter**

```bash
pytest tests/test_sizing.py -v --tb=short
git add app.py
git commit -m "feat: navigation wizard 5 étapes, sidebar Raana simplifiée"
```

---

## Task 4 : ui/results_display.py — Cartes visuelles résultats

**Files:**
- Modify: `ui/results_display.py`

- [ ] **Step 1 : Remplacer `afficher_metriques_dimensionnement()` par le nouveau layout**

Remplacer le contenu complet de la fonction `afficher_metriques_dimensionnement()` dans `ui/results_display.py` par :

```python
def afficher_metriques_dimensionnement() -> None:
    if "dim" not in st.session_state:
        return

    dim = st.session_state.dim
    localisation = get_localisation()
    moyenne = get_consommation_moyenne()
    parametres = get_parametres()
    ville = localisation["ville"].split(",")[0] if localisation else "site"

    tarif = moyenne["tarif_moyen_fcfa_kwh"] if moyenne else float(parametres["tarif_kwh"])
    prix_installation = float(parametres["prix_total_installation"])

    rentabilite = None
    if prix_installation > 0 and localisation:
        try:
            rentabilite = calculer_rentabilite(
                prix_total_installation=prix_installation,
                production_annuelle_kwh=float(localisation["irradiation_annuelle_kwh"]) * dim["puissance_installee_kwc"],
                tarif_kwh=tarif,
            )
            st.session_state.rentabilite = rentabilite
        except (ValueError, KeyError) as e:
            logger.error("Erreur calcul rentabilité : %s", e)

    st.markdown("---")

    # ---- Zone 1 : KPI Cards ----
    roi_class = "gray"
    roi_value = "—"
    roi_sub = "Prix installation non renseigné"
    if rentabilite:
        roi_ans = rentabilite["temps_retour_ans"]
        roi_value = f"{roi_ans} ans"
        roi_sub = f"Économies : {rentabilite['economies_annuelles']:,.0f} FCFA/an"
        roi_class = "green" if roi_ans <= 10 else "dark"

    st.markdown(f"""
    <div class='kpi-row'>
        <div class='kpi-card dark'>
            <div class='kpi-label'>Puissance installée</div>
            <div class='kpi-value'>{dim['puissance_installee_kwc']} kWc</div>
            <div class='kpi-sub'>{dim['nombre_panneaux']} × {dim['puissance_panneau_wc']} Wc</div>
        </div>
        <div class='kpi-card light'>
            <div class='kpi-label'>Batterie</div>
            <div class='kpi-value'>{dim['batterie']['capacite_ah']} Ah</div>
            <div class='kpi-sub'>{dim['batterie']['tension_v']} V — {dim['batterie']['autonomie_jours']} jour(s)</div>
        </div>
        <div class='kpi-card light'>
            <div class='kpi-label'>Onduleur recommandé</div>
            <div class='kpi-value'>{dim['puissance_onduleur_recommandee_kva']} kVA</div>
            <div class='kpi-sub'>Off-grid</div>
        </div>
        <div class='kpi-card {roi_class}'>
            <div class='kpi-label'>Retour investissement</div>
            <div class='kpi-value'>{roi_value}</div>
            <div class='kpi-sub'>{roi_sub}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Zone 2 : Component Cards ----
    # Card Panneaux PV
    strings_html = ""
    if dim.get("configuration_strings"):
        for s in dim["configuration_strings"].get("strings", []):
            if s.get("nb_panneaux_affectes", 0) > 0:
                strings_html += f"<div class='cc-row'><span>Entrée PV {s['numero_string']}</span><span>{s['nb_serie_affecte']}S × {s['nb_parallele_affecte']}P</span></div>"

    surface_html = ""
    if dim.get("surface_champ"):
        surface_html = f"<div class='cc-row'><span>Surface champ</span><span>{dim['surface_champ']['surface_totale_m2']} m²</span></div>"

    # Card Batterie
    batterie_html = f"""
        <div class='cc-row'><span>Configuration</span><span>—</span></div>
        <div class='cc-row'><span>Nb batteries</span><span>—</span></div>
        <div class='cc-row'><span>Tension parc</span><span>{dim['batterie']['tension_v']} V</span></div>
        <div class='cc-row'><span>Capacité réelle</span><span>{dim['batterie']['capacite_ah']} Ah</span></div>
    """
    if dim.get("configuration_batterie"):
        cb = dim["configuration_batterie"]
        batterie_html = f"""
            <div class='cc-row'><span>Configuration</span><span>{cb['nb_batteries_serie']}S × {cb['nb_batteries_parallele']}P</span></div>
            <div class='cc-row'><span>Nb batteries</span><span>{cb['nb_batteries_total']} unités</span></div>
            <div class='cc-row'><span>Tension parc</span><span>{cb['tension_parc_v']} V</span></div>
            <div class='cc-row'><span>Capacité réelle</span><span>{cb['capacite_reelle_ah']} Ah</span></div>
        """

    source = "Équipements" if dim["source_consommation"] == "equipements" else "Factures"

    st.markdown(f"""
    <div class='component-cards-row'>
        <div class='component-card'>
            <div class='cc-title'>🔆 Panneaux PV</div>
            <div class='cc-row'><span>Nb panneaux</span><span>{dim['nombre_panneaux']}</span></div>
            <div class='cc-row'><span>Puissance unitaire</span><span>{dim['puissance_panneau_wc']} Wc</span></div>
            {strings_html}
            {surface_html}
        </div>
        <div class='component-card'>
            <div class='cc-title'>🔋 Parc Batterie</div>
            {batterie_html}
        </div>
        <div class='component-card'>
            <div class='cc-title'>📄 Fiche technique</div>
            <div class='cc-row'><span>Consommation</span><span>{dim['consommation_journaliere_kwh']} kWh/j</span></div>
            <div class='cc-row'><span>Source</span><span>{source}</span></div>
            <div class='cc-row'><span>HSP utilisé</span><span>{dim['hsp_utilise']} h/j</span></div>
            <div class='cc-row'><span>Performance Ratio</span><span>{PERFORMANCE_RATIO_DEFAULT}</span></div>
            <div class='cc-row'><span>DoD batterie</span><span>{int(dim['batterie']['profondeur_decharge'] * 100)} %</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Avertissements ----
    avertissements = []
    if dim.get("configuration_strings"):
        avertissements.extend(dim["configuration_strings"].get("avertissements", []))
        non_affectes = dim["configuration_strings"].get("panneaux_non_affectes", 0)
        if non_affectes > 0:
            avertissements.append(f"⚠️ {non_affectes} panneau(x) non affecté(s)")
    if dim.get("configuration_batterie") and dim["configuration_batterie"].get("avertissement_tension"):
        avertissements.append(dim["configuration_batterie"]["avertissement_tension"])
    for avert in avertissements:
        st.warning(avert)

    # ---- Zone 3 : Graphe + Export ----
    if rentabilite:
        st.subheader("💰 Projection rentabilité 10 ans")
        afficher_graphe_rentabilite(rentabilite)
    else:
        st.info("💡 Renseignez le prix total de l'installation dans **Configurations → Paramètres économiques** pour voir la rentabilité.")

    st.markdown("<br>", unsafe_allow_html=True)
    try:
        pdf_bytes = generer_pdf_dimensionnement(
            dim=dim,
            localisation=localisation,
            rentabilite=rentabilite,
            moyenne=moyenne,
            parametres=parametres
        )
        st.download_button(
            label="📥 Exporter en PDF",
            data=pdf_bytes,
            file_name=f"raana_{ville}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    except Exception as e:
        logger.error("Erreur génération PDF : %s", e)
        st.error("❌ Erreur lors de la génération du PDF.")
```

- [ ] **Step 2 : Vérifier visuellement en lançant l'app et en allant sur l'étape Analyse**

```bash
streamlit run app.py
```
Naviguer vers Étape 5 → Analyse. Lancer l'analyse. Vérifier :
- 4 KPI cards en haut
- 3 component cards (Panneaux, Batterie, Fiche technique)
- Graphe Plotly si prix installation renseigné
- Bouton PDF fonctionnel

- [ ] **Step 3 : Commiter**

```bash
pytest tests/test_sizing.py -v --tb=short
git add ui/results_display.py
git commit -m "feat: résultats en cartes visuelles (kpi-card + component-card)"
```

---

## Task 5 : ui/input_forms.py — Équipements tableau inline + compteur live

**Files:**
- Modify: `ui/input_forms.py`

- [ ] **Step 1 : Remplacer `afficher_formulaire_equipements()` par le nouveau layout**

Remplacer la fonction complète `afficher_formulaire_equipements()` :

```python
def afficher_formulaire_equipements() -> None:
    equipements = get_equipements()
    total_wh = sum(e["conso_jour_wh"] for e in equipements) if equipements else 0
    total_kwh = round(total_wh / 1000, 2)
    nb = len(equipements)

    # --- Compteur live ---
    st.markdown(f"""
    <div class='consumption-counter'>
        <div class='cc-left'>
            <div class='cc-label'>Consommation totale estimée</div>
            <div class='cc-total'>{total_wh:,.0f} <span style='font-size:16px;font-weight:normal'>Wh/j</span></div>
        </div>
        <div class='cc-right'>
            <div class='cc-kwh'>{total_kwh} kWh/j</div>
            <div class='cc-count'>{'✓ ' + str(nb) + ' appareil(s)' if nb > 0 else '⚠ Aucun appareil'}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Formulaire ajout ---
    with st.form("form_equipement", clear_on_submit=True):
        col_nom, col_w, col_h, col_q, col_btn = st.columns([3, 1.5, 1.5, 1, 1.5])
        with col_nom:
            nom = st.text_input("Appareil", placeholder="Ex: Réfrigérateur", label_visibility="collapsed")
        with col_w:
            puissance = st.number_input("W", min_value=0, step=10, label_visibility="collapsed",
                                        placeholder="Puissance W")
        with col_h:
            heures = st.number_input("h/j", min_value=0.0, max_value=24.0, step=0.5,
                                     label_visibility="collapsed", placeholder="Heures/j")
        with col_q:
            quantite = st.number_input("Qté", min_value=1, step=1, label_visibility="collapsed")
        with col_btn:
            submit = st.form_submit_button("➕ Ajouter", use_container_width=True)

        if submit:
            if nom and nom.strip() and puissance > 0:
                conso = puissance * heures * quantite
                try:
                    ajouter_equipement(nom.strip(), puissance, heures, quantite, conso)
                    st.success(f"✅ {nom.strip()} ajouté !")
                except ValueError as e:
                    st.error(f"❌ {e}")
                st.rerun()
            else:
                st.error("Veuillez renseigner un nom et une puissance > 0.")

    # --- Tableau des équipements ---
    if equipements:
        st.markdown("**Équipements enregistrés :**")

        # En-tête tableau
        header_cols = st.columns([3, 1.5, 1.5, 1, 1.5, 0.8])
        headers = ["Appareil", "Puissance (W)", "Heures/jour", "Qté", "Conso (Wh/j)", ""]
        for col, h in zip(header_cols, headers):
            col.markdown(f"<div style='font-size:12px;color:#888;font-weight:600'>{h}</div>", unsafe_allow_html=True)

        for e in equipements:
            row_cols = st.columns([3, 1.5, 1.5, 1, 1.5, 0.8])
            row_cols[0].write(e["nom"])
            row_cols[1].write(str(e["puissance_w"]))
            row_cols[2].write(str(e["heures_par_jour"]))
            row_cols[3].write(str(e["quantite"]))
            row_cols[4].markdown(f"**{e['conso_jour_wh']:,.0f}**")
            if row_cols[5].button("✕", key=f"suppr_{e['id']}", help="Supprimer"):
                supprimer_equipement(e["id"])
                st.rerun()

        st.markdown("---")

        # --- Barres de répartition ---
        if total_wh > 0:
            st.markdown("**Répartition de la consommation :**")
            colors = ["#1B2A4A", "#F4A300", "#27AE60", "#E74C3C", "#9B59B6", "#16A085"]
            for i, e in enumerate(sorted(equipements, key=lambda x: x["conso_jour_wh"], reverse=True)):
                pct = round(e["conso_jour_wh"] / total_wh * 100, 1)
                color = colors[i % len(colors)]
                st.markdown(f"""
                <div class='distrib-bar-container'>
                    <div class='distrib-bar-header'>
                        <span>{e['nom']}</span><span>{pct}%</span>
                    </div>
                    <div class='distrib-bar-track'>
                        <div class='distrib-bar-fill' style='width:{pct}%; background:{color}'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Effacer tous les équipements"):
            effacer_equipements()
            st.rerun()
```

- [ ] **Step 2 : Vérifier visuellement — naviguer vers Étape 2 Équipements**

```bash
streamlit run app.py
```
Vérifier :
- Compteur `0 Wh/j` affiché en haut avant saisie
- Formulaire compact sur une ligne
- Après ajout : compteur se met à jour, barre de répartition visible
- Bouton ✕ dans le tableau supprime l'équipement

- [ ] **Step 3 : Commiter**

```bash
pytest tests/test_sizing.py -v --tb=short
git add ui/input_forms.py
git commit -m "feat: formulaire équipements — tableau inline, compteur live, barres répartition"
```

---

## Task 6 : ui/input_forms.py — Factures upload amélioré

**Files:**
- Modify: `ui/input_forms.py`

- [ ] **Step 1 : Remplacer le bloc récapitulatif moyenne dans `afficher_formulaire_factures()`**

Dans la fonction `afficher_formulaire_factures()`, remplacer le bloc `col1, col2, col3 = st.columns(3)` + metrics par des cards HTML :

```python
        moyenne = get_consommation_moyenne()
        if moyenne:
            st.markdown(f"""
            <div class='kpi-row' style='grid-template-columns: repeat(3, 1fr);'>
                <div class='kpi-card light'>
                    <div class='kpi-label'>Conso. journalière moyenne</div>
                    <div class='kpi-value'>{moyenne['consommation_journaliere_moyenne_kwh']} kWh/j</div>
                </div>
                <div class='kpi-card light'>
                    <div class='kpi-label'>Tarif moyen</div>
                    <div class='kpi-value'>{moyenne['tarif_moyen_fcfa_kwh']} FCFA</div>
                    <div class='kpi-sub'>par kWh</div>
                </div>
                <div class='kpi-card dark'>
                    <div class='kpi-label'>Factures analysées</div>
                    <div class='kpi-value'>{moyenne['nombre_factures']}</div>
                    <div class='kpi-sub'>✓ Données exploitables</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
```

- [ ] **Step 2 : Améliorer le label du file_uploader**

Remplacer :
```python
    fichiers = st.file_uploader(
        label="Ajouter des factures (PDF ou image)",
```
Par :
```python
    fichiers = st.file_uploader(
        label="📂 Glissez-déposez vos factures ici ou cliquez pour sélectionner",
```

- [ ] **Step 3 : Vérifier visuellement — naviguer vers Étape 1 Factures**

```bash
streamlit run app.py
```
Vérifier que le récapitulatif post-analyse affiche bien 3 cards (conso, tarif, nb factures).

- [ ] **Step 4 : Commiter**

```bash
pytest tests/test_sizing.py -v --tb=short
git add ui/input_forms.py
git commit -m "feat: formulaire factures — cards récapitulatif, zone upload améliorée"
```

---

## Task 7 : ui/localisation_composants.py — Localisation + indicateurs configs

**Files:**
- Modify: `ui/localisation_composants.py`

- [ ] **Step 1 : Ajouter Enter pour recherche dans `afficher_localisation()`**

Envelopper le champ ville et le bouton dans un `st.form` :

Remplacer le bloc depuis `st.write("Rechercher un lieu :")` jusqu'à `if rechercher and ville:` par :

```python
    st.write("Rechercher un lieu :")

    with st.form("form_localisation", enter_to_submit=True):
        col_input, col_btn = st.columns([4, 1])
        with col_input:
            ville = st.text_input(
                "Ville",
                placeholder="Ex: Lomé, Abidjan, Dakar...",
                label_visibility="collapsed",
                max_chars=100
            )
        with col_btn:
            rechercher = st.form_submit_button("🔍 Rechercher", use_container_width=True)

    if rechercher and ville:
```

- [ ] **Step 2 : Remplacer le résumé localisation par des cards dans `afficher_localisation()`**

Remplacer le bloc `if localisation:` (qui utilise `st.metric`) par :

```python
    localisation = get_localisation()
    if localisation:
        ville_affichee = localisation['ville'].split(',')[0]
        st.markdown(f"""
        <div class='kpi-row' style='grid-template-columns: repeat(4, 1fr);'>
            <div class='kpi-card dark'>
                <div class='kpi-label'>Lieu</div>
                <div class='kpi-value' style='font-size:18px'>{ville_affichee}</div>
                <div class='kpi-sub'>✓ Enregistré</div>
            </div>
            <div class='kpi-card light'>
                <div class='kpi-label'>HSP moyen</div>
                <div class='kpi-value'>{localisation['hsp_moyen']}</div>
                <div class='kpi-sub'>heures/jour</div>
            </div>
            <div class='kpi-card light'>
                <div class='kpi-label'>Irradiation</div>
                <div class='kpi-value' style='font-size:18px'>{localisation['irradiation_annuelle_kwh']}</div>
                <div class='kpi-sub'>kWh/m²/an</div>
            </div>
            <div class='kpi-card light'>
                <div class='kpi-label'>Coordonnées</div>
                <div class='kpi-value' style='font-size:14px'>{localisation['latitude']:.3f}°</div>
                <div class='kpi-sub'>{localisation['longitude']:.3f}° — PVGIS ✓</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
```

- [ ] **Step 3 : Ajouter indicateurs ✓/✗ dans les onglets de `afficher_composants()`**

Remplacer le début de la fonction `afficher_composants()` :

```python
def afficher_composants() -> None:
    """Page configurations avec quatre sous-onglets."""
    onduleur = get_onduleur()
    module = get_module_pv()
    batterie = get_batterie()
    parametres = get_parametres()

    ok_onduleur = "✓" if onduleur else "—"
    ok_module = "✓" if module else "—"
    ok_batterie = "✓" if batterie else "—"
    prix = float(parametres["prix_total_installation"]) if parametres else 0
    ok_params = "✓" if prix > 0 else "—"

    tab_onduleur, tab_module, tab_batterie, tab_params = st.tabs([
        f"⚡ Onduleur {ok_onduleur}",
        f"🔆 Module PV {ok_module}",
        f"🔋 Batterie {ok_batterie}",
        f"💰 Paramètres éco {ok_params}"
    ])
```

- [ ] **Step 4 : Vérifier visuellement**

```bash
streamlit run app.py
```
Vérifier :
- Étape 3 Localisation : Enter dans le champ ville déclenche la recherche
- Résumé localisation en 4 cards
- Étape 4 Configurations : onglets affichent ✓ quand composant enregistré

- [ ] **Step 5 : Commiter**

```bash
pytest tests/test_sizing.py -v --tb=short
git add ui/localisation_composants.py
git commit -m "feat: localisation cards + Enter pour recherche + indicateurs onglets configs"
```

---

## Task 8 : ui/results_display.py — Page Analyse IA fonctionnelle

**Files:**
- Modify: `ui/results_display.py`

- [ ] **Step 1 : Remplacer `afficher_rapport_agent()` par le formulaire agent**

Remplacer la fonction `afficher_rapport_agent()` par :

```python
def afficher_rapport_agent() -> None:
    if "dim" not in st.session_state:
        st.info("💡 Lancez d'abord une analyse depuis l'étape **Analyse** avant de consulter l'agent.")
        if st.button("→ Aller à l'analyse", type="primary"):
            st.session_state.page_active = "Analyse"
            st.rerun()
        return

    st.write("Posez une question à l'agent IA solaire. Il a accès à vos données de projet.")
    st.caption("Exemples : *Optimise ma configuration*, *Explique le calcul de batterie*, *Quel panneau recommandes-tu ?*")

    question = st.text_area(
        "Votre question",
        placeholder="Ex: Explique-moi le dimensionnement et propose des optimisations...",
        height=100,
        label_visibility="collapsed"
    )

    if st.button("🤖 Envoyer à l'agent", type="primary", use_container_width=True, disabled=not question.strip()):
        with st.spinner("L'agent analyse votre projet..."):
            try:
                from agent.agent import creer_agent
                agent = creer_agent()
                result = agent.invoke({"messages": [{"role": "user", "content": question.strip()}]})
                messages = result.get("messages", [])
                # Récupérer le dernier message de l'agent (pas un ToolMessage)
                reponse = ""
                for msg in reversed(messages):
                    if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_call_id"):
                        reponse = msg.content
                        break
                if reponse:
                    st.markdown("---")
                    st.markdown("**Réponse de l'agent :**")
                    st.markdown(reponse)
                else:
                    st.warning("L'agent n'a pas retourné de réponse textuelle.")
            except Exception as e:
                logger.error("Erreur agent IA : %s", e)
                st.error(f"❌ Erreur de l'agent : {e}")
```

- [ ] **Step 2 : Ajouter l'import manquant en haut de results_display.py si absent**

Vérifier que `logging` est importé (déjà présent). Pas de nouvel import nécessaire — `creer_agent` est importé localement dans la fonction.

- [ ] **Step 3 : Vérifier visuellement**

```bash
streamlit run app.py
```
Aller dans la sidebar → Analyse IA. Vérifier :
- Sans analyse lancée : message d'invite + bouton → Analyse
- Avec analyse lancée : formulaire de question visible
- Après envoi : réponse de l'agent affichée (nécessite GROQ_API_KEY dans .env)

- [ ] **Step 4 : Commiter**

```bash
pytest tests/test_sizing.py -v --tb=short
git add ui/results_display.py
git commit -m "feat: page Analyse IA — formulaire agent fonctionnel"
```

---

## Task 9 : Vérification finale

- [ ] **Step 1 : Lancer tous les tests**

```bash
pytest tests/test_sizing.py -v
```
Expected : 59 passed, 0 failed

- [ ] **Step 2 : Vérifier le parcours complet dans le navigateur**

```bash
streamlit run app.py
```

Checklist manuelle :
- [ ] Logo "Raana" visible dans la sidebar, sous-titre "Fahishal" en gris `#aaa`
- [ ] Barre wizard 5 étapes visible dans le contenu principal
- [ ] Étape 1 Factures : upload fonctionnel, cards récapitulatif après analyse
- [ ] Étape 2 Équipements : compteur live, tableau inline, barres répartition
- [ ] Étape 3 Localisation : recherche avec Enter, 4 cards résumé
- [ ] Étape 4 Configurations : indicateurs ✓/✗ dans les onglets
- [ ] Étape 5 Analyse : 4 KPI cards + 3 component cards + graphe + PDF
- [ ] Nom PDF contient "raana_" et heure
- [ ] Guide & Notions accessible depuis sidebar
- [ ] Analyse IA : formulaire visible après analyse lancée
- [ ] Mobile : réduire la fenêtre à <768px, vérifier que les cards passent en 2 colonnes

- [ ] **Step 3 : Commit final**

```bash
git add -A
git commit -m "feat: Raana UI redesign complet — wizard, cartes, formulaires, mobile"
```
