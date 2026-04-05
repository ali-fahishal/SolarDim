# Raana — Refactoring UI complet

**Date :** 2026-04-05  
**Approche :** B — Refactoring UI uniquement (`app.py`, `ui/`, `style.py`)  
**Contrainte absolue :** `core/`, `agent/`, `storage.py`, `sizing.py`, `config.py` ne sont jamais modifiés. Les 59 tests existants passent sans changement.  
**Cibles :** Desktop + Mobile (techniciens PV sur le terrain au Togo)

---

## 1. Renommage SolarDim → Raana

Remplacement de toutes les occurrences de "SolarDim" par "Raana" dans les fichiers UI uniquement.

**Fichiers concernés :**
- `app.py` — `page_title="Raana"`, texte sidebar logo
- `ui/style.py` — texte "SolarDim" dans les commentaires et valeurs CSS
- `export/pdf_generator.py` — en-tête du rapport PDF
- `README.md` — titre du projet

**Ce qui ne change pas :** le nom du répertoire, les imports, les variables Python.

---

## 2. Navigation — Wizard 5 étapes

**Problème actuel :** 7 boutons sidebar non ordonnés, état actif basé sur un hack CSS `button:has(div:contains())` fragile, aucune indication de progression pour l'utilisateur.

**Solution :** Barre de progression horizontale en haut de page avec 5 étapes numérotées, boutons Précédent/Suivant, indicateur visuel d'état par étape.

**Ordre des étapes :**
1. Factures *(optionnel si équipements)*
2. Équipements *(optionnel si factures)*
3. Localisation *(obligatoire)*
4. Configurations *(optionnel — module, onduleur, batterie, paramètres éco)*
5. Analyse *(résultats + export)*

**État visuel par étape :**
- ✓ vert : étape complétée (données en DB)
- Cercle orange : étape active
- Cercle gris : étape non complétée

**Navigation libre conservée :** l'utilisateur peut sauter des étapes en cliquant directement sur un numéro. Le wizard guide sans bloquer.

**Structure sidebar après refactoring :** La sidebar est simplifiée — elle ne contient plus que 2 boutons (Guide & Notions, Analyse IA) sous le logo Raana. Les 5 étapes du workflow principal sont exclusivement dans la barre de progression en haut du contenu. Sur mobile, la sidebar réduite est masquée par défaut.

**Fichiers modifiés :** `app.py` (routing + rendu wizard), `ui/style.py` (CSS barre de progression + boutons nav).

---

## 3. Page Résultats — Cartes visuelles

**Problème actuel :** 3 tableaux HTML bruts côte à côte (`result-table`), en-têtes à 24px (trop grands), layout 50/50 peu lisible sur mobile.

**Solution :** Layout en 3 zones :

**Zone 1 — KPI row (4 cards horizontales) :**
- Puissance installée (kWc) — card bleu marine
- Capacité batterie (Ah / V) — card blanche
- Onduleur recommandé (kVA) — card blanche
- ROI (années) — card verte si rentable (`rentabilite` disponible), orange si ROI > 10 ans, grise avec "—" si `rentabilite=None` (prix installation non renseigné)

**Zone 2 — Détails composants (3 cards) :**
- Panneaux PV : nb panneaux, config strings (nS × nP), surface m²
- Parc Batterie : config (nS × nP), nb unités, tension, capacité réelle
- Fiche technique : conso kWh/j, HSP, PR, DoD, source consommation

**Zone 3 — Graphe + Export :**
- Graphe Plotly rentabilité 10 ans — identique à l'actuel
- Bouton PDF — identique, nom de fichier `raana_{ville}_{date}_{heure}.pdf`

**Fix CSS :** `result-table thead th` passe de `font-size: 24px` à `font-size: 14px`.

**Données :** la structure du dict `dim` retourné par `calculer_dimensionnement_complet()` n'est pas modifiée. Le rendu seul change.

**Fichiers modifiés :** `ui/results_display.py` (layout + rendu), `ui/style.py` (CSS nouvelles cards).

---

## 4. Formulaire Équipements — Tableau inline + compteur live

**Problème actuel :** formulaire d'ajout séparé du tableau, aucun retour visuel pendant la saisie, suppression ligne par ligne avec bouton 🗑️ en dehors du tableau.

**Solution :**

**Compteur de consommation en temps réel :**
- Card fixe en haut de la page affichant le total Wh/j et kWh/j
- Se recalcule après chaque ajout/suppression (via `st.rerun()` existant)

**Tableau avec ligne d'ajout intégrée :**
- Le tableau affiche les équipements existants + une dernière ligne vide pour l'ajout
- Colonnes : Appareil, W, h/j, Qté, Wh/j (calculé auto), ✕
- Le bouton ✕ de suppression est dans la colonne du tableau (plus de boutons flottants)

**Barres de répartition :**
- Sous le tableau, mini barres horizontales proportionnelles à la consommation de chaque appareil
- Permet d'identifier visuellement le plus gros consommateur

**Logique inchangée :** `ajouter_equipement()`, `supprimer_equipement()`, `get_equipements()` — aucun changement dans `core/storage.py`.

