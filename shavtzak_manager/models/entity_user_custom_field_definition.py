from django.db import models

class EntityUserCustomFieldDefinition(models.Model):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, related_name='custom_field_definitions')
    field_name = models.CharField(max_length=50)  # Name of the custom field
    field_type = models.CharField(max_length=20)  # Type of the field (e.g., CharField, IntegerField, etc.)

    def __str__(self):
        return f"{self.field_name} ({self.field_type}) for {self.entity.name}"
