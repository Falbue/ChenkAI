from tkinter import *
import tkinter as tk
# from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText 
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askinteger
import openai

# устанавливаем ключ API для OpenAI
openai.api_key = "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"

# переменные для цветовой гаммы и размера шрифта
bg_color = "#FFFFFF"
fg_color = "#000000"

#Более тёмные объекты
r, g, b = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
r = max(r - 30, 0)
g = max(g - 30, 0)
b = max(b - 30, 0)
bg_color_dark = f'#{r:02X}{g:02X}{b:02X}'

font_size = 12

user = 'You'
bot = 'Bot'

delay = 25
delay_state = "ВКЛ"

welcome_text = """Привет. Это ChenkGPT
#testк

Инструкция:
1. Если окно зависло, значит бот грузит Ваш запрос
2. Для копирования и вставки текста, нужно переключится на английскую раскладку
3. Если окно уже не виснет, а бот ничего не присал, попробуйте отключить proxy сервер
3.1 Если вариант выше не помог, отключите Ethernet кабель, proxy сервер и подкючитесь с помощью Вашего смартфона через USB модем
4. По всем вопросам обращаться на почту: ChenkGPT@gmail.com

Falbue <3
ver: 0.6"""

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
    text_chat.config( bg=bg_color,fg=fg_color)
    check = text_chat.get("1.0", END)
    check = check.strip('\n')
    print(check)
    if check == welcome_text:
      text_chat.configure(state="normal")
      text_chat.delete("1.0", END)
      text_chat.configure(state="disabled")

    # получаем вопрос, который пользователь задал боту
    question = message_input.get("1.0", END)
    if question.endswith('\n'):
      question = question.strip('\n')
    # очищаем поле ввода
    message_input.delete("1.0", END)
    # выводим вопрос в консоль
    print("User: " + question)

    text_chat.configure(state="normal")
    text_chat.insert(END, '\n')
    text_chat.insert(END, user + ": ", "bold")
    text_chat.insert(END, question, "user")
    text_chat.tag_configure("user", background=bg_color, selectbackground="#87CEFA")
    text_chat.insert(END, '\n')
    text_chat.configure(state="disabled")

    # устанавливаем placeholder, который появится в поле чата
    text_chat.tag_configure("bold", font=("Arial", font_size, "bold"))
    text_chat.configure(state="normal")
    text_chat.insert(END, '\n')
    text_chat.insert(END, bot + " печатает...", "bot_placeholder bold")
    text_chat.configure(state="disabled")
    text_chat.see(END)
    root_chat.update()

    # отправляем вопрос на обработку OpenAI
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "assistant", "content": question}]) 

  # выводим ответ, который вернул OpenAI, в консоль
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

        text_chat.insert(END, '\n')
        text_chat.tag_configure("bot", background=bg_color_dark, selectbackground="#87CEFA")
        text_chat.tag_configure("code", background = "#565656")
        text_chat.configure(state="disabled")

    show_text_slowly(answer)
    text_chat.see(END)

    root_chat.update()


def colors_objects(): # объекты, которые меняют цвета
    text_chat.configure(bg=bg_color, fg=fg_color)
    message_input.configure(bg=bg_color, fg=fg_color)

    btn_send.configure(bg=bg_color, activebackground=bg_color_dark, fg=fg_color)
    btn_settings.configure(bg=bg_color, activebackground=bg_color_dark, fg=fg_color)
    btn_clear_chat.configure(bg=bg_color, activebackground=bg_color_dark, fg=fg_color)

    root_chat.configure(bg=bg_color_dark)

    frame_btn.configure(bg=bg_color_dark)
    frame_chat.configure(bg=bg_color_dark)


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


