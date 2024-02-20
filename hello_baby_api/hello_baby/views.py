from django.http import JsonResponse
from .models import user, baby, forum, message, pregnancie, biberon
from .serializers import UserSerializer, BabySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics

@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = user.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_details(request, id):
    try:
        user_id = user.objects.get(pk=id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user_id)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def user_baby(request, id):
    try:
        user_id = baby.objects.get(id_user=id)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user_id)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def baby_details(request, id):
    try:
        baby_id = baby.objects.get(pk=id)
    except baby.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BabySerializer(baby_id)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BabySerializer(baby_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        baby_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BabyUser(generics.ListAPIView):
    queryset = baby.objects.all()
    serializer_class = BabySerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            id_user=self.kwargs['id_user']
        )

