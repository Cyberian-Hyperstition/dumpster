import telegram
import asyncio
import sqlite3
import random
from PIL import Image
from io import BytesIO
from telegram.ext import Updater

#для постинга в ТГ нужны асинхронные функции. 
async def post_image_to_channel(random_element, table_name):
    # обращаемся к боту через мой токен
    bot = telegram.Bot(token='6204357971:AAF_oelkjZChUpT6iSpv36lSNMKBM6FDcRk')
    # форматируем картинку через Pillow и меняем расширение на .jpeg
    image = Image.open(BytesIO(random_element))
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)

    # Постим и указываем сурс!
    await bot.send_photo(chat_id='@AutoPosterTestingSite', photo=image_bytes, caption=f"source: vk.com/{table_name}")

#эта функция создаёт контент поста.
async def post():
    #подключаемся к SQL-датабазе, делаем курсор, получаем случайную таблицу и случайный элемент из соответствующей случайной таблицы
    conn = sqlite3.connect('virtual_environment/base/memebase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_name = random.choice(tables)[0]
    cursor.execute(f"SELECT * FROM {table_name};")
    elements = cursor.fetchall()
    random_element = random.choice(elements)[2]

    # Call the function to post the image to the channel
    await post_image_to_channel(random_element, table_name)

#асинхронная основная функция
async def main():
    await post()

#функция-триггер. её и вызываем из интерфейса.
def do_it():
    asyncio.run(main())


