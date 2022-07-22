from api.pagination import LimitPageNumberPagination
from api.serializers import CustomUserSerializer
from djoser.views import UserViewSet
from users.models import CustomUser


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination
