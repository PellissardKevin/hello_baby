#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen

Window.size = (430, 932)


kivy.require('2.0.0')


class Contact(Screen):
    pass


class contactfile(App):
    def build(self):
        return Contact()


if __name__ == '__main__':
    contactfile().run()
