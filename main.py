from tkinter import *
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askinteger
import openai
import os

# устанавливаем ключ API для OpenAI

# переменные для цветовой гаммы и размера шрифта
bg_color = "#FFFFFF"
fg_color = "#000000"


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
welcome_text = """Привет. Это ChenkGPT

Инструкция:
1. Если окно зависло, значит бот грузит Ваш запрос
2. Для копирования и вставки текста, нужно переключится на английскую раскладку
3. Если окно уже не виснет, а бот ничего не присал, попробуйте отключить proxy сервер
3.1 Если вариант выше не помог, отключите Ethernet кабель, proxy сервер и подкючитесь с помощью Вашего смартфона через USB модем
4. По всем вопросам обращаться на почту: ChenkGPT@gmail.com

Falbue <3
ver: 0.8.1"""

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

# Подсветка синтаксиса
def code_sintaxis():
    if (code == 1):
        start = "1.0"
        while True:
            start = text_chat.search("```", start+"3", END)
            if not start:
                break
        
            end = text_chat.search("```", start + "3", END)
            if not end:
                break
        
            # Добавляем тег к найденному тексту
            text_chat.tag_add("code", start + "3", end)

            # Продолжаем поиск со следующей позиции
            start = end


# функция, которая вызывается при нажатии кнопки "Отправить"
def btn_send_command():
    global text_error
    try:
        text_chat.config(bg=bg_color, fg=fg_color)
        check = text_chat.get("1.0", END).strip('\n')
        if check == welcome_text:
            text_chat.configure(state="normal")
            text_chat.delete("1.0", END)
            text_chat.configure(state="disabled")
        question = message_input.get("1.0", END).strip('\n')
        message_input.delete("1.0", END)
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
            for i, char in enumerate(text):
                text_chat.insert(END, char, "bot")
                text_chat.see("end")
                root_chat.update()
                root_chat.after(delay)
            text_chat.insert(END, '\n', "bot")
            text_chat.tag_configure("bot", background=bg_color_dark, selectbackground="#87CEFA")
            text_chat.tag_configure("code", background = "#565656")
            text_chat.configure(state="disabled")
        show_text_slowly(answer)
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

    frame_btn.configure(bg=bg_color_dark)
    frame_chat.configure(bg=bg_color_dark)
    expand_button_frame.configure(bg = bg_color_dark)


    check = text_chat.get("1.0", END)
    check = check.strip('\n')
    print(check)
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
    settings_window.destroy()


def clear_colors():
  global bg_color
  global fg_color
  global bg_color_dark

  bg_color = "white"
  fg_color = "#000000"
  bg_color_dark = 'gray90'

  colors_objects()
  settings_window.destroy()



# функция для изменения размера шрифта
def change_font_size():
    global font_size
    font_size = askinteger("Изменить размер шрифта", "Введите новый размер шрифта:", initialvalue=font_size)
    text_chat.tag_configure("user", font=("Arial", font_size))
    text_chat.tag_configure("bot", font=("Arial", font_size))
    text_chat.update()
    message_input.configure(font=("Arial", font_size))

    settings_window.destroy()



 # добавим настройки окна
def settings():
    global settings_window
    global bg_color
    global fg_color
    global font_size
    
    # создаем новое окно с настройками
    settings_window = Toplevel()
    settings_window.geometry("300x300")
    settings_window.resizable(width=False, height=False)
    settings_window.title("Настройки")
    

    frame_button_color = Frame(settings_window, height=30)
    btn_color = create_button(frame_button_color, text="Изменить цвет", command=change_colors)
    btn_clear = create_button(frame_button_color, text="Сбросить", command=clear_colors)
    btn_color.grid(row=0, column=0, padx=5, pady=5)
    btn_clear.grid(row=0, column=1, padx=5, pady=5)

    btn_font_size = create_button(settings_window, text="Изменить размер шрифта", command=change_font_size)
    btn_font_size.pack(side=TOP, fill=X, padx=5, pady=5)

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

    frame_delay = Frame(settings_window)
    label_delay = Label(
      frame_delay,
      text = "Анимация текста:",
      font=("Arial", 16,"bold"),
      bg=bg_color_dark)
    btn_delay = create_button(
      frame_delay,
      text = delay_state,
      command = animations_text)
    label_delay.grid(row=0, column=0, padx=5, pady=5)
    btn_delay.grid(row=0, column=1, padx=5, pady=10)

    btn_close = create_button(settings_window, text="Закрыть", command=settings_window.destroy)
    btn_close.pack(side=BOTTOM, fill=X, padx=5, pady=5)


    # Установка фреймов
    frame_button_color.pack(side=TOP, fill=X, padx=5, pady=5)
    frame_delay.pack(fill=X, padx=5, pady=5)


    # Настойки объектов
    btn_color.configure(bg=bg_color, fg=fg_color)
    btn_clear.configure(bg=bg_color, fg=fg_color)
    btn_font_size.configure(bg=bg_color, fg=fg_color)
    btn_close.configure(bg=bg_color, fg=fg_color)
    btn_delay.configure(bg=bg_color, fg=fg_color)
    label_delay.configure(fg = fg_color)

    frame_button_color.configure(bg=bg_color)
    settings_window.configure(bg=bg_color_dark)
    frame_button_color.configure(bg=bg_color_dark)
    frame_delay.configure(bg=bg_color_dark)



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
        message_input.config(height=3)










