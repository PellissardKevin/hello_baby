import kivy
from kivy.core.window import Window
from kivy.app import App
from client.login.Login import AppState
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime, timedelta
from kivy.network.urlrequest import UrlRequest
import requests

Window.size = (430, 932)

kivy.require('2.0.0')

class Home_user(Screen):
    user_firstname = ""

    def __init__(self, **kwargs):
        super(Home_user, self).__init__(**kwargs)
        self.dropdown = DropDown()

    def on_enter(self):
        self.fetch_user_firstname()
        self.update_pregnancy_countdown()

    def fetch_user_firstname(self):
        try:
            UrlRequest(f'http://127.0.0.1:8000/user/?id_user={AppState.user_id}', self.set_user_firstname)
        except Exception as e:
            print(f"Error fetching user firstname: {e}")
            self.user_firstname = 'Unknown'

    def set_user_firstname(self, req, result):
        try:
            self.user_firstname = result[0]['firstname']
            self.ids.user_button.text = self.user_firstname
        except Exception as e:
            print(f"Error setting user firstname: {e}")
            self.user_firstname = 'Unknown'

    def fetch_data(self):
        # Clear existing widgets in dropdown
        self.dropdown.clear_widgets()

        # Ajoutez du contenu au menu déroulant
        btn = Button(text='Profil', size_hint_y=None, height=20, width=700)
        btn.bind(on_release=lambda btn: self.on_dropdown_select("profil_user"))
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
        if target == "profil_user":
            self.manager.current = "profil_user"
        elif target == "logout":
            response = requests.post('http://127.0.0.1:8000/auth/logout/')
            self.manager.current = "login"
        else:
            baby = requests.get(f'http://127.0.0.1:8000/baby/?firstname={target}', headers=AppState.header).json()
            AppState.baby_id = baby[0]['id_baby']
            self.manager.current = "babyhome"

    def open_dropdown(self, widget):
        # Ouvre le menu déroulant lorsque le bouton est relâché
        self.fetch_data() # Appeler fetch_data lorsque le bouton est pressé
        self.dropdown.open(widget)

    def update_pregnancy_countdown(self, due_date=None):
        if due_date:
            pregnancy_countdown = due_date - datetime.now()
            self.ids.pregnancy_info.text = f"Date d'accouchement : {due_date.strftime('%d-%m-%Y')}\n" \
                                        f"Semaines de grossesse : {pregnancy_countdown.days // 7}\n" \
                                        f"Jours restants : {pregnancy_countdown.days % 7}"
        else:
            self.ids.pregnancy_info.text = "Date d'accouchement : Inconnue\n" \
                                        "Semaines de grossesse : Inconnue\n" \
                                        "Jours restants : Inconnu"
                                        

class userhome(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Home_user(name='home_user'))
        sm.add_widget(Home_baby(name='babyhome'))
        return sm

if __name__ == '__main__':
    userhome().run()
