from django.shortcuts import render
from .serializers import SealStatusSerializer,UnsealKeySerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .models import SealStatus
from rest_framework.response import Response
from rest_framework import status
import secrets
from core.utils import split_secret
from core.security import generte_wraping_key
from core.seal_state import SecretProduct
import base64
from django.core.cache import cache

class InitializeProduct(CreateAPIView):
    serializer_class = SealStatusSerializer
    queryset = SealStatus.objects.none()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            

            if serializer.is_valid():
                threshold = serializer.validated_data['threshold']
                share     = serializer.validated_data['share']

                if SealStatus.objects.exists():
                    return Response({"detail": "Secret Solution Seal key already Created"})
                
                raw_bytes  = secrets.token_bytes(32)
                master_key = base64.urlsafe_b64encode(raw_bytes).decode('utf-8')
                root_token  = secrets.token_hex(16)
                SecretProduct.store_master_key(master_key=master_key)
                ferent = generte_wraping_key(master_key)
                encrypt_root_token =ferent.encrypt(root_token.encode())

                unseal_key  = split_secret(master_key,share,threshold)
                encrypt_unseal_key = []
                for key in unseal_key:
                    encrypt_unseal_key.append(ferent.encrypt(key.encode()).decode())

                SealStatus.objects.create(
                    seal= True,
                    threshold= threshold,
                    share= share,
                    unseal_key= encrypt_unseal_key,
                    root_token= encrypt_root_token
                )

                return Response({'unseal keys': unseal_key, 'root_token': root_token })

        except Exception as e:
            return e


class SubmitUnsealKey(APIView): 
    def post(self, request, *args, **kwargs):
        submit_unseal_keys = cache.get("submit_unseal_key")
        seal_status = SealStatus.objects.first()
        if not submit_unseal_keys:
            seal_status.seal = True
            seal_status.save()

        if seal_status and not seal_status.seal and  submit_unseal_keys:
            return Response({"detail": "Secret Solution already unsealed."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UnsealKeySerializer(data=request.data)
        if serializer.is_valid():
            unseal_key = serializer.validated_data['unseal_key']
            try:
                threshold = SecretProduct.get_threshold()
                

                if submit_unseal_keys and unseal_key in submit_unseal_keys:
                    return Response({"detail": "Key already submitted."})

                result = SecretProduct.submit_key(unseal_key, threshold)

                if result:
                    SecretProduct.store_master_key(result)
                elif not result:
                    return Response({"detail": "Unseal key accepted. Waiting for more."}, status=status.HTTP_202_ACCEPTED)

                try:
                    unseal_keys = SecretProduct.get_unseal_key()
                except Exception:
                    return Response({"detail": "Invalid unseal key"})

                if set(submit_unseal_keys).issubset(unseal_keys):
                    seal_status = SealStatus.objects.first()
                    if seal_status:
                        seal_status.seal = False
                        seal_status.save()

                    return Response({"detail": "Vault unsealed successfully."}, status=status.HTTP_200_OK)

                return Response({"detail": "Invalid unseal key"})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)