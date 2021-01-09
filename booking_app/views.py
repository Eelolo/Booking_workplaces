from rest_framework import generics
from booking_app.serializers import OfficeDetailSerializer, WorkplaceDetailSerializer, ReservationDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from booking_app.permissions import IsOwnerOrReadOnly
from booking_app.models import Office, Workplace, Reservation

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


class WorkplaceCreateView(generics.CreateAPIView):
    serializer_class = WorkplaceDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class WorkplaceListView(generics.ListAPIView):
    serializer_class = WorkplaceDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Workplace.objects.all()


class WorkplaceEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkplaceDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Workplace.objects.all()


class ReservationCreateView(generics.CreateAPIView):
    serializer_class = ReservationDetailSerializer
    permission_classes = (IsAuthenticated,)


class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Reservation.objects.all()


class ReservationEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Reservation.objects.all()