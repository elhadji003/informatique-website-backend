from django.db import models
from .cours_ordinateur import Cours


class Quizz(models.Model):
    cours = models.ForeignKey(Cours, related_name="quizz", on_delete=models.CASCADE)
    titre = models.CharField(max_length=255, default="Quizz du cours")

    def __str__(self):
        return f"{self.cours.titre} - {self.titre}"


class Question(models.Model):
    quizz = models.ForeignKey(Quizz, related_name="questions", on_delete=models.CASCADE)
    texte = models.TextField()
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.ordre} - {self.texte[:50]}"


class Option(models.Model):
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    texte = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.texte
