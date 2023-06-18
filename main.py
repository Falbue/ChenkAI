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
# переменные для цветовой гаммы и размера шрифта
bg_color = "#FFFFFF"
fg_color = "#000000"

# Данные для гитхаба
token_git = 'klt_CxpoPFvnOs4zvMpUkWakMVlCBPC5KK0Fj3ET'
username_git = 'Falbue'
repo_name = 'chenk-data'
file_name = 'data.txt'

shift = 4

login = ''
passw = ''
api = ''
user = ''
bot = ''

#Более тёмные объекты
r, g, b = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
r = max(r - 30, 0)
g = max(g - 30, 0)
b = max(b - 30, 0)
bg_color_dark = f'#{r:02X}{g:02X}{b:02X}'

font_size = 12


delay = 25
delay_state = "ВКЛ"

expand_button_text = "↑"

text_error = ''
version = '1.1.4'
latest_version = '1.0.0'
online = ''

question = ''
answer = ''

welcome_text = f"""Привет. Это ChenkGPT


Инструкция:
1. Если окно зависло, значит бот грузит Ваш запрос
2. Для копирования и вставки текста, нужно переключится на английскую раскладку
3. Если окно уже не виснет, а бот ничего не присал, попробуйте отключить proxy сервер
3.1 Если вариант выше не помог, отключите Ethernet кабель, proxy сервер и подкючитесь с помощью Вашего смартфона через USB модем
4. По всем вопросам обращаться на почту: ChenkGPT@gmail.com

Falbue <3
version: """


# настройка кнопок
def create_button(frame, text, command):
    button = Button(
        frame,
        activebackground=bg_color_dark,
        font=("Arial", 16),
        bg='white',
        fg=fg_color,
        text=text,
        command=command,
        relief='solid',
        border=1,
        highlightbackground="black"
    )
    return button

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
        print(f'{file_name} обновлеён в репозитории {repo_name}')
    except Exception as e:
        print(f'Ошибка обновления файла {file_name} в {repo_name} репозитории: {e}')

def delete_data(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File {filename} deleted successfully")
    else:
        print(f"File {filename} does not exist")



def send_api():
    global answer
    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "assistant", "content": question}]
            )
    print(completion.choices[0].message.content)
    answer = completion.choices[0].message.content

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
                if char == "`" and i < len(text)-2 and text[i+1:i+3] == "``": # проверяем наличие тройных кавычек
                    in_triple_quotes = not in_triple_quotes # меняем значение переменной на противоположное при встрече тройных кавычек
                    if in_triple_quotes:
                        print(line_number)
                        text_chat.tag_add("quote", "end")  # добавляем тег "quote", если находимся внутри тройных кавычек
                    else:
                        text_chat.tag_remove("quote", "end-1c")  # удаляем тег "quote", если уже вышли за пределы тройных кавычек
                text_chat.insert(END, char, "bot" if not in_quotes and not in_triple_quotes else "quote")  # проверяем значение переменных и добавляем соответствующий тег
                text_chat.see("end")
                root_chat.update()
                text_chat.tag_configure("quote", background="black", foreground='white', selectbackground="#87CEFA")
                
                root_chat.after(delay)

            text_chat.insert(END, '\n', "bot")
            text_chat.tag_configure("bot", background=bg_color_dark, selectbackground="#87CEFA")
            text_chat.configure(state="disabled")
    show_text_slowly(answer)
    message_input.configure(state = 'normal')



