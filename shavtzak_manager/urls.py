from django.urls import path
from .views import AddUserView, AddEntityInitializerView

urlpatterns = [
    path('users/add', AddUserView.as_view(), name='add_user'),
    path('users/add/entity-initializer', AddEntityInitializerView.as_view(), name='add_entity_initializer'),
]
