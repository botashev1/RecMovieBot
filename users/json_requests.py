import json

from tmdb_api_requests import authentication


async def get_session_id(user_id: str):
    with open("users/users.json", "r") as json_users:
        users = json.loads(json_users.read())
        try:
            return users[str(user_id)]
        except KeyError:
            await authentication.create_new_guest(user_id)
            return await get_session_id(user_id)


async def add_user(user_id, session_id) -> bool:
    with open("users/users.json", "r") as json_users:
        users = json.loads(json_users.read())

    users[str(user_id)] = session_id

    with open("users/users.json", "w") as file:
        json.dump(users, file)
        return True


async def delete_session_id(user_id) -> bool:
    with open("users/users.json", "r") as json_users:
        users = json.loads(json_users.read())

    if user_id in users:
        del users[user_id]

    with open("users/users.json", "w") as file:
        json.dump(users, file)
        return True


async def add_movie(user_id, movie_id) -> bool:
    with open("users/user_lists.json", "r") as json_user_lists:
        user_lists = json.loads(json_user_lists.read())

    if not str(user_id) in user_lists:
        user_lists[str(user_id)] = dict()

    if len(user_lists[str(user_id)]) <= 50:
        user_lists[str(user_id)][str(movie_id)] = True

    with open("users/user_lists.json", "w") as file:
        json.dump(user_lists, file)
        return True


async def remove_movie(user_id, movie_id) -> bool:
    with open("users/user_lists.json", "r") as json_user_list:
        user_list = json.loads(json_user_list.read())

    if str(user_id) in user_list and str(movie_id) in user_list[str(user_id)]:
        del user_list[str(user_id)][str(movie_id)]

        with open("users/user_lists.json", "w") as file:
            json.dump(user_list, file)
            return True


async def get_movie_list(user_id) -> list:
    with open("users/user_lists.json", "r") as json_user_lists:
        user_lists = json.loads(json_user_lists.read())
        try:
            return user_lists[str(user_id)].keys()
        except KeyError:
            return []
