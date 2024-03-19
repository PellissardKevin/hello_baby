#!/usr/bin/env python3

from kivy.app import App, runTouchApp
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.lang import Builder
from date_picker_widget import CalendarPopup
from client.profil_baby.profil_baby import Profil_baby
from client.profil_user.profil import Profil
from client.home_user.home_user import Home_user
from client.register.Register import Register
from client.login.Login import Login
from client.chatbot.main_chatbot import Chatbot
from client.contact.Contact import Contact
from client.register_baby.register_baby import Baby
from client.home_baby.home_baby import Home_baby
from client.forums.forums import Forums
from client.diagrams.diagrams import Diagrams
from client.diagrams_user.diagramsuser import Diagrams_user
from client.professionnal.professionnal import Professionnal
from client.appointment.appointement import Appointement


Builder.load_file("client/login/loginfile.kv")
Builder.load_file("client/register/registerfile.kv")
Builder.load_file("client/home_user/userhome.kv")
Builder.load_file("client/chatbot/chatbotfile.kv")
Builder.load_file("client/appointment/appointementfile.kv")
Builder.load_file("client/contact/contactfile.kv")
Builder.load_file("client/diagrams/diagramsfile.kv")
Builder.load_file("client/diagrams_user/diagramsuserfile.kv")
Builder.load_file("client/forums/forumsfile.kv")
Builder.load_file("client/home_baby/babyhome.kv")
Builder.load_file("client/register_baby/babyregisterfile.kv")
Builder.load_file("client/professionnal/professionnalfile.kv")
Builder.load_file("client/profil_user/profilfile.kv")
Builder.load_file("client/profil_baby/babyprofil.kv")


class Main(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(Login(name="login"))
        sm.add_widget(Register(name="register"))
        sm.add_widget(Home_user(name="home_user"))
        sm.add_widget(Profil(name="profil_user"))
        sm.add_widget(Chatbot(name="chatbot"))
        sm.add_widget(Home_baby(name="babyhome"))
        sm.add_widget(Profil_baby(name="babyprofil"))
        sm.add_widget(Baby(name="babyregister"))
        sm.add_widget(Forums(name="forums"))
        sm.add_widget(Diagrams(name="diagrams"))
        sm.add_widget(Diagrams_user(name="diagrams_user"))
        sm.add_widget(Appointement(name="appointment"))
        sm.add_widget(Professionnal(name="professionnal"))
        sm.add_widget(Contact(name="contact"))



        return sm


if __name__ == "__main__":
    Window.size = (430, 930)
    Main().run()
