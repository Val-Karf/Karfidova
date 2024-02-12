from kivy.config import Config
Config.set('graphics', 'resizable', True)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
import requests

class FilmCard(BoxLayout):
    def __init__(self, film, **kwargs):
        super(FilmCard, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10

        self.title_label = Label(text=film['nameRu'], size_hint=(None, 1),  height=30, width=200)
        self.add_widget(self.title_label)

        self.poster_image = AsyncImage(source=film['posterUrl'], size_hint=(None, 1), height=200, width=200)
        self.add_widget(self.poster_image)

        self.year_label = Label(text=str(film['year']), size_hint=(None, 1), height=200, width=200)
        self.add_widget(self.year_label)

        #self.description_label = Label(text=str(film['description']), size_hint=(None, 1), height=400, width=200, valign='top', halign='center', text_size=(200, None))
        #self.add_widget(self.description_label)

        self.film = film

        self.bind(on_release=self.open_film_details)

    def open_film_details(self, *args):
        film_id = self.film['filmId']
        response = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}", headers={"X-API-KEY": "e30ffed0-76ab-4dd6-b41f-4c9da2b2735b"})
        if response.status_code == 200:
            #film_details = response.json()
            screen_manager.current = 'film_details'
            #film_details_screen.load_film_details(film_details)
        else:
            print(f"Error getting film details for filmId: {film_id}")
'''
class FilmDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super(FilmDetailsScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.poster_image = AsyncImage(size_hint=(None, None), height=400, width=200)
        self.add_widget(self.poster_image)

        self.description_label = Label(size_hint=(1, None), height=400, width=200)
        self.add_widget(self.description_label)

        self.genre_label = Label(size_hint=(1, None), height=30, width=200)
        self.add_widget(self.genre_label)

        self.country_label = Label(size_hint=(1, None), height=30, width=200)
        self.add_widget(self.country_label)

    def load_film_details(self, film_details):
        self.poster_image.source = film_details['data']['posterUrl']
        self.description_label.text = film_details['data']['description']
        self.genre_label.text = f"Genre: {', '.join(film_details['data']['genres'])}"
        self.country_label.text = f"Production Country: {', '.join(film_details['data']['countries'])}"
'''
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.scrollview = ScrollView(size_hint=(1, None), height=700, width=400)
        self.add_widget(self.scrollview)

        self.films_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=700, width=400)
        self.scrollview.add_widget(self.films_layout)

        self.load_popular_films()

    def load_popular_films(self):
        url = "https://kinopoiskapiunofficial.tech/api/v2.2/films/top"
        headers = {
            "X-API-KEY": "e30ffed0-76ab-4dd6-b41f-4c9da2b2735b"
        }
        params = {
            "type": "TOP_100_POPULAR_FILMS"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            films = response.json()['films']
            self.display_films(films)
        else:
            print("Error getting list of popular films")

    def display_films(self, films):
        for film in films:
            film_card = FilmCard(film)
            self.films_layout.add_widget(film_card)

screen_manager = ScreenManager()

main_screen = MainScreen(name='main', size_hint=(1, None), height=700, width = 400)
screen_manager.add_widget(main_screen)

#film_details_screen = FilmDetailsScreen(name='film_details', size_hint=(1, None), height=700, width = 400)
#screen_manager.add_widget(film_details_screen)

class FilmApp(App):
    def build(self):
        return screen_manager
        
if __name__ == '__main__':
    FilmApp().run()