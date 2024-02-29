from rest_framework import serializers
from django.contrib.auth.models import User
from reviews.models import user
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = user
        fields = ('firstname', 'lastname', 'email', 'password', 'birthday', 'couple', 'weight', 'picture_profil')
        extra_kwargs = {
            'email': {'required': True},
            'firstname': {'required': True},
            'lastname': {'required': False, 'default': None},
            'birthday': {'required': False, 'default': None},
            'couple': {'required': False, 'default': None},
            'weight': {'required': False, 'default': None},
            'picture_profil': {'required': False, 'default': None},
        }

    def create(self, validated_data):
        userbaby = user.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            email=validated_data['email'],
            password=validated_data['password'],
            birthday=validated_data['birthday'],
            couple=validated_data['couple'],
            weight=validated_data['weight']
        )

        userAuth = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['firstname']
        )

        userAuth.set_password(validated_data['password'])
        userAuth.save()
        userbaby.save()

        return userAuth, userbaby


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance
