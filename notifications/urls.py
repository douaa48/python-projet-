from django.urls import path
from .views import notifications_list, mark_as_read, mark_all_read

urlpatterns = [
    path('', notifications_list, name='notifications'),
    path('read/<int:id>/', mark_as_read, name='mark_as_read'),
    path('read-all/', mark_all_read, name='mark_all_read'),
]