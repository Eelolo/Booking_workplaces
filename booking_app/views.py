from rest_framework import generics
from booking_app.serializers import OfficeDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from booking_app.models import Office

class OfficeCreateView(generics.CreateAPIView):
    serializer_class = OfficeDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class OfficeListView(generics.ListAPIView):
    serializer_class = OfficeDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Office.objects.all()


class OfficeEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OfficeDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Office.objects.all()