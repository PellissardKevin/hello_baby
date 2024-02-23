#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.carousel import Carousel


Window.size = (430, 932)

kivy.require('2.0.0')


class Baby(BoxLayout):
    def __init__(self, nom='', prénom='', date_de_naissance='%d-%m-%Y',
                 poids=0, taille=0):
        super(Baby, self).__init__()
        self.nom = nom
        self.prénom = prénom
        self.date_de_naissance = date_de_naissance
        self.poids = poids
        self.taille = taille


class babyfile(App):
    def build(self):
        return Baby()


if __name__ == '__main__':
    babyfile().run()
