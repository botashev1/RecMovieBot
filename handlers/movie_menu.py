from aiogram import types, Dispatcher

import handlers.categories_menu
from handlers.estimate_menu import send_estimate_menu

from resources import button_names, messages

from tmdb_api_requests import movie

from tools import decorators

from users import json_requests


async def send_movie_menu(dp: Dispatcher, user_id, film: dict, category,
                          send_estimate=True, send_add=True):
    movie_menu = types.InlineKeyboardMarkup(resize_keyboard=True)
    movie_menu_buttons = [
        types.InlineKeyboardButton(button_names.movie_menu['backToCategory'],
                                   callback_data='_'.join([str(user_id), 'backToCategory'])),
        types.InlineKeyboardButton(button_names.movie_menu['next'],
                                   callback_data='_'.join([str(user_id), category])),
    ]

    if send_add:
        movie_menu_buttons.append(
            types.InlineKeyboardButton(button_names.movie_menu['add'],
                                       callback_data='_'.join([str(user_id),
                                                               'add', str(film['id']), category])),
        )
    if send_estimate:
        movie_menu_buttons.append(
            types.InlineKeyboardButton(button_names.movie_menu['estimate'],
                                       callback_data='_'.join([str(user_id),
                                                               'estimate', str(film['id']), category])),
        )

    movie_menu.add(*movie_menu_buttons[:2])
    movie_menu.add(*movie_menu_buttons[2:])

    try:
        await dp.bot.send_photo(user_id, caption=messages.movie_info(movie.get_by_id(film['id'])),
                                photo='https://image.tmdb.org/t/p/w500' + film['poster_path'],
                                reply_markup=movie_menu)
    except:
        await dp.bot.send_message(user_id, messages.movie_info(movie.get_by_id(film['id'])),
                                  reply_markup=movie_menu)


async def send_more_info_movie_menu(call):
    more_info_movie_menu = types.InlineKeyboardMarkup(resize_keyboard=True)
    data = call.data.split('_')
    user_id, movie_id = data[1], data[2]
    more_info_movie_menu.add(
        types.InlineKeyboardButton(
            button_names.short_movie_menu['deleteFromList'],
            callback_data='_'.join(('deleteFromList', str(user_id), str(movie_id)))
        ),
        types.InlineKeyboardButton(
            button_names.short_movie_menu['hide'],
            callback_data='_'.join(('hide', str(user_id), str(movie_id)))
        ),
    )

    await call.message.edit_text(messages.movie_info(movie.get_by_id(movie_id)), reply_markup=more_info_movie_menu)


async def send_short_movie_menu(call, dp: Dispatcher = None, user_id=None, movie_id=None):
    short_movie_menu = types.InlineKeyboardMarkup(resize_keyboard=True)

    if call:
        data = call.data.split('_')
        user_id, movie_id = data[1], data[2]

    short_movie_menu.add(
        types.InlineKeyboardButton(
            button_names.short_movie_menu['deleteFromList'],
            callback_data='_'.join(('deleteFromList', str(user_id), str(movie_id)))
        ),
        types.InlineKeyboardButton(
            button_names.short_movie_menu['moreInfo'],
            callback_data='_'.join(('moreInfo', str(user_id), str(movie_id)))
        ),
    )

    if call:
        await call.message.edit_text(messages.short_movie_info(movie.get_by_id(movie_id)),
                                     reply_markup=short_movie_menu)
    else:
        film = movie.get_by_id(movie_id)
        await dp.bot.send_message(user_id, messages.short_movie_info(film),
                                  reply_markup=short_movie_menu)


async def catch_movie_menu_requests(dp: Dispatcher, call):
    action = list(call.data.split('_'))
    user_id, act = action[0], action[1]
    match act:
        case 'backToCategory':
            await call.message.delete()
            await handlers.categories_menu.send_categories_menu(dp, user_id)
        case 'estimate':
            user_id, act, film_id, category = action
            await send_estimate_menu(call, user_id, film_id, category)
        case 'add':
            await call.message.delete()
            user_id, act, movie_id, category = action
            await send_movie_menu(dp, user_id, movie.get_by_id(movie_id), category, send_add=False)
            await json_requests.add_movie(user_id, movie_id)


async def catch_user_list(dp: Dispatcher, call):
    action, user_id, movie_id = call.data.split('_')
    match action:
        case 'moreInfo':
            await send_more_info_movie_menu(call)
        case 'hide':
            await send_short_movie_menu(call)
        case 'deleteFromList':
            await json_requests.remove_movie(user_id, movie_id)
            await call.message.delete()


def register_movie_menu(dp: Dispatcher):
    dp.register_callback_query_handler(decorators.send_other_args(dp)(catch_movie_menu_requests),
                                       lambda call:
                                       call.data.count('_') >= 1 and
                                       call.data.split('_')[1] in button_names.movie_menu)
    dp.register_callback_query_handler(decorators.send_other_args(dp)(catch_user_list),
                                       lambda call:
                                       call.data.split('_')[0] in button_names.short_movie_menu)