# функция, которая вызывается при нажатии кнопки "Отправить"
def btn_send_command():
    global text_error, question
    try:
        text_chat.config(bg=bg_color, fg=fg_color)
        check = text_chat.get("1.0", END).strip('\n')
        if check == welcome_text:
            text_chat.configure(state="normal")
            text_chat.delete("1.0", END)
            text_chat.configure(state="disabled")
        question = message_input.get("1.0", END).strip('\n')
        message_input.delete("1.0", END)
        message_input.config(state = 'disabled')
        print("User: " + question)
        text_chat.configure(state="normal")
        text_chat.insert(END, '\n')
        text_chat.insert(END, user + ": ", "bold")
        text_chat.insert(END, question, "user")
        text_chat.tag_configure("user", background=bg_color, selectbackground="#87CEFA")
        text_chat.insert(END, '\n')
        text_chat.configure(state="disabled")
        text_chat.tag_configure("bold", font=("Arial", font_size, "bold"))
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
    except Exception as e:
        text_chat.configure(state="normal")
        text_chat.delete("bot_placeholder.first", "bot_placeholder.last")
        text_chat.insert(END, bot + ": ", "bold")
        text_chat.insert(END, "Извините, возникла ошибка:" + "\n", "null")
        text_chat.insert(END, str(e), "error")
        text_chat.tag_configure("error", font=("Arial", font_size, "bold"), foreground="#FF0000")
        text_chat.insert(END, '\n')
        text_chat.configure(state="disabled")
        text_error = e
        print(e)


def colors_objects(): # объекты, которые меняют цвета
    text_chat.configure(bg=bg_color, fg=fg_color)
    message_input.configure(bg=bg_color, fg=fg_color)
    scrollbar_chat.configure(background = bg_color, troughcolor = bg_color_dark)

    btn_send.configure(bg=bg_color, activebackground=bg_color_dark, fg=fg_color)
    btn_settings.configure(bg=bg_color, activebackground=bg_color_dark, fg=fg_color)
    btn_clear_chat.configure(bg=bg_color, activebackground=bg_color_dark, fg=fg_color)
    expand_button.configure(bg = bg_color, activebackground = bg_color_dark, fg = fg_color)

    root_chat.configure(bg=bg_color_dark)

    frame_root_chat.configure(bg = bg_color_dark)
    frame_btn.configure(bg=bg_color_dark)
    frame_chat.configure(bg=bg_color_dark)
    expand_button_frame.configure(bg = bg_color_dark)


    btn_color.configure(bg=bg_color, fg=fg_color, activebackground=bg_color_dark)
    btn_clear.configure(bg=bg_color, fg=fg_color, activebackground=bg_color_dark)
    btn_font_size.configure(bg=bg_color, fg=fg_color, activebackground=bg_color_dark)
    btn_sapper.config(bg = bg_color, fg = fg_color, activebackground = bg_color_dark)
    btn_close.configure(bg=bg_color, fg=fg_color, activebackground=bg_color_dark)
    btn_delay.configure(bg=bg_color, fg=fg_color)
    label_delay.configure(fg = fg_color, bg = bg_color_dark)
    btn_update.configure(fg = fg_color, bg = bg_color, activebackground=bg_color_dark)

    setting_frame.config(bg = bg_color_dark)
    frame_button_color.configure(bg=bg_color)
    settings_window.configure(bg=bg_color_dark)
    frame_button_color.configure(bg=bg_color_dark)
    frame_delay.configure(bg=bg_color_dark)
    lbl_news_update.configure(fg = bg_color, bg = bg_color_dark)


    check = text_chat.get("1.0", END)
    check = check.strip('\n')
    if check == welcome_text:
      text_chat.configure(state="normal")
      text_chat.configure(fg = bg_color_dark)
      text_chat.configure(state="disabled")

    text_chat.tag_configure("user", background=bg_color)
    text_chat.tag_configure("bot", background=bg_color_dark)


# функция для изменения цветовой гаммы
def change_colors():
    global bg_color
    global fg_color
    global bg_color_dark

    bg_color = askcolor()[1]
    fg_color = "#FFFFFF" if ((int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16)) < (127, 127, 127)) else "#000000"

    #Более тёмные объекты
    r, g, b = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
    r = max(r - 30, 0)
    g = max(g - 30, 0)
    b = max(b - 30, 0)
    bg_color_dark = f'#{r:02X}{g:02X}{b:02X}'

    colors_objects()


