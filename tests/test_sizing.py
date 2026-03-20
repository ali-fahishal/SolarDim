"""
Tests unitaires pour core/sizing.py
Couvre toutes les fonctions de calcul de dimensionnement PV.
"""
import math
import pytest
from core.sizing import (
    calculer_consommation_journaliere,
    calculer_puissance_total_equipement,
    calculer_puissance_crete,
    calculer_nombre_panneaux,
    calculer_configuration_strings,
    calculer_surface_champ,
    calculer_batterie,
    calculer_configuration_batterie,
    calculer_rentabilite,
    calculer_dimensionnement_complet,
)
from config import (
    PERFORMANCE_RATIO_DEFAULT,
    PUISSANCE_PANNEAU_DEFAULT_WC,
    TENSION_BATTERIE_DEFAULT_V,
    PROFONDEUR_DECHARGE_DEFAULT,
    TARIF_KWH_DEFAULT_FCFA,
)


# ==============================
# FIXTURES
# ==============================

@pytest.fixture
def equipements_simples():
    return [
        {"puissance_w": 100, "heures_jour": 8, "quantite": 2, "conso_jour_wh": 1600.0},
        {"puissance_w": 50,  "heures_jour": 4, "quantite": 1, "conso_jour_wh": 200.0},
    ]


@pytest.fixture
def module_complet():
    return {
        "puissance_crete_wc": 400,
        "voc_v": 49.5,
        "vmp_v": 41.2,
        "isc_a": 10.1,
        "imp_a": 9.7,
        "longueur_m": 1.722,
        "largeur_m": 1.134,
    }


@pytest.fixture
def string_unique():
    return [{"numero_string": 1, "voc_max_v": 600, "vmppt_min_v": 100, "vmppt_max_v": 500, "imax_a": 30}]


@pytest.fixture
def batterie_unitaire():
    return {"tension_v": 12.0, "capacite_ah": 100.0}


# ==============================
# calculer_consommation_journaliere
# ==============================

class TestConsommationJournaliere:
    def test_liste_normale(self, equipements_simples):
        assert calculer_consommation_journaliere(equipements_simples) == 1800.0

    def test_liste_vide(self):
        assert calculer_consommation_journaliere([]) == 0.0

    def test_un_equipement(self):
        eq = [{"conso_jour_wh": 500.0}]
        assert calculer_consommation_journaliere(eq) == 500.0

    def test_valeurs_flottantes(self):
        eq = [{"conso_jour_wh": "250.5"}, {"conso_jour_wh": "249.5"}]
        assert calculer_consommation_journaliere(eq) == 500.0


# ==============================
# calculer_puissance_total_equipement
# ==============================

class TestPuissanceTotale:
    def test_calcul_avec_quantite(self, equipements_simples):
        # 100W×2 + 50W×1 = 250W
        assert calculer_puissance_total_equipement(equipements_simples) == 250.0

    def test_liste_vide(self):
        assert calculer_puissance_total_equipement([]) == 0.0

    def test_quantite_defaut_1(self):
        eq = [{"puissance_w": 200}]  # pas de clé quantite
        assert calculer_puissance_total_equipement(eq) == 200.0


# ==============================
# calculer_puissance_crete
# ==============================

class TestPuissanceCrete:
    def test_calcul_de_base(self):
        # 5000 / (5.0 × 0.65) = 1538.46 Wc
        result = calculer_puissance_crete(5000, 5.0)
        assert result == pytest.approx(1538.46, rel=1e-3)

    def test_pr_personnalise(self):
        result = calculer_puissance_crete(1000, 4.0, performance_ratio=0.8)
        assert result == pytest.approx(312.5, rel=1e-3)

    def test_conso_nulle(self):
        assert calculer_puissance_crete(0, 5.0) == 0.0

    def test_hsp_invalide_zero(self):
        with pytest.raises(ValueError, match="HSP invalide"):
            calculer_puissance_crete(5000, 0)

    def test_hsp_trop_grand(self):
        with pytest.raises(ValueError, match="HSP invalide"):
            calculer_puissance_crete(5000, 13.0)

    def test_conso_negative(self):
        with pytest.raises(ValueError, match="Consommation invalide"):
            calculer_puissance_crete(-100, 5.0)

    def test_pr_invalide(self):
        with pytest.raises(ValueError, match="Performance Ratio invalide"):
            calculer_puissance_crete(5000, 5.0, performance_ratio=0.0)

    def test_pr_superieur_a_1(self):
        with pytest.raises(ValueError, match="Performance Ratio invalide"):
            calculer_puissance_crete(5000, 5.0, performance_ratio=1.1)


# ==============================
# calculer_nombre_panneaux
# ==============================

class TestNombrePanneaux:
    def test_arrondi_superieur(self):
        # 1538.46 / 500 = 3.077 → 4
        assert calculer_nombre_panneaux(1538.46, 500) == 4

    def test_nombre_exact(self):
        assert calculer_nombre_panneaux(1000, 500) == 2

    def test_puissance_panneau_nulle(self):
        assert calculer_nombre_panneaux(1000, 0) == 0

    def test_puissance_crete_nulle(self):
        assert calculer_nombre_panneaux(0, 500) == 0

    def test_petit_systeme(self):
        # 100Wc / 400Wc = 0.25 → 1 panneau
        assert calculer_nombre_panneaux(100, 400) == 1


# ==============================
# calculer_configuration_strings
# ==============================

class TestConfigurationStrings:
    def test_retourne_none_si_pas_de_strings(self, module_complet):
        assert calculer_configuration_strings(4, module_complet, []) is None

    def test_retourne_none_si_module_vide(self, string_unique):
        assert calculer_configuration_strings(4, {}, string_unique) is None

    def test_retourne_none_si_voc_vmp_manquants(self, string_unique):
        module_sans_voc = {"puissance_crete_wc": 400}
        assert calculer_configuration_strings(4, module_sans_voc, string_unique) is None

    def test_calcul_serie_parallele(self, module_complet, string_unique):
        # vmp=41.2 → nb_serie_min=ceil(100/41.2)=3, nb_serie_max_mppt=floor(500/41.2)=12
        result = calculer_configuration_strings(8, module_complet, string_unique)
        assert result is not None
        assert "strings" in result
        s = result["strings"][0]
        assert s["nb_serie_min"] == math.ceil(100 / 41.2)
        assert s["nb_serie_max_mppt"] == math.floor(500 / 41.2)

    def test_panneaux_non_affectes_si_capacite_insuffisante(self, module_complet):
        strings_limitees = [{"numero_string": 1, "voc_max_v": 200, "vmppt_min_v": 40,
                              "vmppt_max_v": 160, "imax_a": 10}]
        result = calculer_configuration_strings(100, module_complet, strings_limitees)
        assert result["panneaux_non_affectes"] >= 0

    def test_zero_panneaux_restants(self, module_complet, string_unique):
        result = calculer_configuration_strings(0, module_complet, string_unique)
        assert result is not None
        s = result["strings"][0]
        assert s["nb_panneaux_affectes"] == 0


# ==============================
# calculer_surface_champ
# ==============================

class TestSurfaceChamp:
    def test_calcul_de_base(self, module_complet):
        # 4 panneaux × (1.722 × 1.134) × 1.1
        surface_module = 1.722 * 1.134
        attendu = round(4 * surface_module * 1.1, 2)
        result = calculer_surface_champ(4, module_complet)
        assert result["surface_totale_m2"] == attendu

    def test_retourne_none_si_dimensions_manquantes(self):
        module_sans_dim = {"puissance_crete_wc": 400}
        assert calculer_surface_champ(4, module_sans_dim) is None

    def test_retourne_none_si_module_none(self):
        assert calculer_surface_champ(4, None) is None

    def test_coefficient_aeration_personnalise(self, module_complet):
        result = calculer_surface_champ(4, module_complet, coefficient_aeration=1.2)
        assert result["coefficient_aeration"] == 1.2
        surface_module = 1.722 * 1.134
        assert result["surface_totale_m2"] == round(4 * surface_module * 1.2, 2)


# ==============================
# calculer_batterie
# ==============================

class TestBatterie:
    def test_calcul_de_base(self):
        # C = (5000 × 1) / (48 × 0.95) = 109.65 Ah
        result = calculer_batterie(5000)
        assert result["capacite_ah"] == pytest.approx(109.65, rel=1e-3)
        assert result["capacite_kwh"] == pytest.approx(5.0, rel=1e-3)
        assert result["tension_v"] == TENSION_BATTERIE_DEFAULT_V

    def test_autonomie_2_jours(self):
        result = calculer_batterie(5000, autonomie_jours=2)
        assert result["capacite_ah"] == pytest.approx(219.30, rel=1e-3)
        assert result["autonomie_jours"] == 2.0

    def test_tension_personnalisee(self):
        result = calculer_batterie(5000, tension_batterie_v=24)
        assert result["tension_v"] == 24.0

    def test_tension_invalide(self):
        with pytest.raises(ValueError, match="Tension batterie invalide"):
            calculer_batterie(5000, tension_batterie_v=0)

    def test_profondeur_decharge_invalide_zero(self):
        with pytest.raises(ValueError, match="Profondeur de décharge invalide"):
            calculer_batterie(5000, profondeur_decharge=0)

    def test_profondeur_decharge_invalide_sup_1(self):
        with pytest.raises(ValueError, match="Profondeur de décharge invalide"):
            calculer_batterie(5000, profondeur_decharge=1.1)

    def test_conso_nulle(self):
        result = calculer_batterie(0)
        assert result["capacite_ah"] == 0.0
        assert result["capacite_kwh"] == 0.0


# ==============================
# calculer_configuration_batterie
# ==============================

class TestConfigurationBatterie:
    def test_calcul_serie_parallele(self, batterie_unitaire):
        batterie_necessaire = {"tension_v": 48.0, "capacite_ah": 250.0}
        result = calculer_configuration_batterie(batterie_necessaire, batterie_unitaire)
        assert result is not None
        # nb_serie = ceil(48 / 12) = 4
        assert result["nb_batteries_serie"] == 4
        # nb_parallele = ceil(250 / 100) = 3
        assert result["nb_batteries_parallele"] == 3
        assert result["nb_batteries_total"] == 12

    def test_retourne_none_si_batterie_unitaire_none(self):
        batterie_necessaire = {"tension_v": 48.0, "capacite_ah": 200.0}
        assert calculer_configuration_batterie(batterie_necessaire, None) is None

    def test_retourne_none_si_donnees_manquantes(self):
        batterie_necessaire = {"tension_v": 48.0, "capacite_ah": 200.0}
        assert calculer_configuration_batterie(batterie_necessaire, {}) is None

    def test_avertissement_tension_onduleur(self, batterie_unitaire):
        batterie_necessaire = {"tension_v": 12.0, "capacite_ah": 100.0}
        onduleur = {"tension_demarrage_batterie_v": 48.0}
        result = calculer_configuration_batterie(batterie_necessaire, batterie_unitaire, onduleur)
        # tension_reelle = 1 × 12V < 48V → avertissement
        assert result["avertissement_tension"] is not None

    def test_pas_avertissement_si_tension_ok(self, batterie_unitaire):
        batterie_necessaire = {"tension_v": 48.0, "capacite_ah": 100.0}
        onduleur = {"tension_demarrage_batterie_v": 48.0}
        result = calculer_configuration_batterie(batterie_necessaire, batterie_unitaire, onduleur)
        # tension_reelle = 4 × 12V = 48V = tension_demarrage → pas d'avertissement
        assert result["avertissement_tension"] is None


# ==============================
# calculer_rentabilite
# ==============================

