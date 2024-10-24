from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import Entity


class EntitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=Entity.objects.all(), message='Name must be unique')])
    class Meta:
        model = Entity
        fields = ['id', 'name', 'description', 'created_at', 'code', 'creator', 'group']
        read_only_fields = ['id', 'created_at', 'code', 'creator', 'group']
