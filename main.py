#!/usr/bin/env python3

from kivy.app import App, runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
import requests
from kivy.graphics.texture import Texture

Builder.load_file('Test_Nad/accountfile.kv')
Builder.load_file('Test_Nad/userfile.kv')


class Login(Screen):
    def authenticate(self, email, password):
        url = 'http://127.0.0.1:8000/api-auth/login/'
        data = {'username': email, 'password': password}
        response = requests.post(url, data=data)
        print(data)
        if response.status_code == 200:
            print("Authentification réussie!")
        else:
            print("Authentification échouée!")

class Register(Screen):
    def create(self, firstname, email, password, lastname=None, birthday=None, couple=None, weight=None):
        url = 'http://127.0.0.1:8000/user/'
        data = {
            "firstname": firstname,
            "email": email,
            "password": password,
            "lastname": lastname,
            "birthday": birthday,
            "couple": couple,
            "weight": weight,
        }
        response = requests.post(url, data=data)
        if response.status_code == 201:
            print("Enregistrement réussie!")
        else:
            print("Enregistrement échouée!")


class Main(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(Login(name='login'))
        sm.add_widget(Register(name='register'))

        return sm


if __name__ == '__main__':
    Window.size=(430,930)
    Main().run()
