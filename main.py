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
from KivyCalendar import CalendarWidget
from datetime import datetime, timedelta
import requests
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
        else:
            print("Authentification échouée!")


class Register(Screen):
        # State labels
    slabel1 = StringProperty()
    slabel2 = StringProperty()

    def savedstate(self):
        # Here we can retrieve user saved radio button state if one exists
        # Assign optional label values
        self.slabel1 = "Oui"
        self.slabel2 = "Non"
        return ["down", "normal"]

    def setDate(self, *args):
        popup = Popup(title='Insert Date', content=CalendarWidget(), size_hint=(.9, .5)).open()
        print(popup)

    def create(
        self,
        firstname,
        email,
        password,
        lastname=None,
        birthday=None,
        couple=savedstate,
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
        response = requests.post(url, data=data)
        if response.status_code == 201 or response.status_code == 200:
            print("Enregistrement réussie!")
        else:
            print("Enregistrement échouée!")

    def createPregnancie(
        self,
        email,
        pregnancie_date=None,
    ):
        url = "http://127.0.0.1:8000/pregnancie/"
        data = {
            "id_user": '',
            "pregnancie_date": pregnancie_date,
            "amenorhea_date": ''
        }
        user = requests.get("http://127.0.0.1:8000/user/", params=email)
        datetime_obj = pregnancie_date
        data['pregnancie_date'] = datetime_obj
        data['amenorhea_date'] = datetime_obj + timedelta(weeks=3)

        response = requests.post(url, data=data)

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
