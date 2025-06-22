from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import WrapSerializer
from cryptography.fernet import Fernet
from rest_framework.response import Response
from django.core.cache import cache
from .seal_state import ProductState
from .models import Wraping_key
# Create your views here.

class SubmitWrappingKeyView(CreateAPIView):
    serializer_class = WrapSerializer
    queryset = Wraping_key.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wrapping_key = serializer.validated_data["wrap_key"]

        try:
            encrypted_master = cache.get("master_key")
            if encrypted_master:
                if isinstance(encrypted_master, str):
                    encrypted_master = encrypted_master.encode()
                master_key = Fernet(wrapping_key.encode()).decrypt(encrypted_master).decode()
                ProductState.store_master_key(master_key)
                return Response({"detail": "Wrapping key accepted. Vault unlocked."})
            return Response({"detail": "No encrypted master key found in cache."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)