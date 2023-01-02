import random

from requests.exceptions import HTTPError

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

# a = tmdb.Movies(id=453).rating_delete(guest_session_id='83072a3395ea9651c21d7e99eb036203')
# print(a)

# 769495999e079c53b0460f3c41937c29
#  {'adult': False, 'backdrop_path': '/198vrF8k7mfQ4FjDJsBmdQcaiyq.jpg', 'genre_ids': [878, 28, 12], 'id': 76600,
#  'original_language': 'en', 'original_title': 'Avatar: The Way of Water',
#  'overview': "После принятия образа аватара солдат Джейк Салли становится предводителем народа на'ви и берет на себя миссию по защите новых друзей от корыстных бизнесменов с Земли. Теперь ему есть за кого бороться — с Джейком его прекрасная возлюбленная Нейтири. Когда на Пандору возвращаются до зубов вооруженные земляне, Джейк готов дать им отпор.",
#  'popularity': 4650.217, 'poster_path': '/1tntyDRcev7PIg6xfo8El56ocoi.jpg', 'release_date': '2022-12-14',
#  'title': 'Аватар: Путь воды', 'video': False, 'vote_average': 8.1, 'vote_count': 793}


# {'adult': False, 'backdrop_path': '/tQ91wWQJ2WRNDXwxuO7GCXX5VPC.jpg',
#  'belongs_to_collection': {'id': 87096, 'name': 'Аватар (Коллекция)', 'poster_path': '/wO67q3lInOFKplkw9wyzrWcvVoM.jpg',
#                            'backdrop_path': '/iaEsDbQPE45hQU2EGiNjXD2KWuF.jpg'}, 'budget': 460000000,
#  'genres': [{'id': 878, 'name': 'фантастика'}, {'id': 28, 'name': 'боевик'}, {'id': 12, 'name': 'приключения'}],
#  'homepage': '', 'id': 76600, 'imdb_id': 'tt1630029', 'original_language': 'en',
#  'original_title': 'Avatar: The Way of Water',
#  'overview': "После принятия образа аватара солдат Джейк Салли становится предводителем народа на'ви и берет на себя миссию по защите новых друзей от корыстных бизнесменов с Земли. Теперь ему есть за кого бороться — с Джейком его прекрасная возлюбленная Нейтири. Когда на Пандору возвращаются до зубов вооруженные земляне, Джейк готов дать им отпор.",
#  'popularity': 4334.092, 'poster_path': '/1tntyDRcev7PIg6xfo8El56ocoi.jpg', 'production_companies': [
#     {'id': 574, 'logo_path': '/iB6GjNVHs5hOqcEYt2rcjBqIjki.png', 'name': 'Lightstorm Entertainment',
#      'origin_country': 'US'},
#     {'id': 127928, 'logo_path': '/cxMxGzAgMMBhTXkcpYYCxWCOY90.png', 'name': '20th Century Studios',
#      'origin_country': 'US'}], 'production_countries': [{'iso_3166_1': 'US', 'name': 'United States of America'}],
#  'release_date': '2022-12-14', 'revenue': 441703887, 'runtime': 192,
#  'spoken_languages': [{'english_name': 'English', 'iso_639_1': 'en', 'name': 'English'}], 'status': 'Released',
#  'tagline': '"Возвращайтесь на Пандору"', 'title': 'Аватар: Путь воды', 'video': False, 'vote_average': 8.079,
#  'vote_count': 939}
