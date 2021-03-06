import datetime as dt
from itertools import product, permutations

time_24h = {
    '12am':'0',
    '1am':'1',
    '2am':'2',
    '3am':'3',
    '4am':'4',
    '5am':'5',
    '6am':'6',
    '7am':'7',
    '8am':'8',
    '9am':'9',
    '10am':'10',
    '11am':'11',
    '12pm':'12',
    '1pm':'13',
    '2pm':'14',
    '3pm':'15',
    '4pm':'16',
    '5pm':'17',
    '6pm':'18',
    '7pm':'19',
    '8pm':'20',
    '9pm':'21',
    '10pm':'22',
    '11pm':'23',
}

days = (
    'mon',
    'tue',
    'wed',
    'thu',
    'fri',
    'sat',
    'sun',
)

def bulk_replace(s, d):
    for t in d:
        s = s.replace(t, d[t])
    return s

class Person:
    def __init__(self, name, classes=[], preferences=[]):
        self.name = name
        self.classes = [Time(c) for c in classes]
        self.preferences = preferences

    def score(self, bible_studies):
        bad = 0

        clash = True
        for study in bible_studies:
            if all(not study.time.is_clash(time) for time in self.classes):
                clash = False
                break

        if clash:
            return 1, 0

        if 'class_day' in self.preferences:
            day = False
            for study in bible_studies:
                if any(study.time.day == time.day for time in self.classes):
                    day = True
                    break
            if not day:
                bad += 1

        # if 'class_time' in self.preferences:
        #     if

        return 0, bad

    def details(self):
        bad = [0]*len(self.preferences)

        clash = []
        for study in bible_studies:
            clash.append(all(not study.time.is_clash(time) for time in self.classes))

        return clash, bad

    def __str__(self):
        return f'Person({name})'

class BibleStudy:
    def __init__(self, hours=1, goals=[]):
        self.hours = hours
        self.goals = goals
        self.time = None
        self.clear_people()

    def clear_people(self):
        self.people = []

    def score(self):
        fails = 0
        bad = 0

        for goal in self.goals:
            if goal == 'even':
                # make the bible studies as even as possible
                pass
            elif goal == 'weekday':
                if self.time.day in ('sat', 'sun'):
                    fails += 1
            elif goal.startswith('after_'):
                pass
            elif goal.startswith('before_'):
                pass
            else:
                raise NotImplementedError(f"goal '{goal}' not implemented")

        return fails, bad

    def set_time(self, day, time):
        self.time = Time(f'{day} {time}-{time+self.hours}')

    def add_person(self, person):
        self.people.append(person)

class Time:
    def __init__(self, time):
        if type(time) == Time:
            self.day = time.day
            self.times = tuple(time.time)
            return

        if ' ' not in time:
            time += ' 0-24'

        time = time.replace('<', '0')
        time = time.replace('>', '24')

        day, times = time.split(' ', 1)

        self.day = day[:3].lower()

        times = times.replace(' ', '')
        times = bulk_replace(times, time_24h).split('-')

        self.times = (int(times[0]), int(times[1]) or 24)

    def is_clash(self, other: 'Time'):
        if self.day != other.day:
            return False

        if self.times[0] < other.times[1] and other.times[0] < self.times[1]:
            return True

        return False

    def distance(self, other: 'Time'):
        if self.day != other.day:
            return 24
        if self.is_clash(self, other):
            return 0
        return min(abs(self.times[0] - other.times[1]), abs(other.times[0] - self.times[1]))

    def __str__(self):
        return f'{self.day} {self.times[0]}-{self.times[1]}'

class Solver:
    study_times = tuple(product(days, list(range(24))))

    def __init__(self, people, studies):
        self.people = people
        self.studies = studies
        self.total_num_scores = len(self.study_times)**len(self.studies)

    def solve(self):
        num_people = len(self.people)
        num_studies = len(self.studies)

        if not self.studies or not self.people:
            return

        for count, times in enumerate(permutations(self.study_times, num_studies)):
            for study, time in zip(self.studies, times):
                study.set_time(*time)

            total_score = [0, 0]
            for person in self.people:
                score = person.score(self.studies)
                total_score = total_score[0] + score[0], total_score[1] + score[1]

            for study in self.studies:
                score = study.score()
                total_score = total_score[0] + score[0], total_score[1] + score[1]
            yield times, total_score, count/self.total_num_scores


# Here's the goals and preferences that people might have
# class_day       - on the same day as a class
# class_time      - close to a class that they have
# friends_[a]_[b] - in a study with friends a and b
# essential_[n]   - one of these people must be at the bible study
#                 - in the case where you need to have one mission worker and
#                 - one minister you would have "essential_1" for the first
#                 - group and "essential_2" for the second
# upper_campus    - bible study can't be within an hour of class

# Here's some goals and preferences that a bible study might have
# even            - each bible study should have equal numbers
# after_[n]       - bible study should be after time [n] (e.g. 11)
# before_[n]      - bible study should be before time [n] (e.g. 2pm)
# weekday         - bible study can only be on a weekday

# cody = Person(
#     "cody",
#     classes=(
#         "Tuesday 1pm-3pm",
#         "Tue 15-16",
#         "Wednesday 15-16",
#     ),
#     goals=(
#         "class_day",
#     ),
#     preferences=(
#         "class_time",
#     ),
# )
#
# alan = Person(
#     "alan",
#     classes=(
#         "tue <-15", # before 3pm on tuesday
#         "tue 17->",
#         "wednesday 15-16",
#         "wed 15-16, 17-18",
#     ),
#     goals=(
#         "class_day",
#     ),
#     preferences=(
#         "class_time",
#     ),
# )
#
# bec = Person(
#     "bec",
#     goals=(
#         "friends_alan_naomi",
#     ),
# )
#
# naomi = Person(
#     "naomi",
#     classes=(
#         "Monday 1pm-3pm",
#         "Wednesday 2pm-3pm",
#         "Wednesday 3pm-4pm",
#     ),
#     goals=(
#         "essential_1",
#     )
# )
#
# ian = Person(
#     "ian",
#     free=(
#         "Tuesday",
#         "Wednesday",
#         "Thu 11-13",
#         "Thu 15-17",
#     ),
#     goals=(
#         "essential_1",
#     )
# )

# # people = (cody, alan, bec, naomi, ian)
# people = (cody, ian)
# studies = (BibleStudy(1, goals=['weekday']), BibleStudy(1))
# # studies = (BibleStudy(1),)
#
# scores = solve(people, studies)
# print(sorted(scores.items(), key=lambda x:x[1])[:100])
# print(len(scores))
