version = '1.1.9'

import os
from tkinter import *
import tkinter as tk
import random
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askinteger
import time
import requests
import threading

import openai
from github import Github

game_over = False

active_setting = True

bg_color = "#FFFFFF"
fg_color = "#000000"
bg_color_dark = 'gray90'

# Данные для гитхаба
token_git = 'klt_Jfj6NuRT0XWBEyeBu9AVPw24XLYGWy4jIJg2'  # До первого сентября
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
fonts = "Arial"
options = ["Arial", "Consolas", "Calibri", "Courier", "Times New Roman", "Verdana", "Tahoma"]


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

info = f'''Что это?

ChenkGPT - это бот, созданный на основе api компании "openai"
Модель, на которой работает ChenkGPT, аналогична модели ChatGPT

Для чего предназначен ChenkGPT?

ChenkGPT был создан, для студентов ЧэНКа, что бы облегчить создание сайтов, и написание кода
Ботом так же можно пользоваться и дома, если Вам нужно

Как пользоваться?

Нужно зарегестрироваться или войти, и можно приступать к взаимодействию с Ботом



По всем вопросом обращаться:
chenkgpt@gmail.com'''


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

def delete_data(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Файл {filename} Успешно удалён")
    else:
        print(f"Файл {filename} не удалён")


def send_api():
    global answer
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "assistant", "content": question}]
            )
        print("Бот дал ответ")
        answer = completion.choices[0].message.content
        message_input.configure(state = "normal")
    except Exception as e:
        answer = str(f'Произошла ошибка: {e}')
        btn_send.configure(state="normal")
        print(f"Произошла ошибка: {e}")
        message_input.configure(state = "normal")
    


    def show_text_slowly(text):
            global delay
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




# функция, которая вызывается при нажатии кнопки "Отправить"
def btn_send_command():
    global text_error, question
    text_chat.configure(bg=bg_color, fg=fg_color)
    check = text_chat.get("1.0", END).strip('\n')
    if check == welcome_text:
        text_chat.configure(state="normal")
        text_chat.delete("1.0", END)
        text_chat.configure(state="disabled")
    question = message_input.get("1.0", END).strip('\n')
    message_input.delete("1.0", END)
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
    


def mutable_objects(): # Изменяемые объекты
    text_chat.configure(bg=bg_color, fg=fg_color, font = (fonts, font_size-4))
    text_chat.tag_configure("quote", font = (fonts, font_size-4))
    text_chat.tag_configure("bold", font = (fonts, font_size-4, "bold"))
    message_input.configure(bg=bg_color, fg=fg_color, font = (fonts, font_size-4))
    scrollbar_chat.configure(background = bg_color, troughcolor = bg_color_dark)

    btn_send.configure(bg=bg_color, activebackground=bg_color_dark, fg=fg_color, font = (fonts, font_size))
    btn_settings.configure(bg=bg_color, activebackground=bg_color_dark, fg=fg_color, font = (fonts, font_size))
    btn_clear_chat.configure(bg=bg_color, activebackground=bg_color_dark, fg=fg_color, font = (fonts, font_size))
    expand_button.configure(bg = bg_color, activebackground = bg_color_dark, fg = fg_color, font = (fonts, font_size))

    root_chat.configure(bg=bg_color_dark)

    frame_root_chat.configure(bg = bg_color_dark)
    frame_btn.configure(bg=bg_color_dark)
    frame_chat.configure(bg=bg_color_dark)
    expand_button_frame.configure(bg = bg_color_dark)


    btn_color.configure(bg=bg_color, fg=fg_color, activebackground=bg_color_dark, font = (fonts, font_size))
    btn_clear.configure(bg=bg_color, fg=fg_color, activebackground=bg_color_dark, font = (fonts, font_size))
    btn_sapper.configure(bg = bg_color, fg = fg_color, activebackground = bg_color_dark, font = (fonts, font_size))
    btn_close.configure(bg=bg_color, fg=fg_color, activebackground=bg_color_dark, font = (fonts, font_size))
    btn_delay.configure(bg=bg_color, fg=fg_color, activebackground=bg_color_dark, font = (fonts, font_size))
    label_delay.configure(fg = fg_color, bg = bg_color_dark, font = (fonts, font_size, "bold"))
    btn_update.configure(fg = fg_color, bg = bg_color, activebackground=bg_color_dark, font = (fonts, font_size))

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
    with open("data.txt", "wb") as f:
        f.write(file_content)

    with open("data.txt", "r") as f:
        for i, line in enumerate(f):
            if f"login: {login}" in line:
                stroke = i
                print(f"Строка c логином '{f.name}' на {i+1}-й строке")
    file = repo.get_contents("data.txt")
    contents = file.decoded_content.decode("utf-8")
    lines = contents.split("\n")

    # Изменение строки номер 5
    lines[stroke+5] = f'version: {updating_vesion}'

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
    os.remove("data.txt")
    root_chat.destroy()
    


 # добавим настройки окна
