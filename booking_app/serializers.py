from rest_framework import serializers
from booking_app.models import Office, Workplace, Reservation


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