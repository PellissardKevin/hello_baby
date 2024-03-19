#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from client.login.Login import AppState
from client.profil_user.profil import Profil
from kivy.uix.dropdown import DropDown
from datetime import timedelta, datetime
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
import requests


Window.size = (430, 932)

kivy.require('2.0.0')

class Home_baby(Screen):
    baby_firstname = ""

    def __init__(self, **kwargs):
        super(Home_baby, self).__init__(**kwargs)
        self.dropdown = DropDown()

    def on_enter(self):
        self.fetch_baby_firstname()

    def fetch_baby_firstname(self):
        try:
            response = requests.get(f'http://127.0.0.1:8000/baby/?id_baby={AppState.baby_id}', headers=AppState.header)
            response_data = response.json()
            self.birthday_baby(response_data[0]['birthday'], response_data[0]['firstname'])
            self.set_baby_firstname(response_data)
        except Exception as e:
            print(f"Error fetching baby firstname: {e}")
            self.baby_firstname = 'Unknown'

    def set_baby_firstname(self, result):
        try:
            new_firstname = result[0]['firstname']
            if new_firstname != self.baby_firstname:  # Vérifier si le nom du bébé a changé
                self.baby_firstname = new_firstname
                self.ids.baby_button.text = self.baby_firstname
                self.fetch_baby_firstname()  # Appel pour mettre à jour le nom du bébé uniquement si nécessaire
        except Exception as e:
            print(f"Error setting baby firstname: {e}")
            self.baby_firstname = 'Unknown'


    def fetch_babies(self):
        # Clear existing widgets in dropdown
        self.dropdown.clear_widgets()
        # Ajoutez du contenu au menu déroulant
        btn = Button(text='Profil', size_hint_y=None, height=20, width=700)
        btn.bind(on_release=lambda btn: self.on_dropdown_select("profil_baby"))
        self.dropdown.add_widget(btn)

        # Django REST endpoint URL
        endpoint_url = f'http://127.0.0.1:8000/baby/?id_user={AppState.user_id}'
        try:
            # Make GET request to the endpoint
            response = requests.get(endpoint_url, headers=AppState.header)
            response_data = response.json()

            # Create a dynamic list based on the user ID
            if response_data:
                for baby in response_data:
                    # Ajoutez du contenu au menu déroulant
                    name_baby = baby.get('firstname', 'Unknown')
                    btn = Button(text=f'{name_baby}', size_hint_y=None, height=20, width=700)
                    btn.bind(on_release=lambda btn, name=name_baby: self.on_dropdown_select(name))
                    self.dropdown.add_widget(btn)
        except Exception as e:
            self.add_widget(Label(text=f"Error: {e}"))

        btnlog = Button(text='Logout', size_hint_y=None, height=20, width=700)
        btnlog.bind(on_release=lambda btn: self.on_dropdown_select("logout"))
        self.dropdown.add_widget(btnlog)

    def on_dropdown_select(self, target):
        # Fonction appelée lorsque vous sélectionnez un bouton dans le menu déroulant
        if target == "profil_baby":
            self.manager.current = "babyprofil"
        elif target == "logout":
            response = requests.post('http://127.0.0.1:8000/auth/logout/', data={"refresh_token": AppState.refresh_token}, headers=AppState.header)
            self.manager.current = "login"
        else:
            baby = requests.get(f'http://127.0.0.1:8000/baby/?firstname={target}', headers=AppState.header).json()
            AppState.baby_id = baby[0]['id_baby']
            self.fetch_baby_firstname()
            self.manager.current = "babyhome"

        # Fermer le menu déroulant
        self.dropdown.dismiss()

    def open_dropdown(self, widget):
        # Ouvre le menu déroulant lorsque le bouton est relâché
        self.fetch_babies()  # Appeler fetch_data lorsque le bouton est pressé
        self.dropdown.open(widget)

    def birthday_baby(self, due_date_str, firstname):
        try:
            # Convertir la chaîne de date en objet datetime
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')

            # Calcul de l'âge de l'enfant en semaines
            age_in_weeks = (datetime.now() - due_date).days // 7

            # Calcul de l'âge de l'enfant en mois
            age_in_months = age_in_weeks // 4  # En supposant qu'un mois a 4 semaines

            # Calcul des jours restants jusqu'à l'anniversaire
            next_birthday = due_date.replace(year=datetime.now().year)

            if next_birthday < datetime.now():
                next_birthday = next_birthday.replace(year=datetime.now().year + 1)
            days_until_next_birthday = (next_birthday - datetime.now()).days

            self.ids.baby_info.text = f"{firstname} est agé(e) de {age_in_weeks} semaines\n" \
                                        f"ou {age_in_months} mois\n" \
                                        f"Son prochain anniversaire est dans {days_until_next_birthday} jours"
        except Exception as e:
            # Gérer l'exception appropriée selon vos besoins
            print(f"Une erreur s'est produite : {e}")


class babyhome(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Home_baby(name='babyhome'))
        sm.add_widget(Profil(name='profil_user'))
        sm.add_widget(Home_user(name='home_user'))
        sm.add_widget(Profil_baby(name='babyprofil'))
        return sm


if __name__ == '__main__':
    babyhome().run()
