from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from booking_app.validations import Validations
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


class CreateReservationMixin(CreateModelMixin, Validations):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = self.run_all_validations(request)
        if content:
            raise ValidationError(content)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReservationUpdateMixin(UpdateModelMixin, Validations):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        content = self.run_all_validations(request, **kwargs)
        if content:
            raise ValidationError(content)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
