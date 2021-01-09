from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include('booking_app.urls'))
]

handler400 = 'booking_app.utils.views.error_400'
handler404 = 'booking_app.utils.views.error_404'
handler500 = 'booking_app.utils.views.error_500'