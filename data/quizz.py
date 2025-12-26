from bureautique.models.quizz import Quizz, Question, Option
from bureautique.models.cours_ordinateur import Cours

def import_quizz():
    cours = Cours.objects.get(id=1)  # 🔴 change l'id si besoin

    quizz = Quizz.objects.create(
        titre="Quizz – Découvrir l’ordinateur",
        cours=cours
    )

    questions = [
        # 🖥️ Général
        {
            "question": "À quoi sert principalement un ordinateur ?",
            "options": [
                ("Travailler, apprendre et communiquer", True),
                ("Dormir", False),
                ("Cuisiner", False),
                ("Marcher", False),
            ],
        },
        {
            "question": "Un ordinateur est une machine :",
            "options": [
                ("Électronique", True),
                ("Mécanique", False),
                ("Naturelle", False),
                ("Manuelle", False),
            ],
        },

        # 💻 Portable
        {
            "question": "Quelle est la particularité d’un ordinateur portable ?",
            "options": [
                ("Il fonctionne avec une batterie", True),
                ("Il est fixé au bureau", False),
                ("Il n’a pas d’écran", False),
                ("Il n’a pas de clavier", False),
            ],
        },
        {
            "question": "Un ordinateur portable est surtout utilisé pour :",
            "options": [
                ("La mobilité", True),
                ("Les jeux uniquement", False),
                ("La cuisine", False),
                ("La décoration", False),
            ],
        },

        # 🖥️ Fixe
        {
            "question": "Un ordinateur fixe est composé de :",
            "options": [
                ("Écran, unité centrale, clavier, souris", True),
                ("Écran seulement", False),
                ("Téléphone", False),
                ("Batterie seule", False),
            ],
        },
        {
            "question": "L’ordinateur fixe est généralement :",
            "options": [
                ("Plus puissant", True),
                ("Plus petit", False),
                ("Portable", False),
                ("Sans écran", False),
            ],
        },

        # ⌨️ Clavier
        {
            "question": "Le clavier sert principalement à :",
            "options": [
                ("Saisir du texte", True),
                ("Afficher des images", False),
                ("Éteindre l’ordinateur", False),
                ("Nettoyer l’écran", False),
            ],
        },
        {
            "question": "Quel clavier est utilisé dans les pays francophones ?",
            "options": [
                ("AZERTY", True),
                ("QWERTY", False),
                ("DVORAK", False),
                ("NUMPAD", False),
            ],
        },
        {
            "question": "Le clavier QWERTY est surtout utilisé dans :",
            "options": [
                ("Les pays anglophones", True),
                ("L’Afrique francophone", False),
                ("La France uniquement", False),
                ("Les téléphones", False),
            ],
        },

        # 🖱️ Souris
        {
            "question": "Quel bouton de la souris est le plus utilisé ?",
            "options": [
                ("Bouton gauche", True),
                ("Bouton droit", False),
                ("Molette", False),
                ("Bouton arrière", False),
            ],
        },
        {
            "question": "Le bouton droit de la souris sert à :",
            "options": [
                ("Afficher un menu d’options", True),
                ("Écrire du texte", False),
                ("Éteindre l’ordinateur", False),
                ("Faire défiler la page", False),
            ],
        },
        {
            "question": "La molette (scroll) permet de :",
            "options": [
                ("Faire défiler une page", True),
                ("Copier", False),
                ("Coller", False),
                ("Supprimer", False),
            ],
        },

        # ⚡ Raccourcis clavier
        {
            "question": "Que fait le raccourci Ctrl + C ?",
            "options": [
                ("Copier", True),
                ("Coller", False),
                ("Couper", False),
                ("Annuler", False),
            ],
        },
        {
            "question": "Que fait le raccourci Ctrl + V ?",
            "options": [
                ("Coller", True),
                ("Copier", False),
                ("Supprimer", False),
                ("Sélectionner tout", False),
            ],
        },
        {
            "question": "Ctrl + X permet de :",
            "options": [
                ("Couper", True),
                ("Copier", False),
                ("Coller", False),
                ("Annuler", False),
            ],
        },
        {
            "question": "Ctrl + Z sert à :",
            "options": [
                ("Annuler la dernière action", True),
                ("Copier", False),
                ("Coller", False),
                ("Fermer l’ordinateur", False),
            ],
        },
        {
            "question": "Ctrl + A permet de :",
            "options": [
                ("Tout sélectionner", True),
                ("Annuler", False),
                ("Coller", False),
                ("Fermer une page", False),
            ],
        },

        # 🎯 Mix final
        {
            "question": "Quel périphérique permet de déplacer le curseur ?",
            "options": [
                ("La souris", True),
                ("Le clavier", False),
                ("L’écran", False),
                ("L’unité centrale", False),
            ],
        },
        {
            "question": "Quel élément est considéré comme le cerveau de l’ordinateur ?",
            "options": [
                ("L’unité centrale", True),
                ("La souris", False),
                ("Le clavier", False),
                ("L’écran", False),
            ],
        },
        {
            "question": "Quel outil est indispensable pour écrire un texte ?",
            "options": [
                ("Le clavier", True),
                ("La souris", False),
                ("L’écran", False),
                ("La batterie", False),
            ],
        },
    ]

    for index, q in enumerate(questions, start=1):
        question = Question.objects.create(
            quizz=quizz,
            texte=q["question"],
            ordre=index
        )

        for texte, is_correct in q["options"]:
            Option.objects.create(
                question=question,
                texte=texte,
                is_correct=is_correct
            )

    print("✅ Quizz importé avec succès (20 questions)")
