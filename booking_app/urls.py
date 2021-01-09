from django.urls import path
from booking_app.views import OfficeCreateView

urlpatterns = [
    path('office/create/', OfficeCreateView.as_view()),
]