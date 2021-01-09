from rest_framework import generics
from booking_app.serializers import OfficeDetailSerializer, WorkplaceDetailSerializer, ReservationDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from booking_app.permissions import IsOwnerOrReadOnly
from booking_app.models import Office, Workplace, Reservation
from booking_app.mixins import CreateReservationMixin, ReservationUpdateMixin
from datetime import datetime
from django.db.models import Q


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

    def get_queryset(self):
        try:
            date_from = datetime.strptime(self.kwargs['date_from'], "%Y-%m-%d")
            date_to = datetime.strptime(self.kwargs['date_to'], "%Y-%m-%d")
            if date_from > date_to:
                return Workplace.objects.all()
        except KeyError:
            return Workplace.objects.all()
        except ValueError:
            return Workplace.objects.all()

        reservations = Reservation.objects.all().filter(
            (Q(initial_day__lte=date_from) & Q(reservation_ends__gte=date_from) & Q(reservation_ends__lte=date_to)) |
            (Q(initial_day__gte=date_from) & Q(initial_day__lte=date_to) & Q(reservation_ends__gte=date_to)) |
            (Q(initial_day__gte=date_from) & Q(reservation_ends__lte=date_to))
        )
        workplaces_to_exclude = []
        for dictionary in reservations.values('workplace'):
            workplaces_to_exclude.append(dictionary['workplace'])

        return Workplace.objects.all().exclude(pk__in=workplaces_to_exclude)


class WorkplaceEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkplaceDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Workplace.objects.all()


class ReservationCreateView(generics.CreateAPIView, CreateReservationMixin):
    serializer_class = ReservationDetailSerializer
    permission_classes = (IsAuthenticated,)


class ReservationListView(generics.ListAPIView):
    serializer_class = ReservationDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Reservation.objects.all()


class ReservationsWithWorkplace(generics.ListAPIView):
    serializer_class = ReservationDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        workplace_id = self.kwargs['pk']
        return Reservation.objects.all().filter(workplace=workplace_id)


class ReservationEditView(generics.RetrieveUpdateDestroyAPIView, ReservationUpdateMixin):
    serializer_class = ReservationDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Reservation.objects.all()