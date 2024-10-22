from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import UserType
from django.core.exceptions import PermissionDenied
from ..serializers import EntitySerializer

class EntityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user has the appropriate type to create an entity
        if request.user.user_system_custom_fields.user_type != UserType.ENTITY_INITIALIZER.value:
            raise PermissionDenied("Only entity initializers can create entities.")

        # Use the serializer for validation and creation
        serializer = EntitySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            entity = serializer.save()
            return Response({
                'id': entity.id,
                'name': entity.name,
                'code': entity.code,
                'creator': entity.creator.email,
                'created_at': entity.created_at.isoformat(),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
