import tkinter as tk
import random
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