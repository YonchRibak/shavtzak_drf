from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from shavtzak_manager.models import Entity
from shavtzak_manager.permissions import IsEntityInitializer
from shavtzak_manager.serializers import EntitySerializer


class EntityViewSet(GenericViewSet, CreateModelMixin):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [IsAuthenticated, IsEntityInitializer]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["creator"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
