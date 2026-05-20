from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================
# 👤 USER
# =========================
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


# =========================
# 👤 PROFILE
# =========================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # 📞 infos personnelles
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # 🎯 préférences
    DESTINATION_CHOICES = [
        ('plage', 'Plage'),
        ('montagne', 'Montagne'),
        ('ville', 'Ville'),
        ('desert', 'Désert'),
    ]

    STYLE_CHOICES = [
        ('luxe', 'Luxe'),
        ('eco', 'Économique'),
        ('famille', 'Famille'),
        ('aventure', 'Aventure'),
    ]

    preferred_destination = models.CharField(
        max_length=50,
        choices=DESTINATION_CHOICES,
        blank=True
    )

    travel_style = models.CharField(
        max_length=50,
        choices=STYLE_CHOICES,
        blank=True
    )

    # 📄 document
    passport = models.FileField(
        upload_to='documents/',
        null=True,
        blank=True
    )

    # 🖼️ BONUS (important pour UI)
    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    # 📅 date création
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil de {self.user.username}"