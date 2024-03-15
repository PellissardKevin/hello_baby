from .serializers import UserSerializer, ImageSerializer, BabySerializer, PregnancieSerializer, ForumSerializer, MessageSerializer, BiberonSerializer
from .models import user, Image, baby, pregnancie, forum, message, biberon
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import generics
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
    filterset_fields = ('id_user', 'firstname', )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = baby.objects.all()
        return queryset

class PregnancieViewSet(FlexFieldsMixin, ModelViewSet):
    serializer_class = PregnancieSerializer
    filterset_fields = ('id_user',)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = pregnancie.objects.all()
        return queryset

class ForumViewSet(FlexFieldsMixin, ModelViewSet):
    serializer_class = ForumSerializer
    filterset_fields = ('id_user', 'id_forums', 'title')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = forum.objects.all()
        return queryset

class MessageViewSet(FlexFieldsMixin, ModelViewSet):
    serializer_class = MessageSerializer
    filterset_fields = ('id_user','id_forums',)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = message.objects.all()
        return queryset

class BiberonViewSet(FlexFieldsMixin, ModelViewSet):
    serializer_class = BiberonSerializer
    filterset_fields = ('id_baby',)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = biberon.objects.all()
        return queryset

class UserModelDeleteAPIView(FlexFieldsMixin, ModelViewSet):
    queryset = user.objects.all()
    filterset_fields = ('id_user','email',)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BabyModelDeleteAPIView(FlexFieldsMixin, ModelViewSet):
    queryset = baby.objects.all()
    filterset_fields = ('id_user',)
    serializer_class = BabySerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
