from aiogram import Dispatcher

from . import start, categories_menu, estimate_menu, movie_menu


def register_all_handlers(dp: Dispatcher):
    start.register_start(dp)
    categories_menu.register_movie_menu(dp)
    estimate_menu.register_estimate_menu(dp)
    movie_menu.register_movie_menu(dp)
