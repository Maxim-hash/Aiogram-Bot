from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Command
from config import bot_config
from func import morze_translate, get_words, check, get_records, set_record, get_lang
from aiogram.dispatcher import FSMContext
from main import dp
from states import Test, Lang
from keyboards import main_keyboard, lang_keyboard, inline_lang_keyboard
from re import split
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random


scheduler = AsyncIOScheduler()
scheduler.start()

@dp.message_handler(Command("start"), state=None)
async def start(message: Message):
    msg = f"Приветствую вас {message.from_user.first_name}, я умею кодировать ваш текст в код морзе также есть следующте команды"
    msg = "\n".join([msg, "/test - запускает тест состоящий из n-го количества слов которые нужно будет ввести на азбуке морзе а я всё внимательно проверю"])
    msg = "\n".join([msg, "/records - вывести таблицу рекордов"])
    msg = "\n".join([msg, "/lang - настройки языка"])
    await message.answer(msg , reply_markup=main_keyboard)

@dp.message_handler(Command("records"), state=None)
async def records(message: Message):
    msg = "Список ваших рекордов:\n"
    msg += "Nickname    | Score |  Language    |  Total Count  |"
    records = get_records()
    for i in records:
        msg += f"\n    {i[0]}    |       {i[1]}     |         {i[2]}          |            {i[3]}            |\x20"
    await message.answer(msg)        

@dp.message_handler(Command("lang"), state=None)
async def lang(message: Message):
    language = get_lang(bot_config.lang)
    await message.answer(f"Сейчас используется язык: {language[0]}", reply_markup=lang_keyboard)
    await Lang.step1.set()

@dp.message_handler(Command("edit"), state=Lang.step1)
async def lang(message: Message, state:FSMContext):
    await message.answer("На какой язык хотите сменить?", reply_markup = inline_lang_keyboard)

@dp.callback_query_handler(lambda callback:True, state = Lang.step1)
async def editLang(callback, state:FSMContext):
    new_lang = split(":", callback.data)
    old_lang = get_lang(bot_config.lang)
    bot_config.lang = new_lang[1]
    
    await state.finish()
    await callback.message.answer(f"Язык успешно сменён с {old_lang[0]} на {new_lang[0]}!", reply_markup = main_keyboard)

@dp.message_handler(Command("return"), state=Lang.step1)
async def lang(message: Message, state:FSMContext):
    await state.finish()
    await message.answer("Вернёмся обратно", reply_markup=main_keyboard)


@dp.message_handler(Command("test"), state=None)
async def test(message: Message):
    await message.answer("Сколько слов?\nПрошу ввести любое положительно число кроме 1", reply_markup=ReplyKeyboardRemove())

    await Test.step1.set()

@dp.message_handler(Text)
async def send_answer(message: Message):
    words = message.text

    cod = morze_translate(words, bot_config.lang)

    await message.answer(cod)

@dp.message_handler(state=Test.step1)
async def test(message: Message, state: FSMContext):
    item = message.text
    msg = ""
    if item.isdigit() and int(item) not in (0, 1):
        msg = "Отлично тогда начнём"
    else:
        item = random.randint(5, 10)
        msg = "Я просил вас ввести число, но не получил его, я сам выберу кол-во слов в тесте"
        msg = "\n".join([msg, f"Количество слов в тесте: {item}"])
    
    await message.answer(msg)

    word = get_words(bot_config.lang)
    
    msg = await message.answer(word[0])
    await state.update_data(total_count=int(item))
    await state.update_data(count=int(item) - 2)
    await state.update_data(msg=msg)
    await state.update_data(lastWord=word[0])
    await state.update_data(score=0)

    await Test.next()

@dp.message_handler(state=Test.step2)
async def test(message:Message, state:FSMContext):
    data = await state.get_data()
    msg = data['msg']
    countN = data["count"]
    lastWord = data["lastWord"]
    score = data["score"]
    string = ""

    checked = check(lastWord, message.text)

    if checked:
        score += 1
        string = "\U00002714"
    else:
        string = "\U0000274E"

    word = get_words(bot_config.lang)
    countN -= 1   

    scheduler.add_job(edit_msg, kwargs={"message": msg, "string":string})

    temp = await message.answer(word[0])
    await state.update_data(msg=temp)
    await state.update_data(count=countN)
    await state.update_data(lastWord=word[0])
    await state.update_data(score=score)
    if countN <= -1:
        await Test.next()

async def edit_msg(message:Message, string:str):
    msg = ' '.join([message.text, string])
    await message.edit_text(msg)


@dp.message_handler(state=Test.step3)
async def test(message:Message, state:FSMContext):
    data = await state.get_data()
    msg = data['msg']
    totalCount = data["total_count"]
    lastWord = data["lastWord"]
    score = data["score"]
    string = ""

    checked = check(lastWord, message.text)

    if checked:
        score += 1
        string = "\U00002714"
    else:
        string = "\U0000274E"  

    scheduler.add_job(edit_msg, kwargs={"message": msg, "string":string})

    set_record(message.from_user.first_name, score, totalCount)

    await message.answer(f"Правильно введеных слов: {score}\nЗапись успешно добавлена в таблицу рекордов", reply_markup=main_keyboard)
    await state.finish()