def clear_colors():
  global bg_color
  global fg_color
  global bg_color_dark

  bg_color = "white"
  fg_color = "#000000"
  bg_color_dark = 'gray90'

  colors_objects()



# функция для изменения размера шрифта
def change_font_size():
    global font_size
    font_size = askinteger("Изменить размер шрифта", "Введите новый размер шрифта:", initialvalue=font_size)
    text_chat.tag_configure("user", font=("Arial", font_size))
    text_chat.tag_configure("bot", font=("Arial", font_size))
    text_chat.update()
    message_input.configure(font=("Arial", font_size))



def compare_versions(version, latest_version):
    v1_parts = [int(x) for x in version.split(".")]
    v2_parts = [int(x) for x in latest_version.split(".")]
    for i in range(min(len(v1_parts), len(v2_parts))):
        if v1_parts[i] < v2_parts[i]:
            return -1
        elif v1_parts[i] > v2_parts[i]:
            return 1
    if len(v1_parts) < len(v2_parts):
        print('1')
        return -1
    elif len(v1_parts) > len(v2_parts):
        print('2')
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
    # находим идентификатор окна файла
    # window = pywinauto.Desktop(backend="uia").window(title=path)
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
    # y = -1
    print(y)
    global bg_color
    global fg_color
    global font_size

    frame_root_chat.pack_forget()
    settings_window.pack(fill=BOTH, expand=YES)
    root_chat.resizable(False, False)


    if y == -1:
        print(f"{latest_version} больше чем {version}")
        btn_update.pack(side=BOTTOM, fill=X, padx=5, pady=5)
        lbl_news_update.config(text = 'Доступно обновление!')
        lbl_news_update.pack(side=BOTTOM)
    else:
        lbl_news_update.config(text = 'Обновлений не найдено')
        lbl_news_update.pack(side=BOTTOM)
        print(f"{latest_version} равны {version}")
    
def animations_text():
    global delay, delay_state

    if (delay_state == "ВКЛ"):
      delay_state="ВЫКЛ"
      btn_delay.config(text=delay_state)
      delay = 0
    else:
      delay_state = "ВКЛ"
      btn_delay.config(text=delay_state)
      delay = 25

def close_setting():
    frame_root_chat.pack(fill=BOTH, expand=YES)
    settings_window.pack_forget()
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
        expand_button.config(text = expand_button_text)
        message_input.config(height=20)  # увеличиваем высоту окна ввода сообщений

    elif (expand_button_text == "↓"):
        expand_button_text = '↑'
        expand_button.config(text = expand_button_text)
        message_input.config(height=2)








def entry_design(frame):
    entry = Entry(
        frame,
        font=("Arial", 16),
        bg='white',
        fg=fg_color,
        relief='solid',
        border=1,
        highlightbackground="black"
    )
    return entry

def label_design(frame, text):
    label = Label(
        frame,
        text=text,
        font=('Arial',14)
        )
    return label


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
        error_message_login.config(text='Пользователь с таким логином уже зарегистрирован')
        os.remove("data.txt")
        return
    passw = entry_password.get()
    confirm_password = entry_confirm_password.get()
    api = entry_api_key.get()


    

    # проверяем совпадение паролей
    if passw != confirm_password:
        error_message_login.config(text='Пароли не совпадают')
        os.remove("data.txt")
        return
    # проверяем длину пароля
    if len(passw) < 5:
        error_message_login.config(text='Пароль должен быть не короче 5 символов')
        os.remove("data.txt")
        return
    # проверяем логин на английские символы
    if not all(c.isalpha() and ord(c) < 128 for c in login):
        error_message_login.config(text='Логин может содержать только английские буквы')
        os.remove("data.txt")
        return
    # проверяем длину api ключа
    if len(api) < 40:
        error_message_login.config(text='API ключ должен быть не короче 40 символов')
        os.remove("data.txt")
        return

    success_message_login.config(text='Регистрация прошла успешно')
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
    print(f"Последняя версия {latest_version}")
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
                version = lines[i+5].replace('version: ','').strip()

                decrypt(text_api, shift)
                api = decrypt(text_api, shift)
                print (api)
                if username_sign == login and password_sign == passw:
                    success_message_sign.config(text='Авторизация успешна')
                    openai.api_key = api
                    root_login.pack_forget()
                    frame_root_chat.pack(fill=BOTH, expand=YES)
                    root_chat.resizable(True, True)
                    file.close()
                    os.remove("data.txt")
                    welcome_text = welcome_text + f"{version}"
                    clear_chat()
                    print(version)
                    return
                    
    except Exception as e:
        error_message_sign.config(text='Неверный логин или пароль')
    error_message_sign.config(text='Неверный логин или пароль')
    file.close()
    os.remove("data.txt")


    

