import streamlit as st
import vk_api

# установка библиотеки vk_api
st.write("Установка библиотеки vk_api...")
!pip install vk_api

# импортирование библиотеки vk_api
st.write("Импортирование библиотеки vk_api...")
import vk_api
import requests
import json
import os
import time
import re
import vk_api
import sqlite3
import shutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO


##функция для vk_api
def get_group_posts(access_token):
    #Стартуем сессию в VK API
    vk_session = vk_api.VkApi(token=access_token)
    vk = vk_session.get_api()

    #получаем инфу о группе с картинками и количеством постов, которые надо обработать
    print("write the VK Group short link (e.g. abotai for vk.com/abotai): ")
    group_name = input()
    print("write the approximate number of memes you want to steal: ")
    count = int(input())

    print("This may take a long time. Please wait... ") #на будущее

    #получаем айди группы через VK API
    response = vk.utils.resolveScreenName(screen_name=group_name)
    group_id = response['object_id']

    #инициализируем виртуальную среду
    venv_dir = os.environ.get('virtual_environment')

    #создаём папки/проверяем их наличие
    try:
        os.mkdir('virtual_environment/memes')
        os.mkdir('virtual_environment/base')
    except: pass
    #указываем путь к технической папке для загрузки картинок, а потом к папке с базой данных SQL
    folder_path = 'virtual_environment/memes'
    database_path = 'virtual_environment/base'

    #цикл, существующий для обработки большего чем 100 количества постов (ВК API не даёт больше ста элементов за один запрос)
    offset = 0
    while count-offset>0:
        #получаем первые 100 данных картинок --> переходим к новой сотне
        url = f"https://api.vk.com/method/wall.get?owner_id=-{group_id}&count={count-offset}&offset={offset}&access_token={access_token}&v=5.131"
        response = requests.get(url)
        data = json.loads(response.text)
        downloaded = data["response"]["items"]
        meme_links = []

        #фильтруем пережатые картинки-дубликаты и делаем массив со ссылками на самые качественные фотки. игнорируем ошибки (они от постов без фоток).
        for memes in range(len(downloaded)):
            try:
                size = downloaded[memes]["attachments"][0]["photo"]["sizes"] #downloaded - это довольно странного вида кортеж. индексы получены эмпирикой
                width = 0
                for i in range(len(size)):
                    if size[i]["width"]>width:
                        width = size[i]["width"]
                        desired_url = size[i]["url"]
                meme_links.append(desired_url)
            except: pass 

        #сохраняем первые 100 картинок и повышаем "пол" для нашего запроса к VK. убираем "мусор" в строках и делаем нормальные названия
        for url in meme_links:
            response = requests.get(url)
            filename = re.sub('[^A-Za-z0-9.]+', '', os.path.basename(url)) #о, regular expression!
            filename = filename.split('.jpg')[0] + '.jpg'
            #записываем в временную папку
            with open(os.path.join(folder_path, filename), 'wb') as file:
                file.write(response.content)

        #повышаем оффсет, "пол" запроса. ВК пропустит offset записей и вернёт следующий набор до ста штук
        offset+=100

    #инициализируем SQL датабазу, объявляем курсор, создаём/чекаем наличие таблицы с именем группы, из которой загружаем
    conn = sqlite3.connect('virtual_environment/base/memebase.db')
    c = conn.cursor()
    query = "CREATE TABLE {} (id INTEGER PRIMARY KEY, name TEXT, data BLOB)".format(group_name)
    c.execute(query)
    
    #заносим в датабазу все картинки из технической папки в формате имя файла -- бинарная запись фотки
    for filename in os.listdir("virtual_environment/memes"):
        with open("virtual_environment/memes/" + filename, 'rb') as f:
            photo_data = f.read()
            c.execute("INSERT INTO {} (name, data) VALUES (?, ?)".format(group_name), (filename, photo_data))

    #сохраняем манипуляции с датабазой и закрываем её
    conn.commit()
    conn.close()

    #удаляем техническую папку.
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

#Легаси-функция. В коде не используется. 
#Можно использовать, если хочешь закачать фотки не из ВК. 
#Использует Selenium и chromedriver, а не vk_api
def get_image_data():
    print("write the url (e.g vk.com/id1): ")
    page_id = input()
    url = f"https://{page_id}"
    print("write the approximate number of downscrollings: ")
    number = int(input())
    driver = webdriver.Chrome()
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    i=0
    
    while i<(number-1):
        time.sleep(0.75)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i+=1
    images = driver.find_elements(By.TAG_NAME, "img")

    filtered_images = [img for img in images if not re.search('50x50', img.get_attribute("src")) 
                                            and not re.search('100x100', img.get_attribute("src"))
                                            and not re.search('200x200', img.get_attribute("src"))
                                            and not re.search('.png', img.get_attribute("src"))
                                            and not re.search('sticker', img.get_attribute("src"))
                                            and not re.search('audio', img.get_attribute("src"))]

    meme_links = [img.get_attribute("src") for img in filtered_images]
    return meme_links

#функция, которая удаляет базу данных. ОЧЕНЬ ПОЛЕЗНАЯ ФУНКЦИЯ.
def clear_db():
    base_path = 'virtual_environment/base'
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
