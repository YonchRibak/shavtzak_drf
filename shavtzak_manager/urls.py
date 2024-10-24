from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AddUserView, AddEntityInitializerView, EntityView

urlpatterns = [
    path('users/add', AddUserView.as_view(), name='add_user'),
    path('users/add/entity-initializer', AddEntityInitializerView.as_view(), name='add_entity_initializer'),
    path('api-token-auth/', TokenObtainPairView.as_view(), name='api-token-obtain-pair'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('entities/', EntityView.as_view(), name='create_entity' )
]
