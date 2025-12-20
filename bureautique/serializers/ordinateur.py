from rest_framework import serializers
from ..models import Cours, Etape, TypeObjet, ProgressionUtilisateur, PartiePrincipale, Utilite

# Serializers de base
class TypeObjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeObjet
        fields = ['nom', 'emoji', 'description', 'modal_type']

class PartiePrincipaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartiePrincipale
        fields = ['nom', 'description']

class UtiliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilite
        fields = ['texte']

# Serializer pour une étape complète
class EtapeSerializer(serializers.ModelSerializer):
    types_objets = TypeObjetSerializer(many=True, read_only=True)
    parties_principales = PartiePrincipaleSerializer(many=True, read_only=True)
    utilites = UtiliteSerializer(many=True, read_only=True)
    
    class Meta:
        model = Etape
        fields = [
            'id', 'ordre', 'titre',
            'intro_titre', 'intro_texte',
            'def_titre', 'def_texte',
            'types_objets', 'parties_principales', 'utilites'
        ]

# Serializer pour un cours complet
class ProgressionUtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressionUtilisateur
        fields = ['user', 'cours', 'is_started']

class CoursSerializer(serializers.ModelSerializer):
    etapes = EtapeSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='total_likes', read_only=True)
    liked_by_user = serializers.SerializerMethodField()
    progress_user = serializers.SerializerMethodField()
    users_started_count = serializers.SerializerMethodField()


    class Meta:
        model = Cours
        fields = ['id', 'titre', 'description', 'etapes', 'likes_count', 'liked_by_user', 'progress_user', 'users_started_count']
    
    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        return user in obj.likes.all() if user.is_authenticated else False
    
    def get_users_started_count(self, obj):
        return ProgressionUtilisateur.objects.filter(cours=obj, is_started=True).count()

    def get_progress_user(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return None
        progression = ProgressionUtilisateur.objects.filter(user=user, cours=obj).first()
        if progression:
            return ProgressionUtilisateurSerializer(progression).data
        return None


