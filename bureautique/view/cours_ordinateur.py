# cours/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Cours, Etape
from ..serializers.ordinateur import CoursSerializer, EtapeSerializer, ProgressionUtilisateur


class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all().order_by('id')
    serializer_class = CoursSerializer
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        cours = self.get_object()
        progression, created = ProgressionUtilisateur.objects.get_or_create(
            user=request.user, cours=cours
        )
        progression.is_started = True
        progression.save()
        return Response({'status': 'cours démarré'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        cours = self.get_object()
        user = request.user

        # print("User :", user)

        if user in cours.likes.all():
            cours.likes.remove(user)  # unlike
            liked = False
        else:
            cours.likes.add(user)  # like
            liked = True

        return Response({"liked": liked, "total_likes": cours.total_likes()})


class EtapeViewSet(viewsets.ModelViewSet):
    queryset = Etape.objects.all().order_by('id')
    serializer_class = EtapeSerializer
    permission_classes = [permissions.IsAuthenticated]

