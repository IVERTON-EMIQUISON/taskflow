"""
URL configuration for Sistema_de_tarefas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from users.api.views import UserProfileExampleViewSet
from users.api.register_apiview import RegistroUsuario
from django.views.generic import TemplateView
from django.conf import settings
# Removed duplicate import of path
from users.api.register_apiview import LoginAPIView
from tarefas.views import buscar_tarefa_por_titulo


router = SimpleRouter()

router.register("users", UserProfileExampleViewSet, basename="users")

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),   # Redireciona para a página de login
    path("admin/", admin.site.urls),
    path("api/token-auth/", views.obtain_auth_token),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('tarefas/', include('tarefas.urls')),  
    path('registro.html', TemplateView.as_view(template_name="registro.html"), name='registro_html'), 
    path('home.html', TemplateView.as_view(template_name="home.html"), name='home.html'),
    path('registro/', RegistroUsuario.as_view(), name='registro_usuario'),  
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('buscar-tarefa/<str:titulo>/', buscar_tarefa_por_titulo, name='buscar_tarefa_por_titulo'),  
   
    path('lista/', TemplateView.as_view(template_name="lista.html"), name='lista'),  
    
]+router.urls
