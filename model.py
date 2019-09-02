
hours = ["10:00","10:30","11:00","11:30","12:00","12:30","1:00","1:30","2:00","2:30","3:00","3:30"]


class Guest:
    def __init__(self, first_name="Open", last_name="",email="",phone="", type="d",times = [], choices = [],status=0):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.status = status
        self.times = times
        self.choices = choices
        
    def display(self):
        return "{} {}, email:{}, phone:{}".format(self.first_name, self.last_name, self.email, self.phone)

    def __repr__(self):
        return "{},{},{},{}".format(self.first_name, self.last_name, self.email, self.times)

    def full_name(self):
        return self.first_name + " " + self.last_name
    
class Schedule:

    def __init__(self, name, period, num_attendants):
        self.name=  name
        self.period = period
        self.num_attendants = num_attendants

    def __repr__(self):
        return "{},{},{}".format(self.name, self.period, self.num_attendants)

    def build(self, data):
        
        data[self.name] = dict()
        for hour in hours:
            if hour not in data[self.name] :
                data[self.name][hour] = dict()
            for person in range(self.num_attendants):
                if person not in data[self.name][hour] :
                    data[self.name][hour][person] = dict()
                for time_slot in range(self.period):
                    data[self.name][hour][person][time_slot] = Guest()
        return data