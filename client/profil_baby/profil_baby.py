#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from datetime import datetime, timedelta
from date_picker_widget import CalendarPopup


Window.size = (430, 932)

kivy.require('2.0.0')


class Profil_baby(Screen):
    def __init__(self, **kwargs):
        super(Profil_baby, self).__init__(**kwargs)
        self.setData = CalendarPopup(size_hint=(0.8, 0.6))

    def delete_baby(self, firstname, birthday, lastname=None, size=None, weight=None):
        url = "http://127.0.0.1:8000/baby/"
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "birthday": birthday,
            "size": size,
            "weight": weight,
        }

class babyprofil(App):
    def build(self):
        return Profil_baby()


if __name__ == '__main__':
    babyprofil().run()