def clear_error_message(event):
    error_message_login.config(text='')
    error_message_sign.config(text='')


def login():
  btn_sign.config(state = 'normal')
  btn_login.config(state = 'disabled')
  sign_frame.pack_forget()
  login_frame.pack(pady=20)
  button_submit_sign.pack_forget()
  button_submit_login.pack(side=BOTTOM, fill='x', pady=5, padx=5)

def sign():
  btn_sign.config(state = 'disabled')
  btn_login.config(state = 'normal')
  sign_frame.pack(pady=20)
  login_frame.pack_forget()
  button_submit_login.pack_forget()
  button_submit_sign.pack(side=BOTTOM, fill='x', pady=5, padx=5)




try:
    os.remove("installer.exe")
except:
    print('Файл уже удалён')



def on_resize(event):
    width = event.width
    if width > max_width:
        settings_window.configure(width=400)
        btn_settings.place_forget()
    else:
        # settings_window.pack_forget()
        settings_window.pack_propagate(0)
        settings_window.configure(width=0)
              

# -------------------------------------
# hello_window()
# создаем главное окно
root_chat = Tk()
try:
    icon = PhotoImage(file = "ico.png")
    root_chat.iconphoto(False, icon)
except:
    print("Ошибка загрузки иконки")
root_chat.title('ChenkGPT')
root_chat.geometry('400x600')
root_chat.wm_minsize(400, 600)
root_chat.resizable(False, False)
root_chat.config(bg=bg_color_dark)
# root_chat.bind("<Configure>", on_resize) Доделать

screen_width = root_chat.winfo_screenwidth()
max_width = int(screen_width * 0.7)


frame_root_chat = Frame(root_chat, bg = bg_color_dark)




frame_chat = Frame(frame_root_chat)

# создаем текстовое поле для чата
text_chat = Text(
    frame_chat,
    height=1,
    wrap="word",
    font=("Arial", font_size),
    padx = 20,
    # state='disabled',
    bg=bg_color,
    fg=fg_color,
    relief='flat',
    border = 1, 
    selectbackground="#87CEFA")

frame_chat.pack(fill=BOTH, expand=True)
text_chat.config(state='disabled',fg=bg_color_dark)

# создаем слайдер для текст чата
scrollbar_chat = Scrollbar(
    frame_chat,
     width=20,
     background = 'red',
     troughcolor = 'red')
scrollbar_chat.pack(side=RIGHT, fill='y')
# устанавливаем связь между слайдером и текстом чата
scrollbar_chat.config(command=text_chat.yview)
# устанавливаем параметры для текстового поля и добавляем на главное окно
text_chat.config(yscrollcommand=scrollbar_chat.set)
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
    font=("Arial", font_size),
    padx = 5,
    width=10,
    bg=bg_color,
    fg=fg_color,
    relief = 'solid', )
# устанавливаем фокус на окно ввода сообщений
message_input.focus()
# устанавливаем сочетание клавиш для отправки сообщения (Ctrl + Enter)
message_input.bind('<Control-Return>', lambda event: btn_send.invoke())



frame_btn.config(bg=bg_color_dark)
# создаем кнопки с помощью функции
btn_settings = create_button(frame_btn, '\u2699', settings)
btn_send = create_button(frame_btn, '→', btn_send_command)


