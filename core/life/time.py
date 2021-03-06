__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""


class Time:
    minute_lenght = 60
    hour_lenght = 60
    day_lenght = 24
    week_lenght = 7
    year_lenght = 52

    def __init__(self):
        self.time = 0

    @staticmethod
    def get_x_in_y_lenght(x: str, y: str):
        """Return the value X in the Y unity"""
        order = [
            "minute",
            "hour",
            "day",
            "week",
            "year"
        ]
        unities = {
            "minute": Time.minute_lenght,
            "hour": Time.hour_lenght,
            "day": Time.day_lenght,
            "week": Time.week_lenght,
            "year": Time.year_lenght
        }

        if x in unities.keys() and y in unities.keys():
            space = order.index(y) - order.index(x)
            start_index = order.index(x)
            work = 1
            to_treat = order[start_index:space + 1] if space > 0 else order[::-1][start_index:abs(space) + 1]
            for e in to_treat:
                work *= unities[e]
            return work
        return None

    def next(self):
        """Update the current time"""
        self.time += 1

    def get_in_minutes(self) -> int:
        """Return the current time in minutes"""
        return self.time // Time.minute_lenght

    def get_in_hours(self) -> int:
        """Return the current time in hours"""
        return self.get_in_minutes() // Time.hour_lenght

    def get_in_days(self) -> int:
        """Return the current time in days"""
        return self.get_in_hours() // Time.day_lenght

    def get_in_weeks(self) -> int:
        """Return the current time in weeks"""
        return self.get_in_days() // Time.week_lenght

    def get_in_year(self) -> int:
        """Return the current time in years"""
        return self.get_in_weeks() // Time.year_lenght

    def get_full_year_length_in(self, category: str) -> int:
        """Return the length of the year in 'category' unit"""
        if category.lower() in ['years', 'weeks', 'days', 'hours', 'minutes', 'seconds']:
            if category.lower() == 'years':
                return 1
            elif category.lower() == 'weeks':
                return Time.year_lenght
            elif category.lower() == 'days':
                return Time.week_lenght * self.get_full_year_length_in('weeks')
            elif category.lower() == 'hours':
                return Time.day_lenght * self.get_full_year_length_in('days')
            elif category.lower() == 'minutes':
                return Time.hour_lenght * self.get_full_year_length_in('hours')
            elif category.lower() == 'seconds':
                return Time.minute_lenght * self.get_full_year_length_in('minutes')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.time)


class Condition:
    def __init__(self, key: str, value, importance: float):
        self.key = key
        self.value = value
        self.importance = importance

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{k}: {v} ({i})".format(k=self.key, v=self.value, i=self.importance)


class TriggerEvent:
    def __init__(self, at: float, cond: list):
        self.triggered = False
        self.time = at
        self.condition = cond

    def check(self, current: list) -> bool:
        """Check if the trigger should be launched or not"""
        total = 0.0
        current_time = -1

        for state in current:
            if state.key == "time":
                current_time = state.value

            for cond in self.condition:
                if state.key == cond.key and state.value == cond.value:
                    total += cond.importance
                if total >= 1.0:
                    break
            if total >= 1.0:
                break

        if total and current_time % Time.get_x_in_y_lenght("minute", "year") == self.time:
            self.trigger()
        elif total:
            # to continue the action in the time if needed
            pass
        else:
            self.untrigger()

        return self.triggered

    def should_last(self, states: list) -> bool:
        """Check if the trigger should stay on for a time or turn off"""
        for state in states:
            for cond in self.condition:
                if cond.key == "end_time" and state.key == "time" and cond.value == state.value:
                    return False
                elif cond.key == "end_time" and state.key == "time" and cond.value > state.value:
                    return True
        return False

    def untrigger(self):
        """Disable the trigger"""
        self.triggered = False

    def trigger(self):
        """Activate the trigger"""
        self.triggered = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "condition: {c} ; at: {t}".format(c=self.condition, t=self.time)


class Action:
    def __init__(self, name: str=""):
        self.name = name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class Habit:
    def __init__(self, name: str, trigger_event: TriggerEvent, action: Action):
        self.name = name
        self.trigger_event = trigger_event
        self.launched = False
        self.action = action

    def check(self, states: list) -> bool:
        """Check if the habit should be launched"""
        self.trigger_event.check(states)

        if self.trigger_event.triggered and not self.launched:
            self.start()
        elif self.launched:
            if not self.trigger_event.should_last(states):
                self.stop()

        return self.launched

    def start(self) -> object:
        """Start 'doing' the habit"""
        self.launched = True
        return self

    def stop(self) -> object:
        """Stop 'doing' an habit"""
        self.launched = False
        return self

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name, self.action


class Event(Habit):
    def __init__(self, name: str, trigger_event: TriggerEvent, action: Action):
        super().__init__(name, trigger_event, action)
        self.has_already_been_launched = False

    def start(self) -> object:
        """Start 'doing' the habit"""
        if not self.has_already_been_launched:
            self.has_already_been_launched = True
            self.launched = True
        return self