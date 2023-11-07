version = '1.2.0'

import os
from tkinter import *
import tkinter as tk
import random
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askinteger
import time
import requests
import threading
from pygments.lexers import PythonLexer
from pygments.token import Token
import openai
from github import Github
import time
import webbrowser
import shutil

from data.design_elements import *
from data.sapper import *


game_over = False

premium = True
countdown_running = False

registration = False

bg_color = "#FFFFFF"
fg_color = "#000000"
bg_color_dark = 'gray90'

# Данные для гитхаба
token_git = 'klt_Jfj6NuRT0XWBEyeBu9AVPw24XLYGWy4jIJg2'
username_git = 'Falbue'
repo_name = 'chenk-data'
file_name = 'data.txt'

shift = 4

login = ''
passw = ''
api = ''
user = ''
bot = ''


font_size = 16
options_size = [8, 10 , 12, 14, 16, 18, 20]
fonts = "Tahoma"
options = ["Tahoma", "Consolas", "Calibri", "Courier", "Times New Roman", "Verdana", "Arial"]


delay = 25
delay_state = "ВКЛ"

expand_button_text = "↑"

text_error = ''
latest_version = '1.0.0'
online = ''

question = ''
answer = ''

with open("data/hello_text.txt", "r", encoding="utf-8") as file:
    welcome_text = file.read()

with open("data/info_text.txt", "r", encoding="utf-8") as file:
    info = file.read()


def open_help():
    login_frame.pack_forget()
    sign_frame.pack_forget()
    shift_frame.pack_forget()
    button_submit_sign.pack_forget()
    button_submit_login.pack_forget()

    frame_info.pack(fill=BOTH, expand=True)

def close_info():
    frame_info.pack_forget()
    shift_frame.pack(side="top", anchor="nw", fill='x')
    sign()

# Определяем функцию для шифрования текста
def encrypt(text_api, shift):
    result = ""
    for i in range(len(text_api)):
        char = text_api[i]
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result

def decrypt(text_api, shift):
    result = ""
    for i in range(len(text_api)):
        char = text_api[i]
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - shift - 65) % 26 + 65)
            else:
                result += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            result += char
    return result


text_api = token_git
text_api = decrypt(text_api, shift)
token_git = text_api



def update_data(token, username, repo_name, file_name, content, commit_message):
    global token_git, username_git
    g = Github(token_git)

    repo = g.get_user(username_git).get_repo(repo_name)
    try:
        contents = repo.get_contents(file_name)
        old_content = contents.decoded_content.decode()
        new_content = old_content + '\n' + content
        repo.update_file(contents.path, commit_message, new_content, contents.sha, branch="main")
        print(f'{file_name} обновлён в репозитории {repo_name}')
    except Exception as e:
        print(f'Ошибка обновления файла {file_name} в {repo_name} репозитории: {e}')

def delete_data():
    if os.path.exists("data/data.txt"):
        os.remove("data/data.txt")
        print(f"Файл data/data.txt Успешно удалён")
    else:
        print(f"Файл data/data.txt не удалён")


def send_api():
    global answer
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "assistant", "content": question}]
            )
        print("Бот дал ответ")
        answer = completion.choices[0].message.content
    except Exception as e:
        answer = str(f'Произошла ошибка: {e}')
        btn_send.configure(state="normal")
        print(f"Произошла ошибка: {e}")
    


    def show_text_slowly(text):
        global delay, premium_time
        text_chat.configure(state="normal")
        text_chat.delete("bot_placeholder.first", "bot_placeholder.last")
        text_chat.insert(END, bot + ": ", "bold")
        in_quotes = False
        in_triple_quotes = False
        line_number = 0
        for i, char in enumerate(text):
            line_number += 1
            if char == "`" and i < len(text)-2 and text[i+1:i+3] == "``":
                in_triple_quotes = not in_triple_quotes
                if in_triple_quotes:
                    text_chat.tag_add("quote", "end")  # добавляем тег "quote" на следующую строку
                else:
                    text_chat.tag_remove("quote", "end-1c")  # удаляем тег "quote", если уже вышли за пределы тройных кавычек
            text_chat.insert(END, char, "bot" if not in_quotes and not in_triple_quotes else "quote")  # проверяем значение переменных и добавляем соответствующий тег
            text_chat.see("end")
            root_chat.update()
            text_chat.tag_configure("quote", background="black", foreground='white', selectbackground="#87CEFA")
            root_chat.after(delay)

        text_chat.insert(END, "\n", "bot")
        text_chat.tag_configure("bot", background=bg_color_dark, selectbackground="#87CEFA")
        text_chat.configure(state="disabled")
    show_text_slowly(answer)
    btn_send.configure(state="normal")
    if premium == False:
        countdown(300)

def countdown(n):
    global premium_time, countdown_running
    countdown_running = True
    premium_time = n
    with open('data/time.hui', 'w') as file:
        file.write(str(premium_time))
    print("Таймер запущен")
    while premium_time > 0:
        with open('data/time.hui', 'r') as file:
            premium_time = int(file.read())
        premium_time -= 1
        print(premium_time)
        time.sleep(1)
        with open('data/time.hui', 'w') as file:
            file.write(str(premium_time))
    print('Время вышло')

