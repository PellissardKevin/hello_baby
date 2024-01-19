import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.carousel import Carousel


Window.size = (430, 932)

kivy.require('2.0.0')


class Home_user(BoxLayout):
    def __init__(self, nom='', prénom='', date_de_naissance='%d-%m-%Y',
                 poids=0, début_de_grossesse='%d-%m-%Y', couple=False,
                 email='', mot_de_passe=''):
        super(Home_user, self).__init__()
        self.nom = nom
        self.prénom = prénom
        self.date_de_naissance = date_de_naissance
        self.poids = poids
        self.début_de_grossesse = début_de_grossesse
        self.couple = couple
        self.email = email
        self.mot_de_passe = mot_de_passe


class userhome(App):
    def build(self):
        return Home_user()


if __name__ == '__main__':
    userhome().run()
