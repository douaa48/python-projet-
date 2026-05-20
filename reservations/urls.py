from django.urls import path
from .views import cancel_reservation, reservation_list, reservation_form

urlpatterns = [
    path('', reservation_list, name='reservation_list'),
    path('form/<int:id>/', reservation_form, name='reservation_form'),
    path('cancel/<int:id>/', cancel_reservation, name='cancel_reservation'),
]