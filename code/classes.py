class TimeSent():
    def __init__(self, year, month, day, hour, min):
        self.time={'year':year,'month':month,'day':day, 'hour':hour, 'min':min}
        self.string = self.time['year'] + "-" + self.time['month']+"-"+self.time['day'] + " " + self.time['hour'] + ":" + \
                 self.time['min']
        self.id=self.string[:7]
    def __get__(self, inp):
        return self.time[inp]

    def __str__(self):
        return self.string

class Thread():
    def __init__(self, name, participants=[], messages={}):
        self.name=name
        self.participants=participants
        self.messages=messages

    def addUser(self,name):
        self.participants.append(name)
        self.messages[name]=[]

    def addMessages(self, name, time, text):
        self.messages[name].append(Message(time, text))


class Message():
    def __init__(self, timeSent, body):
        self.timeSent=timeSent
        self.body=body

class Person():
    def __init__(self, name, messages=[]):
        self.name=name
        self.messages=messages

    def add_message(self, time, body):
        self.messages.append(Message(time, body))