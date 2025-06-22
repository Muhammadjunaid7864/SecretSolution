from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.core.cache import cache
import secrets
from .models import SealStaus
from core.seal_state import ProductState
from .serializers import InitVaultSerializer, UnsealKeySerializer
from core.utils import split_secret

class InitVaultView(CreateAPIView):
    serializer_class = InitVaultSerializer
    queryset = SealStaus.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        total = serializer.validated_data["total_shares"]
        threshold = serializer.validated_data["threshold"]

        if SealStaus.objects.exists():
            return Response({"detail": "Vault is already initialized."}, status=400)

        master_key = secrets.token_hex(32)  # safe string
        root_token = secrets.token_hex(16)

        unseal_keys = split_secret(master_key, total, threshold)

        SealStaus.objects.create(
            sealed=True,
            share=total,
            threshold=threshold,
            encrypted_root_token=root_token
        )

        cache.set("master_key", master_key, timeout=None)

        return Response({
            "unseal_keys": unseal_keys,
            "root_token": root_token
        })

class SubmitUnsealKeyView(CreateAPIView):
    serializer_class = UnsealKeySerializer
    queryset = SealStaus.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unseal_key = serializer.validated_data["unseal_key"]

        try:
            threshold = ProductState.get_threshold()
            result = ProductState.submit_key(unseal_key, threshold)
            if result:
                ProductState.store_master_key(result)
                return Response({"detail": "Vault unsealed successfully."})
            return Response({"detail": "Unseal key accepted. Waiting for more."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)