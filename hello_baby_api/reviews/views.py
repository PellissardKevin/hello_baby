from .serializers import UserSerializer, ImageSerializer, BabySerializer, PregnancieSerializer, ForumSerializer, MessageSerializer, BiberonSerializer, PasswordResetSerializer
from .models import user, Image, baby, pregnancie, forum, message, biberon
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import generics
from rest_framework.views import APIView
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
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
    filterset_fields = ('id_user', 'firstname', 'id_baby')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = baby.objects.all()
        return queryset

class PregnancieViewSet(FlexFieldsMixin, ModelViewSet):
    serializer_class = PregnancieSerializer
    filterset_fields = ('id_user',)

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
    filterset_fields = ('id_user','id_forum',)
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
    filterset_fields = ('id_user', 'id_baby')
    serializer_class = BabySerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PasswordResetAPIView(FlexFieldsMixin, APIView):
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']

            try:
                user_instance = user.objects.get(email=email)
            except user.DoesNotExist:
                return Response({"error": "Aucun utilisateur trouvé avec cette adresse e-mail."}, status=status.HTTP_404_NOT_FOUND)

            # Réinitialisation du mot de passe
            user_instance.password = make_password(new_password)
            user_instance.save()

            return Response({"message": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
