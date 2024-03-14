#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import Graph
from client.login.Login import AppState
import requests


Window.size = (430, 932)


kivy.require('2.0.0')


class Diagrams(Screen):
    def __init__(self, **kwargs):
        super(Diagrams, self).__init__(**kwargs)
        self.graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                           x_ticks_major=25, y_ticks_major=1,
                           y_grid_label=True, x_grid_label=True,
                           padding=5, x_grid=True, y_grid=True,
                           xmin=-0, xmax=100, ymin=-1, ymax=1)
        self.add_widget(self.graph)
        self.update_graph()

    def update_graph(self):
        response = requests.get(f'http://127.0.0.1:8000/biberon/?id_baby={AppState.baby_id}')
        if response.status_code == 200:
            data = response.json().get('donnees', [])
            for entry in data:
                # Ajouter les données au graphique
                graph.add_plot([entry.get('champ1', 0), entry.get('champ2', 0)], color=[1, 0, 0, 1])


class diagramsfile(App):
    def build(self):
        return Diagrams()


if __name__ == '__main__':
    diagramsfile().run()
