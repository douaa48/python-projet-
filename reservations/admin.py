from django.contrib import admin
from django.utils.html import format_html
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'voyage',
        'personnes',
        'total',
        'status_colored',
        'duree_voyage',
        'paiement_status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
        'voyage',
    )

    search_fields = (
        'user__username',
        'voyage__title',
    )

    list_editable = (
        'personnes',
    )

    ordering = (
        '-created_at',
    )

    date_hierarchy = 'created_at'

    
    readonly_fields = (
        'created_at',
        'updated_at',
        'total',
    )

    list_per_page = 10

    actions = [
        'mark_as_confirmed',
        'mark_as_cancelled',
        'mark_as_completed',
    ]

   
    def status_colored(self, obj):

        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'cancelled': 'red',
            'completed': 'blue',
        }

        return format_html(
            '<strong style="color:{};">{}</strong>',
            colors.get(obj.status),
            obj.get_status_display()
        )

    status_colored.short_description = "Statut"

    
    def duree_voyage(self, obj):
        return f"{obj.duree()} jours"

    duree_voyage.short_description = "Durée"

    
    def paiement_status(self, obj):

        if obj.paiement_complet():
            return format_html(
                '<span style="color:green;">✔ Payé</span>'
            )

        return format_html(
            '<span style="color:red;">✘ Non payé</span>'
        )

    paiement_status.short_description = "Paiement"

    
    def mark_as_confirmed(self, request, queryset):

        updated = queryset.update(
            status='confirmed'
        )

        self.message_user(
            request,
            f"{updated} réservation(s) confirmée(s)"
        )

    mark_as_confirmed.short_description = "✔ Confirmer"

    
    def mark_as_cancelled(self, request, queryset):

        updated = queryset.update(
            status='cancelled'
        )

        self.message_user(
            request,
            f"{updated} réservation(s) annulée(s)"
        )

    mark_as_cancelled.short_description = "❌ Annuler"

   
    def mark_as_completed(self, request, queryset):

        updated = queryset.update(
            status='completed'
        )

        self.message_user(
            request,
            f"{updated} réservation(s) terminée(s)"
        )

    mark_as_completed.short_description = "🏁 Terminer"