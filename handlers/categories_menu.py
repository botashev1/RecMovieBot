from aiogram import types, Dispatcher
from aiogram.utils import exceptions

from handlers.movie_menu import send_movie_menu
import handlers.start

from resources import button_names, messages
from tmdb_api_requests import movie

from tools import decorators


async def send_categories_menu(dp, user_id):
    categories_menu = types.InlineKeyboardMarkup(resize_keyboard=True)
    categories_menu_buttons = [
        types.InlineKeyboardButton(button_names.categories[key],
                                       callback_data='_'.join([str(user_id), key]))
        for key in button_names.categories
    ]
    categories_menu.add(*categories_menu_buttons[:2])
    categories_menu.add(*categories_menu_buttons[2:])
    await dp.bot.send_message(user_id, messages.which_category, reply_markup=categories_menu)


async def catch_categories_menu_requests(dp: Dispatcher, call):
    user_id, action = call.data.split('_')
    if action == 'backToGA':
        await handlers.start.start(dp, call.message)
    elif action == 'popular':
        film = await movie.get_next_movie('popular')
        await send_movie_menu(dp, user_id, film, 'popular')
    elif action == 'best':
        film = await movie.get_next_movie('best')
        await send_movie_menu(dp, user_id, film, 'best')
    elif action == 'latest':
        film = await movie.get_next_movie('latest')
        await send_movie_menu(dp, user_id, film, 'latest')
    try:
        await call.message.delete()
    except exceptions.MessageToDeleteNotFound:
        pass

def register_movie_menu(dp: Dispatcher):
    dp.register_callback_query_handler(decorators.send_other_args(dp)(catch_categories_menu_requests),
                                       lambda call:
                                       call.data.count('_') >= 1 and
                                       call.data.split('_')[1] in button_names.categories)
