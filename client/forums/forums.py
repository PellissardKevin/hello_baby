#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp


Window.size = (430, 932)


kivy.require('2.0.0')


class Forums(Screen):
    titles = ListProperty([])
    messages = ListProperty([])
    selected_title_index = None

    def __init__(self, **kwargs):
        super(Forums, self).__init__(**kwargs)

    def create_forum(self, title, message):
        self.titles.append(title)
        self.messages.append(message)
        self.update_forum()

    def update_forum(self):
        pass

    def add_comment_to_forum(self, comment):
        if self.selected_title_index is not None:
            # Ajouter le commentaire au message correspondant à l'index
            self.messages[self.selected_title_index] += f"\nCommentaire: {comment}"

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
            # Update the scroll view after adding a new message
            self.update_scrollview()

    def update_scrollview(self):
        # Update the scroll view to reflect the new messages
        self.ids.scroll_view.update_from_scroll()

    def open_comment_popup(self, title):
        content = BoxLayout(orientation='vertical')

        # Récupérer l'index du titre sélectionné
        self.selected_title_index = self.titles.index(title)

        # Récupérer le message correspondant à l'index
        message = self.messages[self.selected_title_index]

        # Calculer la hauteur du texte
        text_height = len(message.split('\n')) * 20  # Supposons que chaque ligne a une hauteur de 20 pixels

        # Afficher le message dans le popup
        message_label = Label(text=message, size_hint_y=None, height=text_height)
        content.add_widget(message_label)

        input_comment = TextInput(hint_text='Votre commentaire')
        content.add_widget(input_comment)
        content.add_widget(Button(text='Ajouter', on_press=lambda instance: self.add_comment_to_forum(input_comment.text)))

        # Calculer la hauteur du contenu total
        total_height = text_height + dp(200)  # dp(200) pour la hauteur du reste du contenu

        popup = Popup(title=f"{title}", content=content, size_hint=(None, None), size=(400, total_height))
        popup.open()

class forumsfile(App):
    def build(self):
        return Forums()


if __name__ == '__main__':
    forumsfile().run()
