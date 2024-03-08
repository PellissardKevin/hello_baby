#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
import requests

Window.size = (430, 932)

kivy.require('2.0.0')


class Login(Screen):
    def authenticate(self, email, password):
        url = "http://127.0.0.1:8000/auth/login/"
        data = {"username": email, "password": password}
        response = requests.post(url, data=data)
        if response.status_code == 201 or response.status_code == 200:
            print("Authentification réussie!")
            user = requests.get(f"http://127.0.0.1:8000/user/?expand=email&email={email}").json()
            user_id = user[0]['id_user']
            token = response.json()['access']
            headers = {'Authorization': f'Bearer {token}'}
            if requests.get(f'http://127.0.0.1:8000/baby/?expand=id_user&id_user={user_id}', headers=headers).json() != [] :
                self.manager.current = 'babyhome'
            else:
                response = requests.get(f'http://127.0.0.1:8000/user/{user_id}', headers=headers)
                self.manager.current = 'home_user'
        else:
            print("Authentification échouée!")

class loginfile(App):
    def build(self):
        return Login()


if __name__ == '__main__':
    loginfile().run()
