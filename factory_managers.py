import datetime


class Machine:
    def __init__(self,name,is_active=True):
        self.name = name
        self.is_active = is_active


class CementBlockMachine(Machine):
    def produce(self,amount):
        if self.is_active:
            self.amount = amount
            now = datetime.datetime.now()
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            with open("data/production_logs.txt", "a", encoding="utf-8") as file:
                file.write(f"[{formatted_time}] : device {self.name} with {self.amount} kg. is created ✅\n")
            return "✅ Production registered successfully."
        else:
            return f"❌ The {self.name} is off and cannot produce!"


class AsphaltMachine(Machine):
    def produce(self,amount):
        if self.is_active:
            self.amount = amount
            now = datetime.datetime.now()
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            with open("data/production_logs.txt", "a", encoding="utf-8") as file:
                file.write(f"[{formatted_time}] : device {self.name} with {self.amount} kg. is created ✅\n")
            return "✅ Production registered successfully."
        else:
            return f"❌ The {self.name} is off and cannot produce!"





