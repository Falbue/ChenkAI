from tkinter import *
import tkinter as tk

root_login = Tk()
root_login.title('Вход')
root_login.geometry('400x200')

def check_data():
    # получаем данные из текстовых полей
    username = entry_username.get()
    password = entry_password.get()

    # проверяем совпадение логинов и паролей
    with open('user_data.txt', 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 4):
            login = lines[i+0].replace('login: ','').strip()
            passw = lines[i+1].replace('password: ','').strip()
            if username == login and password == passw:
                success_message.config(text='Авторизация успешна')
                return
    error_message.config(text='Неверный логин или пароль')

def clear_error_message(event):
    error_message.config(text='')

# создаем метки и текстовые поля для ввода данных
label_username = Label(root_login, text='Логин:')
label_username.pack()
entry_username = Entry(root_login)
entry_username.pack()

label_password = Label(root_login, text='Пароль:')
label_password.pack()
entry_password = Entry(root_login, show='*')
entry_password.pack()

# создаем кнопку для отправки данных
button_submit = Button(root_login, text='Войти', bg='#3366CC', fg='#FFF', command=check_data)
button_submit.pack()

# создаем метку для вывода сообщений об ошибках или успехе
error_message = Label(root_login, fg='red')
error_message.pack()
success_message = Label(root_login, fg='green')
success_message.pack()

entry_username.bind('<Button-1>', clear_error_message)
entry_password.bind('<Button-1>', clear_error_message)

root_login.mainloop()