if os.path.exists('data/time.hui'):
    with open('data/time.hui', 'r') as file:
        premium_time = int(file.read())
else:
    premium_time = 0

# функция, которая вызывается при нажатии кнопки "Отправить"
def btn_send_command():
    global text_error, question
    text_chat.configure(bg=bg_color, fg=fg_color)
    check = text_chat.get("1.0", END).strip('\n')
    question = message_input.get("1.0", END).strip('\n')
    message_input.delete("1.0", END)
    if check == welcome_text:
        text_chat.configure(state="normal")
        text_chat.delete("1.0", END)
        text_chat.configure(state="disabled")

    if premium == False and premium_time > 0:
        text_chat.configure(state="normal")
        text_chat.tag_configure("bold", font = (fonts, font_size-4, "bold"))
        text_chat.insert(END, '\n')
        text_chat.insert(END, bot + ": ", "bold")
        text_chat.tag_configure("bot", background=bg_color_dark, selectbackground="#87CEFA")
        text_chat.insert(END, f"До ввода следующего сообщения осталось: {premium_time} секунд.\n", "bot")
        text_chat.configure(state="disabled")
        if countdown_running == False:
            thread_premium = threading.Thread(target=countdown, args=(premium_time,))
            thread_premium.start()
    else:
        message_input.configure(state='disabled')
        btn_send.configure(state='disabled')
        print("Пользватель задал вопрос")
        text_chat.configure(state="normal")
        text_chat.insert(END, '\n')
        text_chat.insert(END, user + ": ", "bold")
        text_chat.tag_configure("bold", font = (fonts, font_size-4, "bold"))
        text_chat.insert(END, question, "user")
        text_chat.tag_configure("user", background=bg_color, selectbackground="#87CEFA")
        text_chat.insert(END, '\n')
        text_chat.configure(state="disabled")
        text_chat.tag_configure("bold", font=(fonts, font_size - 4, "bold"))
        text_chat.configure(state="normal")
        text_chat.insert(END, '\n')
        text_chat.insert(END, bot + " печатает...", "bot_placeholder bold")
        text_chat.configure(state="disabled")
        text_chat.see(END)
        root_chat.update()
        thread = threading.Thread(target=send_api)
        thread.start() 
        text_chat.see(END)
        root_chat.update()
        message_input.configure(state="normal")
    


def mutable_objects(): # Изменяемые объекты
    # Кнопки
    def set_button_properties(button, bg_color, fg_color, bg_color_dark, fonts, font_size):
        button.configure(bg=bg_color, fg=fg_color, activebackground=bg_color_dark, font=(fonts, font_size))
        button.bind("<Enter>", lambda event: button.configure(bg=bg_color_dark))
        button.bind("<Leave>", lambda event: button.configure(bg=bg_color))
    buttons = [btn_send, btn_clear, btn_sapper, btn_close, btn_delay, btn_update, btn_settings, btn_clear_chat, btn_color, expand_button]
    for button in buttons:
        set_button_properties(button, bg_color, fg_color, bg_color_dark, fonts, font_size)

    text_chat.configure(bg=bg_color, fg=fg_color, font = (fonts, font_size-4))
    text_chat.tag_configure("quote", font = (fonts, font_size-4))
    text_chat.tag_configure("bold", font = (fonts, font_size-4, "bold"))
    message_input.configure(bg=bg_color, fg=fg_color, font = (fonts, font_size-4))
    scrollbar_chat.configure(background = bg_color, troughcolor = bg_color_dark)

    root_chat.configure(bg=bg_color_dark)

    frame_root_chat.configure(bg = bg_color_dark)
    frame_btn.configure(bg=bg_color_dark)
    frame_chat.configure(bg=bg_color_dark)

    label_delay.configure(fg = fg_color, bg = bg_color_dark, font = (fonts, font_size, "bold"))

    setting_frame.configure(bg = bg_color_dark)
    frame_font_setting.configure(bg = bg_color_dark)
    lbl_font.configure(fg = fg_color, bg = bg_color_dark, font = (fonts, font_size, "bold"))
    option_menu.configure(bg = bg_color, activebackground = bg_color_dark, highlightbackground = 'black', border = 1, highlightthickness = 0, fg = fg_color, activeforeground = fg_color, font = (fonts,font_size))
    option_menu["menu"].configure(bg=bg_color_dark, font=(fonts, font_size-4), fg = fg_color,activebackground = bg_color,)
    option_menu_size.configure(bg = bg_color, activebackground = bg_color_dark, highlightbackground = 'black', border = 1, highlightthickness = 0, fg = fg_color, activeforeground = fg_color, font = (fonts,font_size))
    option_menu_size["menu"].configure(bg=bg_color_dark, font=(fonts, font_size-4), fg = fg_color,activebackground = bg_color,)
    frame_button_color.configure(bg=bg_color_dark)
    settings_window.configure(bg=bg_color_dark)
    frame_button_color.configure(bg=bg_color_dark)
    frame_delay.configure(bg=bg_color_dark)
    lbl_news_update.configure(fg = bg_color, bg = bg_color_dark, font = (fonts, font_size,"bold"))

    popup_menu_input.configure(bg=bg_color_dark, font=(fonts, font_size-6), fg = fg_color,activebackground = bg_color)
    popup_menu.configure(bg=bg_color_dark, font=(fonts, font_size-6), fg = fg_color,activebackground = bg_color)


    check = text_chat.get("1.0", END)
    check = check.strip('\n')
    if check == welcome_text:
      text_chat.configure(state="normal")
      text_chat.configure(fg = bg_color_dark, font = (fonts, font_size-4))
      text_chat.configure(state="disabled")

    text_chat.tag_configure("user", background=bg_color, font = (fonts, font_size - 4))
    text_chat.tag_configure("bot", background=bg_color_dark, font = (fonts, font_size - 4))


