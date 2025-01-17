from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import Resource

class ResourceSerializer(ModelSerializer):
    class Meta:
        model = Resource
        fields = ['created_by', 'name', 'description']
