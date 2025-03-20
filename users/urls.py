from django.urls import path
from .views import LoginView

urlpatterns = [
    # Outras URLs existentes...
    path('login/', LoginView.as_view(), name='login'),
]
