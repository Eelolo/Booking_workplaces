from rest_framework import serializers
from booking_app.models import Office, Workplace, Reservation
from datetime import date
from datetime import timedelta


class OfficeDetailSerializer(serializers.ModelSerializer):
    workplaces_id = serializers.SerializerMethodField('get_workplaces_id')

    class Meta:
        model = Office
        fields = (
            'id', 'workplaces', 'workplaces_id'
        )

    def get_workplaces_id(self, office_model):
        office_id = office_model.pk

        workplaces_id = []
        for workplace in Workplace.objects.all().filter(office=office_id):
            workplaces_id.append(workplace.pk)

        return workplaces_id


class WorkplaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = '__all__'


class ReservationDetailSerializer(serializers.ModelSerializer):
    reservation_days = serializers.SerializerMethodField('get_reservation_days_list')

    class Meta:
        model = Reservation
        fields = (
            'id', 'office', 'workplace',
            'initial_day', 'reservation_ends', 'reservation_days', 'user'
        )

    def get_reservation_days_list(self, reservation_model):
        initial_day = reservation_model.initial_day
        reservation_ends = reservation_model.reservation_ends
        reservation_days = []

        for delta in range((reservation_ends - initial_day).days + 1):
            reservation_days.append(date.isoformat(initial_day + timedelta(days=delta)))

        return reservation_days