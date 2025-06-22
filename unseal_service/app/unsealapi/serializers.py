from rest_framework import serializers
from .models import SealStaus

class UnsealKeySerializer(serializers.Serializer):
    unseal_key = serializers.CharField()

class InitVaultSerializer(serializers.Serializer):
    total_shares = serializers.IntegerField()
    threshold = serializers.IntegerField()