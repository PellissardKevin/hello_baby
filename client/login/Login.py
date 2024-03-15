#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
import requests

Window.size = (430, 932)

kivy.require('2.0.0')

class AppState:
    user_id = None
    token = None
    id_forum = None
    id_message = None
    baby_id = None
    header = None


class Login(Screen):
    def authenticate(self, email, password):
        url = "http://127.0.0.1:8000/auth/login/"
        data = {"username": email, "password": password}
        response = requests.post(url, data=data)
        if response.status_code == 201 or response.status_code == 200:
            print("Authentification réussie!")
            user = requests.get(f"http://127.0.0.1:8000/user/?email={email}").json()
            AppState.user_id = user[0]['id_user']
            AppState.token = response.json()['access']
            AppState.headers = {'Authorization': f'Bearer {AppState.token}'}
            baby_list = requests.get(f'http://127.0.0.1:8000/baby/?id_user={AppState.user_id}', headers=AppState.headers).json()
            if baby_list != [] :
                AppState.baby_id = baby_list[0]['id_baby']
                self.manager.current = 'babyhome'
            else:
                response = requests.get(f'http://127.0.0.1:8000/user/{AppState.user_id}/', headers=AppState.headers)
                self.manager.current = 'home_user'
        else:
            print("Authentification échouée!")

    def clear_input(self):
        # Accéder à l'objet TextInput par son ID et effacer son contenu
        self.ids.email.text = ""
        self.ids.password.text = ""

class loginfile(App):
    def build(self):
        return Login()


if __name__ == '__main__':
    loginfile().run()
