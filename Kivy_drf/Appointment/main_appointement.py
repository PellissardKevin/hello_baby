#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


Window.size = (430, 932)


kivy.require('2.0.0')


class Appointement(BoxLayout):
    def __init__(self):
        super(Appointement, self).__init__()


class appointementfile(App):
    def build(self):
        return Appointement()


if __name__ == '__main__':
    appointementfile().run()
