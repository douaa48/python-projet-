from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError

from reservations.models import Reservation


class Payment(models.Model):

    # =========================
    # METHODES
    # =========================
    METHOD_CHOICES = [

        ('card', 'Carte bancaire'),

        ('paypal', 'PayPal'),

        ('cash', 'Espèces'),

    ]

    # =========================
    # TYPES
    # =========================
    TYPE_CHOICES = [

        ('full', 'Paiement total'),

        ('deposit', 'Acompte'),

        ('installment', 'Paiement échelonné'),

    ]

    # =========================
    # STATUTS
    # =========================
    STATUS_CHOICES = [

        ('pending', 'En attente'),

        ('paid', 'Payé'),

        ('refunded', 'Remboursé'),

        ('failed', 'Refusé'),

    ]

    # =========================
    # RELATION
    # =========================
    reservation = models.ForeignKey(

        Reservation,

        on_delete=models.CASCADE,

        related_name="payments"
    )

    # =========================
    # MONTANT
    # =========================
    amount = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=Decimal('0.00')
    )

    # =========================
    # TYPE PAIEMENT
    # =========================
    payment_type = models.CharField(

        max_length=20,

        choices=TYPE_CHOICES,

        default='full'
    )

    # =========================
    # METHODE
    # =========================
    method = models.CharField(

        max_length=20,

        choices=METHOD_CHOICES,

        default='card'
    )

    # =========================
    # STATUT
    # =========================
    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =========================
    # META
    # =========================
    class Meta:

        ordering = ['-created_at']

        verbose_name = "Paiement"

        verbose_name_plural = "Paiements"

    # =========================
    # VALIDATION
    # =========================
    def clean(self):

        if self.amount <= 0:

            raise ValidationError(
                "Montant invalide"
            )

    # =========================
    # SAVE
    # =========================
    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    # =========================
    # PAIEMENT REUSSI
    # =========================
    def is_success(self):

        return self.status == 'paid'

    # =========================
    # REMBOURSEMENT
    # =========================
    def is_refunded(self):

        return self.status == 'refunded'

    def can_refund(self):

        return self.status == 'paid'

    def refund(self):

        if self.can_refund():

            self.status = 'refunded'

            self.save()

    # =========================
    # RESTE A PAYER
    # =========================
    def reste_reservation(self):

        total_paid = sum(

            p.amount

            for p in self.reservation.payments.filter(
                status='paid'
            )

        )

        return (

            self.reservation.total -
            total_paid

        )

    # =========================
    # PAIEMENT COMPLET
    # =========================
    def reservation_paid(self):

        return self.reste_reservation() <= 0

    # =========================
    # STRING
    # =========================
    def __str__(self):

        return (

            f"{self.reservation} - "

            f"{self.amount} DH "

            f"({self.status})"
        )