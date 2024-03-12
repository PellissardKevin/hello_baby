#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

Window.size = (430, 932)

kivy.require('2.0.0')

class Forums(Screen):
    forums_data = DictProperty({})

    def __init__(self, **kwargs):
        super(Forums, self).__init__(**kwargs)
        self.popups = []

    def create_forum(self, title, message):
        self.forums_data[title] = message
        self.update_forum()

    def update_forum(self):
        # Effacer le contenu précédent dans le GridLayout
        self.ids.scroll_view.clear_widgets()

        # Créer un nouvel GridLayout pour contenir les labels des discussions
        layout = GridLayout(cols=1, size_hint_y=None)

        # Parcourir les titres de discussion et les ajouter au GridLayout
        for title in self.forums_data.keys():
            label = Label(text=title, size_hint_y=None, color=(0, 0, 0, 1), height=dp(50),
                        text_size=(self.width, None), size=(self.width, dp(50)),
                        padding=('10dp', '10dp'), halign='center', valign='middle')
            label.bind(on_touch_up=lambda instance, touch, title=title: self.open_comment_popup(title) if instance.collide_point(*touch.pos) else None)

            layout.add_widget(label)

        # Ajouter le GridLayout contenant les labels à la ScrollView
        self.ids.scroll_view.add_widget(layout)

    def add_comment_to_forum(self, title, comment):
        if title in self.forums_data:
            self.forums_data[title] += f"\nCommentaire: {comment}"

    def open_popup(self):
        content = BoxLayout(orientation='vertical')
        self.input_title = TextInput(hint_text='Titre du message')
        self.input_message = TextInput(hint_text='Votre message')
        content.add_widget(self.input_title)
        content.add_widget(self.input_message)
        content.add_widget(Button(text='Ajouter', on_press=self.add_message))

        self.popup = Popup(title='Créer une discussion', content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def add_message(self, instance):
        title = self.input_title.text
        message = self.input_message.text
        if title and message:
            message_with_comment = f"{message}\n"
            self.create_forum(title, message_with_comment)
            self.popup.dismiss()

    def open_comment_popup(self, title, *args):
        content = BoxLayout(orientation='vertical')

        if title in self.forums_data:
            message = self.forums_data[title]
            text_height = len(message.split('\n')) * 20

            message_label = Label(text=message, size_hint_y=None, height=text_height)
            content.add_widget(message_label)

            input_comment = TextInput(hint_text='Votre commentaire')
            content.add_widget(input_comment)
            content.add_widget(Button(text='Ajouter', on_press=lambda instance: self.add_comment_to_forum(title, input_comment.text)))

            total_height = text_height + dp(200)
            popup = Popup(title=f"{title}", content=content, size_hint=(None, None), size=(400, total_height))
            popup.open()
        else:
            print(f"Le titre '{title}' n'est pas trouvé dans la liste des titres.")





class forumsfile(App):
    def build(self):
        return Forums()


if __name__ == '__main__':
    forumsfile().run()
