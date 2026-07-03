
from fastapi import FastAPI
import factory_managers
from pydantic import BaseModel


server = FastAPI()
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
