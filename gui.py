import Sudoku
from Puzzles import Puzzles
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import time
import random

class SudokuGui:

    def update_square(self, row, column):
            value = self.sudoku.get_square(row, column)
            if (value == 0):
                self.squares[row][column].configure(text="")
            else:
                self.squares[row][column].configure(text=str(value))
                self.squares[row][column].configure(bg="lightgreen")
            self.window.update()
            time.sleep(0.001)
            self.squares[row][column].configure(bg="white")
            self.window.update()

    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(width=False, height=False)
        self.window.title("SUDOKU")
        normal_font = tkfont.Font(family="Helvetica", size=9)
        bold_font = tkfont.Font(family="Helvetica", size=9, weight="bold")

        button_labels = ["New", "Clear", "Check", "Solve"]
        buttons = []

        self.squares = []
        self.sudoku = None
        self.check_highlights = False

        frame0 = tk.Frame(master=self.window, width=450, height=500)
        frame0.pack()

        frame1 = tk.Frame(master=frame0, height=450)
        frame1.pack(padx=20, pady=20)

        frame2 = tk.Frame(master=frame0, width=450, height=50)
        frame2.pack(padx=10, pady=(0,20))

        def load_puzzle(new_puzzle):
            self.sudoku = Sudoku.SudokuPuzzle(new_puzzle, self)
            puzzle = self.sudoku.puzzle
            for i in range(0, 9):
                for j in range(0, 9):
                    if (puzzle[i][j].value == 0):
                        self.squares[i][j].configure(text="", font = normal_font, bg="white")
                    else:
                        self.squares[i][j].configure(text=puzzle[i][j].value, font = bold_font, bg="lightgray")

        def update_square(row, column):
            self.sudoku.solved = False
            value = self.sudoku.get_square(row, column)
            if (value == 0):
                self.squares[row][column].configure(text="")
            else:
                self.squares[row][column].configure(text=str(value))

        def clear_puzzle():
            self.sudoku.solved = False
            for i in range(0, 9):
                for j in range(0, 9):
                    if (not(self.sudoku.get_square_fixed(i, j))):
                        self.squares[i][j].configure(text="")
                        self.sudoku.set_square(i, j, 0)

        def check_puzzle():
            if (not(self.sudoku.no_blanks())):
                messagebox.showwarning("Incomplete Puzzle", "Warning: Not all squares are filled.")
            else:
                solved = True
                for i in range (0, 9):
                    for j in range (0, 9):
                        if (not(self.sudoku.check_square(i, j))):
                            solved = False
                            self.squares[i][j].configure(bg="red")
                if (not(solved)):
                    self.check_highlights = True
                    messagebox.showerror("", "Current solution incorrect. Try again.")
                else:
                    messagebox.showinfo("", "Puzzle Solved. Your solution is correct.")

        def solve_puzzle():
            solved = True
            for i in range (0, 9):
                for j in range (0, 9):
                    if (not(self.sudoku.check_square(i, j))):
                        solved = False
            if (not(solved)):
                clear_puzzle()
                self.sudoku.solve_puzzle()
                messagebox.showinfo("", "Puzzle solved.")
            else:
                messagebox.showwarning("", "Puzzle already solved.")

        def new_puzzle():
            number = random.randint(0, len(Puzzles.puzzles) - 1)
            load_puzzle(Puzzles.puzzles[number])


        def main_button_click(name):
            if (self.check_highlights):
                reset_all_square_colors()
                self.check_highlights = False

            if (name == "Clear"):
                clear_puzzle()
            elif (name == "Check"):
                check_puzzle()
            elif (name == "Solve"):
                solve_puzzle()
            elif (name == "New"):
                new_puzzle()

        def reset_all_square_colors():
            for i in range (0, 9):
                for j in range (0, 9):
                    if (not(self.sudoku.get_square_fixed(i, j))):
                        self.squares[i][j].configure(bg="white")

        def unbind_all(bindings):
            for i in range(0, len(bindings)):
                self.window.unbind(bindings[i])

        def select_cell(row, column):
            if (self.check_highlights):
                reset_all_square_colors()
                self.check_highlights = False

            if (not(self.sudoku.get_square_fixed(row, column))):
                bindedkeys = []
                self.squares[row][column].configure(relief=tk.RIDGE)

                def handle_number_entry(event):
                    if (event.char == "" or ord(event.char) == 8 or ord(event.char) == 48): #ascii
                        self.sudoku.set_square(row, column, 0)
                        unbind_all(bindedkeys)
                    elif (ord(event.char) > 48 and ord(event.char) < 58): #ascii
                        self.sudoku.set_square(row, column, int(event.char))
                        unbind_all(bindedkeys)
                    update_square(row, column)
                    return select_cell(row, column)
                self.window.bind("<Key>", handle_number_entry)
                bindedkeys.append("<Key>")

                def handle_up_arrow(event):
                    if (row != 0 and not(self.sudoku.get_square_fixed(row - 1, column))):
                        self.squares[row][column].configure(relief=tk.FLAT)
                        unbind_all(bindedkeys)
                        select_cell(row - 1, column)
                self.window.bind("<Up>", handle_up_arrow)
                bindedkeys.append("<Up>")

                def handle_left_arrow(event):
                    if (column != 0 and not(self.sudoku.get_square_fixed(row, column - 1))):
                        self.squares[row][column].configure(relief=tk.FLAT)
                        unbind_all(bindedkeys)
                        select_cell(row, column - 1)
                self.window.bind("<Left>", handle_left_arrow)
                bindedkeys.append("<Left>")

                def handle_right_arrow(event):
                    if (column != 8 and not(self.sudoku.get_square_fixed(row, column + 1))):
                        self.squares[row][column].configure(relief=tk.FLAT)
                        unbind_all(bindedkeys)
                        select_cell(row, column + 1)
                self.window.bind("<Right>", handle_right_arrow)
                bindedkeys.append("<Right>")

                def handle_down_arrow(event):
                    if (row != 8 and not(self.sudoku.get_square_fixed(row + 1, column ))):
                        self.squares[row][column].configure(relief=tk.FLAT)
                        unbind_all(bindedkeys)
                        select_cell(row + 1, column)
                self.window.bind("<Down>", handle_down_arrow)
                bindedkeys.append("<Down>")

                def handle_return(event):
                    self.squares[row][column].configure(relief=tk.FLAT)
                    unbind_all(bindedkeys)
                self.window.bind("<Return>", handle_return)
                bindedkeys.append("<Return>")

                def handle_mouseclick(event):
                    self.squares[row][column].configure(relief=tk.FLAT)
                    unbind_all(bindedkeys)
                self.window.bind("<Button>", handle_mouseclick)
                bindedkeys.append("<Button>")

        def add_buttons():
            for i in range(9):
                self.squares.append([])
                for j in range(9):
                    frame = tk.Frame(master=frame1, relief=tk.RIDGE, borderwidth=1)
                    frame.grid(row=i, column=j)
                    button = tk.Button(master=frame, width=5, height=2, font = normal_font,
                    relief=tk.FLAT, text="", command = lambda row=i, column=j: select_cell(row,column))
                    self.squares[i].append(button)
                    button.pack()
            for i in range(4):
                frame = tk.Frame(master=frame2, relief=tk.GROOVE, borderwidth=2)
                frame.grid(row=1, column=i, padx=10)
                button = tk.Button(master=frame, width=10, height=2, text=button_labels[i],
                command = lambda name=button_labels[i]: main_button_click(name))
                buttons.append(button)
                button.pack()

        add_buttons()
        new_puzzle()
        self.window.mainloop()