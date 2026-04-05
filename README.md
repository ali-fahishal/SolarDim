# ☀️ Raana
### Outil intelligent de dimensionnement de systèmes photovoltaïques off-grid

---

## 📋 Description

Raana est une application web dédiée aux techniciens en énergie solaire, 
permettant de dimensionner rapidement et précisément un système photovoltaïque 
off-grid à partir de factures d'électricité ou d'une liste d'équipements.

L'outil s'adapte aux données disponibles : plus vous renseignez de paramètres, 
plus les résultats sont détaillés.

---

## 🚀 Fonctionnalités

- 📄 **Analyse automatique de factures** — extraction intelligente via IA (Groq / LLaMA)
- 🔌 **Saisie des équipements** — calcul de la consommation journalière
- 📍 **Données solaires** — récupération automatique via PVGIS (HSP, irradiation)
- ⚡ **Dimensionnement complet** — panneaux, batteries, onduleur
- 🔧 **Configuration avancée** — strings MPPT, configuration série/parallèle, surface du champ
- 💰 **Étude de rentabilité** — projection sur 10 ans, ROI, économies annuelles
- 📥 **Export PDF** — rapport professionnel téléchargeable
- 📖 **Guide intégré** — explication des notions solaires

---

## 🏗️ Architecture

```
pv-dimensioning/
├── app.py                        # Point d'entrée Streamlit
├── core/
│   ├── storage.py                # Base de données SQLite
│   ├── sizing.py                 # Calculs de dimensionnement (Python pur)
│   ├── solar_data.py             # API Nominatim + PVGIS
│   └── facture_extractor.py      # Extraction IA des factures
├── export/
│   └── pdf_generator.py          # Génération des rapports PDF
├── agent/
│   ├── agent.py                  # Agent LangChain (Analyse IA)
│   └── tools.py                  # Outils de l'agent
└── ui/
    ├── input_forms.py            # Formulaires factures & équipements
    ├── localisation_composants.py # Localisation & configurations
    ├── results_display.py         # Affichage des résultats
    ├── guide.py                   # Guide & notions
    └── style.py                   # CSS personnalisé
```

---

## 🧮 Logique de calcul

Les calculs sont entièrement déterministes en Python — zéro LLM impliqué :

```
Puissance crête = Consommation journalière / (HSP × PR)
PR = 0.65 (standard off-grid Afrique de l'Ouest)

Capacité batterie = (Conso × Autonomie) / (Tension × DoD)
DoD = 0.95 (lithium) | Autonomie = 1 jour

Nb panneaux série  : ceil(Vmppt_min / Vmp) → floor(Vmppt_max / Vmp)
Nb panneaux // max : floor(Imax_string / Imp)

Surface champ = Nb panneaux × (L × l) × 1.1 (coefficient aération)
```

---

## ⚙️ Installation

### Prérequis
- Python 3.12+
- Clé API Groq (gratuit sur console.groq.com)

### Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/USERNAME/solardim-pro.git
cd solardim-pro

# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Editer .env et ajouter votre clé GROQ_API_KEY

# Lancer l'application
streamlit run app.py
```

---

## 🔑 Variables d'environnement

Créez un fichier `.env` à la racine :

```env
GROQ_API_KEY=votre_cle_api_groq
```

---

## 📦 Stack technique

| Composant | Technologie |
|-----------|-------------|
| Framework | Streamlit |
| Base de données | SQLite |
| LLM | Groq (LLaMA 3.3 70B) |
| Vision OCR | LLaMA 4 Scout (factures) |
| Données solaires | PVGIS API v5.2 |
| Géocodage | Nominatim (OpenStreetMap) |
| Graphiques | Plotly |
| Export PDF | ReportLab |
| Agent IA | LangChain + LangGraph |

---

## 🌍 Contexte

Développé pour les techniciens en énergie solaire en **Afrique de l'Ouest** (Togo).  
Devise : **FCFA** | Langue : **Français** | Systèmes : **Off-grid uniquement**

---

## 📄 Licence

Projet privé — tous droits réservés.

---

## 👤 Auteur

Développé avec ❤️ pour le marché de l'énergie solaire en Afrique de l'Ouest.