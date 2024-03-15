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
        response = requests.post(url, data=data, headers=AppState.header)
        # Vérifier la réponse
        if response.status_code == 201 or response.status_code == 200:
            print("Discussion créée avec succès!")
            forum_data = response.json()
            forum_id = forum_data['id_forums']  # Récupérer l'ID du forum créé

            # Maintenant, envoyons le message à la base de données
            message_url = f'http://127.0.0.1:8000/message/?id_forums={AppState.id_forum}'
            message_data = {'id_forum': forum_id, 'id_user': user_id, 'text_message': message}
            message_response = requests.post(message_url, data=message_data, headers=AppState.header)

            if message_response.status_code == 201 or message_response.status_code == 200:
                print("Message ajouté avec succès!")
            else:
                print("Erreur lors de l'ajout du message:", message_response.text)

            # Ajouter la discussion aux données locales
            self.forums_data[title] = message
            self.update_forum(title)
        else:
            print("Erreur lors de la création de la discussion:", response.text)

    def update_forum(self, title):
        # Clear the previous content in the GridLayout
        self.ids.scroll_view.clear_widgets()

        # Request to get all discussions
        forum_response = requests.get('http://127.0.0.1:8000/forum/', headers=AppState.header)
        if forum_response.status_code == 200 or forum_response.status_code == 201:
            forum_data = forum_response.json()
            if forum_data:
                # Create a new GridLayout to hold all forum labels
                layout = GridLayout(cols=1, size_hint_y=None)

                for forums_item in forum_data:
                    title = forums_item['title']
                    AppState.id_forum = forums_item['id_forums']

                    # Request to get the id of the messages
                    message_response = requests.get(f'http://127.0.0.1:8000/message/?id_forums={AppState.id_forum}', headers=AppState.header)
                    if message_response.status_code == 200 or message_response.status_code == 201:
                        message_data = message_response.json()
                        if message_data:  # Check if message_data is empty or not
                            AppState.id_message = message_data[0]['id_message']

                    # Create a new GridLayout for each discussion
                    forum_layout = GridLayout(cols=1, size_hint_y=None)

                    # Add the title of each discussion to the GridLayout
                    label = Label(text=title, size_hint_y=None, color=(0, 0, 0, 1), height=dp(50),
                                text_size=(self.width - 20, None), size=(self.width, dp(50)),
                                padding=('10dp', '10dp'), halign='center', valign='middle')
                    label.bind(on_touch_up=lambda instance, touch, title=title: self.open_comment_popup(title) if instance.collide_point(*touch.pos) else None)

                    forum_layout.add_widget(label)

                    # Add the GridLayout for each discussion to the main GridLayout
                    layout.add_widget(forum_layout)

                # Add the main GridLayout to the ScrollView
                self.ids.scroll_view.add_widget(layout)
            else:
                print("Erreur lors de la récupération des discussions:", forum_response.text)

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
            user_id = AppState.user_id
            forum_id = AppState.id_forum
            self.check_and_add_delete_button(content, forum_id, title)

            # Réajuster la taille du Popup en fonction de la taille du contenu
            popup_width = min(self.width, sp(400))
            popup_height = min(text_height + sp(200) + sp(40), self.height)
            popup = Popup(title=f"{title}", content=content, size_hint=(None, None), size=(popup_width, popup_height))

            # Définir le défilement vers le haut du ScrollView
            popup.bind(on_open=self.scroll_scrollview_to_top)

            popup.open()
        else:
            print(f"Le titre '{title}' n'est pas trouvé dans la liste des titres.")

    def check_and_add_delete_button(self, content, forum_id, title):
        # Vérifier si l'utilisateur est l'auteur du forum pour afficher le bouton de suppression
        url = f'http://127.0.0.1:8000/forum/{forum_id}/'
        response = requests.get(url, headers=AppState.header)
        if response.status_code == 200 or response.status_code == 201:
            forum_data = response.json()
            forum_author_id = forum_data['id_user']

            if forum_author_id == AppState.user_id:
                delete_button = Button(text='Supprimer', size_hint=(None, None), size=(100, sp(40)))
                delete_button.bind(on_press=lambda instance: self.delete_forum(AppState.id_forum, title))
                content.add_widget(delete_button)
        else:
            print("Erreur lors de la vérification de l'auteur du forum:", response.text)

    def delete_forum(self, forum_id, title):
        url = f'http://127.0.0.1:8000/forum/{forum_id}/'
        response = requests.delete(url, headers=AppState.header)
        if response.status_code == 204:
            print("Discussion supprimée avec succès!")
            # Supprimer la discussion des données locales
            del self.forums_data[title]
            # Réorganiser l'affichage pour refléter la suppression de la discussion
            self.update_forum_list()
        else:
            print("Erreur lors de la suppression de la discussion:", response.text)

    def update_forum_list(self):
        # Effacer le contenu précédent dans le GridLayout
        self.ids.scroll_view.clear_widgets()

        # Créer un nouvel GridLayout pour contenir les labels des discussions
        layout = GridLayout(cols=1, size_hint_y=None)

        # Parcourir les titres de discussion et les ajouter au GridLayout
        for title in self.forums_data.keys():
            label = Label(text=title, size_hint_y=None, color=(0, 0, 0, 1), height=dp(50),
                        text_size=(self.width - 20, None), size=(self.width, dp(50)),
                        padding=('10dp', '10dp'), halign='center', valign='middle')
            label.bind(on_touch_up=lambda instance, touch, title=title: self.open_comment_popup(title) if
            instance.collide_point(*touch.pos) else None)

            layout.add_widget(label)

        # Ajouter le GridLayout contenant les labels à la ScrollView
        self.ids.scroll_view.add_widget(layout)

    def scroll_scrollview_to_top(self, instance):
        # Cette fonction sera appelée lorsque le popup sera ouvert
        # Elle assure que le ScrollView défile vers le haut
        instance.content.children[0].scroll_y = 1


class forumsfile(App):
    def build(self):
        return Forums()


if __name__ == '__main__':
    forumsfile().run()
