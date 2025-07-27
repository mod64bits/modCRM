from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import RondaPointViewSet, RondaLogViewSet

router = DefaultRouter()
router.register(r'ronda-points', RondaPointViewSet, basename='rondapoint')
router.register(r'ronda-logs', RondaLogViewSet, basename='rondalog')

urlpatterns = [
    path('', include(router.urls)),
]