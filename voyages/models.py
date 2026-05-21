from django.db import models
from django.core.exceptions import ValidationError

class Voyage(models.Model):

    CATEGORY_CHOICES = [
        ('plage', 'Plage'),
        ('montagne', 'Montagne'),
        ('ville', 'Ville'),
        ('desert', 'Désert'),
    ]

    title = models.CharField(
        max_length=200
    )

    destination = models.CharField(
        max_length=100
    )

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='ville'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    start_date = models.DateField()

    end_date = models.DateField()

    image = models.ImageField(
        upload_to='voyages/',
        null=True,
        blank=True
    )

    
    itinerary = models.TextField(
        blank=True,
        null=True
    )

   
    points_interet = models.TextField(
        blank=True,
        null=True
    )

   
    places = models.PositiveIntegerField(
        default=20
    )

    
    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    
    class Meta:

        ordering = ['start_date']

        verbose_name = "Voyage"

        verbose_name_plural = "Voyages"

   
    def __str__(self):

        return (
            f"{self.title} "
            f"({self.start_date} → {self.end_date})"
        )

    
    def clean(self):

        if self.end_date <= self.start_date:

            raise ValidationError(
                "La date de fin doit être après la date de début"
            )

   
    def duree(self):

        return (
            self.end_date - self.start_date
        ).days

   
    def places_restantes(self):

        reserved = sum(

            r.personnes

            for r in self.reservations.filter(
                status__in=['pending', 'confirmed']
            )

        )

        return self.places - reserved

   
    def est_disponible(self):

        return (

            self.places_restantes() > 0

            and self.is_active

        )
    

    def total_reservations(self):

        return self.reservations.count()

    def revenus_generes(self):

        confirmed = self.reservations.filter(
            status='confirmed'
        )

        return sum(
            r.total or 0
            for r in confirmed
        )

    
    def est_populaire(self):

        return self.total_reservations() >= 5



class Option(models.Model):

    voyage = models.ForeignKey(
        Voyage,
        on_delete=models.CASCADE,
        related_name="options_list"
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

   
    class Meta:

        verbose_name = "Option"

        verbose_name_plural = "Options"

    def __str__(self):

        return (
            f"{self.name} "
            f"(+{self.price} DH)"
        )
    
    
