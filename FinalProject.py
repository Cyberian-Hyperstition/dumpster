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


#Интерфейс, отвечает на цифры 1-6 и вызывает функционал, описанный выше.
def main():
    st.write("""
    Hi there! This is AutoShitposter.

    My functions are:
    (1) Add group posts to my database
    (2) Draw a graph of group re-posts
    (3) Discover re-posting connections between two groups in my database
    (4) Post random memes in my Telegram channel
    (5) Clear my database
    (6) Terminate my work

    With all that said, commands are sent via single digits (e.g. 1)

    Enter your command
    """)
    st.title("Streamlit Interface")
    st.sidebar.title("Commands")
    command = st.sidebar.radio("Choose a command", ("Select", "1", "2", "3", "4", "5", "Exit"))

    if command == "1":
        memes.get_group_posts(access_token)
        st.write("Command 1 executed")
    elif command == "2":
        ic.draw_graph()
        st.write("Command 2 executed")
    elif command == "3":
        name_1 = st.text_input("Please input first group name (e.g. abotai for vk.com/abotai)")
        name_2 = st.text_input("Please input second group name")
        if st.button("Compare Memes"):
            connection = ic.compare_memes(name_1, name_2)
            st.write(f"Found {connection} re-posts")
    elif command == "4":
        num = st.number_input("Введите число постов:", value=1, step=1)
        if st.button("Execute Command 4"):
            for i in range(num):
                tg.do_it()
                time.sleep(5)
            st.write("Command 4 executed")
    elif command == "5":
        if st.button("Clear DB"):
            memes.clear_db()
            st.write("Database cleared")
    elif command == "Exit":
        st.write("Goodbye!")
        st.stop()
    else:
        st.write("Please select a command")

if __name__ == "__main__":
    main()
        



