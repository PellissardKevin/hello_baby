#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen


Window.size = (430, 932)


kivy.require('2.0.0')


class Diagrams(Screen):
    def __init__(self, **kwargs):
        super(Diagrams, self).__init__(**kwargs)


class diagramsfile(App):
    def build(self):
        return Diagrams()


if __name__ == '__main__':
    diagramsfile().run()
