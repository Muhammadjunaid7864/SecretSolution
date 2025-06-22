from rest_framework import serializers
from .models import Wraping_key


class WrapSerializer(serializers.ModelSerializer):
    class Meta:
        model       = Wraping_key
        fields      = '__all__'