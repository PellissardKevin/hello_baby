#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen


Window.size = (430, 932)

kivy.require('2.0.0')


class Baby(Screen):
    def __init__(self, **kwargs):
        super(Baby, self).__init__(**kwargs)


class babyregisterfile(App):
    def build(self):
        return Baby()


if __name__ == '__main__':
    babyregisterfile().run()
