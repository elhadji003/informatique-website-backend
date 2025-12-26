from rest_framework import serializers
from ..models import Cours, Etape, TypeObjet, ProgressionUtilisateur, PartiePrincipale, Utilite
from .quizz import QuizzSerializer

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
        fields = ['cours', 'is_started', "is_finished", 'date']

class CoursSerializer(serializers.ModelSerializer):
    etapes = EtapeSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='total_likes', read_only=True)
    liked_by_user = serializers.SerializerMethodField()
    progress_user = serializers.SerializerMethodField()
    users_started_count = serializers.SerializerMethodField()
    quizz = QuizzSerializer(many=True, read_only=True)

    class Meta:
        model = Cours
        fields = ['id', 'titre', 'description', 'etapes', 'quizz', 'likes_count', 'liked_by_user', 'progress_user', 'users_started_count']
    
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


class ListeCoursSerializers(serializers.ModelSerializer):
    progress_user = serializers.SerializerMethodField()

    class Meta:
        model = Cours
        fields = ['id', 'titre', 'progress_user']

    def get_progress_user(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        if not user or not user.is_authenticated:
            return {
                "is_started": False,
                "is_finished": False,
            }

        progression = ProgressionUtilisateur.objects.filter(
            user=user,
            cours=obj
        ).first()

        if not progression:
            return {
                "is_started": False,
                "is_finished": False,
            }

        return {
            "is_started": progression.is_started,
            "is_finished": progression.is_finished,
        }
