class Clock:
    # A tick represents a minute
    # 480 is 8:00 AM
    # 545 ticks = 9:05 AM
    def __init__(self):
        self.ticks = 480
        self.nineOFive = False
        self.tenTwenty = False

    def __str__(self):
        return self.ticks

    # Converts 'ticks' into clock time
    def get_formatted_time(self):
        minute = self.ticks % 60
        if minute < 10:
            minute = f"0{minute}"
        if self.ticks > 779:
            hour = int((self.ticks / 60) - 12)
        else:
            hour = int(self.ticks / 60)
        return f"{hour}:{minute} {self.am_or_pm()}"

    def advance_time(self):
        self.ticks += 1
        # Reset time
        if self.ticks == 1500:
            self.ticks = 60

    def am_or_pm(self):
        if self.ticks > 779:
            return "PM"
        else:
            return "AM"