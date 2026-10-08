import customtkinter as ctk
import requests
import random
import webbrowser
from datetime import datetime
from urllib.parse import quote

from PIL import Image
from io import BytesIO


API_URL = "https://www.freetogame.com/api"


class Game:

    def __init__(
        self,
        name,
        description,
        genre,
        platform,
        developer,
        publisher,
        release_date,
        image_url
    ):
        self.name = name
        self.description = description
        self.genre = genre
        self.platform = platform
        self.developer = developer
        self.publisher = publisher
        self.release_date = release_date
        self.image_url = image_url

    @classmethod
    def from_api(cls, data):

        return cls(
            name=data.get("title", "Невідомо"),
            description=data.get(
                "short_description",
                "Опис відсутній."
            ),
            genre=data.get(
                "genre",
                "Невідомо"
            ),
            platform=data.get(
                "platform",
                "Невідомо"
            ),
            developer=data.get(
                "developer",
                "Невідомо"
            ),
            publisher=data.get(
                "publisher",
                "Невідомо"
            ),
            release_date=data.get(
                "release_date",
                "Невідомо"
            ),
            image_url=data.get(
                "thumbnail",
                ""
            )
        )


class GameAPI:

    def __init__(self):
        self.api_url = API_URL

    def get_all_games(self):

        response = requests.get(
            f"{self.api_url}/games",
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def search_game(self, game_name):

        games = self.get_all_games()

        game_name = game_name.lower()

        for game in games:

            title = game.get(
                "title",
                ""
            ).lower()

            if game_name in title:

                game_id = game.get("id")

                return self.get_game(
                    game_id
                )

        return None

    def get_random_game(self):

        games = self.get_all_games()

        if not games:
            return None

        game = random.choice(games)

        game_id = game.get("id")

        if not game_id:
            return None

        return self.get_game(game_id)

    def get_game(self, game_id):

        response = requests.get(
            f"{self.api_url}/game",
            params={
                "id": game_id
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()


class GameHub:

    def __init__(self, root):

        self.root = root
        self.api = GameAPI()

        self.game_image = None
        self.current_game = None

        self.setup_window()
        self.create_interface()

    def setup_window(self):

        self.root.title(
            "GameHub — Пошук ігор"
        )

        self.root.geometry(
            "1000x700"
        )

        self.root.minsize(
            850,
            600
        )

        self.root.grid_columnconfigure(
            0,
            weight=1
        )

        self.root.grid_rowconfigure(
            1,
            weight=1
        )

    def create_interface(self):

        header = ctk.CTkFrame(
            self.root,
            corner_radius=0
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        title = ctk.CTkLabel(
            header,
            text="🎮 GameHub",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            padx=30,
            pady=(20, 5),
            sticky="w"
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Пошук інформації про безкоштовні відеоігри",
            text_color="gray70"
        )

        subtitle.grid(
            row=1,
            column=0,
            padx=32,
            pady=(0, 15),
            sticky="w"
        )

        search_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        search_frame.grid(
            row=2,
            column=0,
            padx=30,
            pady=(0, 20),
            sticky="ew"
        )

        search_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=45,
            placeholder_text="Введіть назву гри..."
        )

        self.search_entry.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="ew"
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_game()
        )

        self.search_button = ctk.CTkButton(
            search_frame,
            text="ПОШУК",
            width=120,
            height=45,
            command=self.search_game
        )

        self.search_button.grid(
            row=0,
            column=1,
            padx=(0, 10)
        )

        self.random_button = ctk.CTkButton(
            search_frame,
            text="🎲 ЩО ПОГРАТИ?",
            width=150,
            height=45,
            command=self.random_game
        )

        self.random_button.grid(
            row=0,
            column=2
        )


        content = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        content.grid(
            row=1,
            column=0,
            padx=30,
            pady=20,
            sticky="nsew"
        )

        content.grid_columnconfigure(
            1,
            weight=1
        )

        content.grid_rowconfigure(
            0,
            weight=1
        )

        self.image_label = ctk.CTkLabel(
            content,
            text="Гру не вибрано",
            width=350,
            height=250,
            corner_radius=15
        )

        self.image_label.grid(
            row=0,
            column=0,
            padx=(0, 25),
            sticky="n"
        )



        info_frame = ctk.CTkFrame(
            content,
            corner_radius=15
        )

        info_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        info_frame.grid_columnconfigure(
            0,
            weight=1
        )

        info_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.info_box = ctk.CTkTextbox(
            info_frame,
            corner_radius=15,
            font=ctk.CTkFont(
                size=14
            ),
            wrap="word"
        )

        self.info_box.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="nsew"
        )


        buttons_frame = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        buttons_frame.grid(
            row=1,
            column=1,
            pady=(15, 0),
            sticky="ew"
        )

        buttons_frame.grid_columnconfigure(
            0,
            weight=1
        )

        buttons_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.wikipedia_button = ctk.CTkButton(
            buttons_frame,
            text="📖 ВІДКРИТИ У WIKIPEDIA",
            height=40,
            command=self.open_wikipedia
        )

        self.wikipedia_button.grid(
            row=0,
            column=0,
            padx=(0, 5),
            sticky="ew"
        )

        self.random_button_bottom = ctk.CTkButton(
            buttons_frame,
            text="🎲 ІНША ГРА",
            height=40,
            command=self.random_game
        )

        self.random_button_bottom.grid(
            row=0,
            column=1,
            padx=(5, 0),
            sticky="ew"
        )


        self.status_label = ctk.CTkLabel(
            self.root,
            text="Готово",
            text_color="gray60"
        )

        self.status_label.grid(
            row=2,
            column=0,
            padx=30,
            pady=(0, 15),
            sticky="w"
        )

        self.show_text(
            "Ласкаво просимо до GameHub!\n\n"
            "🔎 Введіть назву безкоштовної гри "
            "та натисніть «ПОШУК».\n\n"
            "🎲 Або натисніть «ЩО ПОГРАТИ?», "
            "щоб програма випадково порадила гру.\n\n"
            "📖 Після вибору гри її можна відкрити "
            "у Wikipedia.\n\n"
            f"ℹ️ Інформація актуальна станом на "
            f"{datetime.now().year} рік."
        )


    def show_text(self, text):

        self.info_box.configure(
            state="normal"
        )

        self.info_box.delete(
            "1.0",
            "end"
        )

        self.info_box.insert(
            "1.0",
            text
        )

        self.info_box.configure(
            state="disabled"
        )


    def search_game(self):

        game_name = self.search_entry.get().strip()

        if not game_name:

            self.status_label.configure(
                text="Введіть назву гри."
            )

            return

        self.search_button.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Пошук гри..."
        )

        self.root.update_idletasks()

        try:

            data = self.api.search_game(
                game_name
            )

            if data is None:

                self.show_text(
                    "❌ Гру не знайдено.\n\n"
                    "Спробуйте ввести іншу назву."
                )

                self.status_label.configure(
                    text="Гру не знайдено."
                )

                return

            game = Game.from_api(
                data
            )

            self.current_game = game

            self.display_game(
                game
            )

            self.status_label.configure(
                text="Гру знайдено!"
            )

        except requests.RequestException:

            self.show_text(
                "❌ Помилка підключення.\n\n"
                "Перевірте підключення до Інтернету "
                "та спробуйте ще раз."
            )

            self.status_label.configure(
                text="Помилка мережі."
            )

        except Exception as error:

            self.show_text(
                f"❌ Виникла помилка:\n\n{error}"
            )

            self.status_label.configure(
                text="Помилка."
            )

        finally:

            self.search_button.configure(
                state="normal"
            )


    def random_game(self):

        self.random_button.configure(
            state="disabled"
        )

        self.random_button_bottom.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="🎲 Шукаємо випадкову гру..."
        )

        self.root.update_idletasks()

        try:

            data = self.api.get_random_game()

            if data is None:

                self.show_text(
                    "❌ Не вдалося отримати випадкову гру."
                )

                return

            game = Game.from_api(
                data
            )

            self.current_game = game

            self.display_game(
                game
            )

            self.status_label.configure(
                text="🎲 Програма радить цю гру!"
            )

        except requests.RequestException:

            self.show_text(
                "❌ Помилка підключення.\n\n"
                "Перевірте підключення до Інтернету."
            )

            self.status_label.configure(
                text="Помилка мережі."
            )

        except Exception as error:

            self.show_text(
                f"❌ Виникла помилка:\n\n{error}"
            )

            self.status_label.configure(
                text="Помилка."
            )

        finally:

            self.random_button.configure(
                state="normal"
            )

            self.random_button_bottom.configure(
                state="normal"
            )


    def open_wikipedia(self):

        if self.current_game is None:

            self.status_label.configure(
                text="Спочатку знайдіть або виберіть гру."
            )

            return

        game_name = self.current_game.name

        wikipedia_url = (
            "https://uk.wikipedia.org/wiki/Special:"
            "Search?search="
            + quote(game_name)
        )

        webbrowser.open(
            wikipedia_url
        )

        self.status_label.configure(
            text="Wikipedia відкрито."

        )


    def display_game(self, game):

        current_year = datetime.now().year

        information = (
            f"🎮 {game.name}\n\n"

            f"📅 Дата випуску:\n"
            f"{game.release_date}\n\n"

            f"⭐ Жанр:\n"
            f"{game.genre}\n\n"

            f"💻 Платформа:\n"
            f"{game.platform}\n\n"

            f"👨‍💻 Розробник:\n"
            f"{game.developer}\n\n"

            f"🏢 Видавець:\n"
            f"{game.publisher}\n\n"

            f"📝 Опис:\n"
            f"{game.description}\n\n"

            f"────────────────────\n\n"

            f"ℹ️ Актуальність інформації:\n"
            f"станом на {current_year} рік"
        )

        self.show_text(
            information
        )

        self.load_image(
            game.image_url
        )


    def load_image(self, image_url):

        if not image_url:

            self.image_label.configure(
                image=None,
                text="Зображення відсутнє"
            )

            return

        try:

            response = requests.get(
                image_url,
                timeout=10
            )

            response.raise_for_status()

            image = Image.open(
                BytesIO(
                    response.content
                )
            )

            image.thumbnail(
                (350, 250)
            )

            self.game_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )

            self.image_label.configure(
                image=self.game_image,
                text=""
            )

        except Exception:

            self.image_label.configure(
                image=None,
                text="Не вдалося завантажити зображення"
            )



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


root = ctk.CTk()

app = GameHub(
    root
)

root.mainloop()