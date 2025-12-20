# cours/admin.py
from django.contrib import admin
from .models import Cours, Etape, TypeObjet, PartiePrincipale, Utilite, ProgressionUtilisateur

# 🔹 Inline pour les types d’objets, parties principales et utilités
class TypeObjetInline(admin.TabularInline):
    model = TypeObjet
    extra = 1

class PartiePrincipaleInline(admin.TabularInline):
    model = PartiePrincipale
    extra = 1

class UtiliteInline(admin.TabularInline):
    model = Utilite
    extra = 1

# 🔹 Admin pour les étapes avec inlines
@admin.register(Etape)
class EtapeAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'ordre')
    list_filter = ('cours',)
    search_fields = ('titre', 'def_titre', 'intro_titre')
    inlines = [TypeObjetInline, PartiePrincipaleInline, UtiliteInline]
    ordering = ('cours', 'ordre')

# 🔹 Admin pour les cours avec les étapes en lecture seule
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre',)
    search_fields = ('titre',)
    ordering = ('titre',)

# 🔹 Admin pour la progression utilisateur
@admin.register(ProgressionUtilisateur)
class ProgressionUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'cours', 'is_started', 'date')
    list_filter = ('is_started', 'date')
    search_fields = ('user__username', 'cours__titre')
    ordering = ('-date',)

# 🔹 Admin pour les modèles simples
@admin.register(TypeObjet)
class TypeObjetAdmin(admin.ModelAdmin):
    list_display = ('nom', 'etape', 'modal_type')
    list_filter = ('modal_type',)
    search_fields = ('nom',)

@admin.register(PartiePrincipale)
class PartiePrincipaleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'etape')
    search_fields = ('nom',)

@admin.register(Utilite)
class UtiliteAdmin(admin.ModelAdmin):
    list_display = ('texte', 'etape')
    search_fields = ('texte',)