# функция для изменения цветовой гаммы
def change_colors():
    global bg_color
    global fg_color
    global bg_color_dark
    bg_color = askcolor()[1]
    if bg_color == None:
        print("Цвет не выбран")
    else:
        fg_color = "#FFFFFF" if ((int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16)) < (127, 127, 127)) else "#000000"
        #Более тёмные объекты
        r, g, b = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
        r = max(r - 30, 0)
        g = max(g - 30, 0)
        b = max(b - 30, 0)
        bg_color_dark = f'#{r:02X}{g:02X}{b:02X}'
        mutable_objects()


def clear_colors():
  global bg_color
  global fg_color
  global bg_color_dark

  bg_color = "white"
  fg_color = "#000000"
  bg_color_dark = 'gray90'

  mutable_objects()



# функция для изменения размера шрифта
def select_font_size(value_size):
    global font_size
    font_size = value_size
    print(f'Выбран размер шрифта: {font_size}')
    mutable_objects()
    

def select_fonts(value):
    global fonts
    fonts = value
    print(f"Выбран шрифт: {fonts}")
    mutable_objects()
    


def compare_versions(version, latest_version):
    v1_parts = [int(x) for x in version.split(".")]
    v2_parts = [int(x) for x in latest_version.split(".")]
    for i in range(min(len(v1_parts), len(v2_parts))):
        if v1_parts[i] < v2_parts[i]:
            return -1
        elif v1_parts[i] > v2_parts[i]:
            return 1
    if len(v1_parts) < len(v2_parts):
        return -1
    elif len(v1_parts) > len(v2_parts):
        return 1
    else:
        return 0

