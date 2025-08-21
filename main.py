import asyncio
from aiogram import Bot, Dispatcher
from backend.handlers import router
import os

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher()

# Main function with bot polling
async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)

# Infinite loop for main function
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
