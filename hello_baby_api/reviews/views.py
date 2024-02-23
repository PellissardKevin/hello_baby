from .serializers import UserSerializer, ImageSerializer
from .models import user, Image
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet
from rest_flex_fields import is_expanded
from rest_framework.permissions import IsAuthenticated


class UserViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permit_list_expands = ['firstname', 'lastname', 'email', 'password', 'birthday', 'couple', 'weight']
    def get_queryset(self):
        queryset = user.objects.all()

        if is_expanded(self.request, 'firstname'):
            queryset = queryset.prefetch_related('firstname')

        if is_expanded(self.request, 'lastname'):
            queryset = queryset.prefetch_related('lastname')

        if is_expanded(self.request, 'email'):
            queryset = queryset.prefetch_related('email')

        if is_expanded(self.request, 'birthday'):
            queryset = queryset.prefetch_related('birthday')

        if is_expanded(self.request, 'couple'):
            queryset = queryset.prefetch_related('couple')

        return queryset

class ImageViewSet(FlexFieldsModelViewSet):

    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]
