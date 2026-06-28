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

def update_machine_production(machine_name, new_amount, target_date): 
    try:
        connection = sqlite3.connect("factory.db")
        cursor = connection.cursor()  
        cursor.execute(
                "UPDATE production SET amount = ? WHERE machine_name = ? AND date = ?;",
                (new_amount, machine_name, target_date)
            )
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error as e:
        print("❌ Database Error inside update function:", e)
        return False
def delete_production_record(record_id):
    try:
        connection = sqlite3.connect("factory.db")
        cursor = connection.cursor()
        
        cursor.execute(
            "DELETE FROM production WHERE id = ?;",
            (record_id,)
        )
        
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error as e:
        print("❌ Database Error inside delete function:", e)
        return False
