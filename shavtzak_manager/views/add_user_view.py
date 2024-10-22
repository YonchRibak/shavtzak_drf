from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..serializers import AddUserSerializer

# View to add a user to an existing entity
class AddUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User added to the entity successfully.',
                'user_id': user.id,
                'email': user.email,
                'entity': user.group.name
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)