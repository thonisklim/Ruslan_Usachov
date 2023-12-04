import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters.command import Command, CommandObject
from aiogram.enums import ParseMode
from settings import settings
from aiogram.fsm.state import State, StatesGroup
from handler_router import handler_router

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(handler_router)

file_storage = {}
d_path = settings.DOWNLOAD_PATH.get_secret_value()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("<b>Hello!</b> <i>world</i>")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("*Текст:*\n"
                         "Надішли текст використовуючи HTML і я відповідно відформатую його\!\n"
                         "<b\> *Жирний* </b\>\n"
                         "<i\> _Курсив_ </i\>\n"
                         "<u\> __Підкреслений__ </u\>\n"
                         "<s\> ~Закреслений~ </s\>\n"
                         "\n*Файли:*\n"
                         "Надішли файл і він буде завантажений на сервер, можеш його завантажити "
                         "за допомогою /download, а відправити /send", parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(Command("send"))
async def cmd_send(message: Message, command: CommandObject):
    if command.args is None:
        file_names = '\n'.join(file_storage)
        await message.answer(f"This chat id is: {message.chat.id}\n"
                             f"Syntax: <b>/send [file name] [chat id]</b>\n"
                             f"list of uploaded files:\n"
                             f"{file_names}")
        return
    try:
        args = command.args.split(' ', maxsplit=2)
        file_name = args[0]
        tag = args[1]
    except ValueError:
        await message.answer("Incorect format.\n"
                             "Example: <b>/send [file name] [@example_tag]</b>")
        return
    if file_name not in file_storage.keys():
        await message.answer(f"There is no file named \"{file_name}\"")
        return
    else:
        await bot.send_document(tag, FSInputFile(file_storage[file_name]))


@dp.message(Command("download"))
async def cmd_download(message: Message, command: CommandObject):
    if command.args is None:
        file_names = '\n'.join(file_storage)
        await message.answer("Input file name after /download from the list:\n" + file_names)
        return
    try:
        file_name = command.args.split(' ', maxsplit=1)[0]
    except ValueError:
        await message.answer("Incorect format.\n"
                             "Example: /download [file name]")
        return
    if file_name not in file_storage.keys():
        await message.answer(f"There is no file named \"{file_name}\"")
        return
    else:
        await message.answer_document(FSInputFile(file_storage[file_name]))


@dp.message(F.document)
async def handle_doc(message: Message):
    path = d_path + message.document.file_name
    file_storage[message.document.file_name] = path
    await bot.download(message.document, path)
    await message.answer(f"Successfully downloaded <b>{message.document.file_name}</b>")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
