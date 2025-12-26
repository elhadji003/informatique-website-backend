from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Le cours principal
class Cours(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


    # Nouveau : likes et suivi user
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_cours", blank=True)
    
    def total_likes(self):
        return self.likes.count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.titre

# Chaque étape d’un cours
class Etape(models.Model):
    cours = models.ForeignKey(Cours, related_name="etapes", on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField()
    titre = models.CharField(max_length=255)
    
    # Contenu générique
    intro_titre = models.CharField(max_length=255)
    intro_texte = models.TextField()
    
    def_titre = models.CharField(max_length=255)
    def_texte = models.TextField()
    
    def __str__(self):
        return f"{self.cours.titre} - Étape {self.ordre}"

# Types spécifiques (ex: ordinateur, logiciel, outil)
class TypeObjet(models.Model):
    etape = models.ForeignKey(Etape, related_name="types_objets", on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, blank=True)
    description = models.TextField()
    modal_type = models.CharField(max_length=50, blank=True)  # frontend : quel composant modal utiliser

# Parties principales (uniforme pour chaque étape)
class PartiePrincipale(models.Model):
    etape = models.ForeignKey(Etape, related_name="parties_principales", on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    description = models.TextField()

# Utilité ou fonctionnalités
class Utilite(models.Model):
    etape = models.ForeignKey(Etape, related_name="utilites", on_delete=models.CASCADE)
    texte = models.CharField(max_length=255)

# Suivi de progression par utilisateur
class ProgressionUtilisateur(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progress"

    )
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    is_started = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
