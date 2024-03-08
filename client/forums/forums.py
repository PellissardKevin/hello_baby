#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


Window.size = (430, 932)


kivy.require('2.0.0')


class Forums(Screen):
    titles = ListProperty([])
    messages = ListProperty([])

    def __init__(self, **kwargs):
        super(Forums, self).__init__(**kwargs)

    def create_forum(self, title, message):
        self.titles.append(title)
        self.messages.append(message)
        self.update_forum()

    def update_forum(self):
        # Clear the current text in the label
        self.ids.forum_case.text = ""
        # Iterate through all messages and display them in the label
        for message in self.messages:
            self.ids.forum_case.text += message + '\n\n'

    def add_comment(self, message_index, comment):
        # Add the comment to the selected message
        self.messages[message_index] += "\nComment: " + comment

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
            self.create_forum(title, message)
            self.popup.dismiss()
            # Update the scroll view after adding a new message
            self.update_scrollview()

    def update_scrollview(self):
        # Update the scroll view to reflect the new messages
        self.ids.scroll_view.update_from_scroll()



class forumsfile(App):
    def build(self):
        return Forums()


if __name__ == '__main__':
    forumsfile().run()
