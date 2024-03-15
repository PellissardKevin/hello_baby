#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from client.login.Login import AppState
from client.profil_user.profil import Profil
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import requests


Window.size = (430, 932)

kivy.require('2.0.0')

class Home_baby(Screen):
    def __init__(self, **kwargs):
        super(Home_baby, self).__init__(**kwargs)
        self.dropdown = DropDown()

    def fetch_data(self):
        # Clear existing widgets in dropdown
        self.dropdown.clear_widgets()
        # Ajoutez du contenu au menu déroulant
        btn = Button(text='Profil', size_hint_y=None, height=20, width=500)
        btn.bind(on_release=lambda btn: self.on_dropdown_select("profil_user"))
        self.dropdown.add_widget(btn)

        # Django REST endpoint URL
        endpoint_url = f'http://127.0.0.1:8000/baby/?id_user={AppState.user_id}'
        try:
            # Make GET request to the endpoint
            response = requests.get(endpoint_url, headers=AppState.headers)
            response_data = response.json()

            # Create a dynamic list based on the user ID
            if response_data:
                for baby in response_data:
                    # Ajoutez du contenu au menu déroulant
                    name_baby = baby.get('firstname', 'Unknown')
                    btn = Button(text=f'{name_baby}', size_hint_y=None, height=20, width=500)
                    btn.bind(on_release=lambda btn, name=name_baby: self.on_dropdown_select(name))
                    self.dropdown.add_widget(btn)
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
        else:
            baby = requests.get(f'http://127.0.0.1:8000/baby/?firstname={target}', headers=AppState.headers).json()
            AppState.baby_id = baby[0]['id_baby']
            self.manager.current = "babyhome"

    def open_dropdown(self, widget):
        # Ouvre le menu déroulant lorsque le bouton est relâché
        self.fetch_data()  # Appeler fetch_data lorsque le bouton est pressé
        self.dropdown.open(widget)



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
