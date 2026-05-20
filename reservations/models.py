from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from voyages.models import Option, Voyage
from notifications.models import Notification

from datetime import date
from decimal import Decimal


class Reservation(models.Model):

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
        ('completed', 'Terminée'),
    ]

    # =========================
    # RELATIONS
    # =========================
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    voyage = models.ForeignKey(
        Voyage,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    options = models.ManyToManyField(
        Option,
        blank=True,
        related_name="reservations"
    )

    # =========================
    # INFOS RESERVATION
    # =========================
    date_arrivee = models.DateField(
        null=True,
        blank=True
    )

    date_retour = models.DateField(
        null=True,
        blank=True
    )

    personnes = models.PositiveIntegerField(
        default=1
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================
    # META
    # =========================
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"

    # =========================
    # STRING
    # =========================
    def __str__(self):

        if self.voyage_id:
            return f"{self.user.username} - {self.voyage.title}"

        return f"{self.user.username} - Reservation"

    # =========================
    # VALIDATION
    # =========================
    def clean(self):

        if self.voyage_id:

            # Validation date arrivée
            if self.date_arrivee:
                if self.date_arrivee < self.voyage.start_date:
                    raise ValidationError(
                        "La date d'arrivée est avant le début du voyage"
                    )

            # Validation date retour
            if self.date_retour:
                if self.date_retour > self.voyage.end_date:
                    raise ValidationError(
                        "La date de retour dépasse la fin du voyage"
                    )

            # Validation dates entre elles
            if self.date_arrivee and self.date_retour:

                if self.date_retour <= self.date_arrivee:
                    raise ValidationError(
                        "La date de retour doit être après la date d'arrivée"
                    )

            # Validation places
            reserved = sum(
                reservation.personnes
                for reservation in self.voyage.reservations
                .filter(status__in=['pending', 'confirmed'])
                .exclude(pk=self.pk)
            )

            places_disponibles = self.voyage.places - reserved

            if self.personnes and self.personnes > places_disponibles:
                raise ValidationError(
                    "Nombre de places insuffisant"
                )

        # Validation personnes
        if self.personnes < 1:
            raise ValidationError(
                "Nombre de personnes invalide"
            )

    # =========================
    # CALCUL TOTAL
    # =========================
    def calculer_total(self, options=None):

        if not self.voyage_id:
            return Decimal('0.00')

        duree = self.duree() or 1

        base = self.voyage.price * self.personnes * duree

        if options is None:

            options_total = (
                sum(option.price for option in self.options.all())
                if self.pk else Decimal('0.00')
            )

        else:
            options_total = sum(option.price for option in options)

        return base + options_total

    # =========================
    # SAVE
    # =========================
    def save(self, *args, **kwargs):

        skip_validation = kwargs.pop('skip_validation', False)

        if not skip_validation:
            self.full_clean()

        is_new = self.pk is None

        previous_status = None

        if not is_new:

            previous_status = (
                Reservation.objects
                .filter(pk=self.pk)
                .values_list('status', flat=True)
                .first()
            )

        # Calcul total
        if self.voyage_id and self.personnes and not self.total:
            self.total = self.calculer_total()

        super().save(*args, **kwargs)

        # Notification création
        if is_new and self.voyage_id:

            Notification.objects.create(
                user=self.user,
                title="Nouvelle réservation",
                message=f"Votre réservation pour {self.voyage.title} a été créée avec succès.",
                type='reservation'
            )

        status_changed = previous_status != self.status

        # Notification confirmation
        if (
            not is_new
            and status_changed
            and self.status == 'confirmed'
            and self.voyage_id
        ):

            Notification.objects.create(
                user=self.user,
                title="Réservation confirmée",
                message=f"Votre réservation pour {self.voyage.title} a été confirmée.",
                type='reservation'
            )

        # Notification annulation
        elif (
            not is_new
            and status_changed
            and self.status == 'cancelled'
            and self.voyage_id
        ):

            Notification.objects.create(
                user=self.user,
                title="Réservation annulée",
                message=f"Votre réservation pour {self.voyage.title} a été annulée.",
                type='reservation'
            )

    # =========================
    # DUREE
    # =========================
    def duree(self):

        if self.date_arrivee and self.date_retour:
            return (self.date_retour - self.date_arrivee).days

        return 0

    # =========================
    # ANNULATION
    # =========================
    def jours_avant_depart(self):

        if self.date_arrivee:
            return (self.date_arrivee - date.today()).days

        return 0

    def peut_annuler(self):

        if self.status == 'cancelled':
            return False

        return self.jours_avant_depart() >= 3

    # =========================
    # REMBOURSEMENT
    # =========================
    def taux_remboursement(self):

        jours = self.jours_avant_depart()

        if jours >= 7:
            return Decimal('1.0')

        elif 3 <= jours < 7:
            return Decimal('0.5')

        return Decimal('0.0')

    def montant_remboursement(self):

        return self.total_paye() * self.taux_remboursement()

    # =========================
    # PAIEMENT
    # =========================
    def total_paye(self):

        if hasattr(self, 'payments'):

            return sum(
                p.amount
                for p in self.payments.filter(status='paid')
            )

        return Decimal('0.00')

    def reste_a_payer(self):

        total = self.total or Decimal('0.00')

        paye = self.total_paye()

        return total - paye

    def paiement_complet(self):

        return self.reste_a_payer() <= 0

    def acompte(self):

        total = self.total or Decimal('0.00')

        return total * Decimal('0.3')

    # =========================
    # STATISTIQUES ADMIN
    # =========================
    @classmethod
    def total_revenus(cls):

        reservations = cls.objects.filter(status='confirmed')

        return sum(r.total or 0 for r in reservations)