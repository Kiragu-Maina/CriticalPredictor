from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PotholeDataViewSet

router = DefaultRouter()
router.register(r'pothole-data', PotholeDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
