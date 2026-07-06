# test_diagnostic.py

from diagnostic_algo import calculer_score_global

reponses_test = {
    "Présence en ligne": {
        "presence_confiance": 7,
        "presence_seo": 6,
        "presence_mobile": 8,
        "presence_reseaux": 5,
        "presence_avis": 6,
    },
    "Contenu et communication": {
        "contenu_structure": 5,
        "contenu_message": 8,
        "contenu_ton": 6,
        "contenu_regularite": 4,
        "contenu_conversion": 6,
    },
    "Stratégie et positionnement": {
        "strategie_differenciation": 3,
        "strategie_cible": 7,
        "strategie_offre": 5,
        "strategie_coherence": 6,
        "strategie_objectifs": 4,
    },
    "Performance et conversion": {
        "perf_vitesse": 9,
        "perf_tunnel": 6,
        "perf_donnees": 3,
        "perf_relance": 4,
        "perf_roi": 5,
    },
}

resultats = calculer_score_global(reponses_test)

print("Score global :", resultats["score_global"])
print()

for categorie, details in resultats["categories"].items():
    print(f"--- {categorie} ---")
    print("Score :", details["score"])
    for question_label, interpretation in details["interpretations"].items():
        print(f"  Q: {question_label}")
        print(f"  → {interpretation}")
    print()
