from django.urls import path
from .views import AddUserView, AddEntityInitializerView, LoginView, EntityView

urlpatterns = [
    path('users/add', AddUserView.as_view(), name='add_user'),
    path('users/add/entity-initializer', AddEntityInitializerView.as_view(), name='add_entity_initializer'),
    path('login/', LoginView.as_view(), name='login' ),
    path('entities/', EntityView.as_view(), name='create_entity' )
]
