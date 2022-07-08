from djoser.views import UserViewSet

from users.models import CustomUser
from api.serializers import CustomUserSerializer

from api.pagination import LimitPageNumberPagination


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        return CustomUser.objects.all()
