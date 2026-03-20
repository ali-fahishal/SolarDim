# ==============================
# CONFIGURATION SOLARDIM PRO
# Constantes métier centralisées
# ==============================

# --- Dimensionnement PV ---
PERFORMANCE_RATIO_DEFAULT = 0.65        # PR standard Afrique de l'Ouest (35% de pertes)
PUISSANCE_PANNEAU_DEFAULT_WC = 500      # Puissance crête panneau par défaut (Wc)
COEFFICIENT_AERATION_DEFAULT = 1.1      # Coefficient d'espacement entre panneaux
HSP_MIN = 0.1                           # Heures de Soleil Pic minimum acceptable
HSP_MAX = 12.0                          # Heures de Soleil Pic maximum acceptable

# --- Batterie ---
TENSION_BATTERIE_DEFAULT_V = 48         # Tension système batterie par défaut (V)
PROFONDEUR_DECHARGE_DEFAULT = 0.95      # Profondeur de décharge lithium (DoD)
AUTONOMIE_DEFAULT_JOURS = 1             # Autonomie batterie par défaut (jours)

# --- Onduleur ---
FACTEUR_SECURITE_ONDULEUR = 1.25        # Surdimensionnement onduleur (+25%)
HSP_EQUIVALENT_FACTURES = 8             # Heures d'utilisation estimées (mode factures)

# --- Économie ---
TARIF_KWH_DEFAULT_FCFA = 150            # Tarif électricité par défaut (FCFA/kWh)
