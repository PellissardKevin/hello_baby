#!/usr/bin/env python3

import kivy
import requests
import time
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.garden.graph import Graph, MeshLinePlot
from client.login.Login import AppState


Window.size = (430, 932)


kivy.require('2.0.0')


class Diagrams(Screen):
    def __init__(self, **kwargs):
        super(Diagrams, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # Définir la taille du graphique
        graph_size = (Window.width * 0.9, Window.height * 0.8)

        # Créer le graphique
        self.graph = Graph(xlabel='Time', ylabel='Value', size=graph_size)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.graph.add_plot(self.plot)
        self.layout.add_widget(self.graph)

        self.add_widget(self.layout)

        # Appeler la méthode pour mettre à jour le graphique
        self.on_enter()

    def on_enter(self):
        Clock.schedule_interval(self.update_graph, 5)  # Mettre à jour le graphique toutes les 5 secondes

    def update_graph(self, dt):
        # Fonction pour mettre à jour le graphique avec les données de l'API
        try:
            response = requests.get(f'http://127.0.0.1:8000/biberon/?id_baby={AppState.baby_id}', headers=AppState.header)
            if response.status_code == 200:
                data = response.json()
                x_values = []  # Liste pour stocker les valeurs de l'axe X
                y_values = []  # Liste pour stocker les valeurs de l'axe Y
                for entry in data:
                    # Ajouter les données au graphique
                    x_values.append(entry['date_biberon'])  # Ajouter les dates en tant que valeurs X
                    y_values.append(entry['quantity'])      # Ajouter les quantités en tant que valeurs Y

                # Mettre à jour le graphique
                self.plot.points = zip(x_values, y_values)

        except Exception as e:
            print("Erreur lors de la récupération des données:", e)


class MyScreenManager(ScreenManager):
    pass

class diagramsfile(App):
    def build(self):
        # Créer une instance de GraphScreen
        graph_screen = Diagrams(name='graph_screen')

        # Ajouter GraphScreen au ScreenManager
        sm = MyScreenManager()
        sm.add_widget(graph_screen)

        return sm


if __name__ == '__main__':
    diagramsfile().run()
