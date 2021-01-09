from django.urls import path, re_path
from booking_app.views import (
    OfficeCreateView, OfficeListView, OfficeEditView, WorkplaceCreateView,
    WorkplaceListView,WorkplaceEditView, ReservationCreateView,
    ReservationListView, ReservationEditView,ReservationsWithWorkplace
)

urlpatterns = [
    path('office/create/', OfficeCreateView.as_view()),
    path('offices/', OfficeListView.as_view()),
    path('office/edit/<int:pk>/', OfficeEditView.as_view(), name='OfficeEditView'),

    path('workplace/create/', WorkplaceCreateView.as_view()),
    path('workplaces/', WorkplaceListView.as_view()),
    re_path(
        'workplaces/(?P<date_from>[\w\-\.]+)/(?P<date_to>[\w\-\.]+)/$',
        WorkplaceListView.as_view(),
        name='Free_workplaces_in_range'
    ),
    path('workplace/edit/<int:pk>/', WorkplaceEditView.as_view(), name='WorkplaceEditView'),

    path('reservation/create/', ReservationCreateView.as_view()),
    path('reservations/', ReservationListView.as_view()),
    path('reservations/<int:pk>/', ReservationsWithWorkplace.as_view(), name='ReservationsWithWorkplaceView'),
    path('reservation/edit/<int:pk>/', ReservationEditView.as_view(), name='ReservationEditView'),
]
