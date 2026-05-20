from django.contrib import admin
from django.utils.html import format_html
from .models import Voyage, Option


# =========================
# INLINE OPTIONS
# =========================
class OptionInline(admin.TabularInline):

    model = Option

    extra = 1


# =========================
# VOYAGE ADMIN
# =========================
@admin.register(Voyage)
class VoyageAdmin(admin.ModelAdmin):

    # =========================
    # DISPLAY
    # =========================
    list_display = (
        'image_preview',
        'title',
        'destination',
        'category',
        'price',
        'duree_voyage',
        'reservations_count',
        'revenus',
        'disponibilite',
        'is_active_colored',
    )

    # =========================
    # FILTERS
    # =========================
    list_filter = (
        'category',
        'is_active',
        'start_date',
    )

    # =========================
    # SEARCH
    # =========================
    search_fields = (
        'title',
        'destination',
    )

    # =========================
    # EDITABLE
    # =========================
    list_editable = (
        'price',
    )

    # =========================
    # ORDERING
    # =========================
    ordering = (
        '-start_date',
    )

    # =========================
    # PAGINATION
    # =========================
    list_per_page = 10

    # =========================
    # DATE
    # =========================
    date_hierarchy = 'start_date'

    # =========================
    # READONLY
    # =========================
    readonly_fields = (
        'created_at',
        'image_preview',
    )

    # =========================
    # INLINE
    # =========================
    inlines = [OptionInline]

    # =========================
    # FIELDSETS
    # =========================
    fieldsets = (

        (
            "Informations principales",
            {
                'fields': (
                    'title',
                    'destination',
                    'description',
                    'category',
                    'price',
                )
            }
        ),

        (
            "Dates",
            {
                'fields': (
                    'start_date',
                    'end_date',
                )
            }
        ),

        (
            "Disponibilité",
            {
                'fields': (
                    'places',
                    'is_active',
                )
            }
        ),

        (
            "Programme",
            {
                'fields': (
                    'itinerary',
                    'points_interet',
                )
            }
        ),

        (
            "Image",
            {
                'fields': (
                    'image',
                    'image_preview',
                )
            }
        ),

    )

    # =========================
    # IMAGE PREVIEW
    # =========================
    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" width="70" height="50" style="border-radius:8px;" />',
                obj.image.url
            )

        return "Aucune image"

    image_preview.short_description = "Image"

    # =========================
    # DUREE
    # =========================
    def duree_voyage(self, obj):

        return f"{obj.duree()} jours"

    duree_voyage.short_description = "Durée"

    # =========================
    # RESERVATIONS
    # =========================
    def reservations_count(self, obj):

        return obj.total_reservations()

    reservations_count.short_description = "Réservations"

    # =========================
    # REVENUS
    # =========================
    def revenus(self, obj):

        return f"{obj.revenus_generes()} DH"

    revenus.short_description = "Revenus"

    # =========================
    # DISPONIBILITE
    # =========================
    def disponibilite(self, obj):

        restantes = obj.places_restantes()

        if restantes <= 0:

            return format_html(
                '<strong style="color:red;">Complet ❌</strong>'
            )

        elif restantes <= 5:

            return format_html(
                '<strong style="color:orange;">{} ⚠️</strong>',
                restantes
            )

        return format_html(
            '<strong style="color:green;">{} ✔</strong>',
            restantes
        )

    disponibilite.short_description = "Disponibilité"

    # =========================
    # ACTIVE STATUS
    # =========================
    def is_active_colored(self, obj):

        if obj.is_active:

            return format_html(
                '<strong style="color:green;">✔ Actif</strong>'
            )

        return format_html(
            '<strong style="color:red;">❌ Inactif</strong>'
        )

    is_active_colored.short_description = "Statut"

    # =========================
    # ACTIONS
    # =========================
    actions = [
        'activer_voyages',
        'desactiver_voyages',
    ]

    def activer_voyages(self, request, queryset):

        updated = queryset.update(
            is_active=True
        )

        self.message_user(
            request,
            f"{updated} voyage(s) activé(s)"
        )

    activer_voyages.short_description = "✔ Activer"

    def desactiver_voyages(self, request, queryset):

        updated = queryset.update(
            is_active=False
        )

        self.message_user(
            request,
            f"{updated} voyage(s) désactivé(s)"
        )

    desactiver_voyages.short_description = "❌ Désactiver"


# =========================
# OPTION ADMIN
# =========================
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'price',
        'voyage',
        'is_active',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'voyage',
        'is_active',
    )