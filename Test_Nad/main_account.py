#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
import requests

Window.size = (430, 932)


kivy.require('2.0.0')


class Login(BoxLayout):
    def authenticate(self, email, password):
        url = 'http://127.0.0.1/login/'

        data = {'email': email, 'password': password}

        response = requests.post(url, data=data)

        if response.status_code == 200:
            print("Authentification réussie!")
        else:
            print("Authentification échouée!")


class accountfile(App):
    def build(self):
        return Login()


if __name__ == '__main__':
    accountfile().run()
