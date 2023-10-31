from github import Github
import requests
import os
from tkinter import *
import tkinter as tk
import threading
import time
from tqdm import tqdm
import zipfile
import pylnk3
import shutil

token_git = 'klt_Jfj6NuRT0XWBEyeBu9AVPw24XLYGWy4jIJg2'
shift = 4

try:
    folder_name = f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT"
    # Используем функцию os.rmdir() для удаления папки
    shutil.rmtree(folder_name)
except:
    print("Папка уже удалена")

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

    if not os.path.exists(f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT_download"):
        os.mkdir(f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT_download")
    else:
        print(f"Папка уже есть")

    g = Github(token_git)
    repo_name = "Falbue/ChenkGPT"
    repo = g.get_repo(repo_name)
    releases = repo.get_releases()
    latest_release = releases[0]
    assets = list(latest_release.get_assets())
    total_files = len(assets)
    downloaded_files = 0

    with tqdm(total=total_files, unit="file") as pbar:
        for asset in latest_release.get_assets():
            if asset.name.endswith(".zip"):
                file_url = asset.browser_download_url
                r = requests.get(file_url)
                with open(f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT_download/{asset.name}", "wb") as f:
                    f.write(r.content)
                    downloaded_files += 1
                    pbar.update(1)

    lbl_progress.config(text="Обновление завершено!")
    btn_run.pack(expand=True)
    btn_cancel.pack_forget()

def close():
    path_zip = f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT_download/ChenkGPT.zip"
    destination = f"C:/Users/{os.getlogin()}/Desktop"
    with zipfile.ZipFile(path_zip, 'r') as zip_ref:
        zip_ref.extractall(destination)
    os.startfile(f"C:/Users/{os.getlogin()}/Desktop/ChenkGPT/ChenkGPT.exe")
    time.sleep(1)
    root.destroy()

def cancel():
    root.destroy()

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