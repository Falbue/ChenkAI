from github import Github
import requests
import os
from tkinter import *
import tkinter as tk
import threading
import time

token_git = 'klt_bpGFDtb4bwPdlm2FjM85HZXyGMvCAV0SIl6u'
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
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_name = 'ChenkGPT'
    new_folder_path = os.path.join(desktop_path, folder_name)

    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)
    else:
        print(f"Папка {folder_name} уже существует на рабочем столе.")

    g = Github(token_git)
    repo_name = "Falbue/ChenkGPT"
    repo = g.get_repo(repo_name)
    releases = repo.get_releases()
    latest_release = releases[0]
    assets = list(latest_release.get_assets())
    total_files = len(assets)
    downloaded_files = 0

    for asset in latest_release.get_assets():
        if asset.name.endswith(".exe"):
            file_url = asset.browser_download_url
            r = requests.get(file_url)
            with open(f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT/{asset.name}", "wb") as f:
                f.write(r.content)
                downloaded_files += 1
                progress = f"Загрузка файлов: {downloaded_files}/{total_files}"
                lbl_progress.config(text=progress)
                btn_cancel.config(state=tk.DISABLED)

                if downloaded_files == total_files:
                    lbl_progress.config(text="Обновление завершено.")
                    btn_run.pack(expand=True)
                    btn_cancel.pack_forget()

def close():
    path = f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT/ChenkGPT.exe"
    os.startfile(path)
    time.sleep(1)
    root.destroy()

def cancel():
    lbl_progress.config(text="Обновление отменено.")
    btn_cancel.config(state=tk.DISABLED)
    btn_run.pack(expand=True)
    btn_cancel.pack_forget()

root = tk.Tk()
root.geometry('300x200')

lbl_progress = Label(
    text='Обновление...',
    font=("Arial", 16, 'bold'))
lbl_progress.pack(expand=True)

btn_cancel = Button(
    font=("Arial", 16),
    text='Отменить',
    command=cancel,
    relief='solid',
    border=1,
    highlightbackground="black")
btn_cancel.pack(expand=True)

btn_run = Button(
    font=("Arial", 16),
    text='Запустить',
    command=close,
    relief='solid',
    border=1,
    highlightbackground="black")

thread = threading.Thread(target=update)
thread.start()

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()