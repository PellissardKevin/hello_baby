#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy_garden.mapview import MapView, MapMarker
import googlemaps
from datetime import datetime


import sys
import os

# Ajoutez le chemin parent de hello_baby au chemin de recherche de Python
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from hello_baby_api import config

Window.size = (430, 932)

kivy.require('2.0.0')


class Professionnal(BoxLayout):
    def __init__(self):
        super(Professionnal, self).__init__()


    def search_location(self, query):
        # Utilisez la bibliothèque googlemaps pour effectuer une recherche
        gmaps = googlemaps.Client(key=config.google_maps_key)
        search_results = gmaps.places(query, location=(self.ids.mapview.lat, self.ids.mapview.lon), radius=50000, type='doctor')

        # Affichez les résultats de la recherche sur la carte en mettant à jour le marqueur
        if search_results['results']:
            result = search_results['results'][0]
            location = result['geometry']['location']
            self.marker.lat = location['lat']
            self.marker.lon = location['lng']

class professionnalfile(App):
    def build(self):
        return Professionnal()

if __name__ == '__main__':
    professionnalfile().run()
