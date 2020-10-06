import tkinter as tk
from tkinter import font as tkfont
import suduko

window = tk.Tk()
window.resizable(width=False, height=False)
window.title("SUDOKU")
normal_font = tkfont.Font(family="Helvetica", size=9)
bold_font = tkfont.Font(family="Helvetica", size=9, weight="bold")

squares = []
puzzle = []

frame0 = tk.Frame(master=window, width=450, height=500)
frame0.pack()

frame1 = tk.Frame(master=frame0, height=450)
frame1.pack(padx=20, pady=20)

def load_puzzle(new_puzzle):
    for i in range(0, 9):
        puzzle.append([])
        for j in range(0, 9):
            puzzle[i].append(new_puzzle[i][j])
            if (new_puzzle[i][j] == 0):
                squares[i][j].configure(text="")
            else:
                squares[i][j].configure(text=new_puzzle[i][j], font = bold_font)

def handle_click(event):
    print("The button was clicked!")

def select_cell(row, column):
    squares[row][column].configure(relief=tk.RIDGE)

    def handle_number_entry(event):
        if (event.char == "" or ord(event.char) == 8): #ascii
            squares[row][column].configure(text="")
            squares[row][column].configure(relief=tk.FLAT)
            window.unbind("<Key>")
        elif (ord(event.char) > 48 and ord(event.char) < 58): #ascii
            squares[row][column].configure(text=event.char)
            squares[row][column].configure(relief=tk.FLAT)
            window.unbind("<Key>")
    window.bind("<Key>", handle_number_entry)

    def handle_mouseclick(event):
        squares[row][column].configure(relief=tk.FLAT)
        window.unbind("<Key>")
    window.bind("<Button>", handle_mouseclick)

for i in range(9):
    squares.append([])
    for j in range(9):
        frame = tk.Frame(master=frame1, relief=tk.RIDGE, borderwidth=1)
        frame.grid(row=i, column=j)
        button = tk.Button(master=frame, width=5, height=2, font = normal_font,
         relief=tk.FLAT, text="", command = lambda row=i, column=j: select_cell(row,column))
        squares[i].append(button)
        button.pack()

frame2 = tk.Frame(master=frame0, width=450, height=50)
frame2.pack(padx=10, pady=(0,20))

for i in range(4):
    frame = tk.Frame(master=frame2, relief=tk.GROOVE, borderwidth=2)
    frame.grid(row=1, column=i, padx=10)
    button = tk.Button(master=frame, width=10, height=2, text='button')
    button.bind("<Button>", handle_click)
    button.pack()


puzzle2 = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
           [6, 0, 0, 1, 9, 5, 0, 0, 0],
           [0, 9, 8, 0, 0, 0, 0, 6, 0],
           [8, 0, 0, 0, 6, 0, 0, 0, 3],
           [4, 0, 0, 8, 0, 3, 0, 0, 1],
           [7, 0, 0, 0, 2, 0, 0, 0, 6],
           [0, 6, 0, 0, 0, 0, 2, 8, 0],
           [0, 0, 0, 4, 1, 9, 0, 0, 5],
           [0, 0, 0, 0, 8, 0, 0, 7, 9]]
load_puzzle(puzzle2)

window.mainloop()