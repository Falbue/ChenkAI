from tkinter import *
import tkinter as tk

root_login = Tk()
root_login.title('Регистрация')
root_login.geometry('400x250')

def save_data():
    # получаем данные из текстовых полей
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    api_key = entry_api_key.get()

    # проверяем совпадение паролей
    if password != confirm_password:
        error_message.config(text='Пароли не совпадают')
        return
    # проверяем длину пароля
    if len(password) < 5:
        error_message.config(text='Пароль должен быть не короче 5 символов')
        return
    # проверяем логин на английские символы
    if not all(c.isalpha() and ord(c) < 128 for c in username):
        error_message.config(text='Логин может содержать только английские буквы')
        return
    # проверяем длину api ключа
    if len(api_key) < 40:
        error_message.config(text='API ключ должен быть не короче 40 символов')
        return

    # проверяем совпадение логинов
    with open('user_data.txt', 'r') as file:
        logins = [line.strip() for line in file.readlines()[::2]] # получаем список записанных логинов
    if username in logins:
        error_message.config(text='Логин уже зарегистрирован')
    else:
        # сохраняем данные в файл
        with open('user_data.txt', 'a') as file:
          file.write('login: '+username + '\n')
          file.write('password: '+password + '\n')
          file.write('api: '+api_key + '\n')
          file.write('\n')
        success_message.config(text='Регистрация прошла успешно')


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

label_confirm_password = Label(root_login, text='Подтвердите пароль:')
label_confirm_password.pack()
entry_confirm_password = Entry(root_login, show='*')
entry_confirm_password.pack()

label_api_key = Label(root_login, text='API ключ:')
label_api_key.pack()
entry_api_key = Entry(root_login)
entry_api_key.pack()

# создаем кнопку для отправки данных
button_submit = Button(root_login, text='Зарегистрироваться', bg='#3366CC', fg='#FFF', command=save_data)
button_submit.pack()

# создаем метку для вывода сообщений об ошибках или успехе
error_message = Label(root_login, fg='red')
error_message.pack()
success_message = Label(root_login, fg='green')
success_message.pack()

entry_username.bind('<Button-1>', clear_error_message)
entry_password.bind('<Button-1>', clear_error_message)
entry_confirm_password.bind('<Button-1>', clear_error_message)
entry_api_key.bind('<Button-1>', clear_error_message)

root_login.mainloop()