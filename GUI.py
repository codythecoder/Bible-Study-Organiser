# Author:  Cody Lovett

from tkinter import *
# import bible_study_organiser as b
#
# studies =[None, None]
#
# main = Tk()
# frame=Frame(main)
# Grid.rowconfigure(main, 0, weight=1)
# Grid.columnconfigure(main, 0, weight=1)
# frame.grid(sticky=N+S+E+W)
# grid=Frame(frame)
# grid.grid(sticky=N+S+E+W)
# Grid.rowconfigure(frame, 0, weight=1)
# Grid.columnconfigure(frame, 0, weight=1)
#
# Grid.columnconfigure(grid, 0, weight=0)
# for i, day in enumerate(b.days):
#     btn = Label(grid, text=day.capitalize())
#     btn.grid(column=i+1, row=0, sticky=N+S+E+W)
#     Grid.columnconfigure(grid, i+1, weight=1)
#
# Grid.rowconfigure(grid, 0, weight=0)
# for i, time in enumerate(b.time_24h):
#     btn = Label(grid, text=time)
#     btn.grid(column=0, row=i+1, sticky=N+S+E+W)
#     Grid.rowconfigure(grid, i+1, weight=1)
#
# import random
# for i, day in enumerate(b.days):
#     for j, time in enumerate(b.time_24h):
#         frm = Frame(grid)
#         frm.grid(column=i+1, row=j+1, sticky=N+S+E+W, pady=(0, 5))
#         # Grid.columnconfigure(frm, 0, weight=1)
#         for k in range(len(studies)):
#             color = random.randrange(255)
#             rgb = f'#00{color:0>2x}00'
#             Grid.columnconfigure(frm, 0, weight=1, uniform="fred")
#             btn = Button(frm, bg=rgb, text=f'{color}')
#             btn.grid(row=k, column=0, sticky=N+S+E+W)
#             Grid.rowconfigure(frm, k, weight=1, uniform="fred")
#
# main.title("HI!")
#
# main.mainloop()

people_types = (
    'student',
    'mission worker',
    'pastor',
)

class TKSuggestion:
    def __init__(self, root):
        self.root = root
        Grid.columnconfigure(root, 0, weight=1)
        Grid.rowconfigure(root, 0, weight=1)

        self.times_box = Listbox(self.root)
        self.times_box.grid(row=0, column=0, rowspan=3, sticky=N+E+S+W)
        self.times_box.insert(END, 'Tue 10am-11am, Wed 2pm-3pm')

        frm = Frame(root)
        frm.grid(row=0, column=1, sticky=N+E)
        Button(frm, text='add person', command=lambda: TKPerson(root, self.add_person)).pack(fill=BOTH)
        Button(frm, text='add bible study', command=lambda: TKBibleStudy(root, self.add_bible_study)).pack(fill=BOTH)
        Button(frm, text='settings', command=self.change_settings).pack(fill=BOTH)

        self.people_box = Listbox(self.root, height=1)
        self.people_box.grid(row=1, column=1, sticky=N+E+S+W)

        self.bible_box = Listbox(self.root, height=1)
        self.bible_box.grid(row=2, column=1, sticky=N+E+S+W)

    def add_person(self, person):
        self.people_box.insert(END, person)
        self.people_box.config(height=self.people_box.size())

    def add_bible_study(self, study):
        size = self.bible_box.size()
        self.bible_box.insert(END, f'Bible study {size+1}')
        self.bible_box.config(height=size+1)

    def change_settings(self):
        print('change_settings')


class TKPerson:
    def __init__(self, root, add_fn):
        self.add_fn = add_fn
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.title('Add Person')

        Label(self.root, text='Name:').grid(row=0, column=0, sticky=N+E)
        Label(self.root, text='Class times:').grid(row=1, column=0, sticky=N+E)
        Label(self.root, text='Role:').grid(row=2, column=0, sticky=N+E+S)
        Label(self.root, text='Preferences:').grid(row=3, column=0, sticky=N+E)

        self.input_role = StringVar(self.root)
        self.input_pref_day = IntVar(self.root)

        self.input_role.set(people_types[0])

        self.input_name = Entry(self.root)
        self.input_name.grid(row=0, column=1, sticky=E+W)
        self.input_times = Text(self.root, width=20, height=10)
        self.input_times.grid(row=1, column=1)

        OptionMenu(self.root, self.input_role, *people_types).grid(row=2, column=1, sticky=W)

        Checkbutton(self.root, text='class day', variable=self.input_pref_day).grid(row=3, column=1, sticky=W)

        Button(self.root, text='Submit', command=self.submit).grid(row=4, column=1, sticky=E)

    def submit(self):
        self.add_fn(self.input_name.get())
        self.root.grab_release()
        self.root.destroy()


class TKBibleStudy:
    def __init__(self, root, add_fn):
        self.add_fn = add_fn
        self.root = Toplevel(root)
        self.root.grab_set()
        self.root.title('Add Bible Study')

        Label(self.root, text='Length:').grid(row=0, column=0, sticky=N+E)
        Label(self.root, text='Days:').grid(row=1, column=0, sticky=N+E)

        Spinbox(self.root, from_=1, to=10).grid(row=0, column=1, sticky=E+W)

        Checkbutton(self.root, text='monday', variable=None).grid(row=1, column=1, sticky=W)
        Checkbutton(self.root, text='tuesday', variable=None).grid(row=2, column=1, sticky=W)
        Checkbutton(self.root, text='wednesday', variable=None).grid(row=3, column=1, sticky=W)
        Checkbutton(self.root, text='thursday', variable=None).grid(row=4, column=1, sticky=W)
        Checkbutton(self.root, text='friday', variable=None).grid(row=5, column=1, sticky=W)
        Checkbutton(self.root, text='saturday', variable=None).grid(row=6, column=1, sticky=W)
        Checkbutton(self.root, text='sunday', variable=None).grid(row=7, column=1, sticky=W)

        Button(self.root, text='Submit', command=self.submit).grid(row=8, column=1, sticky=E)


    def submit(self):
        self.add_fn(None)
        self.root.grab_release()
        self.root.destroy()


main = Tk()

TKSuggestion(main)

main.mainloop()
