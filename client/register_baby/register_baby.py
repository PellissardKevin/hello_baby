#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from datetime import datetime, timedelta
from date_picker_widget import CalendarPopup


Window.size = (430, 932)

kivy.require('2.0.0')


class Baby(Screen):
    def __init__(self, **kwargs):
        super(Baby, self).__init__(**kwargs)
        self.setData = CalendarPopup(size_hint=(0.8, 0.6))

    def create_baby(self, firstname, birthday, lastname=None, size=None, weight=None):
        url = "http://127.0.0.1:8000/baby/"
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "birthday": birthday,
            "size": size,
            "weight": weight,
        }

    def create_new_baby(self, firstname, birthday, lastname=None, size=None, weight=None):
        url = "http://127.0.0.1:8000/baby/"
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "birthday": birthday,
            "size": size,
            "weight": weight,
        }

class babyregisterfile(App):
    def build(self):
        return Baby()


if __name__ == '__main__':
    babyregisterfile().run()
