from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField


class user(models.Model):
    id_user = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=56)
    lastname = models.CharField(max_length=56, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)
    couple = models.BooleanField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    picture_profil = models.BinaryField(null=True, blank=True)

    def __str__(self):
        if self.lastname:
            return self.firstname + ' ' + self.lastname
        else:
            return self.firstname

class baby(models.Model):
    id_baby = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=56)
    lastname = models.CharField(max_length=56, null=True, blank=True)
    birthday = models.DateField()
    size = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    id_user = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        if self.lastname:
            return self.firstname + ' ' + self.lastname
        else:
            return self.firstname

class biberon(models.Model):
    id_biberon = models.AutoField(primary_key=True)
    id_baby = models.ForeignKey(baby, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    nb_biberon = models.IntegerField(null=True, blank=True)

class forum(models.Model):
    id_forums = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(user, on_delete=models.CASCADE)

class message(models.Model):
    id_message = models.AutoField(primary_key=True)
    text_message = models.CharField(max_length=56)
    id_forum = models.ForeignKey(forum, on_delete=models.CASCADE)
    id_user = models.ForeignKey(user, on_delete=models.CASCADE)

class pregnancie(models.Model):
    id_pregnancy = models.AutoField(primary_key=True)
    pregnancy_date = models.DateField(null=True, blank=True)
    amenorhea_date = models.DateField(null=True, blank=True)
    id_user = models.ForeignKey(user, on_delete=models.CASCADE)

class Image(models.Model):
    name = models.CharField(max_length=255)
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return self.name
