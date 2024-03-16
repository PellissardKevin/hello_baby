#!/usr/bin/env python3

import kivy
import requests
from datetime import datetime
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import plotly.graph_objects as go
from kivy.uix.label import Label
import io
from PIL import Image as PILImage
import plotly.graph_objects as go
from kivy.uix.image import Image
from client.login.Login import AppState
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp

Window.size = (430, 932)

kivy.require('2.0.0')


class Diagrams(Screen):
    def __init__(self, **kwargs):
        super(Diagrams, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # Create the Plotly widget
        self.plotly_widget = PlotlyWidget()
        self.layout.add_widget(self.plotly_widget)
        self.add_widget(self.layout)

        self.popup = None

        # Call the method to update the plot
        self.on_enter()

    def on_enter(self):
        self.update_graph()

    def update_graph(self, dt=None):
        try:
            response = requests.get(f'http://127.0.0.1:8000/biberon/?id_baby={AppState.baby_id}', headers=AppState.header)
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                x_values = []
                y_values = []
                for entry in data:
                    date_biberon = datetime.strptime(entry['date_biberon'], '%Y-%m-%dT%H:%M:%SZ')
                    x_values.append(date_biberon)
                    y_values.append(float(entry['quantity']))

                self.plotly_widget.update_plot(x_values, y_values)

        except Exception as e:
            print("Error fetching data:", e)

    def get_data_from_response(self, data):
        x_values = []
        y_values = []
        for entry in data:
            date_biberon = datetime.strptime(entry['date_biberon'], '%Y-%m-%dT%H:%M:%SZ')
            x_values.append(date_biberon)
            y_values.append(float(entry['quantity']))
        return x_values, y_values

    def enter_data_bib(self):
        content = BoxLayout(orientation='vertical')
        quantity_input = TextInput(hint_text='Quantité en ml', multiline=True)
        add_button = Button(text='Ajouter', size_hint_y=None, height=dp(50))
        add_button.bind(on_release=lambda btn: self.add_quantity(quantity_input.text))
        content.add_widget(quantity_input)
        content.add_widget(add_button)

        self.popup = Popup(title='Ajouter un biberon', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def add_quantity(self, quantity):
        try:
            quantity = float(quantity)
            if quantity <= 0:
                print("Veuillez entrer une quantité positive.")
                return

            data = {
                "id_baby": AppState.baby_id,
                "quantity": quantity,
                "date_biberon": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            }

            response = requests.post('http://127.0.0.1:8000/biberon/', headers=AppState.header, data=data)
            if response.status_code == 201 or response.status_code == 200:
                print("Biberon ajouté avec succès!")
                self.update_graph()
            else:
                print("Erreur lors de l'ajout du biberon:", response.status_code)
            if self.popup:
                self.popup.dismiss()
                self.popup = None
        except ValueError:
            print("Veuillez entrer une quantité valide.")


class PlotlyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(PlotlyWidget, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.plotly_figure = go.Figure()

    def update_plot(self, x_values, y_values):
        # Remove previous traces from the figure
        self.plotly_figure.data = []

        # Add new trace with updated data
        self.plotly_figure.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers'))

        # Convert Plotly figure to PIL image
        buf = io.BytesIO()
        self.plotly_figure.write_image(buf, format='png')
        buf.seek(0)
        pil_image = PILImage.open(buf)
        pil_image.save('plotly_graph.png')  # Save the image temporarily

        # Display the image using Kivy Image widget
        self.clear_widgets()  # Remove previous image
        self.add_widget(Image(source='plotly_graph.png', allow_stretch=True))


class MyScreenManager(ScreenManager):
    pass


class diagramsfile(App):
    def build(self):
        # Create an instance of PlotlyDiagrams
        plotly_diagrams_screen = Diagrams(name='plotly_diagrams_screen')

        # Add PlotlyDiagrams to the ScreenManager
        sm = MyScreenManager()
        sm.add_widget(plotly_diagrams_screen)

        return sm


if __name__ == '__main__':
    diagramsfile().run()
