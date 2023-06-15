from github import Github
import requests
import os
from tkinter import *
import tkinter as tk
import threading
import time

token_git = 'klt_CxpoPFvnOs4zvMpUkWakMVlCBPC5KK0Fj3ET'
shift = 4

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
print(token_git)

def update():
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


    g = Github(token_git)
    repo_name = "Falbue/ChenkGPT"
    repo = g.get_repo(repo_name)
    releases = repo.get_releases()
    latest_release = releases[0]

    for asset in latest_release.get_assets():
        if asset.name.endswith(".exe"):
            file_url = asset.browser_download_url
            r = requests.get(file_url)
            with open(f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT/{asset.name}", "wb") as f:
                f.write(r.content)
                lbl.pack_forget()
                btn.pack(expand=True)
    

def close():
    path = f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT/ChenkGPT.exe"
    os.startfile(path)
    time.sleep(1)
    root.destroy()

thread = threading.Thread(target=update)
thread.start()

root = tk.Tk()
root.geometry('400x200')
lbl = Label(
    text = 'Обновляется...',
    font = ("Arial", 16, 'bold'))
lbl.pack(expand=True)
btn = Button(
    font=("Arial", 16),
    text='Закрыть',
    command=close,
    relief='solid',
    border=1,
    highlightbackground="black")

root.mainloop()
