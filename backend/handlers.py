from aiogram.types import Message
from aiogram import F, Router

router = Router()

# Handler for command /start
@router.message(F.text)
async def echo(message: Message) -> None:
    await message.answer(message.text)

