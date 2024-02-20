#!/usr/bin/env python3

from kivy.app import App, runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.graphics.texture import Texture

Builder.load_file('templates/register.kv')
Builder.load_file('templates/login.kv')

class Login(Screen):
    pass

class Register(Screen):
    pass

class Main(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(Login(name='login'))
        sm.add_widget(Register(name='register'))

        return sm


if __name__ == '__main__':
    Window.size=(430,930)
    Main().run()
