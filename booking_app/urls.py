from django.urls import path
from booking_app.views import OfficeCreateView, OfficeListView

urlpatterns = [
    path('office/create/', OfficeCreateView.as_view()),
    path('offices/', OfficeListView.as_view()),
]