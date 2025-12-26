from rest_framework import serializers
from .ordinateur import ProgressionUtilisateurSerializer


class UserStatsSerializer(serializers.Serializer):
    total_started = serializers.IntegerField()
    total_finished = serializers.IntegerField()
    completion_rate = serializers.FloatField()

class UserDashboardSerializer(serializers.Serializer):
    stats = UserStatsSerializer()
    progress = ProgressionUtilisateurSerializer(many=True)
    last_course = serializers.SerializerMethodField()

    def get_last_course(self, obj):
        progress_qs = obj["progress"]

        last_progress = progress_qs.order_by("-date").first()
        if last_progress:
            return {
                "id": last_progress.cours.id,
                "titre": last_progress.cours.titre,
            }
        return None

