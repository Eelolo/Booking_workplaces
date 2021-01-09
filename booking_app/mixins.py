from rest_framework.mixins import CreateModelMixin
from booking_app.validations import Validations
from rest_framework.response import Response
from rest_framework import status

class CreateReservationMixin(CreateModelMixin, Validations):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = self.run_all_validations(request)
        if content:
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)