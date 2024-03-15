#!/usr/bin/env python3

import kivy
import requests
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from datetime import datetime, timedelta
from date_picker_widget import CalendarPopup
from client.login.Login import AppState


Window.size = (430, 932)

kivy.require('2.0.0')


class Baby(Screen):
    def __init__(self, **kwargs):
        super(Baby, self).__init__(**kwargs)
        self.setData = CalendarPopup(size_hint=(0.8, 0.6))

    def create_baby(self, firstname, birthday, lastname=None, size=0, weight=0):
        url = "http://127.0.0.1:8000/baby/"
        data = {
            "id_user": AppState.user_id,
            "firstname": firstname,
            "lastname": lastname,
            "birthday": birthday,
            "size": size,
            "weight": weight,
        }
        # send request to the endpoint
        birthday_obj = datetime.strptime(birthday, '%d/%m/%Y')
        data['birthday'] = birthday_obj.strftime('%Y-%m-%d')

        response = requests.post(url, data=data, headers=AppState.header)
        if response.status_code == 201 or response.status_code == 200:
            print("Enregistrement Bébé réussie!")
        else:
            print("Enregistrement Bébé échouée!")

    def clear_input(self):
        # Accéder à l'objet TextInput par son ID et effacer son contenu
        self.ids.firstname.text = ""
        self.ids.lastname.text = ""
        self.ids.birthday.text = ""
        self.ids.size_baby.text = ""
        self.ids.weight.text = ""

class babyregisterfile(App):
    def build(self):
        return Baby()


if __name__ == '__main__':
    babyregisterfile().run()
