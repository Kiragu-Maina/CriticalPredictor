from rest_framework import viewsets
from .models import PotholeData
from .serializers import PotholeDataSerializer

class PotholeDataViewSet(viewsets.ModelViewSet):
    queryset = PotholeData.objects.all()
    serializer_class = PotholeDataSerializer
