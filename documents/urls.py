from django.urls import path
from .views import delete_document, documents_list

urlpatterns = [
    path('', documents_list, name='documents'),
    path('delete/<int:id>/', delete_document, name='delete_document'),
]