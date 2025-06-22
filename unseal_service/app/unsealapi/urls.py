from django.urls import path
from .views import InitializeProduct,SubmitUnsealKey

app_code = "unseal"
urlpatterns = [
    path('init/', InitializeProduct.as_view(), name="initialization"),
    path('unseal/',SubmitUnsealKey.as_view(), name="submit_unseal"),
]