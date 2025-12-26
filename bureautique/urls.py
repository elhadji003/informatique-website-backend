# cours/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .view.cours_ordinateur import (
    CoursViewSet,
    EtapeViewSet,
    ListeCoursViewSet,
)
from .view.user_dashboard import UserDashboardView

app_name = "cours"

router = DefaultRouter()
router.register(r"cours", CoursViewSet, basename="cours")
router.register(r"etapes", EtapeViewSet, basename="etapes")
router.register(r"liste-cours", ListeCoursViewSet, basename="liste-cours")

urlpatterns = [
    path(
        "me/dashboard/",
        UserDashboardView.as_view(),
        name="user-dashboard",
    ),
]

urlpatterns += router.urls
