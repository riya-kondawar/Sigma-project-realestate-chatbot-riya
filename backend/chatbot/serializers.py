from rest_framework import serializers
from .models import RealEstateData

class RealEstateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateData
        fields = '__all__'