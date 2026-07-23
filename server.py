import os
import asyncpg
import aiosql
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from security import hash_password

load_dotenv()

# --- Load SQL Queries ---
queries = aiosql.from_path("queries.sql", "asyncpg", mandatory_parameters=False)

# --- Database Connection Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mahdiar_user:my_secure_password@127.0.0.1:5433/arman_tak_db")

# --- Async Lifetime & Database Pool Setup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await asyncpg.create_pool(DATABASE_URL)
    
    async with app.state.db.acquire() as conn:
        await queries.create_table_factory_managers(conn)
        await queries.create_table_machines(conn)
        await queries.create_table_production(conn)
        await queries.create_table_users(conn)
        
    yield
    await app.state.db.close()

# --- FastAPI Initialization ---
server = FastAPI(
    title="Arman Tak System API",
    description="Clean Architecture API with Separate SQL Layer",
    version="3.0.0",
    lifespan=lifespan
)

# --- Pydantic Schemas ---
class MachineCreate(BaseModel):
    machine_name: str = Field(..., example="CementBlockMachine")
    model_year: int = Field(..., example=2024)

class ProductionCreate(BaseModel):
    machine_id: int = Field(..., example=1, description="ID of the machine")
    amount: int = Field(..., gt=0, example=200, description="Production amount must be > 0")
    date: str = Field(..., example="2026-07-21", description="Date formatted YYYY-MM-DD")

class ProductionUpdate(BaseModel):
    record_id: int = Field(..., example=1)
    new_amount: int = Field(..., gt=0, example=250)

class UserRegister(BaseModel):
    username: str = Field(..., example="mahdiar")
    password: str = Field(..., example="secret123")

# --- Endpoints ---

@server.get("/", tags=["General"])
async def home():
    return {"message": "Welcome to ARMAN TAK Factory API (Clean SQL Architecture)"}

# 1. Create Machine
@server.post("/machines", status_code=status.HTTP_201_CREATED, tags=["Machines"])
async def create_machine(machine: MachineCreate):
    async with server.state.db.acquire() as conn:
        new_id = await queries.create_machine(conn, machine_name=machine.machine_name, model_year=machine.model_year)
        return {"status": "success", "machine_id": new_id, "message": "Machine created successfully"}

# 2. Insert Production Log
@server.post("/insert_production", status_code=status.HTTP_201_CREATED, tags=["Production"])
async def add_production_log(record: ProductionCreate):
    async with server.state.db.acquire() as conn:
        machine_exists = await queries.check_machine_exists(conn, machine_id=record.machine_id)
        if not machine_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Machine with ID {record.machine_id} does not exist."
            )

        production_id = await queries.insert_production(
            conn, machine_id=record.machine_id, amount=record.amount, date=record.date
        )
        return {
            "status": "success",
            "message": "Production record logged successfully",
            "data": {"id": production_id, "machine_id": record.machine_id, "amount": record.amount, "date": record.date}
        }

# 3. Update Production Log
@server.put("/update_production", tags=["Production"])
async def update_production_log(data: ProductionUpdate):
    async with server.state.db.acquire() as conn:
        updated_id = await queries.update_production(conn, new_amount=data.new_amount, record_id=data.record_id)
        if not updated_id:
            raise HTTPException(status_code=404, detail=f"Record with ID {data.record_id} not found.")

        return {"status": "success", "message": "Record updated successfully"}

# 4. Delete Production Log
@server.delete("/delete_production/{record_id}", tags=["Production"])
async def delete_production_log(record_id: int):
    async with server.state.db.acquire() as conn:
        deleted_id = await queries.delete_production(conn, record_id=record_id)
        if not deleted_id:
            raise HTTPException(status_code=404, detail=f"Record with ID {record_id} not found.")

        return {"status": "success", "message": "Record deleted successfully"}

# 5. Analytics Endpoint
@server.get("/analytics/{machine_id}", tags=["Analytics"])
async def get_factory_analytics(machine_id: int):
    async with server.state.db.acquire() as conn:
        result = await queries.get_analytics(conn, machine_id=machine_id)
        if not result or result['total_production'] is None:
            raise HTTPException(status_code=404, detail="No production records found for this machine.")

        return {
            "machine_id": machine_id,
            "total_production": result['total_production'],
            "average_production": round(float(result['average_production']), 2)
        }

# 6. User Register
@server.post("/register", status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register_user(user_data: UserRegister):
    hashed_pwd = hash_password(user_data.password)
    
    async with server.state.db.acquire() as conn:
        try:
            new_user_id = await queries.register_user(conn, username=user_data.username, password=hashed_pwd)
            return {
                "status": "success",
                "message": "User registered successfully",
                "user_id": new_user_id
            }
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=400, 
                detail="Username already exists. Please choose another username."
            )