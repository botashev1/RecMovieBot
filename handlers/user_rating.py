from aiogram import Dispatcher

from resources import messages
from tmdb_api_requests import movie


async def send_user_rating(dp: Dispatcher, user_id):
    page = 1
    tmp_movie_rating = await movie.get_user_rated_movies(user_id, page)
    movie_rating = tmp_movie_rating
    while tmp_movie_rating:
        page += 1
        tmp_movie_rating = await movie.get_user_rated_movies(user_id, page)
        movie_rating.extend(tmp_movie_rating)
    tmp_movie_rating.clear()

    if movie_rating:
        await dp.bot.send_message(user_id, messages.user_rated_movies(movie_rating))
    else:
        await dp.bot.send_message(user_id, messages.no_rated)
