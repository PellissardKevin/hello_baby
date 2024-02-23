from django.http import JsonResponse
from .models import Account, User
from .serializers import AccountSerializer, UserSerializer

def account_list(request):
    accounts = Account.objects.all()
    serializer_account = AccountSerializer(accounts, many=True)
    return JsonResponse(serializer_account.data, safe=False)

def user_list(request):
    users = User.objects.all()
    serializer_user = UserSerializer(users, many=True)
    return JsonResponse(serializer_user.data, safe=False)
