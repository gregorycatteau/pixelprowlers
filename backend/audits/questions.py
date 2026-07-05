AUDIT_SERIES = [
    {
        "id": "visibilite_presence",
        "label": "Visibilité & Présence en ligne",
        "questions": [
            {"id": "visibilite_presence_1", "label": "Votre site permet-il de comprendre clairement qui vous êtes et ce que vous proposez ?"},
            {"id": "visibilite_presence_2", "label": "Votre site inspire-t-il confiance dès les premières secondes de navigation ?"},
            {"id": "visibilite_presence_3", "label": "Vos informations essentielles sont-elles faciles à trouver pour un visiteur ?"},
            {"id": "visibilite_presence_4", "label": "Votre présence en ligne reflète-t-elle votre activité actuelle ?"},
            {"id": "visibilite_presence_5", "label": "Vos contenus sont-ils suffisamment à jour pour éviter les malentendus ?"},
        ],
    },
    {
        "id": "organisation_processus",
        "label": "Organisation interne & Processus",
        "questions": [
            {"id": "organisation_processus_1", "label": "Votre équipe sait-elle qui est responsable des outils numériques importants ?"},
            {"id": "organisation_processus_2", "label": "Vos procédures numériques sont-elles documentées et accessibles ?"},
            {"id": "organisation_processus_3", "label": "Pouvez-vous retrouver rapidement les informations utiles en cas de problème ?"},
            {"id": "organisation_processus_4", "label": "Vos accès sont-ils transmis proprement quand une personne change de rôle ?"},
            {"id": "organisation_processus_5", "label": "Votre organisation peut-elle continuer à fonctionner si la personne référente est absente ?"},
        ],
    },
    {
        "id": "outils_infrastructure",
        "label": "Outils & Infrastructure numérique",
        "questions": [
            {"id": "outils_infrastructure_1", "label": "Vos outils numériques sont-ils adaptés à vos usages réels ?"},
            {"id": "outils_infrastructure_2", "label": "Vos sauvegardes sont-elles régulières et vérifiées ?"},
            {"id": "outils_infrastructure_3", "label": "Vos comptes importants sont-ils protégés par des accès robustes ?"},
            {"id": "outils_infrastructure_4", "label": "Votre site et vos services restent-ils performants dans les moments importants ?"},
            {"id": "outils_infrastructure_5", "label": "Votre infrastructure peut-elle être maintenue sans dépendance excessive à un prestataire unique ?"},
        ],
    },
    {
        "id": "relation_engagement",
        "label": "Relation & Engagement",
        "questions": [
            {"id": "relation_engagement_1", "label": "Vos visiteurs savent-ils facilement comment vous contacter ?"},
            {"id": "relation_engagement_2", "label": "Vos formulaires ou canaux de contact fonctionnent-ils de manière fiable ?"},
            {"id": "relation_engagement_3", "label": "Votre communication numérique donne-t-elle envie d'engager un échange ?"},
            {"id": "relation_engagement_4", "label": "Vos réponses aux demandes entrantes sont-elles suivies et organisées ?"},
            {"id": "relation_engagement_5", "label": "Votre présence numérique aide-t-elle réellement votre relation avec vos publics ?"},
        ],
    },
]

QUESTION_IDS = [question["id"] for serie in AUDIT_SERIES for question in serie["questions"]]
