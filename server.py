
from fastapi import FastAPI
import factory_managers
from pydantic import BaseModel
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mahdiar_user:my_secure_password@127.0.0.1:5433/arman_tak_db")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # ۱. جدول factory_managers
    cur.execute("""
        CREATE TABLE IF NOT EXISTS factory_managers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            role VARCHAR(50) NOT NULL
        );
    """)
    
    # ۲. جدول machines
    cur.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id SERIAL PRIMARY KEY,
            machine_name VARCHAR(100) NOT NULL,
            model_year INTEGER
        );
    """)

    # ۳. جدول production
    cur.execute("""
        CREATE TABLE IF NOT EXISTS production (
            id SERIAL PRIMARY KEY,
            machine_id INTEGER REFERENCES machines(id),
            amount INTEGER,
            date VARCHAR(50)
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

server = FastAPI()

@server.on_event("startup")
def startup_event():
    init_db()

@server.get("/")
def home():
    return {"message": "Welcome to ARMAN TAK Factory API"}

@server.get("/analytics")
def get_factory_analytics(machine_name: str):
    analytics = factory_managers.get_machine_analytics(machine_name)
    return{
        "machine": machine_name,
        "total_production": analytics[0],
        "average_production": analytics[1]
    }

@server.get("/max_min")
def get_factory_max_min(machine_name: str):
    max_min = factory_managers.get_machine_extremes(machine_name)
    return{
        "machine": machine_name,
        "max_production": max_min[0],
        "min_production": max_min[1]
    }

@server.get("/production_count")
def get_production_count(machine_name: str):
    total_runs = factory_managers.get_machine_production_count(machine_name)
    return{
        "machine": machine_name,
        "Total_Production_Count": total_runs,
    }

class ProductionRecord(BaseModel):
    machine_name: str
    production_amount: float
@server.post("/insert_production")
def add_production_log(record: ProductionRecord):
    factory_managers.save_to_database(record.machine_name, record.production_amount)
    
    return {"status": "success", "message": "Record added successfully"}

class UpdateProduction(BaseModel):
    record_id: int
    new_production_amount: float

@server.put("/update_production")
def update_production_log(data: UpdateProduction):
    factory_managers.update_machine_production(data.record_id, data.new_production_amount) 
    
    return {"status": "success", "message": "Record updated successfully"} 

class DeleteProduction(BaseModel):
     record_id: int
@server.delete("/delete_production") 
def delete_production_log(data: DeleteProduction):
    factory_managers.delete_production_record(data.record_id)

    return {"status": "success", "message": "Record deleted successfully"}  
