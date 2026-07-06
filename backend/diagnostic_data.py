# diagnostic_data.py

DIAGNOSTIC_DATA = {

    "Présence en ligne": {
        "poids_categorie": 0.25,
        "questions": {

            "presence_confiance": {
                "label": "Votre site inspire-t-il confiance dès les premières secondes ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune confiance générée, refonte urgente nécessaire.",
                    1: "Très peu de confiance, problèmes majeurs à corriger.",
                    2: "Confiance faible, plusieurs éléments à revoir.",
                    3: "Confiance limitée, des améliorations sont nécessaires.",
                    4: "Confiance moyenne-basse, des ajustements sont utiles.",
                    5: "Confiance correcte mais perfectible.",
                    6: "Bonne confiance générale, quelques détails à peaufiner.",
                    7: "Très bonne confiance, design professionnel.",
                    8: "Excellente confiance, très bonne première impression.",
                    9: "Confiance quasi parfaite dès l'arrivée sur le site.",
                    10: "Confiance immédiate et totale, expérience optimale."
                }
            },

            "presence_seo": {
                "label": "Votre site est-il facile à trouver sur les moteurs de recherche ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Site invisible sur les moteurs de recherche.",
                    1: "Très mauvais référencement, quasi invisible.",
                    2: "Référencement très faible, gros travail à prévoir.",
                    3: "Référencement limité, peu de visibilité.",
                    4: "Visibilité faible, marge de progression importante.",
                    5: "Visibilité correcte mais loin du potentiel réel.",
                    6: "Bonne visibilité générale sur les recherches.",
                    7: "Très bon référencement, bien positionné.",
                    8: "Excellent référencement, forte visibilité.",
                    9: "Visibilité quasi optimale sur les recherches clés.",
                    10: "Référencement exemplaire, position dominante."
                }
            },

            "presence_mobile": {
                "label": "Votre site est-il parfaitement adapté aux mobiles ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Totalement inadapté au mobile, expérience cassée.",
                    1: "Très mauvaise expérience mobile.",
                    2: "Expérience mobile médiocre.",
                    3: "Adaptation mobile insuffisante.",
                    4: "Adaptation mobile moyenne, des soucis persistent.",
                    5: "Adaptation mobile correcte mais perfectible.",
                    6: "Bonne adaptation mobile globale.",
                    7: "Très bonne expérience mobile.",
                    8: "Excellente adaptation mobile.",
                    9: "Expérience mobile quasi parfaite.",
                    10: "Adaptation mobile irréprochable."
                }
            },

            "presence_reseaux": {
                "label": "Votre présence sur les réseaux sociaux reflète-t-elle votre valeur réelle ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune présence sociale exploitable.",
                    1: "Présence sociale quasi inexistante.",
                    2: "Présence sociale très faible.",
                    3: "Présence sociale insuffisante.",
                    4: "Présence sociale moyenne, peu impactante.",
                    5: "Présence correcte mais peu différenciante.",
                    6: "Bonne présence sociale, cohérente.",
                    7: "Très bonne présence, reflète bien la marque.",
                    8: "Excellente présence sociale, forte cohérence.",
                    9: "Présence sociale quasi optimale.",
                    10: "Présence sociale exemplaire et impactante."
                }
            },

            "presence_avis": {
                "label": "Vos avis clients renforcent-ils clairement votre crédibilité ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucun avis ou avis contre-productifs.",
                    1: "Avis très insuffisants ou négatifs.",
                    2: "Avis faibles, peu rassurants.",
                    3: "Avis limités, crédibilité fragile.",
                    4: "Avis moyens, impact limité.",
                    5: "Avis corrects mais peu mis en valeur.",
                    6: "Bons avis, crédibilité renforcée.",
                    7: "Très bons avis, forte crédibilité.",
                    8: "Excellents avis, très rassurants.",
                    9: "Avis quasi unanimement excellents.",
                    10: "Avis exemplaires, crédibilité maximale."
                }
            },
        }
    },

    "Contenu et communication": {
        "poids_categorie": 0.25,
        "questions": {

            "contenu_structure": {
                "label": "Vos contenus sont-ils bien structurés et faciles à lire ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Contenus totalement désorganisés.",
                    1: "Structure très confuse.",
                    2: "Structure faible, lecture difficile.",
                    3: "Structure insuffisante.",
                    4: "Structure moyenne, des efforts à faire.",
                    5: "Structure correcte mais perfectible.",
                    6: "Bonne structure générale.",
                    7: "Très bonne structure, lecture agréable.",
                    8: "Excellente structure, très claire.",
                    9: "Structure quasi parfaite.",
                    10: "Structure exemplaire, lecture optimale."
                }
            },

            "contenu_message": {
                "label": "Votre message principal est-il compris en moins de 5 secondes ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Message totalement incompréhensible.",
                    1: "Message très confus.",
                    2: "Message peu clair.",
                    3: "Message insuffisamment clair.",
                    4: "Message moyennement clair.",
                    5: "Message correct mais perfectible.",
                    6: "Bon message, globalement compris.",
                    7: "Très bon message, clair et efficace.",
                    8: "Excellent message, immédiatement compris.",
                    9: "Message quasi parfaitement clair.",
                    10: "Message limpide et percutant instantanément."
                }
            },

            "contenu_ton": {
                "label": "Votre ton correspond-il précisément à votre cible ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Ton totalement inadapté à la cible.",
                    1: "Ton très mal ajusté.",
                    2: "Ton peu adapté.",
                    3: "Ton insuffisamment ajusté.",
                    4: "Ton moyennement adapté.",
                    5: "Ton correct mais perfectible.",
                    6: "Bon ton, globalement adapté.",
                    7: "Très bon ton, bien ciblé.",
                    8: "Excellent ton, parfaitement ajusté.",
                    9: "Ton quasi parfaitement calibré.",
                    10: "Ton exemplaire, parfaitement en phase avec la cible."
                }
            },

            "contenu_regularite": {
                "label": "Publiez-vous du contenu de façon suffisamment régulière ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune régularité de publication.",
                    1: "Régularité quasi inexistante.",
                    2: "Régularité très faible.",
                    3: "Régularité insuffisante.",
                    4: "Régularité moyenne.",
                    5: "Régularité correcte mais perfectible.",
                    6: "Bonne régularité générale.",
                    7: "Très bonne régularité.",
                    8: "Excellente régularité.",
                    9: "Régularité quasi optimale.",
                    10: "Régularité exemplaire et parfaitement maîtrisée."
                }
            },

            "contenu_conversion": {
                "label": "Vos contenus donnent-ils clairement envie de passer à l'action ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune incitation à l'action.",
                    1: "Incitation très faible.",
                    2: "Incitation faible.",
                    3: "Incitation insuffisante.",
                    4: "Incitation moyenne.",
                    5: "Incitation correcte mais perfectible.",
                    6: "Bonne incitation à l'action.",
                    7: "Très bonne incitation, efficace.",
                    8: "Excellente incitation à l'action.",
                    9: "Incitation quasi parfaite.",
                    10: "Incitation exemplaire, conversion optimale."
                }
            },
        }
    },

    "Stratégie et positionnement": {
        "poids_categorie": 0.25,
        "questions": {

            "strategie_differenciation": {
                "label": "Votre différence par rapport à la concurrence est-elle limpide ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune différenciation perceptible.",
                    1: "Différenciation quasi inexistante.",
                    2: "Différenciation très faible.",
                    3: "Différenciation insuffisante.",
                    4: "Différenciation moyenne.",
                    5: "Différenciation correcte mais perfectible.",
                    6: "Bonne différenciation.",
                    7: "Très bonne différenciation.",
                    8: "Excellente différenciation.",
                    9: "Différenciation quasi parfaite.",
                    10: "Différenciation exemplaire et immédiatement perçue."
                }
            },

            "strategie_cible": {
                "label": "Votre cible idéale est-elle clairement identifiée et adressée ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune cible clairement définie.",
                    1: "Cible très floue.",
                    2: "Cible peu définie.",
                    3: "Cible insuffisamment définie.",
                    4: "Cible moyennement définie.",
                    5: "Cible correcte mais perfectible.",
                    6: "Bonne définition de la cible.",
                    7: "Très bonne définition de la cible.",
                    8: "Excellente définition de la cible.",
                    9: "Cible quasi parfaitement définie.",
                    10: "Cible exemplaire, parfaitement adressée."
                }
            },

            "strategie_offre": {
                "label": "Votre offre est-elle perçue comme clairement supérieure ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Offre non différenciante, aucune supériorité perçue.",
                    1: "Supériorité très faiblement perçue.",
                    2: "Supériorité faible.",
                    3: "Supériorité insuffisante.",
                    4: "Supériorité moyenne.",
                    5: "Supériorité correcte mais perfectible.",
                    6: "Bonne perception de supériorité.",
                    7: "Très bonne perception de supériorité.",
                    8: "Excellente perception de supériorité.",
                    9: "Supériorité quasi unanimement perçue.",
                    10: "Supériorité exemplaire et évidente."
                }
            },

            "strategie_coherence": {
                "label": "Votre stratégie globale est-elle cohérente sur tous les canaux ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune cohérence entre les canaux.",
                    1: "Cohérence très faible.",
                    2: "Cohérence faible.",
                    3: "Cohérence insuffisante.",
                    4: "Cohérence moyenne.",
                    5: "Cohérence correcte mais perfectible.",
                    6: "Bonne cohérence générale.",
                    7: "Très bonne cohérence.",
                    8: "Excellente cohérence.",
                    9: "Cohérence quasi parfaite.",
                    10: "Cohérence exemplaire sur tous les canaux."
                }
            },

            "strategie_objectifs": {
                "label": "Vos objectifs business sont-ils traduits en actions concrètes ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune traduction en actions concrètes.",
                    1: "Traduction très faible.",
                    2: "Traduction faible.",
                    3: "Traduction insuffisante.",
                    4: "Traduction moyenne.",
                    5: "Traduction correcte mais perfectible.",
                    6: "Bonne traduction en actions.",
                    7: "Très bonne traduction en actions.",
                    8: "Excellente traduction en actions.",
                    9: "Traduction quasi parfaite en actions concrètes.",
                    10: "Traduction exemplaire, stratégie parfaitement actionnable."
                }
            },
        }
    },

    "Performance et conversion": {
        "poids_categorie": 0.25,
        "questions": {

            "perf_vitesse": {
                "label": "Votre site charge-t-il suffisamment vite pour ne perdre personne ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Vitesse catastrophique, perte massive de visiteurs.",
                    1: "Vitesse très mauvaise.",
                    2: "Vitesse faible.",
                    3: "Vitesse insuffisante.",
                    4: "Vitesse moyenne.",
                    5: "Vitesse correcte mais perfectible.",
                    6: "Bonne vitesse générale.",
                    7: "Très bonne vitesse.",
                    8: "Excellente vitesse.",
                    9: "Vitesse quasi optimale.",
                    10: "Vitesse exemplaire, chargement instantané."
                }
            },

            "perf_tunnel": {
                "label": "Votre tunnel de conversion est-il fluide de bout en bout ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Tunnel totalement cassé, conversion impossible.",
                    1: "Tunnel très défaillant.",
                    2: "Tunnel faible, nombreux points de friction.",
                    3: "Tunnel insuffisant.",
                    4: "Tunnel moyen, des frictions notables.",
                    5: "Tunnel correct mais perfectible.",
                    6: "Bon tunnel, globalement fluide.",
                    7: "Très bon tunnel, peu de friction.",
                    8: "Excellent tunnel, très fluide.",
                    9: "Tunnel quasi parfaitement fluide.",
                    10: "Tunnel exemplaire, conversion optimale."
                }
            },

            "perf_donnees": {
                "label": "Analysez-vous vos données pour ajuster vos décisions ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune analyse de données réalisée.",
                    1: "Analyse quasi inexistante.",
                    2: "Analyse très faible.",
                    3: "Analyse insuffisante.",
                    4: "Analyse moyenne.",
                    5: "Analyse correcte mais perfectible.",
                    6: "Bonne analyse des données.",
                    7: "Très bonne analyse des données.",
                    8: "Excellente analyse des données.",
                    9: "Analyse quasi optimale.",
                    10: "Analyse exemplaire, décisions parfaitement data-driven."
                }
            },

            "perf_relance": {
                "label": "Relancez-vous efficacement les prospects non convertis ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune relance des prospects.",
                    1: "Relance quasi inexistante.",
                    2: "Relance très faible.",
                    3: "Relance insuffisante.",
                    4: "Relance moyenne.",
                    5: "Relance correcte mais perfectible.",
                    6: "Bonne relance des prospects.",
                    7: "Très bonne relance, efficace.",
                    8: "Excellente relance des prospects.",
                    9: "Relance quasi parfaitement optimisée.",
                    10: "Relance exemplaire, taux de récupération maximal."
                }
            },

            "perf_roi": {
                "label": "Votre retour sur investissement digital est-il clairement mesuré ?",
                "poids": 0.2,
                "interpretations": {
                    0: "Aucune mesure du ROI.",
                    1: "Mesure quasi inexistante.",
                    2: "Mesure très faible.",
                    3: "Mesure insuffisante.",
                    4: "Mesure moyenne.",
                    5: "Mesure correcte mais perfectible.",
                    6: "Bonne mesure du ROI.",
                    7: "Très bonne mesure du ROI.",
                    8: "Excellente mesure du ROI.",
                    9: "Mesure quasi parfaitement claire.",
                    10: "Mesure exemplaire, ROI parfaitement piloté."
                }
            },
        }
    },

}