def settings():
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
    settings_window.pack_forget()
    frame_root_chat.pack(fill = BOTH, expand = True)
    root_chat.resizable(True, True)
    

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
    with open(file_name, 'r') as f:
        for line in f:
            if 'login: ' in line:
                saved_login = line.replace('login: ','').strip()
                if login == saved_login:
                    return True
    return False


def save_data():
    global login, passw, api, user, bot
    global token, username, repo_name, file_name, content, commit_message

    # Аутентификация с использованием access token
    g = Github(token_git)

    # Получение репозитория по имени владельца и имени репозитория
    repo = g.get_repo("Falbue/chenk-data")

    # Получение содержимого файла по его имени и SHA-хешу последнего коммита
    file_content = repo.get_contents("data.txt").decoded_content

    # Сохранение содержимого в файл на локальном диске
    with open("data.txt", "wb") as f:
        f.write(file_content)


    login = entry_username.get()

    if check_duplicate_login(login):
        error_message_login.configure(text='Пользователь с таким логином уже зарегистрирован')
        os.remove("data.txt")
        return
    passw = entry_password.get()
    confirm_password = entry_confirm_password.get()
    api = entry_api_key.get()


    

    # проверяем совпадение паролей
    if passw != confirm_password:
        error_message_login.configure(text='Пароли не совпадают')
        os.remove("data.txt")
        return
    # проверяем длину пароля
    if len(passw) < 5:
        error_message_login.configure(text='Пароль должен быть не короче 5 символов')
        os.remove("data.txt")
        return
    # проверяем логин на английские символы
    if not all(c.isalpha() and ord(c) < 128 for c in login):
        error_message_login.configure(text='Логин может содержать только английские буквы')
        os.remove("data.txt")
        return
    # проверяем длину api ключа
    if len(api) < 40:
        error_message_login.configure(text='API ключ должен быть не короче 40 символов')
        os.remove("data.txt")
        return

    success_message_login.configure(text='Регистрация прошла успешно')
    user = 'User'
    bot = 'Bot'

    text_api = api
    encrypted_api = encrypt(text_api, shift)

    content = 'login: ' + login + '\n' + 'password: ' + passw + '\n' + 'api: ' + encrypted_api + '\n' + 'user: ' + user + '\n' + 'bot: ' + bot + '\n'
    commit_message = login + ' зарегистрировался'
    update_data(token_git, username_git, repo_name, file_name, content, commit_message)
    # file.close()
    os.remove("data.txt")


    root_login.pack_forget()
    frame_root_chat.pack(fill=BOTH, expand=YES)
    root_chat.resizable(True, True)


def check_data():
    global login, passw, api, user, bot, version, welcome_text, latest_version
    # получаем данные из текстовых полей
    username_sign = entry_username_sign.get()
    password_sign = entry_password_sign.get()

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
    with open("data.txt", "wb") as f:
        f.write(file_content)

    # проверяем совпадение логинов и паролей
    try:
        with open('data.txt', 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 7):
                login = lines[i+0].replace('login: ','').strip()
                passw = lines[i+1].replace('password: ','').strip()
                text_api = lines[i+2].replace('api: ','').strip()
                user = lines[i+3].replace('user: ','').strip()
                bot = lines[i+4].replace('bot: ','').strip()

                decrypt(text_api, shift)
                api = decrypt(text_api, shift)
                if username_sign == login and password_sign == passw:
                    success_message_sign.configure(text='Авторизация успешна')
                    openai.api_key = api
                    root_login.pack_forget()
                    frame_root_chat.pack(fill=BOTH, expand=YES)
                    root_chat.resizable(True, True)
                    file.close()
                    os.remove("data.txt")
                    welcome_text = welcome_text + f"{version}"
                    clear_chat()
                    return
                    
    except Exception as e:
        error_message_sign.configure(text='Неверный логин или пароль')
    error_message_sign.configure(text='Неверный логин или пароль')
    file.close()
    os.remove("data.txt")


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

