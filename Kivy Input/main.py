from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
Window.size = (400, 600) #Tamanho da Tela
Window.clearcolor = (1,1,1,1) #Fundo da Tela

# Telas
class TelaMenu(Screen):
    pass

class TelaConsulta(Screen):
    pass

# Gerenciador das Telas
Gerenciador = ScreenManager()
Gerenciador.add_widget(TelaMenu(name='TelaMenu'))
Gerenciador.add_widget(TelaConsulta(name='TelaConsulta'))

class App(App):
    def build(self):
        self.title = 'ePoggio | Consulta Saldos'
        Telas = Builder.load_file('MyApp.kv')
        return Telas

App().run()