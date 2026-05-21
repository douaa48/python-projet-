from django.contrib import admin
from django.utils.html import format_html

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (

        'reservation',

        'user',

        'amount',

        'payment_type',

        'method',

        'status_colored',

        'created_at',
    )

    list_filter = (

        'status',

        'payment_type',

        'method',

        'created_at',
    )

    search_fields = (

        'reservation__id',

        'reservation__user__username',
    )

    ordering = (
        '-created_at',
    )


    readonly_fields = (
        'created_at',
    )

    
    list_per_page = 10

    
    def user(self, obj):

        return obj.reservation.user

    user.short_description = "Utilisateur"

   
    def status_colored(self, obj):

        colors = {

            'pending': 'orange',

            'paid': 'green',

            'refunded': 'blue',

            'failed': 'red',

        }

        return format_html(

            '<strong style="color:{};">{}</strong>',

            colors.get(obj.status),

            obj.get_status_display()

        )

    status_colored.short_description = "Statut"
    actions = [

        'mark_as_paid',

        'mark_as_refunded',

        'mark_as_failed',
    ]
    def mark_as_paid(self, request, queryset):

        updated = queryset.update(
            status='paid'
        )

        self.message_user(

            request,

            f"{updated} paiement(s) marqué(s) comme payés"

        )

    mark_as_paid.short_description = (
        "💳 Marquer comme payé"
    )
    def mark_as_refunded(self, request, queryset):

        updated = queryset.update(
            status='refunded'
        )

        self.message_user(

            request,

            f"{updated} paiement(s) remboursé(s)"

        )

    mark_as_refunded.short_description = (
        "💸 Marquer comme remboursé"
    )


    def mark_as_failed(self, request, queryset):

        updated = queryset.update(
            status='failed'
        )

        self.message_user(

            request,

            f"{updated} paiement(s) refusé(s)"

        )

    mark_as_failed.short_description = (
        "❌ Marquer comme refusé"
    )