from rest_framework import serializers
from ..models import Entity


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['id', 'name', 'description', 'created_at', 'code', 'creator', 'group']
        read_only_fields = ['id', 'created_at', 'code', 'creator', 'group']
