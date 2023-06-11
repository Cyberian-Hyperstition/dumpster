import streamlit as st
from streamlit_option_menu import option_menu
# установка библиотеки vk_api
#subprocess.call(['pip', 'install', 'vk_api'])
#импортируем мои модули и time
import my_modules.memescrapping as memes
import my_modules.image_comparison as ic
import my_modules.tg_poster as tg
import time

#ЗДЕСЬ МОЙ ПОЛЬЗОВАТЕЛЬСКИЙ ТОКЕН ОТ VK API
access_token = "vk1.a.1RfXiXLjUfZmhwZoNqp3zvj9MrCtHO_VEvQVCJEE0PFFkovmnpo2Aeo3kSWoQnny0WjEhXwLcbQWrUbIzvhKnjGBwCRfp2mNZnTEaDrf5VlzHvrJsseAzIGN3dBfV9ZvRj--wzO49iafw7fyEFRtYbCjG5m9y9BETpgMIW7UgWGjvvWft58mOrRDi18-LeKfj5EozE4M1Zbn-wCqHfmz9w"

#Сообщение-приветствие с описанием функционала
print("Hi there! This is AutoShitposter.", '\n',
      "My functions are:"'\n',
      "(1) Add group posts to my database", '\n', #загружаем картинки из групп в database. рекомендовано: вызвать 3 раза эту функцию, вводя:
                                                  # 1. abotai, 150; 2. societya, 150; fan_club_of_jesus_christ, 50. 
                                                  #(слово перед запятой -- это первый инпут, число -- второй) 
                                                  #работает с любыми инпутами, но иначе может получиться скучно или работать слишком долго
      "(2) Draw a graph of group re-posts", '\n', # граф связей между группами. подробнее в модуле image_comparison
      "(3) Discover re-posting connections between two groups in my database", '\n', #то же самое, что и с графом, но между двумя сообществами. возвращает "силу" ребра. 
                                                                                     #подробнее в модуле image_comparison
      "(4) Post random memes in my Telegram channel", '\n', #публикует рандомные картинки из датабазы в тг-канал! ссылка: https://t.me/AutoPosterTestingSite
      "(5) Clear my database",'\n',     #удаляет датабазу.
      "(6) Terminate my work", '\n',    #удаляет датабазу и завершает работу
      "With all that said, commands are sent via single digits (e.g. 1)", '\n',
      '\n', "Enter your command", '\n')

#Интерфейс, отвечает на цифры 1-6 и вызывает функционал, описанный выше.
#command = st.text_input("Enter your input", key="unique_key")
command = 0
while (command != 6):
    
    command = st.text_input("Enter your input", key="unique_key_2")
    command = int(command) if command is not None and command.isdigit() else None
    if command == 1:
        memes.get_group_posts(access_token)
        print('\n',"Enter new command",'\n')
    elif command == 2:
        ic.draw_graph()
        print('\n',"Enter new command",'\n')
    elif command == 3:
        print("please input first group name (e.g. abotai for vk.com/abotai)")
        name_1 = input()
        print("please input second group name")
        name_2 = input()
        connection = ic.compare_memes(name_1,name_2)
        print("found", connection, "re-posts")
        print('\n',"Enter new command",'\n')
    elif command == 4:
        num = int(input("Введи число постов: "))
        for i in range (num):
            tg.do_it()
            time.sleep(5)
        print('\n',"Enter new command",'\n')
    elif command == 5:
        memes.clear_db()
        print('\n',"Enter new command",'\n')
    elif command == 6:
        print('\n',"Goodbye!")
        break
    else: print('\n',"Enter new command",'\n')
        



