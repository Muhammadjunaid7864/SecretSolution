from rest_framework import serializers
from .models import SealStatus
class SealStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model   = SealStatus
        fields  = ['threshold','share']

class UnsealKeySerializer(serializers.Serializer):
    unseal_key  = serializers.CharField()