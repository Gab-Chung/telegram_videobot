from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import constant as keys
import database as D



engine = create_engine("sqlite:///video.db")
base = declarative_base()



base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


# Initialize bot and dispatcher
bot = Bot(token=keys.BOT_TOKEN)
dp = Dispatcher(bot)

# Keyboards
button1 = KeyboardButton("best videos")
button2 = KeyboardButton("recent videos")
Keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1).add(button2)


@dp.message_handler(commands=['start'])
async def Welcome(message: types.Message):
    user = session.query(D.User).filter(D.User.telegram_id==message.chat.id).first()
    if user is None:
        new_user = D.User(telegram_id=message.chat.id, user_firstname=message.chat.first_name, user_lastname=message.chat.last_name, username=message.chat.username)
        session.add(new_user)
        session.commit()
    await message.reply(
        f"Hi {message.chat.first_name},\nI am a video bot. I help you fetch videos from pexels. " 
        "Search anything you want or click on the buttons below for a quick search", reply_markup=Keyboard1)



@dp.message_handler(commands=['help'])
async def Help(message: types.Message):
    await message.reply(
        "Type the name of the video you would like to get in the search "
        "bar or click on best videos to get the best videos currently on pexels", reply_markup=Keyboard1)


@dp.message_handler()
async def InputSearch(message: types.Message):
    endpoint = f'https://api.pexels.com/videos/search?query={message.text}'
    response_object = requests.get(endpoint, headers={'Authorization': keys.PEXELS_API_TOKEN})
    response_json = response_object.json()
    print(response_json)
    display_videos = []
    count = 0
    for item in response_json['videos']:
        if count > 4:
            break
        display_videos.append(item)
        count += 1

    display_text = ""
    for item in display_videos:
        display_text += f"{item['url']} \n\n"

    search_result = session.query(D.search).filter(D.search.keyword == message.text).first()
    if search_result is None:
        new_search_result = D.search(keyword=message.text)
        session.add(new_search_result)
        session.commit()
        await message.reply(f"Here is the result of {message.text} \n\n {display_text}")

    else:
        await message.reply(f"You have searched for this item before, see the result of {message.text} below\n\n {display_text}")



# Authorization: 563492ad6f91700001000001fb3ba4cf0ae54b7b8cae66e24f31933f
executor.start_polling(dp)
