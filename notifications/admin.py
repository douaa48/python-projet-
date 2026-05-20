from django.contrib import admin
from django.utils.html import format_html
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    # =========================
    # DISPLAY
    # =========================
    list_display = (
        'user',
        'title',
        'type',
        'status_colored',
        'created_at',
    )

    # =========================
    # FILTERS
    # =========================
    list_filter = (
        'type',
        'is_read',
        'created_at',
    )

    # =========================
    # SEARCH
    # =========================
    search_fields = (
        'user__username',
        'title',
        'message',
    )

    # =========================
    # ORDERING
    # =========================
    ordering = (
        '-created_at',
    )

    # =========================
    # READONLY
    # =========================
    readonly_fields = (
        'created_at',
    )

    # =========================
    # PAGINATION
    # =========================
    list_per_page = 10

    # =========================
    # STATUS COLOR
    # =========================
    def status_colored(self, obj):

        if obj.is_read:

            return format_html(
                '<strong style="color:green;">✔ Lue</strong>'
            )

        return format_html(
            '<strong style="color:red;">● Non lue</strong>'
        )

    status_colored.short_description = "État"

    # =========================
    # ACTIONS
    # =========================
    actions = [
        'mark_as_read',
    ]

    def mark_as_read(self, request, queryset):

        updated = queryset.update(
            is_read=True
        )

        self.message_user(
            request,
            f"{updated} notification(s) marquée(s) comme lues"
        )

    mark_as_read.short_description = "✔ Marquer comme lues"