def update_chenkgpt():
    updating_vesion = latest_version
    g = Github(token_git)

    # путь к рабочему столу
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # имя новой папки
    folder_name = 'ChenkGPT'
    # полный путь к новой папке
    new_folder_path = os.path.join(desktop_path, folder_name)

    # проверяем, существует ли уже папка
    if not os.path.exists(new_folder_path):
        # создание новой папки
        os.mkdir(new_folder_path)
    else:
        print(f"Папка {folder_name} уже существует на рабочем столе.")

    repo = g.get_repo('Falbue/ChenkGPT')
    release_name = 'Version 1.1.0'
    releases = repo.get_releases()
    for release in releases:
        if release.title == release_name:
            target_release = release
            break   

    for asset in target_release.get_assets():
        if asset.name.endswith(".exe"):
            file_url = asset.browser_download_url
            r = requests.get(file_url)
            with open(f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT/{asset.name}", "wb") as f:
                f.write(r.content)

    repo = g.get_repo("Falbue/chenk-data")
    file_content = repo.get_contents("data.txt").decoded_content
    with open("data/data.txt", "wb") as f:
        f.write(file_content)

    with open("data/data.txt", "r") as f:
        for i, line in enumerate(f):
            if f"login: {login}" in line:
                stroke = i
                print(f"Строка c логином '{f.name}' на {i+1}-й строке")
    file = repo.get_contents("data.txt")
    contents = file.decoded_content.decode("utf-8")
    lines = contents.split("\n")

    # Изменение строки номер 5
    lines[stroke+5] = f'version: {version}'

    # Объединение строк в новый контент файла
    new_contents = "\n".join(lines)

    repo.update_file(
        path="data.txt",
        message=f"{login} обновил версию приложения",
        content=new_contents,
        sha=file.sha
    )

    # путь к exe файлу на рабочем столе
    path = f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT/installer.exe"
    # запуск exe файла
    os.startfile(path)
    # ждем, пока файл откроется
    time.sleep(1)
    try:
        # выводим окно файла по верх всех окон
        window.set_foreground()
    except:
        print('Похуй')
    os.remove("data/data.txt")
    root_chat.destroy()
    


 # добавим настройки окна
def settings():
    if premium == False:
        print("sdfsdf")
        btn_color.pack_forget()
        btn_clear.pack_forget()
        frame_delay.pack_forget()
        btn_clear_chat.pack_forget()
        btn_sapper.pack_forget()
        frame_font_setting.pack_forget()
        lbl_premium.pack()
        btn_link.pack(side = LEFT)
        btn_qr.pack(padx=(10,0),side=RIGHT)

    y = compare_versions(version, latest_version)
    # y = 1
    global bg_color
    global fg_color
    global font_size

    frame_root_chat.pack_forget()
    settings_window.pack(fill=BOTH, expand=Y)
    root_chat.resizable(False, False)


    if y == -1:
        print(f"Доступна новая версия: {latest_version}")
        btn_update.pack(side=BOTTOM, fill=X, padx=5, pady=5)
        lbl_news_update.configure(text = 'Доступно обновление!')
        lbl_news_update.pack(side=BOTTOM)
    else:
        lbl_news_update.configure(text = 'Обновлений не найдено')
        lbl_news_update.pack(side=BOTTOM)
        print('Нет обновлений')
    
def animations_text():
    global delay, delay_state

    if (delay_state == "ВКЛ"):
      delay_state="ВЫКЛ"
      btn_delay.configure(text=delay_state)
      delay = 0
    else:
      delay_state = "ВКЛ"
      btn_delay.configure(text=delay_state)
      delay = 25

def close_setting():
    if premium == False:
        lbl_premium.pack_forget()
        btn_link.pack_forget()
        btn_qr.pack_forget()
    settings_window.pack_forget()
    frame_root_chat.pack(side = RIGHT,fill=BOTH, expand=YES)
    root_chat.resizable(True, True)
    message_input.focus()
    

def clear_chat():
    text_chat.configure(state="normal")
    text_chat.delete("1.0", END)
    text_chat.insert(END,welcome_text)
    text_chat.configure(state="disabled",fg=bg_color_dark)


# создаем функцию для изменения размера окна ввода сообщений
def expand_text_input():
    global expand_button_text
    if (expand_button_text == "↑"):
        expand_button_text = "↓"
        expand_button.configure(text = expand_button_text)
        message_input.configure(height=20)  # увеличиваем высоту окна ввода сообщений

    elif (expand_button_text == "↓"):
        expand_button_text = '↑'
        expand_button.configure(text = expand_button_text)
        message_input.configure(height=2)


def check_duplicate_login(login):
    with open("data/data.txt", 'r') as f:
        for line in f:
            if 'login: ' in line:
                saved_login = line.replace('login: ','').strip()
                if login == saved_login:
                    return True
    return False

def chek_online(user_login, text):
    print("Запус смены статуса")
    g = Github(token_git)
    repo = g.get_repo("Falbue/chenk-data")
    file_content = repo.get_contents("data.txt").decoded_content
    with open("data/data.txt", "wb") as f:
        f.write(file_content)
    try:
        with open('data/data.txt', 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 8):
                login_data = lines[i+0].replace('login: ','').strip()
                online = lines[i+6].replace('on-line: ','').strip()
                if user_login == login_data:
                    online = text
                    with open("data/data.txt", "r") as f:
                        for i, line in enumerate(f):
                            if f"login: {login_data}" in line:
                                stroke = i
                                print(f"Строка c логином '{f.name}' на {i+1}-й строке")
                    file = repo.get_contents("data.txt")
                    contents = file.decoded_content.decode("utf-8")
                    lines = contents.split("\n")
                    # Изменение строки номер 5
                    lines[stroke+6] = f'on-line: {online}'
                    # Объединение строк в новый контент файла
                    new_contents = "\n".join(lines)
                    if text == "yes":
                        commit_text = "вошёл в сеть"
                    if text == "no":
                        commit_text = "вышел из сети"
                        root_chat.destroy()
                    repo.update_file(
                        path="data.txt",
                        message=f"{login_data} {commit_text}",
                        content=new_contents,
                        sha=file.sha
                    )
    except Exception as e:
        print("Ошибка: "+str(e))
    delete_data()

def save_data():
    global login, passw, api, user, bot
    global token, username, repo_name, file_name, content, commit_message, registration

    # Аутентификация с использованием access token
    g = Github(token_git)

    # Получение репозитория по имени владельца и имени репозитория
    repo = g.get_repo("Falbue/chenk-data")

    # Получение содержимого файла по его имени и SHA-хешу последнего коммита
    file_content = repo.get_contents("data.txt").decoded_content

    # Сохранение содержимого в файл на локальном диске
    with open("data/data.txt", "wb") as f:
        f.write(file_content)


    login = entry_username.get()

    if check_duplicate_login(login):
        error_message_login.configure(text='Пользователь с таким логином уже зарегистрирован')
        os.remove("data/data.txt")
        return
    passw = entry_password.get()
    confirm_password = entry_confirm_password.get()

    # проверяем совпадение паролей
    if passw != confirm_password:
        error_message_login.configure(text='Пароли не совпадают')
        os.remove("data/data.txt")
        return
    # проверяем длину пароля
    if len(passw) < 5:
        error_message_login.configure(text='Пароль должен быть не короче 5 символов')
        os.remove("data/data.txt")
        return
    # проверяем логин на английские символы
    if not all(c.isalpha() and ord(c) < 128 for c in login):
        error_message_login.configure(text='Логин может содержать только английские буквы')
        os.remove("data/data.txt")
        return

    success_message_login.configure(text='Регистрация прошла успешно')
    user = 'User'
    bot = 'Bot'

    content = 'login: ' + login + '\n' + 'password: ' + passw + '\n' + 'api: ' + "none" + '\n' + 'user: ' + user + '\n' + 'bot: ' + bot + '\n' + "version: " + version + '\n' + "on-line: no"+ "\n"
    commit_message = login + ' зарегистрировался'
    update_data(token_git, username_git, repo_name, file_name, content, commit_message)
    file.close()
    os.remove("data/data.txt")
    registration = True
    check_data()




def check_data():
    global login, passw, api, user, bot, version, welcome_text, latest_version, premium, registration
    # получаем данные из текстовых полей
    if registration == False:
        username_sign = entry_username_sign.get()
        password_sign = entry_password_sign.get()
    elif registration == True:
        username_sign = entry_username.get()
        password_sign = entry_password.get()
        registration = False

    # Аутентификация с использованием access token
    g = Github(token_git)

    # Получение репозитория по имени владельца и имени репозитория
    repo = g.get_repo("Falbue/chenk-data")
    # Получение содержимого файла по его имени и SHA-хешу последнего коммита
    file_content = repo.get_contents("data.txt").decoded_content

    repo = g.get_repo("Falbue/ChenkGPT")
    latest_release = repo.get_latest_release()
    latest_version = latest_release.tag_name
    latest_version = latest_version[1:]
    # Сохранение содержимого в файл на локальном диске
    with open("data/data.txt", "wb") as f:
        f.write(file_content)

    # проверяем совпадение логинов и паролей
    try:
        with open('data/data.txt', 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 8):
                login = lines[i+0].replace('login: ','').strip()
                passw = lines[i+1].replace('password: ','').strip()
                text_api = lines[i+2].replace('api: ','').strip()
                user = lines[i+3].replace('user: ','').strip()
                bot = lines[i+4].replace('bot: ','').strip()
                online = lines[i+6].replace('on-line: ','').strip()
                if username_sign == login and online == "no":  
                    if username_sign == login and text_api == 'none': # исправить условие
                        premium = False
                        decrypt(text_api, shift)
                        text_api = lines[2].replace('api: ','').strip()
                        api = decrypt(text_api, shift)
                        print (api)
                    else:
                        decrypt(text_api, shift)
                        api = decrypt(text_api, shift)
                    if username_sign == login and password_sign == passw:
                        success_message_sign.configure(text='Авторизация успешна')
                        openai.api_key = api
                        root_login.pack_forget()
                        frame_root_chat.pack(side = RIGHT,fill=BOTH, expand=YES)
                        root_chat.resizable(True, True)
                        file.close()
                        os.remove("data/data.txt")
                        chek_online(login, "yes")
                        welcome_text = welcome_text + f"{version}"
                        clear_chat()
                        message_input.focus()
                        return
                if username_sign == login and online == "yes": 
                    error_message_sign.configure(text='Вы уже вошли свой аккаунт на другом устройсте!')
                    return
                    
    except Exception as e:
        error_message_sign.configure(text='Данная версия больше не поддерживается!\nПросьба обновить версию в ручную')
        btn_offline_update = button(sign_frame, "Ручное обновление", github_link)
        btn_offline_update.pack(side=BOTTOM, fill = "x", padx=5)
        print(e)
        return

    error_message_sign.configure(text='Неверный логин или пароль')
    file.close()
    os.remove("data/data.txt")


def clear_error_message(event):
    error_message_login.configure(text='')
    error_message_sign.configure(text='')


def login():
  btn_sign.configure(state = 'normal')
  btn_login.configure(state = 'disabled')
  sign_frame.pack_forget()
  login_frame.pack(pady=20)
  button_submit_sign.pack_forget()
  button_submit_login.pack(side=BOTTOM, fill='x', pady=5, padx=5)

def sign():
  btn_sign.configure(state = 'disabled')
  btn_login.configure(state = 'normal')
  sign_frame.pack(pady=20)
  login_frame.pack_forget()
  button_submit_login.pack_forget()
  button_submit_sign.pack(side=BOTTOM, fill='x', pady=5, padx=5)


def copy_text():
    selected_text = message_input.get("sel.first", "sel.last")
    root_chat.clipboard_clear()
    root_chat.clipboard_append(selected_text)
def insert_text():
    text = root_chat.clipboard_get()
    message_input.insert(tk.END, text)
def copy_text2():
    selected_text = text_chat.get("sel.first", "sel.last")
    root_chat.clipboard_clear()
    root_chat.clipboard_append(selected_text)

def open_link():
    webbrowser.open("https://t.me/ChenkGPT_bot")
def open_qr():
    btn_qr.configure(state = "disabled")
    root = Tk()
    root.geometry('1x1')
    image = PhotoImage(file="data/img/tg_link.png")
    image = image.subsample(x=3, y=3)
    label = Label(settings_window, image=image)
    label.pack()
    root.after(1, root.destroy)  # Закрыть окно через 3 секунды
    root.mainloop()
    print("qr")

def github_link():
    webbrowser.open("https://github/Falbue/ChenkGPT/releases")

try:
    os.remove("installer.exe")# Указываем имя папки, которую нужно удалить
except:
    print('Установщик уже удалён')
try:
    folder_name = f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT_download"
    # Используем функцию os.rmdir() для удаления папки
    shutil.rmtree(folder_name)
except:
    print("Папка уже удалена")


# -------------------------------------
# создаем главное окно
root_chat = Tk()
root_chat.protocol("WM_DELETE_WINDOW", lambda: chek_online(login, "no"))
icon = PhotoImage(file = "data/img/ico.png")
root_chat.iconphoto(False, icon)
root_chat.title('ChenkGPT')
root_chat.geometry('400x600')
root_chat.wm_minsize(400, 600)
# root_chat.resizable(False, False)
root_chat.configure(bg=bg_color_dark)



frame_root_chat = frame(root_chat)

def on_resize(event):
    global active_setting
    screen_width = root_chat.winfo_screenwidth()
    max_width = int(screen_width * 0.6)
    width = root_chat.winfo_width()
    if width > max_width and premium == True:
        settings_window.pack(side = LEFT, fill=BOTH)
        btn_settings.pack_forget()
        btn_close.pack_forget()
        lbl_news_update.pack_forget()
        settings_window.configure(width = 350)
    else:
        btn_settings.pack(side=LEFT, padx = (5, 0))
        btn_close.pack(side=BOTTOM, fill=X, padx=5, pady=5)
        settings_window.pack_forget()
frame_root_chat.bind("<Configure>", on_resize)




frame_chat = frame(frame_root_chat)
# создаем текстовое поле для чата
text_chat = Text(
    frame_chat,
    height=1,
    wrap="word",
    font=(fonts, font_size-4),
    padx = 20,
    pady = (20),
    bg=bg_color,
    fg=fg_color,
    relief='flat',
    border = 1, 
    selectbackground="#87CEFA",
    cursor="arrow")

popup_menu = Menu(frame_chat, tearoff=0, bg=bg_color_dark, font=(fonts, font_size-6), fg = fg_color,activebackground = bg_color)
popup_menu.add_command(label="Копировать", command = copy_text2)
text_chat.bind("<Button-3>", lambda e: popup_menu.post(e.x_root, e.y_root))
text_chat.bind("<Button-1>", lambda e: popup_menu.unpost())

frame_chat.pack(fill=BOTH, expand=True)
text_chat.configure(state='disabled',fg=bg_color_dark)

lbl_copy = Label(text='Текст скопирован')

# создаем слайдер для текст чата
scrollbar_chat = Scrollbar(
    frame_chat,
    width=12,
    bg='red',
    troughcolor='red')
scrollbar_chat.pack(side=RIGHT, fill='y')
scrollbar_chat.bind("<FocusIn>", lambda event: scrollbar_chat.configure(width = 20))
# устанавливаем связь между слайдером и текстом чата
scrollbar_chat.configure(command=text_chat.yview)
# устанавливаем параметры для текстового поля и добавляем на главное окно
text_chat.configure(yscrollcommand=scrollbar_chat.set)
# устанавливаем параметры для слайдера и добавляем на главное окно
text_chat.pack(fill=BOTH, expand=True)
expand_button_frame = frame(frame_root_chat)
# создаем кнопку для изменения размера окна ввода сообщений


frame_btn = frame(frame_root_chat)
frame_btn.configure(height=40)
# создаем окно ввода сообщений
message_input = Text(
    frame_btn,
    wrap="word",
    height=2,
    font=(fonts, font_size-4),
    padx = 5,
    width=10,
    bg=bg_color,
    fg=fg_color,
    relief = 'solid', )
# Создаем контекстное меню
popup_menu_input = Menu(frame_btn,
   tearoff=0,
   relief = 'solid',
   activebackground=bg_color_dark,
   bg = bg_color,
   font = (fonts, font_size-6))
popup_menu_input.add_command(label="Копировать", command = copy_text)
popup_menu_input.add_command(label="Вставить", command = insert_text)
message_input.bind("<Button-3>", lambda e: popup_menu_input.post(e.x_root, e.y_root))
message_input.bind("<Button-1>", lambda e: popup_menu_input.unpost())

# устанавливаем сочетание клавиш для отправки сообщения (Ctrl + Enter)
message_input.bind('<Control-Return>', lambda event: btn_send.invoke())
lexer = PythonLexer()
# Создаем теги с разными свойствами, которые будем присваивать соответствующим типам токенов
message_input.tag_config("blue_tag", foreground="#67d8ef")
message_input.tag_config("yellow_tag", foreground='#e7c855')
message_input.tag_config("red_tag", foreground='#f9245e')
message_input.tag_config("green_tag", foreground='#a6e22b')
message_input.tag_config("orange_tag", foreground='#fd8a22')
message_input.tag_config("purple_tag", foreground='#ac80ff')
message_input.tag_config("comment_tag", foreground="#808080")
token_type_to_tag = {
    Token.Keyword: "blue_tag", # ключевые слова
    Token.Literal.String.Single: "yellow_tag", # цвет в ковычках
    Token.Literal.String.Double: "yellow_tag",
    Token.Comment.Single: "comment_tag", # комментарии
    Token.Name.Builtin: "blue_tag", # встроенные функции
    Token.Operator: "red_tag", # операторы
    Token.Literal.Number.Integer: "purple_tag", # числа
    Token.Name.Function: "green_tag",
    Token.Literal.Number.Float: "purple_tag",
    Token.Keyword.Constant: "purple_tag"
}
def get_text_coord(s: str, i: int):
    """
    Из индекса символа получить "координату" в виде "номер_строки_текста.номер_символа_в_строке"
    """
    for row_number, line in enumerate(s.splitlines(keepends=True), 1):
        if i < len(line):
            return f'{row_number}.{i}'
        
        i -= len(line)
def on_edit(event):
    # Удалить все имеющиеся теги из текста
    for tag in message_input.tag_names():
        message_input.tag_remove(tag, 1.0, tk.END)
    
    # Разобрать текст на токены
    s = message_input.get(1.0, tk.END)
    tokens = lexer.get_tokens_unprocessed(s)
    
    for i, token_type, token in tokens:
        # print(i, token_type, repr(token))  # Отладочный вывод - тут видно какие типы токенов выдаются
        j = i + len(token)
        if token_type in token_type_to_tag:
            message_input.tag_add(token_type_to_tag[token_type], get_text_coord(s, i), get_text_coord(s, j))

    # Сбросить флаг редактирования текста
    message_input.edit_modified(0)
message_input.bind('<<Modified>>', on_edit)



frame_btn.configure(bg=bg_color_dark)
# создаем кнопки с помощью функции
btn_settings = button(frame_btn, '\u2699', settings)
btn_send = button(frame_btn, '→', btn_send_command)
expand_button = button(frame_btn, expand_button_text, expand_text_input)

expand_button.pack(side=LEFT, padx = (5, 0))
btn_settings.pack(side=LEFT, padx = (5, 0))
btn_send.pack(side=RIGHT)
message_input.pack(side='right', fill='both', expand=True, padx=5)

frame_btn.pack(fill='x', padx=(0, 5), pady=5)



# Настройки------------------
settings_window = frame(root_chat)
setting_frame = frame(settings_window)
frame_font_setting = frame(setting_frame)
frame_font_setting.pack(fill=X,pady=(10,5))
lbl_font = Label(
    frame_font_setting,
    bg = bg_color_dark,
    fg =fg_color,
    text = "Шрифт:",
    font = (fonts, font_size, "bold")
    )
lbl_font.pack(side = LEFT)


# Создаем переменную tk.StringVar
var = StringVar()
var.set(options[0])  # Задаем начальное значение
# Создаем виджет OptionMenu
option_menu = OptionMenu(frame_font_setting, var, *options, command=select_fonts,)
option_menu.configure(
    font = (fonts, font_size),
    relief='solid',
    border=1,
    bg = bg_color,
    activebackground = bg_color_dark,
    highlightbackground = 'black',
    highlightthickness = 0)
option_menu["menu"].configure(bg=bg_color_dark, font=(fonts, font_size-4), fg = fg_color,activebackground = bg_color, activeforeground = fg_color)
option_menu.pack(side=LEFT, padx=5)

var_size = StringVar()
var_size.set(options_size[4])

option_menu_size = OptionMenu(frame_font_setting, var_size, *options_size, command=select_font_size)
option_menu_size.configure(
    font = (fonts, font_size),
    relief='solid',
    border=1,
    bg = bg_color,
    activebackground = bg_color_dark, 
    highlightbackground = 'black',
    highlightthickness = 0)
option_menu_size["menu"].configure(bg=bg_color_dark, font=(fonts, font_size-4), fg = fg_color,activebackground = bg_color, activeforeground = fg_color)
option_menu_size.pack(side = RIGHT)

frame_button_color = frame(setting_frame)
frame_button_color.configure(height=30)
btn_color = button(frame_button_color, text="Изменить цвет", command=change_colors)
btn_clear = button(frame_button_color, text="Сбросить", command=clear_colors)
btn_color.pack(side = LEFT)
btn_clear.pack(padx=(10,0),side=RIGHT)

lbl_premium = label(frame_button_color, "Полная версия:")
btn_link = button(frame_button_color, text = "Открыть ссылку", command=open_link)
btn_qr = button(frame_button_color, text = "Открыть qr код", command = open_qr)

    
frame_delay = frame(setting_frame)
label_delay = Label(
  frame_delay,
  bg = bg_color_dark,
  text = "Анимация текста:",
  font=(fonts, 16,"bold"))
btn_delay = button(
  frame_delay,
  text = delay_state,
  command = animations_text)
label_delay.pack(side = LEFT)
btn_delay.pack(side = RIGHT)

btn_clear_chat = button(setting_frame, 'Очистить чат', clear_chat)

btn_sapper = button(setting_frame, 'Сапёр', sapper)

btn_close = button(settings_window, text="Закрыть", command=close_setting)
btn_close.pack(side=BOTTOM, fill=X, padx=5, pady=5)

lbl_news_update = Label(
    settings_window, 
    text = '',
    fg = bg_color,
    bg = bg_color_dark,
    font=(fonts, font_size,"bold"))
btn_update = button(settings_window, text='Обновить', command = update_chenkgpt)


# Установка фреймов
setting_frame.pack()
frame_button_color.pack(side=TOP, pady=5, fill=X)
frame_delay.pack( pady=5, fill=X)
btn_clear_chat.pack(pady=5, fill=X)
btn_sapper.pack(pady = 10, fill=X)





# Регистрация------------------
root_login = frame(root_chat)
root_login.pack(side = RIGHT, fill=BOTH, expand=YES)###########################################
# frame_root_chat.pack(side = RIGHT,fill=BOTH, expand=YES)
shift_frame = frame(root_login)

btn_sign = Button(
    shift_frame,
    text='Войти',
    font=(fonts, 16),
    relief = 'solid',
    border = 0,
    state = 'disabled',
    command = sign,
    bg = bg_color_dark,
    activebackground=bg_color_dark)
shift_text = Label(
    shift_frame,
    font=(fonts, 16),
    text=' / ',
    bg = bg_color_dark)

btn_login = Button(shift_frame,
    text='Регистрация',
    font=(fonts, 16),
    relief = 'solid',
    border = 0,
    command = login,
    bg = bg_color_dark,
    activebackground=bg_color_dark)
btn_help = button(shift_frame,text = "?", command = open_help)

btn_sign.pack(side=LEFT)
shift_text.pack(side=LEFT)
btn_login.pack(side=LEFT)
btn_help.pack(side = RIGHT, padx = (0, 1))
shift_frame.pack(side="top", anchor="nw", fill='x')


sign_frame = frame(root_login)

# создаем метки и текстовые поля для ввода данных
label_username_sign = label(sign_frame, text='Логин:')
label_username_sign.pack(side=TOP)
entry_username_sign = entry(sign_frame)
entry_username_sign.pack(pady=10)
entry_username_sign.focus_set()

label_password_sign = label(sign_frame, text='Пароль:')
label_password_sign.pack(side=TOP)
entry_password_sign = entry(sign_frame)
entry_password_sign.configure(show='*')
entry_password_sign.pack(pady=10)
# добавляем обработчик события нажатия на клавишу enter для каждого текстового поля
entry_username_sign.bind('<Return>', lambda event: entry_password_sign.focus())
entry_password_sign.bind('<Return>', lambda event: check_data())


# создаем кнопку для отправки данных
button_submit_sign = button(root_login, text='Войти', command=check_data)
button_submit_sign.configure()
button_submit_sign.pack(side=BOTTOM, fill='x', pady=5, padx=5)


# создаем метку для вывода сообщений об ошибках или успехе
error_message_sign = Label(sign_frame, fg='red', font=("System",16), wraplength=300, bg = bg_color_dark)
error_message_sign.pack(side=TOP, pady=30)
success_message_sign = Label(sign_frame, fg='green', font=("System",16), wraplength=300, bg = bg_color_dark)
success_message_sign.pack(side=TOP, pady=30)

entry_username_sign.bind('<Button-1>', clear_error_message)
entry_password_sign.bind('<Button-1>', clear_error_message)

sign_frame.pack(side=TOP, fill=BOTH, expand=True, pady=20)



login_frame = frame(root_login)

# создаем метки и текстовые поля для ввода данных
label_username = label(login_frame, text='Логин:')
label_username.pack()
entry_username = entry(login_frame)
entry_username.pack(pady=10)

label_password = label(login_frame, text='Пароль:')
label_password.pack()
entry_password = entry(login_frame)
entry_password.configure(show='*')
entry_password.pack(pady=10)

label_confirm_password = label(login_frame, text='Подтвердите пароль:')
label_confirm_password.pack()
entry_confirm_password = entry(login_frame)
entry_confirm_password.configure(show='*')
entry_confirm_password.pack(pady=10)


# создаем кнопку для отправки данных
button_submit_login = button(root_login, text='Зарегистрироваться', command=save_data)


# создаем метку для вывода сообщений об ошибках или успехе
error_message_login = Label(login_frame, fg='red', wraplength=300, font=("System",16), bg = bg_color_dark) 
error_message_login.pack(pady=20)
success_message_login = Label(login_frame, fg='green', font=("System",16), wraplength=300, bg = bg_color_dark) 
success_message_login.pack(pady=20)

entry_username.bind('<Button-1>', clear_error_message)
entry_password.bind('<Button-1>', clear_error_message)
entry_confirm_password.bind('<Button-1>', clear_error_message)



frame_info = frame(root_login)

lbl_info = Label(
    frame_info,
    text = info,
    font = (fonts, font_size-4),
    anchor="e",
    wraplength=390, justify=LEFT,
    bg = bg_color_dark)
lbl_info.pack()

btn_exit = button(frame_info, text = "Выйти", command = close_info)
btn_exit.pack(side=BOTTOM, fill='x', pady=5, padx=5)


# запускаем графический интерфейс
root_chat.mainloop()