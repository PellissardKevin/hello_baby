#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from datetime import datetime, timedelta
from client.login.Login import AppState
from client.home_user.home_user import Home_user
from date_picker_widget import CalendarPopup
import requests
import bcrypt

Window.size = (430, 932)


kivy.require('2.0.0')


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
        weight=None,
    ):
        url = "http://127.0.0.1:8000/user/"
        data = {
            "firstname": firstname,
            "email": email,
            "password": password,
            "lastname": lastname,
            "weight": weight,
        }
        response_reg = requests.post("http://127.0.0.1:8000/auth/register/", data={
            "first_name": firstname,
            "username": email,
            "email": email,
            "password": password
        })

        # Stocker le poids dans un fichier JSON avec la date
        if weight:
            # Récupérer la date actuelle
            current_date = datetime.now().strftime('%Y-%m-%d')
            weight_data = {'date': current_date, 'weight': weight}

            # Charger les données actuelles du fichier JSON s'il existe
            try:
                with open('weight_history.json', 'r') as json_file:
                    weight_history = json.load(json_file)
            except FileNotFoundError:
                weight_history = []

            # Ajouter le poids actuel aux données d'historique
            weight_history.append(weight_data)

            # Écrire les données mises à jour dans le fichier JSON
            with open('weight_history.json', 'w') as json_file:
                json.dump(weight_history, json_file)

        # Register the user if a birthday is provided
        if birthday:
            data['birthday'] = datetime.strptime(birthday, '%d/%m/%Y').strftime('%Y-%m-%d')

        # Generate a salt
        salt = bcrypt.gensalt()
        # converting password to array of bytes
        bytes = password.encode('utf-8')
        # Hash the password
        hashed_password = bcrypt.hashpw(bytes, salt)

        data['password'] = hashed_password

        # send request to the endpoint
        response = requests.post(url, data=data)
        if ((response.status_code == 201 or response.status_code == 200 ) and
                (response_reg.status_code == 200 or response_reg.status_code == 201)):
            print("Enregistrement réussie!")
        else:
            print("Enregistrement échouée!")

    def createPregnancie(
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
        user = requests.get(f"http://127.0.0.1:8000/user/?email={email}").json()

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

    def clear_input(self):
        # Accéder à l'objet TextInput par son ID et effacer son contenu
        self.ids.firstname.text = ""
        self.ids.lastname.text = ""
        self.ids.birthday.text = ""
        self.ids.email.text = ""
        self.ids.password.text = ""
        self.ids.weight.text = ""


class registerfile(App):
    def build(self):
        return Register()

if __name__ == '__main__':
    registerfile().run()
