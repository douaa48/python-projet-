from django.shortcuts import render, get_object_or_404
from .models import Voyage


# ✈️ LISTE VOYAGES
def voyages_list(request):
    voyages = Voyage.objects.all()
    return render(request, 'frontend/voyages/voyages_list.html', {'voyages': voyages})


# 🔍 DETAIL VOYAGE
def voyage_detail(request, id):
    voyage = get_object_or_404(Voyage, id=id)
    return render(request, 'frontend/voyages/voyage_detail.html', {'voyage': voyage})