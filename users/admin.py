from django.contrib import admin
from .models import User, Profile


# 🔥 INLINE PROFILE (afficher dans User)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# 👤 USER ADMIN
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

    inlines = [ProfileInline]


# 👤 PROFILE ADMIN (optionnel mais utile)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'preferred_destination',
        'travel_style'
    )

    search_fields = ('user__username',)