def sapper():
    class Minesweeper:
        def __init__(self, master, width=16, height=16, mines=42): #Иван Вячеславович Шапельский ебаный пидарас
            self.master = master
            self.width = width
            self.height = height
            self.mines = mines
            self.game_over = False
            self.create_widgets()
            self.create_board()
            self.place_mines()
            self.calculate_adj()
        def create_widgets(self):
            self.buttons = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    button = tk.Button(self.master, width=2, bg='grey')
                    button.configure(font = ("Arial", 12, "bold"), width = 2)
                    button.grid(row=i, column=j)
                    button.bind('<Button-1>', lambda e, i=i, j=j: self.button_click(i, j))
                    button.bind('<Button-3>', lambda e, i=i, j=j: self.button_flag(i, j))
                    row.append(button)
                self.buttons.append(row)
        def create_board(self):
            self.board = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    row.append(0)
                self.board.append(row)
        def place_mines(self):
            mines = self.mines
            while mines > 0:
                i = random.randint(0, self.height-1)
                j = random.randint(0, self.width-1)
                if self.board[i][j] == 0:
                    self.board[i][j] = '*'
                    mines -= 1
        def calculate_adj(self):
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j] != '*':
                        count = 0
                        if i > 0 and j > 0 and self.board[i-1][j-1] == '*':
                            count += 1
                        if i > 0 and self.board[i-1][j] == '*':
                            count += 1
                        if i > 0 and j < self.width-1 and self.board[i-1][j+1] == '*':
                            count += 1
                        if j > 0 and self.board[i][j-1] == '*':
                            count += 1
                        if j < self.width-1 and self.board[i][j+1] == '*':
                            count += 1
                        if i < self.height-1 and j > 0 and self.board[i+1][j-1] == '*':
                            count += 1
                        if i < self.height-1 and self.board[i+1][j] == '*':
                            count += 1
                        if i < self.height-1 and j < self.width-1 and self.board[i+1][j+1] == '*':
                            count += 1
                        self.board[i][j] = count
        def button_click(self, i, j):
            if self.game_over:
                return
            if self.board[i][j] == '*':
                self.game_over = True
                for i in range(self.height):
                    for j in range(self.width):
                        if self.board[i][j] == '*':
                            self.buttons[i][j].configure(bg='red', text='*')
                        elif self.board[i][j] != 0:
                            self.buttons[i][j].configure(text=self.board[i][j])
            else:
                self.show_button(i, j)
        def show_button(self, i, j):
            if i < 0 or i >= self.height or j < 0 or j >= self.width:
                return
            button = self.buttons[i][j]
            if button['state'] == tk.DISABLED:
                return
            text = self.board[i][j]
            if text == 0:
                button.configure(text='', state=tk.DISABLED, background = 'white')
                self.show_button(i-1, j-1)
                self.show_button(i-1, j)
                self.show_button(i-1, j+1)
                self.show_button(i, j-1)
                self.show_button(i, j+1)
                self.show_button(i+1, j-1)
                self.show_button(i+1, j)
                self.show_button(i+1, j+1)
            else:
                if text == 1:
                    button.configure(text=text, fg='blue')
                elif text == 2:
                    button.configure(text=text, fg='green')
                elif text == 3:
                    button.configure(text=text, fg='red')
                elif text == 4:
                    button.configure(text=text, fg='purple')
                elif text == 5:
                    button.configure(text=text, fg='maroon')
                elif text == 6:
                    button.configure(text=text, fg='turquoise')
                elif text == 7:
                    button.configure(text=text, fg='black')
                elif text == 8:
                    button.configure(text=text, fg='gray')
                button.configure(text=text, bg='white')
        def button_flag(self, i, j):
            if self.buttons[i][j]['text'] == '🚩':
                self.buttons[i][j].configure(text='', fg='black')
            else:
                self.buttons[i][j].configure(text='🚩')
    root_sapper = tk.Tk()
    root_sapper.title('Minesweeper')
    root_sapper.resizable(False, False)
    game = Minesweeper(root_sapper)
    root_sapper.mainloop()




try:
    os.remove("installer.exe")
except:
    print('Установщик уже удалён')




              

# -------------------------------------
# hello_window()
# создаем главное окно
root_chat = Tk()
try:
    icon = PhotoImage(file = "data/imgico.png")
    root_chat.iconphoto(False, icon)
except:
    print("Ошибка загрузки иконки")
root_chat.title('ChenkGPT')
root_chat.geometry('400x600')
root_chat.wm_minsize(400, 600)
# root_chat.resizable(False, False)
root_chat.configure(bg=bg_color_dark)




