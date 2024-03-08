#!/usr/bin/env python3

import sys
import os

# Ajoutez le chemin parent de hello_baby au chemin de recherche de Python
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from openai import OpenAI
from hello_baby_api import config


Window.size = (430, 932)


kivy.require('2.0.0')


class Chatbot(Screen):
    def __init__(self, **kwargs):
        super(Chatbot, self).__init__(**kwargs)

    def send_message(self, question):
        # Clé API OpenAI
        OPENAI_API_KEY = config.chat_gpt_key

        # Initialisation du client OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Message de la maman (utilisateur)
        message_maman = question

        # Création de la conversation avec GPT-3.5
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message_maman}
            ]
        )

        # Affichage de la réponse de GPT-3.5
        self.ids.chatbot_response.text = str(completion.choices[0].message
                                             .content)

class chatbotfile(App):
    def build(self):
        return Chatbot()


if __name__ == '__main__':
    chatbotfile().run()
