from rest_framework import serializers
from .models import user, baby, forum, message, biberon, pregnancie


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=4, write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = user
        fields = [
            "id_user",
            "firstname",
            "lastname",
            "email",
            "password",
            "birthday",
            "couple",
            "weight"
        ]


class BabySerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = baby
        fields = [
            "id_baby",
            "firstname",
            "lastname",
            "birthday",
            "size",
            "weight",
            "id_user",
        ]

class BiberonSerializer(serializers.ModelSerializer):
    class Meta:
        model = biberon
        fields = [
            "id_biberon",
            "id_baby",
            "quantity",
            "nb_biberon",
        ]

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = forum
        fields = [
            "id_forums",
            "id_user",
        ]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = [
            "id_messages",
            "text_messages"
            "id_forum",
            "id_user",
        ]

class PregnancieSerializer(serializers.ModelSerializer):
    class Meta:
        model = pregnancie
        fields = [
            "id_pregnancy",
            "id_user",
            "pregnancy_date",
            "amenorhea_date",
        ]
