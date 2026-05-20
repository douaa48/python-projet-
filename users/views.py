from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm



# =========================
# 🔐 SIGNUP
# =========================
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # 🔥 login automatique
            login(request, user)

            messages.success(request, "Compte créé avec succès ✔")

            # 👉 redirection intelligente
            if user.is_superuser:
                return redirect('/admin/')
            return redirect('profile')

        else:
            # 🔥 IMPORTANT → afficher erreurs réelles
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field} : {error}")

    else:
        form = CustomUserCreationForm()

    return render(request, "frontend/users/signup.html", {
        "form": form
    })


# =========================
# 🔐 LOGIN
# =========================
def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie ✔")

            # 👉 différenciation admin / user
            if user.is_superuser:
                return redirect('/admin/')
            return redirect('profile')

        else:
            messages.error(request, "Identifiants incorrects ❌")

    return render(request, "frontend/users/login.html")


# =========================
# 🔐 LOGOUT
# =========================
def logout_view(request):
    logout(request)
    messages.success(request, "Déconnexion réussie ✔")
    return redirect('login')


# =========================
# 👤 PROFILE
# =========================
@login_required
def profile_view(request):
    # 🔥 éviter crash si profile n'existe pas
    profile = getattr(request.user, 'profile', None)

    if not profile:
        messages.error(request, "Profil introuvable ❌")
        return redirect('home')

    if request.method == "POST":

        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        preferred_destination = request.POST.get("preferred_destination", "")
        travel_style = request.POST.get("travel_style", "")

        # validation
        if phone and len(phone) > 20:
            messages.error(request, "Numéro invalide ❌")
            return redirect('profile')

        profile.phone = phone
        profile.address = address
        profile.preferred_destination = preferred_destination
        profile.travel_style = travel_style

        # upload fichier
        if request.FILES.get("passport"):
            file = request.FILES["passport"]

            if not file.name.endswith(('.pdf', '.jpg', '.png')):
                messages.error(request, "Format non supporté ❌")
                return redirect('profile')

            profile.passport = file

        profile.save()

        messages.success(request, "Profil mis à jour ✔")
        return redirect('profile')

    return render(request, "frontend/users/profile.html", {
        "profile": profile
    })
