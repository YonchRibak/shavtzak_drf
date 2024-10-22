from rest_framework import serializers
from ..models import Entity

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['id', 'name', 'description', 'created_at', 'code', 'creator', 'group']
        read_only_fields = ['id', 'created_at', 'code', 'creator', 'group']

    def validate(self, data):
       # Ensure that the name is unique (if not already enforced by the model)
        if Entity.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("An entity with this name already exists.")
        
        # Check description length
        if len(data.get('description', '')) > 300:
            raise serializers.ValidationError("Description cannot exceed 300 characters.")
        
        return data

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)
