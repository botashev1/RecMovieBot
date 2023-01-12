import random

from requests.exceptions import HTTPError

from tmdb_api_requests import authentication
from tmdb_api_requests.tmdb_setting import tmdb
from users import json_requests


def movies(category):
    mx = 500
    page = random.randint(1, mx)

    if category == 'popular':
        while page <= mx:
            for film in tmdb.Movies().popular(language='ru', page=page)['results']:
                yield film

            page += 1
            if page > mx:
                page = 1
    elif category == 'best':
        while page <= mx:
            for film in tmdb.Movies().top_rated(language='ru', page=page)['results']:
                yield film

            page += 1
            if page > mx:
                page = 1
    elif category == 'latest':
        while page <= mx:
            for film in tmdb.Movies().upcoming(language='ru', page=page)['results']:
                yield film

            page += 1
            if page > mx:
                page = 1


GET_POPULAR = movies('popular')
GET_BEST = movies('best')
GET_LATEST = movies('latest')


async def get_next_movie(category):
    if category == 'popular':
        return next(GET_POPULAR)
    elif category == 'best':
        return next(GET_BEST)
    elif category == 'latest':
        return next(GET_LATEST)


def get_genres():
    return tmdb.Genres().movie_list(language='ru')['genres']


def get_by_id(film_id):
    return tmdb.movies.Movies(film_id).info(language='ru')


async def post_mark(user_id, film_id, mark):
    try:
        tmdb.Movies(film_id).rating(
            guest_session_id=await json_requests.get_session_id(user_id),
            value=mark,
        )
    except HTTPError:
        await authentication.create_new_guest(user_id)
        tmdb.Movies(film_id).rating(
            guest_session_id=await json_requests.get_session_id(user_id),
            value=mark,
        )


async def get_user_rated_movies(user_id, page=1):
    res = []

    try:
        films = tmdb.GuestSessions(
            guest_session_id=await json_requests.get_session_id(user_id)
        ).rated_movies(language='ru', page=page)['results']
    except HTTPError:
        await json_requests.delete_session_id(user_id)
        films = []

    for film in films:
        res.append((film['title'], film['rating']))
    return res
