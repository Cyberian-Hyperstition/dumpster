import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from PIL import Image
from io import BytesIO

#ИДЕНТИФИКАЦИЯ КАРТИНКИ ЧЕРЕЗ ЯРКОСТЬ
def brightness(image, hash_size=20):
    # преобразование в черно-белое изображение
    image = image.convert('L')
    # сжатие изображения до размеров 20х20
    resized_image = image.resize((hash_size, hash_size))
    # вычисление яркости пикселей
    pixels = list(resized_image.getdata())
    # вычисление среднего значения яркости
    avg_pixel = sum(pixels) / len(pixels)
    # вычисление хеша-таргета
    excess_brightness = 0
    for i in range(hash_size * (hash_size)):
        #если яркость пикселя больше среднего значения, то добавляем 1 в хеш
        if pixels[i] > avg_pixel:
            excess_brightness += 1 << i
    #возвращаем хеш-маркер, по которому можно находить одинаковые пережатые или перезалитые картинки
    return excess_brightness

#получаем колонку с бинарными записями фоток
def getlist(group_name):
    #подключаемся, форматируем в pandas-датафрейм и берём колонку с бинарными записями
    conn = sqlite3.connect('virtual_environment/base/memebase.db')
    c = conn.cursor()
    df = pd.read_sql_query("SELECT * from {}".format(group_name), conn)
    df = df['data']
    conn.close()
    return df

#ищем перепосты в картинках из пабликов по их шорт-линкам
def compare_memes(name_1,name_2):
    print("This action consumes a lot of time. Please wait... ")

    #функция getlist(str) описана выше
    memes_1 = getlist(name_1)
    memes_2 = getlist(name_2)

    #задаём дефолтное количество повторений как 0
    connection_level = 0

    #попарно сравниваем картинки во вложенном цикле и находим количество перепостов
    for i in range (len(memes_1)):
        hash_1 = brightness(Image.open(BytesIO(memes_1[i]))) #brightness описана выше
        for j in range (len(memes_2)):
            hash_2 = brightness(Image.open(BytesIO(memes_2[j])))
            if bin(hash_1 ^ hash_2).count('1') < 10:
                print(f"Image {i+1} from {name_1} and image {j+1} from {name_2} are similar.") #если это не выводить, становится скучно
                connection_level+=1

    return connection_level #наш таргет! используем потом для построения графов

#функция, которая с помощью NetworkX строит граф, узлы которого -- паблики, а рёбра -- количество картинок, которые запощены в обоих из пабликов 
def draw_graph():
    #подключаемся к SQL датабазе
    conn = sqlite3.connect('virtual_environment/base/memebase.db')
    cursor = conn.cursor()

    #получаем список таблиц-пабликов из SQL-датабазы. Сохраняем в массив.
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    groups = []
    for index in range (len(tables)):
        groups.append(tables[index][0])

    #создаём граф
    reposts = nx.Graph()

    #присоединяем узлы
    for group in groups:
        reposts.add_node(group)
    
    #По именам узлов находим edge_strength -- "силу" рёбер. Если она нулевая, ребра нет. Выполняется очень долго при больших объёмах датабазы :с
    for index_1 in range (len(groups)-1):
        for index_2 in range(index_1+1, len(groups)):
            edge_strength =compare_memes(groups[index_1], 
                                         groups[index_2])
            if edge_strength != 0:
                reposts.add_edge(groups[index_1],
                                 groups[index_2], 
                                 label = edge_strength)

    #задаём график нашего NetworkX графа
    pos = nx.spring_layout(reposts, seed=42)
    nx.draw(reposts, pos, with_labels=True)
    labels = nx.get_edge_attributes(reposts, 'label')
    nx.draw_networkx_edge_labels(reposts, pos, edge_labels=labels)
    plt.show()

    #отключаемся от database
    conn.close()
