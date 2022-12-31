from aiogram import Dispatcher, types

import handlers.movie_menu

from resources import button_names

from tmdb_api_requests import movie

from tools import decorators


async def send_estimate_menu(call, user_id, film_id, category):
    estimate_menu = types.InlineKeyboardMarkup()
    estimate_menu_buttons = [
        types.InlineKeyboardButton(
            mark, callback_data='_'.join([str(user_id), 'mark', str(mark), film_id, category])
        )
        for mark in button_names.marks
    ]
    estimate_menu.add(*estimate_menu_buttons)
    estimate_menu.add(
        types.InlineKeyboardButton('Назад',
                                   callback_data='_'.join([str(user_id), 'backToMovie', film_id, category])
                                   )
    )
    await call.message.edit_reply_markup(estimate_menu)


async def catch_user_mark(dp: Dispatcher, call):
    data = call.data.split('_')
    action = data[1]
    await call.message.delete()
    if action == 'backToMovie':
        user_id, action, film_id, category = data
        await handlers.movie_menu.send_movie_menu(dp, user_id, movie.get_by_id(film_id), category)
    elif action == 'mark':
        user_id, action, mark, film_id, category = data
        await movie.post_mark(user_id, film_id, mark)
        await handlers.movie_menu.send_movie_menu(dp, user_id, movie.get_by_id(film_id), category, send_estimate=False)


def register_estimate_menu(dp: Dispatcher):
    dp.register_callback_query_handler(decorators.send_other_args(dp)(catch_user_mark),
                                       lambda call:
                                       call.data.count('_') >= 1 and
                                       call.data.split('_')[1] in ('mark', 'backToMovie'))
