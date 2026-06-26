import datetime
import sqlite3

def save_to_database(machine_name, amount):
    try:
        connection = sqlite3.connect("factory.db")
        cursor = connection.cursor()
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO production (machine_name, amount, date)
            VALUES (?, ?, ?)
        """, (machine_name, amount, now))
        
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error as e:
        print("❌ Database Error:", e)
        return False

class Machine:
    def __init__(self, name, is_active=True):
        self.name = name
        self.is_active = is_active

class CementBlockMachine(Machine):
    def produce(self, amount):
        if self.is_active:
            self.amount = amount
            if save_to_database(self.name, self.amount):
                return f"✅ Production Success: {self.name} produced {self.amount} kg."
            else:
                return "❌ Error: Could not save to database."
        else:
            return f"❌ Error: {self.name} is offline!"

class AsphaltMachine(Machine):
    def produce(self, amount):
        if self.is_active:
            self.amount = amount
            if save_to_database(self.name, self.amount):
                return f"✅ Production Success: {self.name} produced {self.amount} kg."
            else:
                return "❌ Error: Could not save to database."
        else:
            return f"❌ Error: {self.name} is offline!"
        