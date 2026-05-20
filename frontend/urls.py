from django.urls import path
from .views import home_view, voyages_view, contact_view

urlpatterns = [
    path('', home_view, name='home'),
    path('voyages/', voyages_view, name='voyages'),
    path('contact/', contact_view, name='contact'),
]