class TestRentabilite:
    def test_calcul_de_base(self):
        result = calculer_rentabilite(
            prix_total_installation=2_000_000,
            production_annuelle_kwh=1825,
        )
        # economies_annuelles = 1825 × 150 = 273 750 FCFA
        assert result["economies_annuelles"] == pytest.approx(273_750, rel=1e-3)
        # temps_retour = 2_000_000 / 273_750 ≈ 7.3 ans
        assert result["temps_retour_ans"] == pytest.approx(7.3, rel=0.05)

    def test_projection_10_ans(self):
        result = calculer_rentabilite(1_000_000, 1000)
        assert len(result["projection_10_ans"]) == 10
        assert result["projection_10_ans"][0]["annee"] == 1
        assert result["projection_10_ans"][-1]["annee"] == 10

    def test_cumul_croissant(self):
        result = calculer_rentabilite(1_000_000, 1000)
        cumuls = [p["economies_cumulees"] for p in result["projection_10_ans"]]
        assert all(cumuls[i] < cumuls[i + 1] for i in range(len(cumuls) - 1))

    def test_tarif_personnalise(self):
        result = calculer_rentabilite(1_000_000, 1000, tarif_kwh=200)
        assert result["economies_annuelles"] == pytest.approx(200_000, rel=1e-3)

    def test_prix_installation_negatif(self):
        with pytest.raises(ValueError, match="Prix installation invalide"):
            calculer_rentabilite(-1, 1000)

    def test_production_nulle(self):
        with pytest.raises(ValueError, match="Production annuelle invalide"):
            calculer_rentabilite(1_000_000, 0)

    def test_tarif_nul(self):
        with pytest.raises(ValueError, match="Tarif kWh invalide"):
            calculer_rentabilite(1_000_000, 1000, tarif_kwh=0)

    def test_cout_total_restitue(self):
        result = calculer_rentabilite(2_500_000, 1000)
        assert result["cout_total_installation"] == 2_500_000.0


# ==============================
# calculer_dimensionnement_complet
# ==============================

class TestDimensionnementComplet:
    def test_mode_equipements(self, equipements_simples):
        result = calculer_dimensionnement_complet(hsp=5.0, equipements=equipements_simples)
        assert result["source_consommation"] == "equipements"
        assert result["consommation_journaliere_wh"] == 1800.0
        assert result["nombre_panneaux"] > 0

    def test_mode_factures(self):
        result = calculer_dimensionnement_complet(hsp=5.5, conso_journaliere_kwh=10)
        assert result["source_consommation"] == "factures"
        assert result["consommation_journaliere_wh"] == 10_000.0

    def test_hsp_invalide(self, equipements_simples):
        with pytest.raises(ValueError, match="HSP invalide"):
            calculer_dimensionnement_complet(hsp=0.0, equipements=equipements_simples)

    def test_sans_source_consommation(self):
        with pytest.raises(ValueError):
            calculer_dimensionnement_complet(hsp=5.0)

    def test_module_enrichit_puissance_panneau(self, equipements_simples, module_complet):
        result = calculer_dimensionnement_complet(
            hsp=5.0, equipements=equipements_simples, module=module_complet
        )
        assert result["puissance_panneau_wc"] == 400.0

    def test_champs_toujours_presents(self, equipements_simples):
        result = calculer_dimensionnement_complet(hsp=5.0, equipements=equipements_simples)
        for cle in [
            "source_consommation", "consommation_journaliere_wh", "consommation_journaliere_kwh",
            "puissance_crete_necessaire_wc", "nombre_panneaux", "puissance_installee_wc",
            "batterie", "puissance_onduleur_recommandee_w", "hsp_utilise",
            "configuration_strings", "surface_champ", "configuration_batterie",
        ]:
            assert cle in result, f"Clé manquante : {cle}"

    def test_configuration_strings_avec_module_et_strings(
        self, equipements_simples, module_complet, string_unique
    ):
        result = calculer_dimensionnement_complet(
            hsp=5.0, equipements=equipements_simples,
            module=module_complet, strings=string_unique
        )
        assert result["configuration_strings"] is not None

    def test_surface_champ_avec_module_dimensionne(self, equipements_simples, module_complet):
        result = calculer_dimensionnement_complet(
            hsp=5.0, equipements=equipements_simples, module=module_complet
        )
        assert result["surface_champ"] is not None

    def test_configuration_batterie_avec_batterie_unitaire(
        self, equipements_simples, batterie_unitaire
    ):
        result = calculer_dimensionnement_complet(
            hsp=5.0, equipements=equipements_simples, batterie_unitaire=batterie_unitaire
        )
        assert result["configuration_batterie"] is not None
