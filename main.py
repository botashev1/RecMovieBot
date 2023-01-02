from settings import TG_TOKEN

from aiogram import Bot, Dispatcher, executor

from handlers.register_all_handlers import register_all_handlers


def register_all(dp: Dispatcher):
    register_all_handlers(dp)


if __name__ == '__main__':
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher(bot)

    register_all(dp)

    executor.start_polling(dp)
