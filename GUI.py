# Author:  Cody Lovett

from tkinter import *
from tkinter.ttk import Progressbar
from bible_study_organiser import Person, BibleStudy, Solver
import threading
import queue
import time
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

# in ms
max_process_frame = 100
usable_time = 100


class ThreadedToken:
    def __init__(self, value):
        self.value = value

class ThreadGenerator:
    def __init__(self, generator):
        self.generator = generator

    def run(self, queue, finish=None):
        for item in self.generator:
            queue.put(item)
            if finish is not None and finish.value == True:
                break


class TKSuggestion:
    def __init__(self, root):
        self.root = root
        root.protocol("WM_DELETE_WINDOW", self.close)

        Grid.columnconfigure(root, 0, weight=1)
        Grid.rowconfigure(root, 0, weight=1)

        self.times_box = Listbox(self.root)
        self.times_box.grid(row=0, column=0, rowspan=3, sticky=N+E+S+W)

        frm = Frame(root)
        frm.grid(row=0, column=1, sticky=N+E)
        Button(frm, text='add person', command=lambda: TKPerson(root, self.add_person)).pack(fill=BOTH)
        Button(frm, text='add bible study', command=lambda: TKBibleStudy(root, self.add_bible_study)).pack(fill=BOTH)
        Button(frm, text='settings', command=self.change_settings).pack(fill=BOTH)

        self.people_box = Listbox(self.root, height=1)
        self.people_box.grid(row=1, column=1, sticky=N+E+S+W)

        self.bible_box = Listbox(self.root, height=1)
        self.bible_box.grid(row=2, column=1, sticky=N+E+S+W)

        self.progress = Progressbar(self.root,orient=HORIZONTAL,mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=E+W)

        self.people = []
        self.studies = []

        self.suggestion_queue = queue.Queue()
        self.suggestions = []

        self.suggestion_thread = None
        self.finish_suggestions = ThreadedToken(None)
        self.restart_suggestions()
        self.update_suggestions()

    def update_suggestions(self):
        changed = False

        start = time.time()
        while True:
            if time.time() > start + max_process_frame/1000:
                break
            try:
                value, score, done = self.suggestion_queue.get_nowait()
                self.suggestions.append((value, score))
                self.progress['value'] = int(done*100)
                changed = True
                print(done)
            except queue.Empty:
                self.progress['value'] = 100
                break

        if changed:
            self.times_box.delete(0,'end')

            self.suggestions.sort(key=lambda x: x[1])
            for value, score in self.suggestions[:100]:
                text = f'{score[0]:0>3} | {score[1]:0>3} | {", ".join(v[0] + " " + str(v[1]) for v in value)}'
                self.times_box.insert(END, text)

        self.root.after(usable_time, self.update_suggestions)

    def add_person(self, person: Person):
        self.people.append(person)
        self.people_box.insert(END, person.name)
        self.people_box.config(height=self.people_box.size())
        self.restart_suggestions()

    def add_bible_study(self, study: BibleStudy):
        self.studies.append(study)
        size = self.bible_box.size()
        self.bible_box.insert(END, f'Bible study {size+1}')
        self.bible_box.config(height=size+1)
        self.restart_suggestions()

    def change_settings(self):
        print('change_settings')

    def restart_suggestions(self):
        self.progress['value'] = 100
        self.suggestions = []
        self.finish_suggestions.value = True
        if self.suggestion_thread is not None:
            self.suggestion_thread.join()
        self.finish_suggestions.value = False

        self.solver = Solver(self.people, self.studies)
        self.suggestion_generator = ThreadGenerator(self.solver.solve())

        self.suggestion_thread = threading.Thread(
            target=self.suggestion_generator.run,
            args=(
                self.suggestion_queue,
                self.finish_suggestions,
            ),
        )
        self.suggestion_thread.start()

    def close(self):
        self.finish_suggestions.value = True
        self.suggestion_thread.join()
        self.root.destroy()


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
        self.input_times.grid(row=1, column=1, sticky=E+W)

        OptionMenu(self.root, self.input_role, *people_types).grid(row=2, column=1, sticky=W)

        Checkbutton(self.root, text='class day', variable=self.input_pref_day).grid(row=3, column=1, sticky=W)

        Button(self.root, text='Submit', command=self.submit).grid(row=4, column=1, sticky=E)

    def get_person(self):
        name = self.input_name.get()
        times = self.input_times.get("1.0",END).strip().split('\n')
        return Person(name, times)

    def submit(self):
        self.add_fn(self.get_person())
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

        self.input_length = Spinbox(self.root, from_=1, to=10)
        self.input_length.grid(row=0, column=1, sticky=E+W)

        Checkbutton(self.root, text='monday', variable=None).grid(row=1, column=1, sticky=W)
        Checkbutton(self.root, text='tuesday', variable=None).grid(row=2, column=1, sticky=W)
        Checkbutton(self.root, text='wednesday', variable=None).grid(row=3, column=1, sticky=W)
        Checkbutton(self.root, text='thursday', variable=None).grid(row=4, column=1, sticky=W)
        Checkbutton(self.root, text='friday', variable=None).grid(row=5, column=1, sticky=W)
        Checkbutton(self.root, text='saturday', variable=None).grid(row=6, column=1, sticky=W)
        Checkbutton(self.root, text='sunday', variable=None).grid(row=7, column=1, sticky=W)

        Button(self.root, text='Submit', command=self.submit).grid(row=8, column=1, sticky=E)

    def get_study(self):
        length = self.input_length.get()
        return BibleStudy(int(length))

    def submit(self):
        self.add_fn(self.get_study())
        self.root.grab_release()
        self.root.destroy()


main = Tk()

TKSuggestion(main)

main.mainloop()
