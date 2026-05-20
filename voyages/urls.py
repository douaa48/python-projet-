from django.urls import path
from . import views

urlpatterns = [
    path('', views.voyages_list, name='voyages'),
   path('<int:id>/', views.voyage_detail, name='voyage_detail')
]