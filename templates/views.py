from django.shortcuts import render

def home(request):
    return render(request, 'end/home.html')
from voyages.models import Voyage
from django.shortcuts import render

def voyages_view(request):
    voyages = Voyage.objects.all()
    return render(request, 'frontend/voyages/voyage_list.html', {
        'voyages': voyages
    })