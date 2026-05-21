from django.shortcuts import render
from voyages.models import Voyage


def home_view(request):
    voyages = Voyage.objects.all()
    return render(request, 'frontend/home.html', {'voyages': voyages})



def voyages_view(request):
    voyages = Voyage.objects.all()
    return render(request, "frontend/voyages/voyages_list.html", {"voyages": voyages})


def contact_view(request):
    if request.method == "POST":
        return render(request, "frontend/contact/contact.html", {
            "success": "Message envoyé ✔"
        })

    return render(request, "frontend/contact/contact.html")