**Fichiers modifiés :** `ui/input_forms.py` (layout formulaire équipements uniquement).

---

## 5. Formulaire Factures — Upload amélioré

**Problème actuel :** zone d'upload discrète, pas d'indication de progression par fichier, récapitulatif de moyenne peu mis en valeur.

**Solution :**
- Zone drop agrandie avec texte d'instruction explicite
- Spinner individuel par fichier pendant l'analyse LLM (déjà présent, mis en valeur)
- Récapitulatif de moyenne (conso/j, tarif, nb factures) en cards après analyse

**Logique inchangée :** `extraire_donnees_facture()`, `valider_et_enrichir()`, `sauvegarder_facture()` — aucun changement.

**Fichiers modifiés :** `ui/input_forms.py` (layout formulaire factures uniquement).

---

## 6. Page Localisation — Recherche améliorée

**Améliorations :**
- Soumission avec la touche Enter : le champ ville est enveloppé dans un `st.form` avec `enter_to_submit=True` (Streamlit 1.40+, disponible dans la version utilisée)
- Résumé localisation sauvegardée en cards (HSP, irradiation, lat/lon) au lieu de `st.metric` + `st.info`

**Logique inchangée :** `geocoder_ville()`, `get_solar_data()`, `sauvegarder_localisation()` — aucun changement.

**Fichiers modifiés :** `ui/localisation_composants.py` (fonction `afficher_localisation()` uniquement).

---

## 7. Page Configurations — Indicateurs d'état par onglet

**Amélioration :**
- Titre de chaque onglet inclut un indicateur ✓/✗ selon si le composant est enregistré :
  - `⚡ Onduleur ✓` ou `⚡ Onduleur —`
  - `🔆 Module PV ✓` ou `🔆 Module PV —`
  - etc.

**Logique inchangée :** aucun changement dans les fonctions de formulaire.

**Fichiers modifiés :** `ui/localisation_composants.py` (fonction `afficher_composants()` uniquement).

---

## 8. Page Analyse IA — Formulaire agent fonctionnel

**Problème actuel :** page affiche uniquement `st.info("🚧 Fonctionnalité en cours de développement")`.

**Solution :** formulaire de question libre envoyé à l'agent LangGraph existant (`agent/agent.py`), réponse affichée dans la page. L'agent a déjà les outils `get_donnees_projet`, `outil_dimensionnement`, `outil_rentabilite`.

**Condition d'activation :** l'analyse doit avoir été lancée (`"dim" in st.session_state`). Sinon, message d'invite vers l'accueil.

**Fichiers modifiés :** `ui/results_display.py` (fonction `afficher_rapport_agent()`).

---

## 9. Polish global — 8 corrections

| # | Fichier | Correction |
|---|---------|-----------|
| 1 | `app.py:29` | `color:vert` → `color:#aaa` (CSS invalide) |
| 2 | `ui/style.py` | `result-table thead th` : `font-size: 24px` → `font-size: 14px` |
| 3 | `app.py` | État actif sidebar : remplacement du hack CSS par injection `data-active` via session_state |
| 4 | `app.py` | Checklist accueil : 3 cards cliquables avec état intégré |
| 5 | `app.py` | Bouton "Lancer l'analyse" : animation pulse quand toutes étapes complètes |
| 6 | `ui/style.py` | Mobile : sidebar en drawer overlay (hamburger ☰) sur `max-width: 768px` |
| 7 | `export/pdf_generator.py` | Nom PDF : `raana_{ville}_{YYYYMMDD}_{HHMM}.pdf` |
| 8 | `app.py` | Double initialisation `st.session_state.page_active` supprimée (lignes 17 et 42) |

---

## Périmètre — Ce qui ne change pas

- `core/sizing.py` — algorithmes de dimensionnement PV
- `core/storage.py` — ORM SQLite, sessions isolées
- `core/solar_data.py` — APIs Nominatim + PVGIS
- `core/facture_extractor.py` — extraction LLM factures
- `agent/agent.py`, `agent/tools.py` — ReAct agent LangGraph
- `export/pdf_generator.py` — structure du rapport (seul en-tête "Raana" change)
- `config.py` — constantes métier
- `tests/test_sizing.py` — 59 tests, aucune modification

---

## Fichiers modifiés (récapitulatif)

| Fichier | Modifications |
|---------|--------------|
| `app.py` | Routing wizard, sidebar Raana, checklist cards, fix CSS `color:vert`, fix double init |
| `ui/style.py` | CSS wizard, CSS cards résultats, fix font-size tableau, mobile drawer |
| `ui/results_display.py` | Layout cartes résultats, `afficher_rapport_agent()` fonctionnel |
| `ui/input_forms.py` | Tableau inline équipements, compteur live, upload factures amélioré |
| `ui/localisation_composants.py` | Enter pour recherche, indicateurs onglets configs |
| `export/pdf_generator.py` | Nom "Raana" en-tête, nom fichier horodaté |
| `README.md` | Titre "Raana" |
