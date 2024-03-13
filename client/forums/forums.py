#!/usr/bin/env python3

import kivy
import requests
from kivy.core.window import Window
from client.login.Login import AppState
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.metrics import dp, sp

Window.size = (430, 932)

kivy.require('2.0.0')

class Forums(Screen):
    forums_data = DictProperty({})

    def __init__(self, **kwargs):
        super(Forums, self).__init__(**kwargs)
        self.popups = []

    def create_forum(self, title, message, user_id):
        # Appel de l'API pour créer la discussion
        url = 'http://127.0.0.1:8000/forum/'
        data = {'title': title, 'id_user': user_id}  # Ajout de l'ID de l'utilisateur
        response = requests.post(url, data=data)
        # Vérifier la réponse
        if response.status_code == 201 or response.status_code == 200:
            print("Discussion créée avec succès!")
            # Ajouter la discussion aux données locales
            self.forums_data[title] = message
            self.update_forum()
        else:
            print("Erreur lors de la création de la discussion:", response.text)

    def update_forum(self):
        # Effacer le contenu précédent dans le GridLayout
        self.ids.scroll_view.clear_widgets()

        # Request pour récupéré l'id du forum
        forums_data = requests.get(f'http://127.0.0.1:8000/forum/?title={title}').json()
        AppState.id_forum = forums_data[0]['id_forums']

        # Créer un nouvel GridLayout pour contenir les labels des discussions
        layout = GridLayout(cols=1, size_hint_y=None)

        # Parcourir les titres de discussion et les ajouter au GridLayout
        for title in self.forums_data.keys():
            label = Label(text=title, size_hint_y=None, color=(0, 0, 0, 1), height=dp(50),
                        text_size=(self.width - 20, None), size=(self.width, dp(50)),
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
            self.create_forum(title, message_with_comment, AppState.user_id)
            self.popup.dismiss()

    def open_comment_popup(self, title, *args):
        content = BoxLayout(orientation='vertical', padding=(5, 5, 5, 5), spacing=5)

        if title in self.forums_data:
            message = self.forums_data[title]
            text_height = len(message.split('\n')) * sp(20)  # Utilisation de sp() pour la hauteur du texte

            # Créer un layout pour le message
            message_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=text_height)
            message_label = Label(text=message, size_hint_y=None, height=text_height,
                                text_size=(self.width - sp(40), None), halign='center', valign='top',
                                padding=(5, 5))
            message_layout.add_widget(message_label)

            # Créer un ScrollView pour contenir le message
            scroll_view = ScrollView()
            scroll_view.add_widget(message_layout)
            content.add_widget(scroll_view)  # Ajout du ScrollView au GridLayout

            # Créer un layout pour les éléments d'entrée de texte et de bouton
            input_layout = BoxLayout(size_hint=(1, None), height=sp(40))
            input_comment = TextInput(hint_text='Votre commentaire')
            input_layout.add_widget(input_comment)
            input_layout.add_widget(Button(text='Ajouter', size_hint=(None, None), size=(100, sp(40)),
                                        on_press=lambda instance: self.add_comment_to_forum(title, input_comment.text)))
            content.add_widget(input_layout)  # Ajout de l'entrée de texte et du bouton au GridLayout

            # Vérifier si l'utilisateur est l'auteur du forum pour afficher le bouton de suppression
            user_id = 1  # Remplacez ceci par l'ID de l'utilisateur actuellement connecté
            forum_id = 1  # Remplacez ceci par l'ID du forum actuellement ouvert
            self.check_and_add_delete_button(content, user_id, forum_id)

            # Réajuster la taille du Popup en fonction de la taille du contenu
            popup_width = min(self.width, sp(400))
            popup_height = min(text_height + sp(200) + sp(40), self.height)
            popup = Popup(title=f"{title}", content=content, size_hint=(None, None), size=(popup_width, popup_height))

            # Définir le défilement vers le haut du ScrollView
            popup.bind(on_open=self.scroll_scrollview_to_top)

            popup.open()
        else:
            print(f"Le titre '{title}' n'est pas trouvé dans la liste des titres.")

    def check_and_add_delete_button(self, content, user_id, forum_id):
        # Vérifier si l'utilisateur est l'auteur du forum pour afficher le bouton de suppression
        url = f'http://127.0.0.1:8000/forum/{forum_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            forum_author_id = response.json().get('author_id')
            if forum_author_id == user_id:
                content.add_widget(Button(text='Supprimer', size_hint=(None, None), size=(100, sp(40)),
                                          on_press=lambda instance: self.delete_forum(forum_id)))
        else:
            print("Erreur lors de la vérification de l'auteur du forum:", response.text)

    def delete_forum(self, title):
        url = f'http://127.0.0.1:8000/forum/{title}/'
        response = requests.delete(url)
        if response.status_code == 204:
            print("Discussion supprimée avec succès!")
            # Supprimer la discussion des données locales
            for title, data in self.forums_data.items():
                if data.get('id') == forum_id:
                    del self.forums_data[title]
                    break
            self.update_forum()
        else:
            print("Erreur lors de la suppression de la discussion:", response.text)

    def scroll_scrollview_to_top(self, instance):
        # Cette fonction sera appelée lorsque le popup sera ouvert
        # Elle assure que le ScrollView défile vers le haut
        instance.content.children[0].scroll_y = 1


class forumsfile(App):
    def build(self):
        return Forums()


if __name__ == '__main__':
    forumsfile().run()
