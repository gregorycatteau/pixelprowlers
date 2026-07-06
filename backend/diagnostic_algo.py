# diagnostic_algo.py

from diagnostic_data import DIAGNOSTIC_DATA


def calculer_score_categorie(questions_dict, notes):
    """
    questions_dict : dict des questions d'une catégorie (clé = id de question)
    notes : dict {id_question: note (0-10)}
    """
    total_pondere = 0
    total_poids = 0
    interpretations_resultat = {}

    for question_id, question_data in questions_dict.items():
        note = notes.get(question_id, None)

        if note is None:
            continue

        note = int(round(float(note)))
        note = max(0, min(10, note))

        poids = question_data["poids"]
        total_pondere += note * poids
        total_poids += poids

        interpretations_resultat[question_data["label"]] = question_data["interpretations"][note]

    score = total_pondere / total_poids if total_poids > 0 else 0

    return {
        "score": round(score, 2),
        "interpretations": interpretations_resultat
    }


def calculer_score_global(reponses):
    """
    reponses : dict {categorie: {id_question: note}}
    """
    total_pondere = 0
    total_poids = 0
    resultats_categories = {}

    for categorie, categorie_data in DIAGNOSTIC_DATA.items():
        notes_categorie = reponses.get(categorie, {})
        resultat = calculer_score_categorie(categorie_data["questions"], notes_categorie)

        poids_categorie = categorie_data["poids_categorie"]
        total_pondere += resultat["score"] * poids_categorie
        total_poids += poids_categorie

        resultats_categories[categorie] = resultat

    score_global = total_pondere / total_poids if total_poids > 0 else 0

    return {
        "score_global": round(score_global, 2),
        "categories": resultats_categories
    }
