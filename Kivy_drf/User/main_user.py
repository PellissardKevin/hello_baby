#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

Window.size = (430, 932)


kivy.require('2.0.0')


class User(BoxLayout):
    def __init__(self, nom='', prénom='', date_de_naissance='%d-%m-%Y',
                 poids=0, début_de_grossesse='%d-%m-%Y', couple=False,
                 email='', mot_de_passe=''):
        super(User, self).__init__()
        self.nom = nom
        self.prénom = prénom
        self.date_de_naissance = date_de_naissance
        self.poids = poids
        self.début_de_grossesse = début_de_grossesse
        self.couple = couple
        self.email = email
        self.mot_de_passe = mot_de_passe

    def create():
        pass


class userfile(App):
    def build(self):
        return User()


if __name__ == '__main__':
    userfile().run()
