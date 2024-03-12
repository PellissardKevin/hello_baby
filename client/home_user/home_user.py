#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from client.login.Login import AppState
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import requests


Window.size = (430, 932)

kivy.require('2.0.0')

class Home_user(Screen):

    def __init__(self, **kwargs):
        super(Home_user, self).__init__(**kwargs)
        self.dropdown = DropDown()
        self.add_dropdown_content()

    def add_dropdown_content(self):

        # Ajoutez du contenu au menu déroulant
        btn = Button(text='Profil', size_hint_y=None, height=20, width=500)
        btn.bind(on_release=lambda btn: self.on_dropdown_select("profil_user"))
        self.dropdown.add_widget(btn)

        # Django REST endpoint URL
        endpoint_url = f'http://127.0.0.1/baby/?expand=id_user&id_user={AppState.user_id}/'
        try:
            # Make GET request to the endpoint
            response = requests.get(endpoint_url)
            response_data = response.json()
            print(response_data)

            # Create a dynamic list based on the user ID
            if response_data is not []:
                for i in range(1, len(response_data)):
                    # Ajoutez du contenu au menu déroulant
                    name_baby = response_data[i]['firstname']
                    btn1 = Button(text=f'{name_baby}', size_hint_y=None, height=20, width=500)
                    btn1.bind(on_release=lambda btn: self.on_dropdown_select("profil_user"))
                    self.dropdown.add_widget(btn1)
            else:
                self.add_widget(Label(text="No user ID found"))
        except Exception as e:
            self.add_widget(Label(text=f"Error: {e}"))



        btnlog = Button(text='Logout', size_hint_y=None, height=20, width=500)
        btnlog.bind(on_release=lambda btn: self.on_dropdown_select("logout"))
        self.dropdown.add_widget(btnlog)

    def on_dropdown_select(self, target):
        # Fonction appelée lorsque vous sélectionnez un bouton dans le menu déroulant
        if target == "profil_user":
            self.manager.current = "profil_user"
        elif target == "logout":
            response = requests.get('http://127.0.0.1:8000/logout/')
            self.manager.current = "login"

    def open_dropdown(self, widget):
        # Ouvre le menu déroulant lorsque le bouton est relâché
        self.dropdown.open(widget)


class Profil(Screen):
    pass


class Home_baby(Screen):
    pass


class userhome(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Home_user(name='home_user'))
        sm.add_widget(Profil(name='profil_user'))
        sm.add_widget(Home_baby(name='babyhome'))
        return sm


if __name__ == '__main__':
    userhome().run()
