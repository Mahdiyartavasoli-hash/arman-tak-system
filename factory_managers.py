import datetime
import sqlite3

def get_sql_query(query_name):
    try:
        with open("commands.sql", "r", encoding="utf-8") as file:
            content = file.read()
        
        queries = content.split("-- ")
        for q in queries:
            if q.startswith(f"[{query_name}]"):
                return q.replace(f"[{query_name}]", "").strip()
        print(f"⚠️ Query [{query_name}] not found in commands.sql!")
        return None
    except FileNotFoundError:
        print("❌ Error: commands.sql file not found!")
        return None

def save_to_database(machine_name, amount):
    try:
        connection = sqlite3.connect("factory.db")
        cursor = connection.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        sql_command = get_sql_query("INSERT_PRODUCTION")
        if sql_command:
            cursor.execute(sql_command, (machine_name, amount, now))
            connection.commit()
            connection.close()
            return True
        else:
            connection.close()
            return False
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
        
        sql_command = get_sql_query("UPDATE_PRODUCTION")
        if sql_command:
            cursor.execute(sql_command, (new_amount, machine_name, target_date))
            connection.commit()
            connection.close()
            return True
        else:
            connection.close()
            return False
    except sqlite3.Error as e:
        print("❌ Database Error inside update function:", e)
        return False

def delete_production_record(record_id):
    try:
        connection = sqlite3.connect("factory.db")
        cursor = connection.cursor()
        
        sql_command = get_sql_query("DELETE_PRODUCTION")
        if sql_command:
            cursor.execute(sql_command, (record_id,))
            connection.commit()
            connection.close()
            return True
        else:
            connection.close()
            return False
    except sqlite3.Error as e:
        print("❌ Database Error inside delete function:", e)
        return False
    
def get_high_production(machine_name, min_amount):
    try:
        connection = sqlite3.connect("factory.db") 
        cursor = connection.cursor()
        sql_command = get_sql_query("SELECT_HIGH_PRODUCTION")  
        if sql_command:
            cursor.execute(sql_command,(machine_name,min_amount))
            records = cursor.fetchall()
            connection.close()
            return records
        else:
            connection.close()
            return []
    except sqlite3.Error as e:
        print("❌ Database Error:", e)
        return []

def get_ordered_production(machine_name):
    try:
        connection = sqlite3.connect("factory.db") 
        cursor = connection.cursor()
        sql_command = get_sql_query("SELECT_ORDERED_PRODUCTION")  
        if sql_command:
            cursor.execute(sql_command,(machine_name,))
            records = cursor.fetchall()
            connection.close()
            return records
        else:
            connection.close()
            return []
    except sqlite3.Error as e:
        print("❌ Database Error:", e)
        return []


