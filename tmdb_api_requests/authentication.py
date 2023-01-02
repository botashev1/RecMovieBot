from tmdb_api_requests.tmdb_setting import tmdb
from users import json_requests


async def create_new_guest(user_id):
    guest_dict = tmdb.Authentication().guest_session_new()
    if guest_dict['success']:
        await json_requests.add_user(user_id, guest_dict['guest_session_id'])
        return True
    return False
