from djoser.views import UserViewSet

from api.serializers import CustomUserSerializer
from api.pagination import LimitPageNumberPagination
from users.models import CustomUser


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination
