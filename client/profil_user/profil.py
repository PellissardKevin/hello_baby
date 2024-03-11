#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
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

    def delete(
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
        response_reg = requests.post("http://127.0.0.1:8000/auth/register/", data={
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

        data['password'] = hashed_password
        data['birthday'] = datetime.strptime(birthday, '%d/%m/%Y').strftime('%Y-%m-%d')
        # send request to the endpoint
        response = requests.post(url, data=data)
        if ((response.status_code == 201 or response.status_code == 200 ) and
                (response_reg.status_code == 200 or response_reg.status_code == 201)):
            print("Enregistrement réussie!")
        else:
            print("Enregistrement échouée!")

    def deletePregnancie(
        self,
        email,
        pregnancie_date,
    ):
        url_preg = "http://127.0.0.1:8000/pregnancie/"
        data = {
            "pregnancy_date": '',
            "amenorhea_date": '',
            "id_user": ''
        }
        # get the data of user
        user = requests.get("http://127.0.0.1:8000/user/?expand=email&email=%s" % email).json()

        # save and format date
        datetime_obj = datetime.strptime(pregnancie_date, '%d/%m/%Y')
        amenorhea_format = datetime_obj + timedelta(weeks=3)

        data['id_user'] = user[0]['id_user']
        data['pregnancy_date'] = datetime_obj.strftime('%Y-%m-%d')
        data['amenorhea_date'] = amenorhea_format.strftime('%Y-%m-%d')

        # send request to the endpoint
        response = requests.post(url_preg, data=data)
        if response.status_code == 201 or response.status_code == 200:
            print("Enregistrement Grossesse réussie!")
        else:
            print("Enregistrement Grossesse échouée!")


class profilfile(App):
    def build(self):
        return Profil()

if __name__ == '__main__':
    profilfile().run()
