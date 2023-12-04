from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message

handler_router = Router()


@handler_router.message(F.text)
async def handle_text(message: Message):
    await message.answer(message.text, parse_mode=ParseMode.HTML)


@handler_router.message(F.sticker)
async def handle_sticker(message: Message):
    await message.answer("Sticker!")
