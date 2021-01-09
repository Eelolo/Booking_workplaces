from django.urls import path
from booking_app.views import (
    OfficeCreateView, OfficeListView, OfficeEditView, WorkplaceCreateView, WorkplaceListView
)

urlpatterns = [
    path('office/create/', OfficeCreateView.as_view()),
    path('offices/', OfficeListView.as_view()),
    path('office/edit/<int:pk>/', OfficeEditView.as_view()),
    path('workplace/create/', WorkplaceCreateView.as_view()),
    path('workplaces/', WorkplaceListView.as_view()),
]