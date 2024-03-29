#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

Window.size = (430, 932)

kivy.require('2.0.0')

class AppState:
    user_id = None
    token = None
    refresh_token = None
    id_forum = None
    id_message = None
    baby_id = None
    header = None


class PasswordResetPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Réinitialisation du mot de passe"
        self.size_hint = (None, None)
        self.size = (400, 300)

        layout = GridLayout(cols=2)
        layout.add_widget(Label(text="Email :"))
        self.email_input = TextInput(multiline=False)
        layout.add_widget(self.email_input)

        layout.add_widget(Label(text="Nouveau mot de passe :"))
        self.new_password_input = TextInput(multiline=False, password=True)
        layout.add_widget(self.new_password_input)

        layout.add_widget(Label(text="Confirmer le mot de passe :"))
        self.confirm_password_input = TextInput(multiline=False, password=True)
        layout.add_widget(self.confirm_password_input)

        self.error_label = Label(text="", color=(1, 0, 0, 1))
        layout.add_widget(self.error_label)

        layout.add_widget(Button(text="Réinitialiser", on_press=self.reset_password))

        self.content = layout

    def reset_password(self, instance):
        email = self.email_input.text
        new_password = self.new_password_input.text
        confirm_password = self.confirm_password_input.text

        if not email or not new_password or not confirm_password:
            self.error_label.text = "Veuillez remplir tous les champs."
            return

        if new_password != confirm_password:
            self.error_label.text = "Les mots de passe ne correspondent pas."
            return

        data = {"email": email, "new_password": new_password}
        response_auth = requests.post("http://127.0.0.1:8000/auth/reset_password/", data=data)
        response_reviews = requests.post("http://127.0.0.1:8000/reset_password/", data=data)

        if (response_auth.status_code == 200 or response_auth.status_code == 201) and \
            (response_reviews.status_code == 200 or response_reviews.status_code == 201):
            self.error_label.text = "Mot de passe réinitialisé avec succès."
        else:
            self.error_label.text = "Erreur lors de la réinitialisation du mot de passe."

        self.dismiss()


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
            AppState.refresh_token = response.json()['refresh']
            AppState.header = {'Authorization': f'Bearer {AppState.token}'}
            baby_list = requests.get(f'http://127.0.0.1:8000/baby/?id_user={AppState.user_id}', headers=AppState.header).json()
            if baby_list != [] :
                AppState.baby_id = baby_list[0]['id_baby']
                self.manager.current = 'babyhome'
            else:
                response = requests.get(f'http://127.0.0.1:8000/user/{AppState.user_id}/', headers=AppState.header)
                self.manager.current = 'home_user'
        else:
            print("Authentification échouée!")

    def clear_input(self):
        # Accéder à l'objet TextInput par son ID et effacer son contenu
        self.ids.email.text = ""
        self.ids.password.text = ""

    def password_forgotten(self):
        popup = PasswordResetPopup()
        popup.open()


class loginfile(App):
    def build(self):
        return Login()


if __name__ == '__main__':
    loginfile().run()
