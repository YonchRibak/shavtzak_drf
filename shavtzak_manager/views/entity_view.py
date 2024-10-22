from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Entity, UserType
from django.core.exceptions import PermissionDenied

class EntityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user has the appropriate type to create an entity
        if not request.user.user_system_custom_fields.user_type == UserType.ENTITY_INITIALIZER.value:
            raise PermissionDenied("Only entity initializers can create entities.")

        name = request.data.get('name')
        description = request.data.get('description')

        # Create the entity with the logged-in user as the creator
        entity = Entity.objects.create(
            name=name,
            description=description,
            creator=request.user
        )

        # Return a JSON response with the created entity data
        return Response({
            'id': entity.id,
            'name': entity.name,
            'code': entity.code,
            'creator': entity.creator.email,
            'created_at': entity.created_at.isoformat(),
        }, status=status.HTTP_201_CREATED)
