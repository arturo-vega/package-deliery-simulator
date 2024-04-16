class Package:
    # This is the package class
    def __init__(self, id, address, city, state, zipcode, deadline, weight, special_notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = 'Home' # Should only be 'Home', 'Outbound' or 'Delivered'
        self.missedDelivery = False

        self.deliverTime = 0

    def __str__(self):
        if self.deliverTime == 0:
            self.deliverTime = "Awaiting Delivery"
        if self.special_notes == "":
            return f"Package ID: {self.id} - Address: {self.address} | City: {self.city} | State: {self.state} | Zipcode: {self.zipcode} | Deadline: {self.deadline} | Weight: {self.weight} | Status: {self.status} | Time Delivered: {self.deliverTime}\n"
        else:
            return f"Package ID: {self.id} - Address: {self.address} | City: {self.city} | State: {self.state} | Zipcode: {self.zipcode} | Deadline: {self.deadline} | Weight: {self.weight} | Status: {self.status} | Time Delivered: {self.deliverTime}\nSpecial Notes: {self.special_notes}\n"

    # Converts deadline string into an int that can be understood by the Clock
    def get_deadline_in_ticks(self):
        if self.deadline == "EOD":
            deadlineTicks = 1020

        else:
            timeParts = self.deadline.split()
            hoursMinutes = timeParts[0].split(":")
            hours = int(hoursMinutes[0])
            minutes = int(hoursMinutes[1])

            if timeParts[1] == "AM":
                deadlineTicks = (hours * 60) + minutes
            else:
                deadlineTicks = (hours * 60) + minutes + 780

        return deadlineTicks
