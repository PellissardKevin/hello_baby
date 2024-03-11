#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


Window.size = (430, 932)

kivy.require('2.0.0')

class Home_baby(Screen):
    def __init__(self, **kwargs):
        super(Home_baby, self).__init__(**kwargs)
        self.dropdown = DropDown()
        self.add_dropdown_content()

    def add_dropdown_content(self):
        # Ajoutez du contenu au menu déroulant
        btn1 = Button(text='Profil', size_hint_y=None, height=20, width= 200)
        btn1.bind(on_release=lambda btn: self.on_dropdown_select("profil_user"))
        self.dropdown.add_widget(btn1)

        btn2 = Button(text='User home', size_hint_y=None, height=20, width= 200)
        btn2.bind(on_release=lambda btn: self.on_dropdown_select("home_user"))
        self.dropdown.add_widget(btn2)

        btn3 = Button(text='Profil Bébé', size_hint_y=None, height=20, width= 200)
        btn3.bind(on_release=lambda btn: self.on_dropdown_select("babyprofil"))
        self.dropdown.add_widget(btn3)

    def on_dropdown_select(self, target):
        # Fonction appelée lorsque vous sélectionnez un bouton dans le menu déroulant
        if target == "profil_user":
            self.manager.current = "profil_user"
        elif target == "home_user":
            self.manager.current = "home_user"
        elif target == "babyprofil":
            self.manager.current = "babyprofil"

    def open_dropdown(self, widget):
        # Ouvre le menu déroulant lorsque le bouton est relâché
        self.dropdown.open(widget)


class Profil(Screen):
    pass


class Home_user(Screen):
    pass

class Profil_baby(Screen):
    pass


class babyhome(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Home_baby(name='babyhome'))
        sm.add_widget(Profil(name='profil_user'))
        sm.add_widget(Home_user(name='home_user'))
        sm.add_widget(Profil_baby(name='babyprofil'))
        return sm


if __name__ == '__main__':
    babyhome().run()