# ------------------------------------------
def hello_window():
  def username_click(event):
    global user

    chek_username.configure(state='normal')

    if username.get() == 'Введите ваше имя:':
      username.configure(fg = 'black')
      username.delete(0, END) # удалить текст с 0 до конца виджета
      username.insert(0, '') # вставить пустую строку

    if botname.get() == "":
      botname.configure(fg = 'gray60')
      botname.insert(0, 'Введите имя чат-бота:')
      chek_botname.configure(state='disabled')

  def botname_click(event):
    global bot

    chek_botname.configure(state='normal')


    if botname.get() == 'Введите имя чат-бота:':
      botname.configure(fg = 'black')
      botname.delete(0, END) # удалить текст с 0 до конца виджета
      botname.insert(0, '') # вставить пустую строку

    if username.get() == "":
      username.configure(fg = 'gray60')
      username.insert(0, 'Введите ваше имя:')
      chek_username.configure(state='disabled')


  def place_username():
    global user
    user = username.get()

    if (user == ""):
      user = "User"

    username.configure(state='disabled')
    chek_username.configure(state='disabled')

  def place_botname():
    global bot
    bot = botname.get()

    if (bot == ""):
      bot = "Bot"

    botname.configure(state='disabled')
    chek_botname.configure(state='disabled')

    if (chek_botname['state'] == 'disabled')and(chek_username['state'] == 'disabled'):
      btn_further.configure(state='normal')


 # Создаём окно приветствия
  root_hello_window = Tk()
  root_hello_window.title('Приветствие') # Заголовок окна
  root_hello_window.resizable(width=False, height=False) # Убираем возможность изменять размеры окна
  root_hello_window.geometry('400x300') # Задаём размер окна
  root_hello_window.eval('tk::PlaceWindow . center') # Окно окажется по центру экрана

  # Поле ввода Вашего имени
  frame_user = Frame()
  username = Entry(
    frame_user,
    width = 30,
    relief='solid',
    border = 1,
    font=("Arial", 14),
    fg = "gray60")
  username.insert(0, 'Введите ваше имя:') # Устанавливаем текст по умолчанию
  chek_username = Checkbutton(
    frame_user,
    state='disabled',
    command = place_username) # Кнопка "Выбрать"
  var_username = BooleanVar()
  chek_username.config(variable=var_username)
  username.bind('<FocusIn>', username_click) # Событие при нажатии на поле ввода
  username.bind('<Return>', lambda event: place_username())

  username.pack(side="left")
  chek_username.pack(side="left", pady=10)
  frame_user.pack()

  # Поле ввода имени бота
  frame_bot = Frame()
  botname = Entry(
    frame_bot,
    width = 30,
    relief='solid',
    border = 1,
    font=("Arial", 14), 
    fg = "gray60")
  botname.insert(0, 'Введите имя чат-бота:') # Устанавливаем текст по умолчанию

  chek_botname = Checkbutton(
    frame_bot,
    state = 'disabled',
    command = place_botname) # Кнопка "Выбрать"
  var_botname = BooleanVar()
  chek_botname.config(variable=var_botname)
  botname.bind('<FocusIn>', botname_click) # Событие при нажатии на поле ввода
  botname.bind('<Return>', lambda event: place_botname())
  
  botname.pack(side="left")
  chek_botname.pack(side="left", pady=10)
  frame_bot.pack()

  def skip():
    global user, bot # Объявляем глобальные переменные
    user = "User"
    bot = "Bot"
    root_hello_window.destroy() # Уничтожаем окно приветствия
  def further():
    root_hello_window.destroy() # Уничтожаем окно приветствия

  # Кнопки
  frame_btn_hello_window = Frame()
  btn_further = create_button(frame_btn_hello_window,
    text = "Продолжить",    
    command = further)
  btn_skip = create_button(
    frame_btn_hello_window,
    text = 'Пропустить',
    command = skip)

  btn_skip.pack(side="right", padx=10)
  btn_further.pack(side="right", padx=10)
  btn_further.configure(state='disabled') # Кнопка "Продолжить" неактивна
  frame_btn_hello_window.pack(side="bottom", pady=10)

  root_hello_window.mainloop() # Запускаем цикл обработки событий окна




hello_window()
# создаем главное окно
root_chat = Tk()
root_chat.overrideredirect(False)
root_chat.title('ChenkGPT')
root_chat.geometry('600x800')
root_chat.config(bg=bg_color_dark)

frame_chat = Frame()

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

frame_chat.pack(padx=20, fill=BOTH, expand=True)
text_chat.insert(END,welcome_text)
text_chat.config(state='disabled',fg=bg_color_dark)
# создаем слайдер для текст чата
scrollbar_chat = Scrollbar(frame_chat)

# устанавливаем связь между слайдером и текстом чата
scrollbar_chat.config(command=text_chat.yview)
# устанавливаем параметры для текстового поля и добавляем на главное окно
text_chat.config(yscrollcommand=scrollbar_chat.set)

# устанавливаем параметры для слайдера и добавляем на главное окно
# scrollbar_chat.pack(side=RIGHT, fill=Y) нужно настроить цвета
text_chat.pack(fill=BOTH, expand=True)



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

# устанавливаем параметры для окна ввода сообщений и добавляем на главное окно
message_input.pack(fill='x', padx=20, pady=20)


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