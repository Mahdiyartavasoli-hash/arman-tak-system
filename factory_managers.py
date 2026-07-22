import datetime
import os
import psycopg2  

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mahdiar_user:my_secure_password@localhost:5433/arman_tak_db")

def get_db_connection():
    
    return psycopg2.connect(DATABASE_URL)

def get_sql_query(query_name):
    try:
        with open("commands.sql", "r", encoding="utf-8") as file:
            content = file.read()
        
        queries = content.split("-- ")
        for q in queries:
            if q.startswith(f"[{query_name}]"):
                return q.replace(f"[{query_name}]", "").strip().replace("?", "%s")
        print(f"⚠️ Query [{query_name}] not found in commands.sql!")
        return None
    except FileNotFoundError:
        print("❌ Error: commands.sql file not found!")
        return None


def save_to_database(machine_id, amount):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        sql_command = get_sql_query("INSERT_PRODUCTION")
        if sql_command:
            cursor.execute(sql_command, (machine_id, amount, now))
            connection.commit()
            connection.close()
            return True
        else:
            connection.close()
            return False
    except psycopg2.Error as e:
        print("❌ Database Error:", e)
        return False


class Machine:
    def __init__(self, name, machine_id, is_active=True):  
        self.name = name
        self.machine_id = machine_id
        self.is_active = is_active

class CementBlockMachine(Machine):
    def produce(self, amount):
        if self.is_active:
            self.amount = amount
            if save_to_database(self.machine_id, self.amount):
                return f"✅ Production Success: {self.name} produced {self.amount} kg."
            else:
                return "❌ Error: Could not save to database."
        else:
            return f"❌ Error: {self.name} is offline!"

class AsphaltMachine(Machine):
    def produce(self, amount):
        if self.is_active:
            self.amount = amount
            if save_to_database(self.machine_id, self.amount):
                return f"✅ Production Success: {self.name} produced {self.amount} kg."
            else:
                return "❌ Error: Could not save to database."
        else:
            return f"❌ Error: {self.name} is offline!"
        

def update_machine_production(record_id, new_amount): 
    try:
        connection = get_db_connection()
        cursor = connection.cursor()  
        
        sql_command = get_sql_query("UPDATE_PRODUCTION")
        if sql_command:
            cursor.execute(sql_command, (new_amount, record_id))
            connection.commit()
            connection.close()
            return True
        else:
            connection.close()
            return False
    except psycopg2.Error as e:
        print("❌ Database Error inside update function:", e)
        return False


def delete_production_record(record_id):
    try:
        connection = get_db_connection()
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
    except psycopg2.Error as e:
        print("❌ Database Error inside delete function:", e)
        return False
    

def get_high_production(machine_name, min_amount):
    try:
        connection = get_db_connection() 
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
    except psycopg2.Error as e:
        print("❌ Database Error:", e)
        return []


def get_ordered_production(machine_name):
    try:
        connection = get_db_connection() 
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
    except psycopg2.Error as e:
        print("❌ Database Error:", e)
        return []


def get_machine_analytics(machine_name):
    try:
        connection = get_db_connection() 
        cursor = connection.cursor()
        sql_command = get_sql_query("get_analytics")  
        if sql_command:
            cursor.execute(sql_command,(machine_name,))
            record = cursor.fetchone()
            connection.close()
            if record and record[0] is not None:
                return record  
            return (0, 0)
        else:
            connection.close()
            return (0, 0)
    except psycopg2.Error as e:
        print("❌ Database Error:", e)
        return (0, 0)


def get_machine_extremes(machine_name):
    try:
        connection = get_db_connection() 
        cursor = connection.cursor()
        sql_command = get_sql_query("get_max_min")  
        if sql_command:
            cursor.execute(sql_command,(machine_name,))
            record = cursor.fetchone()
            connection.close()
            if record and record[0] is not None:
                return record  
            return (0, 0)
        else:
            connection.close()
            return (0, 0)
    except psycopg2.Error as e:
        print("❌ Database Error:", e)
        return (0, 0)


def get_machine_production_count(machine_name):
    try:
        connection = get_db_connection() 
        cursor = connection.cursor()
        sql_command = get_sql_query("get_production_count")  
        if sql_command:
            cursor.execute(sql_command,(machine_name,))
            record = cursor.fetchone()
            connection.close()
            if record and record[0] is not None:
                return record[0]  
            return 0
        else:
            connection.close()
            return 0
    except psycopg2.Error as e:
        print("❌ Database Error:", e)
        return 0