bg_color = "#FFFFFF"
fg_color = "#000000"
bg_color_dark = 'gray90'
font_size = 16
fonts = "Arial"

from tkinter import Button, Label, Entry
def button(frame, text, command):
    button = Button(
        frame,
        activebackground=bg_color_dark,
        font=(fonts, font_size),
        bg='white',
        fg=fg_color,
        text=text,
        command=command,
        relief='solid',
        border=1,
        highlightbackground=fg_color
    )
    button.bind("<Enter>", lambda event: button.configure(bg=bg_color_dark))
    button.bind("<Leave>", lambda event: button.configure(bg=bg_color))
    return button

def entry(frame):
    entry = Entry(
        frame,
        font=(fonts, 16),
        bg='white',
        fg=fg_color,
        relief='solid',
        border=1,
    )
    entry.bind("<FocusIn>", lambda event: entry.configure(bg=bg_color_dark))
    entry.bind("<FocusOut>", lambda event: entry.configure(bg=bg_color))
    return entry

def label(frame, text):
    label = Label(
        frame,
        text=text,
        font=('Arial',14)
        )
    return label