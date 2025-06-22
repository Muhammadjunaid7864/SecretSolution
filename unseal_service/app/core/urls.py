from django.urls import path
from .views import SubmitWrappingKeyView

app_code = 'core'
urlpatterns = [
    path('wraping/',SubmitWrappingKeyView.as_view()),
]