import asyncio
from aiogram import BaseMiddleware
from create_bot import bot, dp, scheduler
from handlers.start import start_router

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.start import send_horoscope
from datetime import datetime
# from work_time.time_func import send_time_msg


EVERYDAY_TIME = 10


class SchedulerMiddlewhare(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler


    async def __call__(self, handler, event, data):
        data["scheduler"] = self._scheduler
        return await handler(event, data)



async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_horoscope, trigger="cron", hour=EVERYDAY_TIME, start_date=datetime.now())
    scheduler.start()


    dp.update.middleware(
        SchedulerMiddlewhare(scheduler=scheduler)
    )
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())