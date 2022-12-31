from aiogram import types, Dispatcher

import handlers.user_rating
from handlers.categories_menu import send_categories_menu
from handlers.movie_menu import send_short_movie_menu

from resources import messages, button_names

from tools import decorators

from users import json_requests


async def start(dp: Dispatcher, message: types.Message):
    menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_markup.add(button_names.menu['start'], button_names.menu['getList'],)
    menu_markup.add(button_names.menu['ratedMovies'], button_names.menu['feedback'], )

    await dp.bot.send_message(message.chat.id, messages.hello_message, reply_markup=menu_markup)


async def catch_start_request(dp: Dispatcher, message: types.Message):
    user_id = message.chat.id
    if message.text in button_names.menu.values():
        if message.text == button_names.menu['start']:
            await send_categories_menu(dp, user_id)
        elif message.text == button_names.menu['getList']:
            movie_ids = await json_requests.get_movie_list(user_id)
            if movie_ids:
                for movie_id in movie_ids:
                    await send_short_movie_menu(call=None, dp=dp, user_id=user_id, movie_id=movie_id)
            else:
                await dp.bot.send_message(user_id, messages.empty_list)

        elif message.text == button_names.menu['feedback']:
            await dp.bot.send_message(user_id, messages.feedback)
        elif message.text == button_names.menu['ratedMovies']:
            await handlers.user_rating.send_user_rating(dp, user_id)
    else:
        await message.reply(messages.uncorrect_request)


def register_start(dp: Dispatcher):
    dp.register_message_handler(decorators.send_other_args(dp)(start), commands=['start'])
    dp.register_message_handler(decorators.send_other_args(dp)(catch_start_request), content_types='text')
