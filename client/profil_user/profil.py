#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from client.login.Login import AppState
from datetime import datetime, timedelta
from date_picker_widget import CalendarPopup
import requests
import bcrypt

Window.size = (430, 932)


kivy.require('2.0.0')


class Profil(Screen):
    def __init__(self, **kwargs):
        super(Profil, self).__init__(**kwargs)
        self.setData = CalendarPopup(size_hint=(0.8, 0.6))

    def upgrade_profil(
        self,
        firstname,
        email,
        password,
        lastname=None,
        birthday=None,
        weight=None,
    ):
        url = f"http://127.0.0.1:8000/user/{AppState.user_id}"
        data = {
            "firstname": firstname,
            "email": email,
            "password": password,
            "lastname": lastname,
            "birthday": birthday,
            "weight": weight,
        }
        response_reg = requests.put(f"http://127.0.0.1:8000/auth/update_profile/{AppState.user_id}", data={
            "first_name": firstname,
            "username": email,
            "email": email,
            "password": password
        })

        # Generate a salt
        salt = bcrypt.gensalt()
        # converting password to array of bytes
        bytes = password.encode('utf-8')
        # Hash the password
        hashed_password = bcrypt.hashpw(bytes, salt)

        # Register the user if a birthday is provided
        if birthday:
            data['birthday'] = datetime.strptime(birthday, '%d/%m/%Y').strftime('%Y-%m-%d')

        data['password'] = hashed_password
        data['birthday'] = datetime.strptime(birthday, '%d/%m/%Y').strftime('%Y-%m-%d')
        # send request to the endpoint
        response = requests.put(url, data=data)
        if ((response.status_code == 201 or response.status_code == 200 ) and
                (response_reg.status_code == 200 or response_reg.status_code == 201)):
            print("Mise à jour réussie!")
        else:
            print("Mise à jour échouée!")

    def upgrade_pregnancy(
        self,
        email,
        pregnancie_date,
    ):
        url_preg = "http://127.0.0.1:8000/pregnancie/"
        data = {
            "pregnancy_date": '',
            "amenorhea_date": '',
            "id_user": AppState.user_id
        }
        # get the data of user
        user = requests.get(f"http://127.0.0.1:8000/user/?email={email}").json()

        # save and format date
        datetime_obj = datetime.strptime(pregnancie_date, '%d/%m/%Y')
        amenorhea_format = datetime_obj + timedelta(weeks=3)

        data['pregnancy_date'] = datetime_obj.strftime('%Y-%m-%d')
        data['amenorhea_date'] = amenorhea_format.strftime('%Y-%m-%d')

        # send request to the endpoint
        response = requests.put(url_preg, data=data, headers=AppState.header)
        if response.status_code == 201 or response.status_code == 200:
            print("Mise à jour Grossesse réussie!")
        else:
            print("Mise à jour Grossesse échouée!")


class profilfile(App):
    def build(self):
        return Profil()

if __name__ == '__main__':
    profilfile().run()