expand_button = create_button(frame_btn, text=expand_button_text, command=expand_text_input)
expand_button.config(font=("Arial", 16,"bold"))
expand_button.pack(side=LEFT, padx = 5)

btn_settings.pack(side=LEFT)
message_input.pack(side='left', fill='both', expand=True, padx=5)
btn_send.pack(side=LEFT)

frame_btn.pack(fill='x', padx=(0, 5), pady=5)







settings_window = Frame(root_chat)
settings_window.pack(side = LEFT, fill='y')
settings_window.pack_propagate(0)

btn_font_size = create_button(settings_window, text="Изменить размер шрифта", command=change_font_size)
btn_font_size.pack(side=TOP, padx=5, pady=5)

frame_button_color = Frame(settings_window, height=30)
btn_color = create_button(frame_button_color, text="Изменить цвет", command=change_colors)
btn_clear = create_button(frame_button_color, text="Сбросить", command=clear_colors)
btn_color.grid(row=0, column=0, padx=5, pady=5)
btn_clear.grid(row=0, column=1, padx=5, pady=5)

    
frame_delay = Frame(settings_window)
label_delay = Label(
  frame_delay,
  text = "Анимация текста:",
  font=("Arial", 16,"bold"))
btn_delay = create_button(
  frame_delay,
  text = delay_state,
  command = animations_text)
label_delay.grid(row=0, column=0, padx=5, pady=5)
btn_delay.grid(row=0, column=1, padx=5, pady=10)

btn_clear_chat = create_button(settings_window, 'Очистить чат', clear_chat)

btn_close = create_button(settings_window, text="Закрыть", command=close_setting)
btn_close.pack(side=BOTTOM, fill=X, padx=5, pady=5)

lbl_news_update = Label(
    settings_window, 
    text = '',
    fg = bg_color_dark,
    bg = bg_color,
    font=("Arial", 16,"bold"))
btn_update = create_button(settings_window, text='Обновить', command = update_chenkgpt)


# Установка фреймов
frame_button_color.pack(side=TOP, padx=5, pady=5)
frame_delay.pack(padx=5, pady=5)
btn_clear_chat.pack()











root_login = Frame(root_chat)
root_login.pack(side = RIGHT, fill=BOTH, expand=YES)
shift_frame = Frame(root_login)

btn_sign = Button(
    shift_frame,
    text='Войти',
    font=("Arial", 16),
    relief = 'solid',
    border = 0,
    state = 'disabled',
    command = sign)
shift_text = Label(
    shift_frame,
    font=("Arial", 16),
    text=' / ')
btn_login = Button(
    shift_frame,
    text='Регистрация',
    font=("Arial", 16),
    relief = 'solid',
    border = 0,
    command = login)

btn_sign.pack(side=LEFT)
shift_text.pack(side=LEFT)
btn_login.pack(side=LEFT)
shift_frame.pack(side="top", anchor="nw")


sign_frame = Frame(root_login)

# создаем метки и текстовые поля для ввода данных
label_username_sign = label_design(sign_frame, text='Логин:')
label_username_sign.pack(side=TOP)
entry_username_sign = entry_design(sign_frame)
entry_username_sign.pack(pady=10)

label_password_sign = label_design(sign_frame, text='Пароль:')
label_password_sign.pack(side=TOP)
entry_password_sign = entry_design(sign_frame)
entry_password_sign.config(show='*')
entry_password_sign.pack(pady=10)


# создаем кнопку для отправки данных
button_submit_sign = create_button(root_login, text='Войти', command=check_data)
button_submit_sign.config()
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
entry_password.config(show='*')
entry_password.pack(pady=10)

label_confirm_password = label_design(login_frame, text='Подтвердите пароль:')
label_confirm_password.pack()
entry_confirm_password = entry_design(login_frame)
entry_confirm_password.config(show='*')
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


# запускаем графический интерфейс
root_chat.mainloop()