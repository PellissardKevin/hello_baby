from django.db import models

class Account(models.Model):
    email = models.CharField(max_length=200)
    mot_de_passe = models.CharField(max_length=200)

    def __str__(self):
        return self.email + ' ' + self.mot_de_passe


class User(models.Model):
    nom = models.CharField(max_length=200)
    prénom = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mot_de_passe = models.CharField(max_length=200)
    date_de_naissance = models.CharField(max_length=200)
    poids = models.CharField(max_length=200)
    début_de_grossesse = models.CharField(max_length=200)
    couple = models.CharField(max_length=200)

    def __str__(self):
            return (self.nom + ' ' + self.prénom + ' ' + self.email + ' ' +
                    self.mot_de_passe + ' ' + self.date_de_naissance + ' ' +
                    self.poids + ' ' + self.début_de_grossesse + ' ' +
                    self.couple)
