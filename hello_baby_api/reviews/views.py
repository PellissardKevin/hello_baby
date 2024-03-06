from .serializers import UserSerializer, ImageSerializer, BabySerializer, PregnancieSerializer
from .models import user, Image, baby, pregnancie
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet
from rest_framework.permissions import IsAuthenticated


class UserViewSet(FlexFieldsMixin, ModelViewSet):
    serializer_class = UserSerializer
    filterset_fields = ('id_user','email',)
    def get_queryset(self):
        queryset = user.objects.all()
        return queryset


class ImageViewSet(FlexFieldsModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]

class BabyViewSet(FlexFieldsMixin, ModelViewSet):
    serializer_class = BabySerializer
    filterset_fields = ('id_user',)
    def get_queryset(self):
        queryset = baby.objects.all()
        return queryset

class PregnancieViewSet(FlexFieldsMixin, ModelViewSet):
    serializer_class = PregnancieSerializer
    filterset_fields = ('id_user',)
    def get_queryset(self):
        queryset = pregnancie.objects.all()
        return queryset
