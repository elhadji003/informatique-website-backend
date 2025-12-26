# cours/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Cours, Etape, ProgressionUtilisateur
from ..serializers.ordinateur import CoursSerializer, EtapeSerializer, ListeCoursSerializers, ProgressionUtilisateurSerializer


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
    
    @action(detail=True, methods=['post'])
    def finish(self, request, pk=None):
        cours = self.get_object()
        progression, created = ProgressionUtilisateur.objects.get_or_create(
            user=request.user, cours=cours
        )
        progression.is_finished = True
        progression.is_started = False
        progression.save()
        return Response({
            'status': 'cours terminé',
            'progression': ProgressionUtilisateurSerializer(progression).data
        })
    
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


class ListeCoursViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste des cours avec progression utilisateur
    """
    serializer_class = ListeCoursSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cours.objects.all().order_by('id')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
