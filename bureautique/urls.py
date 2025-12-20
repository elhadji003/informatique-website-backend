# cours/urls.py
from rest_framework.routers import DefaultRouter
from .view.cours_ordinateur import CoursViewSet, EtapeViewSet

router = DefaultRouter()
router.register(r'cours', CoursViewSet, basename='cours')
router.register(r'etapes', EtapeViewSet, basename='etapes')

urlpatterns = router.urls
