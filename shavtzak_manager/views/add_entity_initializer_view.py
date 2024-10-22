from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..serializers import AddEntityInitializerSerializer

# View to add a user as an entity initializer
class AddEntityInitializerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddEntityInitializerSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Entity initializer created successfully.',
                'user_id': user.id, 
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)