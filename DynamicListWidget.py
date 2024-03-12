from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from client.login.Login import AppState
from kivy.uix.button import Button
import requests

class DynamicListWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(DynamicListWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.list_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.list_layout)

        self.load_data_button = Button(text='Charger les données')
        self.load_data_button.bind(on_press=self.load_data)
        self.add_widget(self.load_data_button)

    def load_data(self, instance):
        endpoint_url = f'http://127.0.0.1/baby/?expand=id_user&id_user={AppState.user_id}/'
        response = requests.get(endpoint_url)
        data = response.json()

        for item in data:
            new_button = Button(text=item['firstname'])  # Supposons que 'nom' soit une clé dans vos données
            self.list_layout.add_widget(new_button)

class DynamicListApp(App):
    def build(self):
        return DynamicListWidget()

if __name__ == '__main__':
    DynamicListApp().run()
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
import requests

class DynamicListView(RecycleView):
    def __init__(self, **kwargs):
        super(DynamicListView, self).__init__(**kwargs)
        self.get_data()

    def get_data(self):
        # Appel à l'API Django REST pour récupérer les données
        endpoint_url = f'http://127.0.0.1/baby/?expand=id_user&id_user={AppState.user_id}/'
        response = requests.get(endpoint_url)
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            # Ajouter les données à la vue de recyclage
            self.data = [{'text': str(item)} for item in data]
        else:
            print('Erreur lors de la récupération des données depuis l\'API')

class MyApp(App):
    def build(self):
        return DynamicListView()

if __name__ == '__main__':
    MyApp().run()
