from django.shortcuts import render
from voyages.models import Voyage


# 🏠 HOME
def home_view(request):
    voyages = Voyage.objects.all()
    return render(request, 'frontend/home.html', {'voyages': voyages})


# ✈️ LISTE DES VOYAGES
def voyages_view(request):
    voyages = Voyage.objects.all()
    return render(request, "frontend/voyages/voyages_list.html", {"voyages": voyages})


# 📞 CONTACT
def contact_view(request):
    if request.method == "POST":
        return render(request, "frontend/contact/contact.html", {
            "success": "Message envoyé ✔"
        })

    return render(request, "frontend/contact/contact.html")