from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from pacientes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO: remover linha abaixo apos criar sistema de login completo
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html')),
    path('accounts/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('pacientes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)