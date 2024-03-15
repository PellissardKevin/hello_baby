#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import Graph, MeshLinePlot
from client.login.Login import AppState
import requests


Window.size = (430, 932)


kivy.require('2.0.0')


class Diagrams(Screen):
    def __init__(self, **kwargs):
        super(Diagrams, self).__init__(**kwargs)

        # Définir la taille du graphique
        graph_size = (Window.width * 0.9, Window.height * 0.8)

        self.graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                           x_ticks_major=25, y_ticks_major=100,
                           y_grid_label=True, x_grid_label=True,
                           padding=5, x_grid=True, y_grid=True,
                           size_hint=(1, 1))

        self.graph.bind(size=self._update_graph_size)

        # Ajout du layout contenant le graphique à l'ID 'graph_layout'
        self.ids.graph_layout.add_widget(self.graph)

        # Appeler la méthode pour mettre à jour le graphique
        self.on_enter()

    def on_enter(self):
        self.update_graph()

    def _update_graph_size(self, instance, value):
        self.graph.xmax = value[0]  # Mettre à jour xmax avec la largeur du graphique
        self.graph.ymax = 1000  # Définir ymax sur 1000 ou toute autre valeur appropriée pour l'axe Y

    def update_graph(self):
        response = requests.get(f'http://127.0.0.1:8000/biberon/?id_baby={AppState.baby_id}', headers=AppState.header)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                # Ajouter les données au graphique
                plot = MeshLinePlot(color=[1, 0, 0, 1])
                plot.points = [(entry['quantity'], entry['nb_biberon'])]
                self.graph.add_plot(plot)

class diagramsfile(App):
    def build(self):
        return Diagrams()


if __name__ == '__main__':
    diagramsfile().run()
