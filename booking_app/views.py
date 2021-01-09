from rest_framework import generics
from booking_app.serializers import OfficeDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class OfficeCreateView(generics.CreateAPIView):
    serializer_class = OfficeDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