# Вход и регистрация
#-----------------------------------
root_login = Tk()
root_login.resizable(width=False, height=False) # Убираем возможность изменять размеры окна
icon = PhotoImage(file = "icon.png")
root_login.iconphoto(False, icon)
root_login.title('Вход')
root_login.geometry('400x600')

def on_close():
    exit()

# обработчик события закрытия главного окна
root_login.protocol("WM_DELETE_WINDOW", on_close)


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



def save_data():
    # получаем данные из текстовых полей
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    api_key = entry_api_key.get()

    # проверяем на повтор логина
    if os.path.exists('user_data.chnk'):
        with open('user_data.chnk', 'r') as file:
            logins = set(line.split(':')[1].strip() for line in file if line.startswith('login:'))
        if username in logins:
            error_message_login.config(text='Пользователь с таким логином уже зарегистрирован')
            return
        else:
            logins.add(username)
    else:
        logins = {username}

    # проверяем совпадение паролей
    if password != confirm_password:
        error_message_login.config(text='Пароли не совпадают')
        return
    # проверяем длину пароля
    if len(password) < 5:
        error_message_login.config(text='Пароль должен быть не короче 5 символов')
        return
    # проверяем логин на английские символы
    if not all(c.isalpha() and ord(c) < 128 for c in username):
        error_message_login.config(text='Логин может содержать только английские буквы')
        return
    # проверяем длину api ключа
    if len(api_key) < 40:
        error_message_login.config(text='API ключ должен быть не короче 40 символов')
        return

    # сохраняем данные в файл
    with open('user_data.chnk', 'a') as file:
        file.write('login: ' + username + '\n')
        file.write('password: ' + password + '\n')
        file.write('api: ' + api_key + '\n')
        file.write('user: ' + 'User' + '\n')
        file.write('bot: ' + 'Bot' + '\n')
        file.write('\n')

    success_message_login.config(text='Регистрация прошла успешно')



def check_data():
    global login, passw, api, user, bot
    # получаем данные из текстовых полей
    username_sign = entry_username_sign.get()
    password_sign = entry_password_sign.get()

    # проверяем совпадение логинов и паролей
    with open('user_data.chnk', 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 6):
            login = lines[i+0].replace('login: ','').strip()
            passw = lines[i+1].replace('password: ','').strip()
            api = lines[i+2].replace('api: ','').strip()
            user = lines[i+3].replace('user: ','').strip()
            bot = lines[i+4].replace('bot: ','').strip()
            if username_sign == login and password_sign == passw:
                success_message_sign.config(text='Авторизация успешна')
                root_login.destroy()
                return
    error_message_sign.config(text='Неверный логин или пароль')

    

def clear_error_message(event):
    error_message_login.config(text='')
    error_message_sign.config(text='')


def login():
  btn_sign.config(state = 'normal')
  btn_login.config(state = 'disabled')
  sign_frame.pack_forget()
  login_frame.pack(pady=20)
  button_submit_sign.pack_forget()
  button_submit_login.pack(side=BOTTOM,pady=5)

def sign():
  btn_sign.config(state = 'disabled')
  btn_login.config(state = 'normal')
  sign_frame.pack(pady=20)
  login_frame.pack_forget()
  button_submit_login.pack_forget()
  button_submit_sign.pack(side=BOTTOM, pady=5)



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
button_submit_sign.config(width=20)
button_submit_sign.pack(side=BOTTOM, pady=5)


