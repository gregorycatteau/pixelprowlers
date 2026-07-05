REFONTE_SERIES = [
    {
        "id": "contexte_objectifs",
        "label": "Contexte & objectifs",
        "questions": [
            {"id": "refonte_raison", "required": True},
            {"id": "objectif_principal", "required": True},
            {"id": "budget_approx", "required": True},
            {"id": "delai_lancement", "required": True},
            {"id": "decisionnaires", "required": True},
        ],
    },
    {
        "id": "existant",
        "label": "Existant",
        "questions": [
            {"id": "fonctionne_bien", "required": True},
            {"id": "frustrations", "required": True},
            {"id": "contenus_a_conserver", "required": True},
            {"id": "cms_actuel", "required": True},
            {"id": "acces_hebergement", "required": True},
        ],
    },
    {
        "id": "cible_positionnement",
        "label": "Cible & positionnement",
        "questions": [
            {"id": "client_ideal", "required": True},
            {"id": "concurrents_inspiration", "required": True},
            {"id": "ton_marque", "required": True},
            {"id": "charte_graphique", "required": True},
            {"id": "portee_public", "required": True},
        ],
    },
    {
        "id": "fonctionnalites",
        "label": "Fonctionnalités souhaitées",
        "questions": [
            {"id": "boutique_paiement", "required": True},
            {"id": "blog_contenu", "required": True},
            {"id": "multilingue", "required": True},
            {"id": "integrations", "required": True},
            {"id": "espace_client", "required": True},
        ],
    },
]

REFONTE_QUESTION_IDS = [
    question["id"]
    for serie in REFONTE_SERIES
    for question in serie["questions"]
]
