from rest_framework import serializers
from .models import Account, User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'mot_de_passe']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ['id', 'nom', 'prénom', 'email', 'mot_de_passe',
                 'date_de_naissance', 'poids', 'début_de_grossesse', 'couple']
