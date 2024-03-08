#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.carousel import Carousel


Window.size = (430, 932)

kivy.require('2.0.0')

class Home_user(Screen):
    def __init__(self, **kwargs):
        super(Home_user, self).__init__(**kwargs)


class userhome(App):
    def build(self):
        return Home_user()


if __name__ == '__main__':
    userhome().run()
