from tkinter import *
import bible_study_organiser as b

studies =[None, None]

main = Tk()
frame=Frame(main)
Grid.rowconfigure(main, 0, weight=1)
Grid.columnconfigure(main, 0, weight=1)
frame.grid(sticky=N+S+E+W)
grid=Frame(frame)
grid.grid(sticky=N+S+E+W)
Grid.rowconfigure(frame, 0, weight=1)
Grid.columnconfigure(frame, 0, weight=1)

Grid.columnconfigure(grid, 0, weight=0)
for i, day in enumerate(b.days):
    btn = Label(grid, text=day.capitalize())
    btn.grid(column=i+1, row=0, sticky=N+S+E+W)
    Grid.columnconfigure(grid, i+1, weight=1)

Grid.rowconfigure(grid, 0, weight=0)
for i, time in enumerate(b.time_24h):
    btn = Label(grid, text=time)
    btn.grid(column=0, row=i+1, sticky=N+S+E+W)
    Grid.rowconfigure(grid, i+1, weight=1)

import random
for i, day in enumerate(b.days):
    for j, time in enumerate(b.time_24h):
        frm = Frame(grid)
        frm.grid(column=i+1, row=j+1, sticky=N+S+E+W, pady=(0, 5))
        # Grid.columnconfigure(frm, 0, weight=1)
        for k in range(len(studies)):
            color = random.randrange(255)
            rgb = f'#00{color:0>2x}00'
            Grid.columnconfigure(frm, 0, weight=1, uniform="fred")
            btn = Button(frm, bg=rgb, text=f'{color}')
            btn.grid(row=k, column=0, sticky=N+S+E+W)
            Grid.rowconfigure(frm, k, weight=1, uniform="fred")

main.title("HI!")

main.mainloop()