# создаем метку для вывода сообщений об ошибках или успехе
error_message_sign = Label(sign_frame, fg='red', font=("System",16), wraplength=300)
error_message_sign.pack(side=TOP, pady=50)
success_message_sign = Label(sign_frame, fg='green', font=("System",16), wraplength=300)
success_message_sign.pack(side=TOP, pady=50)

entry_username_sign.bind('<Button-1>', clear_error_message)
entry_password_sign.bind('<Button-1>', clear_error_message)

sign_frame.pack(side=TOP, fill=BOTH, expand=True, pady=20)



login_frame = Frame()

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
button_submit_login.config(width=20)


# создаем метку для вывода сообщений об ошибках или успехе
error_message_login = Label(login_frame, fg='red', wraplength=300, font=("System",16))
error_message_login.pack(pady=20)
success_message_login = Label(login_frame, fg='green', font=("System",16), wraplength=300)
success_message_login.pack(pady=20)

entry_username.bind('<Button-1>', clear_error_message)
entry_password.bind('<Button-1>', clear_error_message)
entry_confirm_password.bind('<Button-1>', clear_error_message)
entry_api_key.bind('<Button-1>', clear_error_message)


root_login.mainloop()










# -------------------------------------
# hello_window()
# создаем главное окно
openai.api_key = api
root_chat = Tk()
root_chat.overrideredirect(False)
icon = PhotoImage(file = "icon.png")
root_chat.iconphoto(False, icon)
root_chat.title('ChenkGPT')
root_chat.geometry('400x600')
root_chat.wm_minsize(400, 600)
root_chat.config(bg=bg_color_dark)

frame_chat = Frame()
print(api)

# создаем текстовое поле для чата
text_chat = Text(
    frame_chat,
    height=1,
    wrap="word",
    font=("Arial", font_size),
    # state='disabled',
    bg=bg_color,
    fg=fg_color,
    relief='solid',
    border = 1, 
    selectbackground="#87CEFA")

frame_chat.pack(padx=(20, 0), fill=BOTH, expand=True)
text_chat.insert(END,welcome_text)
text_chat.config(state='disabled',fg=bg_color_dark)

# создаем слайдер для текст чата
scrollbar_chat = Scrollbar(
    frame_chat,
     width=20,
     background = bg_color,
     troughcolor = bg_color_dark)
scrollbar_chat.pack(side=RIGHT, fill='y')
# устанавливаем связь между слайдером и текстом чата
scrollbar_chat.config(command=text_chat.yview)

# устанавливаем параметры для текстового поля и добавляем на главное окно
text_chat.config(yscrollcommand=scrollbar_chat.set)

# устанавливаем параметры для слайдера и добавляем на главное окно
text_chat.pack(fill=BOTH, expand=True)

expand_button_frame = Frame(bg = bg_color_dark)
# создаем кнопку для изменения размера окна ввода сообщений
expand_button = create_button(expand_button_frame, text=expand_button_text, command=expand_text_input)
expand_button.config(font=("Arial", 10,"bold"))

# создаем окно ввода сообщений
message_input = Text(
    root_chat,
    wrap="word",
    height=3,
    font=("Arial", font_size),
    bg=bg_color,
    fg=fg_color,
    relief = 'solid', 
    border = 1)

expand_button_frame.pack(fill ='x')
expand_button.pack(side=RIGHT, padx=20)
# устанавливаем параметры для окна ввода сообщений и добавляем на главное окно
message_input.pack(fill='x', padx=20)


frame_btn = Frame(root_chat,height=40)
frame_btn.config(bg=bg_color_dark)
frame_btn.pack(fill='x', pady=20, padx=20)


# создаем кнопки с помощью функции
btn_settings = create_button(frame_btn, 'Настройки', settings)
btn_send = create_button(frame_btn, 'Отправить', btn_send_command)
btn_clear_chat = create_button(frame_btn, 'Очистить', clear_chat)

# устанавливаем фокус на окно ввода сообщений
message_input.focus()
# устанавливаем сочетание клавиш для отправки сообщения (Ctrl + Enter)
root_chat.bind('<Control-Return>', lambda event: btn_send.invoke())

btn_settings.place(relx=0, rely=0.5, anchor=W)
btn_send.place(relx=0.5, rely=0.5, anchor=CENTER)
btn_clear_chat.place(relx=1, rely=0.5, anchor=E)


# запускаем графический интерфейс
root_chat.mainloop()
