from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):

    TYPE_CHOICES = [
        ('reservation', 'Réservation'),
        ('payment', 'Paiement'),
        ('system', 'Système'),
    ]

    # =========================
    # USER
    # =========================
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    # =========================
    # CONTENU
    # =========================
    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='system'
    )

    # =========================
    # ETAT
    # =========================
    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =========================
    # META
    # =========================
    class Meta:

        ordering = ['-created_at']

        verbose_name = "Notification"

        verbose_name_plural = "Notifications"

    # =========================
    # STRING
    # =========================
    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.title}"
        )