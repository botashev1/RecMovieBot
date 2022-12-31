def send_other_args(*other_args):
    def wrapper(func):
        async def new_func(*args):
            return await func(*other_args, *args)

        return new_func

    return wrapper
