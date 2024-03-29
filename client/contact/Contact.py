#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from client.login.Login import AppState
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

Window.size = (430, 932)


kivy.require('2.0.0')


class Contact(Screen):
    def send(self):
        # Récupérer le contenu des champs de texte
        objet = self.ids.objet_input.text
        description = self.ids.description_input.text

        receiver_email = 'notre email@gmail.com'  # Adresse e-mail du destinataire
        sujet = objet
        corps = description

        # Créer un conteneur de message
        msg = MIMEMultipart()
        msg['To'] = receiver_email
        msg['Subject'] = sujet

        # Attacher le corps du message
        msg.attach(MIMEText(corps, 'plain'))

        # Se connecter au serveur SMTP
        serveur = smtplib.SMTP('smtp.gmail.com', 587)
        serveur.starttls()


        # Envoyer l'email
        texte = msg.as_string()
        serveur.sendmail(receiver_email, texte)

        # Fermer la connexion au serveur SMTP
        serveur.quit()


class contactfile(App):
    def build(self):
        return Contact()


if __name__ == '__main__':
    contactfile().run()
