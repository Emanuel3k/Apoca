from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['email', 'username', 'is_medico', 'is_assistente_social', 'is_nutricionista', ]

    fieldsets = UserAdmin.fieldsets + (
        ('Perfil', {'fields': ('is_medico', 'is_assistente_social', 'is_nutricionista', 'foto')}),
    )

admin.site.register(User, UserAdmin)
