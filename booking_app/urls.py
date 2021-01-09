from django.urls import path
from booking_app.views import (
    OfficeCreateView, OfficeListView, OfficeEditView, WorkplaceCreateView, WorkplaceListView,
    WorkplaceEditView, ReservationCreateView, ReservationListView
)

urlpatterns = [
    path('office/create/', OfficeCreateView.as_view()),
    path('offices/', OfficeListView.as_view()),
    path('office/edit/<int:pk>/', OfficeEditView.as_view()),

    path('workplace/create/', WorkplaceCreateView.as_view()),
    path('workplaces/', WorkplaceListView.as_view()),
    path('workplace/edit/<int:pk>/', WorkplaceEditView.as_view(), name='WorkplaceEditView'),

    path('reservation/create/', ReservationCreateView.as_view()),
    path('reservations/', ReservationListView.as_view()),
]