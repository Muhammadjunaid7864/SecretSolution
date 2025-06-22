from django.urls import path
from .views import SubmitUnsealKeyView,InitVaultView

app_code = 'unseal'
urlpatterns = [
    path("init/", InitVaultView.as_view(), name="init_vault"),
    path('unseal/',SubmitUnsealKeyView.as_view()),
]