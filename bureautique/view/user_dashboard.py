from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from ..serializers.dashboard import UserDashboardSerializer

class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        stats = user.progress.aggregate(
            total_started=Count("id", filter=Q(is_started=True)),
            total_finished=Count("id", filter=Q(is_finished=True)),
        )

        completion_rate = (
            (stats["total_finished"] / stats["total_started"]) * 100
            if stats["total_started"] > 0
            else 0
        )

        data = {
            "stats": {
                "total_started": stats["total_started"],
                "total_finished": stats["total_finished"],
                "completion_rate": round(completion_rate, 1),
            },
            "progress": user.progress.select_related("cours"),
            "user": user,
        }

        serializer = UserDashboardSerializer(
            data,
            context={"request": request}
        )

        return Response(serializer.data)
