from django.urls import path
from booking_app.views import OfficeCreateView, OfficeListView, OfficeEditView

urlpatterns = [
    path('office/create/', OfficeCreateView.as_view()),
    path('offices/', OfficeListView.as_view()),
    path('office/edit/<int:pk>/', OfficeEditView.as_view()),
]