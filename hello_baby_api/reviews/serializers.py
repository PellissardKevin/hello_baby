from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .models import user, baby, forum, message, biberon, pregnancie, Image
from django.contrib.auth.models import User
from versatileimagefield.serializers import VersatileImageFieldSerializer



class UserSerializer(FlexFieldsModelSerializer):
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
            "weight",
            "picture_profil"
        ]
        expandable_fields = {
            'picture_profil': ('reviews.ImageSerializer', {'many': True}),
        }


class BabySerializer(FlexFieldsModelSerializer):
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
        ]
        expandable_fields = {
            'id_user': ('reviews.UserSerializer', {'many': False}),
        }

class BiberonSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = biberon
        fields = [
            "id_biberon",
            "quantity",
            "nb_biberon",
        ]
        expandable_fields = {
            'id_baby': ('reviews.BabySerializer', {'many': False}),
        }

class ForumSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = forum
        fields = [
            "id_forums",
        ]
        expandable_fields = {
            'id_user': ('reviews.UserSerializer', {'many': False}),
        }

class MessageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = message
        fields = [
            "id_messages",
            "text_messages"
            "id_forum",
            "id_user",
        ]
        expandable_fields = {
            'id_user': ('reviews.UserSerializer', {'many': False}),
            'id_forum': ('reviews.ForumsSerializer', {'many': True}),
        }

class PregnancieSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = pregnancie
        fields = [
            "id_pregnancy",
            "pregnancy_date",
            "amenorhea_date",
        ]
        expandable_fields = {
            'id_user': ('reviews.UserSerializer', {'many': False})
        }

class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes='product_headshot'
    )

    class Meta:
        model = Image
        fields = ['pk', 'name', 'image']

