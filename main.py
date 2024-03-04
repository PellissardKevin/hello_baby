#!/usr/bin/env python3

from kivy.app import App, runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.popup import Popup
from datetime import datetime, timedelta
from date_picker_widget import CalendarPopup
import requests
import bcrypt
from kivy.graphics.texture import Texture

Builder.load_file("Test_Nad/accountfile.kv")
Builder.load_file("Test_Nad/userfile.kv")


class Login(Screen):
    def authenticate(self, email, password):
        url = "http://127.0.0.1:8000/auth/login/"
        data = {"username": email, "password": password}
        response = requests.post(url, data=data)
        if response.status_code == 201 or response.status_code == 200:
            print("Authentification réussie!")
            user_id = requests.get("http://127.0.0.1:8000/user/?expand=email&email=%s" % email).json()[0]['id_user']
            token = response.json()['access']
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get('http://127.0.0.1/user/{user_id}', headers=headers)
        else:
            print("Authentification échouée!")


class Register(Screen):
    def __init__(self, **kwargs):
        super(Register, self).__init__(**kwargs)
        self.setData = CalendarPopup(size_hint=(0.8, 0.6))

    def create(
        self,
        firstname,
        email,
        password,
        lastname=None,
        birthday=None,
        couple=False,
        weight=None,
    ):
        url = "http://127.0.0.1:8000/user/"
        data = {
            "firstname": firstname,
            "email": email,
            "password": password,
            "lastname": lastname,
            "birthday": birthday,
            "couple": couple,
            "weight": weight,
        }
        # response_reg = requests.post("http://127.0.0.1:8000/auth/register/", data={
        #     "first_name": firstname,
        #     "username": email,
        #     "email": email,
        #     "password": password
        # })

        # Generate a salt
        salt = bcrypt.gensalt()
        # converting password to array of bytes
        bytes = password.encode('utf-8')
        # Hash the password
        hashed_password = bcrypt.hashpw(bytes, salt)

        data['password'] = hashed_password
        # response = requests.post(url, data=data)
        # if ((response.status_code == 201 or response.status_code == 200 ) and
        #         (response_reg.status_code == 200 or response_reg.status_code == 201)):
        #     print("Enregistrement réussie!")
        # else:
        #     print("Enregistrement échouée!")

    def createPregnancie(
        self,
        email,
        pregnancie_date,
    ):
        url_preg = "http://127.0.0.1:8000/pregnancie/"
        data = {
            "id_user": '',
            "pregnancy_date": '',
            "amenorhea_date": ''
        }
        user = requests.get("http://127.0.0.1:8000/user/?expand=email&email=%s" % email).json()
        datetime_obj = datetime.strptime(pregnancie_date, '%d/%m/%Y')

        data['id_user'] = 2
        data['pregnancy_date'] = datetime_obj
        data['amenorhea_date'] = datetime_obj + timedelta(weeks=3)

        response = requests.post(url_preg, data=data)
        if response.status_code == 201 or response.status_code == 200:
            print("Enregistrement Grossesse réussie!")
        else:
            print("Enregistrement Grossesse échouée!")

class Main(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(Login(name="login"))
        sm.add_widget(Register(name="register"))

        return sm


if __name__ == "__main__":
    Window.size = (430, 930)
    Main().run()