def on_resize(event):
    global active_setting
    root_chat.update_idletasks()
    screen_width = root_chat.winfo_screenwidth()
    max_width = int(screen_width * 0.7)
    width = root_chat.winfo_width()
    if width > max_width:
        btn_settings.pack_forget()
        settings_window.pack(side = LEFT, fill=BOTH)
        settings_window.configure(width = 350)
        btn_close.pack_forget()
    else:
        # close_setting()
        btn_settings.pack(side=LEFT, padx = (5, 0))
        btn_close.pack(side=BOTTOM, fill=X, padx=5, pady=5)

if active_setting == False: # менять на тру, что бы работало
    root_chat.bind("<Configure>", on_resize)

frame_root_chat = Frame(root_chat, bg = bg_color_dark)


frame_chat = Frame(frame_root_chat)
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

frame_chat.pack(fill=BOTH, expand=True)
text_chat.configure(state='disabled',fg=bg_color_dark)

lbl_copy = Label(text='Текст скопирован')

# создаем слайдер для текст чата
scrollbar_chat = Scrollbar(
    frame_chat,
    width=10,
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
expand_button_frame = Frame(frame_root_chat, bg = bg_color_dark)
# создаем кнопку для изменения размера окна ввода сообщений


frame_btn = Frame(frame_root_chat,height=40)
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
# устанавливаем фокус на окно ввода сообщений
message_input.focus()
# устанавливаем сочетание клавиш для отправки сообщения (Ctrl + Enter)
message_input.bind('<Control-Return>', lambda event: btn_send.invoke())



frame_btn.configure(bg=bg_color_dark)
# создаем кнопки с помощью функции
btn_settings = create_button(frame_btn, '\u2699', settings)
btn_send = create_button(frame_btn, '→', btn_send_command)


expand_button = create_button(frame_btn, text=expand_button_text, command=expand_text_input)
expand_button.configure(font=(fonts, 16,"bold"))
expand_button.pack(side=LEFT, padx = (5, 0))

btn_settings.pack(side=LEFT, padx = (5, 0))
btn_send.pack(side=RIGHT)
message_input.pack(side='right', fill='both', expand=True, padx=5)

frame_btn.pack(fill='x', padx=(0, 5), pady=5)



# Настройки------------------
settings_window = Frame(root_chat, bg=bg_color_dark)
setting_frame = Frame(settings_window, bg=bg_color_dark)
frame_font_setting = Frame(setting_frame, bg = bg_color_dark)
frame_font_setting.pack(fill=X)
lbl_font = Label(
    frame_font_setting,
    bg = bg_color_dark,
    fg =fg_color,
    text = "Шрифт:",
    font = (fonts, font_size, "bold")
    )
lbl_font.grid(row=0, column=0, padx=(0, 5), pady=5)


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
option_menu.grid(row=0, column=1, padx=5, pady=5)

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
option_menu_size.grid(row=0, column=2, padx=5, pady=5)

frame_button_color = Frame(setting_frame, height=30, bg=bg_color_dark)
btn_color = create_button(frame_button_color, text="Изменить цвет", command=change_colors)
btn_clear = create_button(frame_button_color, text="Сбросить", command=clear_colors)
btn_color.grid(row=0, column=0, padx=(0, 5), pady=5)
btn_clear.grid(row=0, column=1, padx=5, pady=5)

    
frame_delay = Frame(setting_frame, bg=bg_color_dark)
label_delay = Label(
  frame_delay,
  bg = bg_color_dark,
  text = "Анимация текста:",
  font=(fonts, 16,"bold"))
btn_delay = create_button(
  frame_delay,
  text = delay_state,
  command = animations_text)
label_delay.grid(row=0, column=0, padx=(0, 5), pady=5)
btn_delay.grid(row=0, column=1, padx=5, pady=10)

btn_clear_chat = create_button(setting_frame, 'Очистить чат', clear_chat)

btn_sapper = create_button(setting_frame, 'Сапёр', sapper)

btn_close = create_button(settings_window, text="Закрыть", command=close_setting)
btn_close.pack(side=BOTTOM, fill=X, padx=5, pady=5)

lbl_news_update = Label(
    settings_window, 
    text = '',
    fg = bg_color,
    bg = bg_color_dark,
    font=(fonts, font_size,"bold"))
btn_update = create_button(settings_window, text='Обновить', command = update_chenkgpt)


# Установка фреймов
setting_frame.pack()
frame_button_color.pack(side=TOP, pady=5, fill=X)
frame_delay.pack( pady=5, fill=X)
btn_clear_chat.pack(pady=10, fill=X)
btn_sapper.pack(pady = 10, fill=X)





# Регистрация------------------
root_login = Frame(root_chat)
root_login.pack(side = RIGHT, fill=BOTH, expand=YES)###########################################
# frame_root_chat.pack(side = RIGHT,fill=BOTH, expand=YES)
shift_frame = Frame(root_login)

btn_sign = Button(
    shift_frame,
    text='Войти',
    font=(fonts, 16),
    relief = 'solid',
    border = 0,
    state = 'disabled',
    command = sign)
shift_text = Label(
    shift_frame,
    font=(fonts, 16),
    text=' / ')
btn_login = Button(
    shift_frame,
    text='Регистрация',
    font=(fonts, 16),
    relief = 'solid',
    border = 0,
    command = login)
btn_help = create_button(shift_frame,text = "?", command = open_help)

btn_sign.pack(side=LEFT)
shift_text.pack(side=LEFT)
btn_login.pack(side=LEFT)
btn_help.pack(side = RIGHT, padx = (0, 1))
shift_frame.pack(side="top", anchor="nw", fill='x')


sign_frame = Frame(root_login)

# создаем метки и текстовые поля для ввода данных
label_username_sign = label_design(sign_frame, text='Логин:')
label_username_sign.pack(side=TOP)
entry_username_sign = entry_design(sign_frame)
entry_username_sign.pack(pady=10)
entry_username_sign.focus_set()

label_password_sign = label_design(sign_frame, text='Пароль:')
label_password_sign.pack(side=TOP)
entry_password_sign = entry_design(sign_frame)
entry_password_sign.configure(show='*')
entry_password_sign.pack(pady=10)
# добавляем обработчик события нажатия на клавишу enter для каждого текстового поля
entry_username_sign.bind('<Return>', lambda event: entry_password_sign.focus())
entry_password_sign.bind('<Return>', lambda event: check_data())


# создаем кнопку для отправки данных
button_submit_sign = create_button(root_login, text='Войти', command=check_data)
button_submit_sign.configure()
button_submit_sign.pack(side=BOTTOM, fill='x', pady=5, padx=5)


# создаем метку для вывода сообщений об ошибках или успехе
error_message_sign = Label(sign_frame, fg='red', font=("System",16), wraplength=300)
error_message_sign.pack(side=TOP, pady=50)
success_message_sign = Label(sign_frame, fg='green', font=("System",16), wraplength=300)
success_message_sign.pack(side=TOP, pady=50)

entry_username_sign.bind('<Button-1>', clear_error_message)
entry_password_sign.bind('<Button-1>', clear_error_message)

sign_frame.pack(side=TOP, fill=BOTH, expand=True, pady=20)



login_frame = Frame(root_login)

# создаем метки и текстовые поля для ввода данных
label_username = label_design(login_frame, text='Логин:')
label_username.pack()
entry_username = entry_design(login_frame)
entry_username.pack(pady=10)

label_password = label_design(login_frame, text='Пароль:')
label_password.pack()
entry_password = entry_design(login_frame)
entry_password.configure(show='*')
entry_password.pack(pady=10)

label_confirm_password = label_design(login_frame, text='Подтвердите пароль:')
label_confirm_password.pack()
entry_confirm_password = entry_design(login_frame)
entry_confirm_password.configure(show='*')
entry_confirm_password.pack(pady=10)

label_api_key = label_design(login_frame, text='API ключ:')
label_api_key.pack()
entry_api_key = entry_design(login_frame)
entry_api_key.pack(pady=10)

# создаем кнопку для отправки данных
button_submit_login = create_button(root_login, text='Зарегистрироваться', command=save_data)


# создаем метку для вывода сообщений об ошибках или успехе
error_message_login = Label(login_frame, fg='red', wraplength=300, font=("System",16))
error_message_login.pack(pady=20)
success_message_login = Label(login_frame, fg='green', font=("System",16), wraplength=300)
success_message_login.pack(pady=20)

entry_username.bind('<Button-1>', clear_error_message)
entry_password.bind('<Button-1>', clear_error_message)
entry_confirm_password.bind('<Button-1>', clear_error_message)
entry_api_key.bind('<Button-1>', clear_error_message)



frame_info = Frame(root_login)

lbl_info = Label(
    frame_info,
    text = info,
    font = (fonts, font_size-4),
    anchor="e",
    wraplength=390, justify=LEFT)
lbl_info.pack()

btn_exit = create_button(frame_info, text = "Выйти", command = close_info)
btn_exit.pack(side=BOTTOM, fill='x', pady=5, padx=5)


# запускаем графический интерфейс
root_chat.mainloop()