from resources.button_names import add_or_remove


def short_movie_info(film):
    return '«' + film['title'] + '», ' + film['release_date'][:4]

def user_rated_movies(movie_rating):
    res = 'Список оцененных вами фильмов:\n\n'
    for movie, rating in movie_rating:
        res += f'«{movie}», {int(rating)}/10\n'
    return res

def movie_info(film):
    name = film['title']

    genres = ', '.join(genre['name'] for genre in film['genres'])

    release_year = film['release_date'][:4]

    runtime = film['runtime']

    overview = film['overview']

    average_mark = film['vote_average']
    count_marks = film['vote_count']

    return f"Название: «{name}»\n\n" \
           f"Год выпуска: {release_year}\n" \
           f"Длительность: {runtime} минут\n" \
           f"Жанр: {genres}\n" \
           f"Средняя оценка на TMDB: {average_mark}\n" \
           f"Всего оценок: {count_marks}\n\n" + \
        (f"Описание:\n{overview}" if len(overview) > 0 else "")

def add_or_not(movie_name: str):
    return f'Добавить фильм "{movie_name}" в ваш список?'


feedback = 'Если вы столкнулись с проблемой или у вас есть идея, как улучшить бота, свяжитесь со мной — @return400'

hello_message = 'Привет! Я бот, который поможет подобрать тебе фильм.\n' \
                'Пиши "Начать", чтобы подобрать себе фильм/сериал для просмотра'


which_category = 'Из какой категории будем выбирать фильм?'


start_rec_system = 'Начинаем! Я буду предлагать тебе фильм, а ты ставь оценку от 1 до 5, где 5 - это идеально, ' \
                   'а 1 - очень плохо.\n' \
                   f'Чтобы добавить фильм в твой личный список, нажимай "{add_or_remove["add"]}"'

uncorrect_request = 'Прости, я не понимаю тебя'

empty_list = 'Кажется, ты не добавил ни один фильм в свой список.\nЧтобы добавить понравившийся фильм, жми "Добавить"'

no_rated = 'Кажется, ты не поставил оценку ни одному фильму :('