import os
import asyncpg
import aiosql
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from security import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from exceptions import DuplicateEntityError, EntityNotFoundError
from handlers import duplicate_entity_exception_handler, entity_not_found_exception_handler
from celery_app import generate_heavy_analytics_report

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
        
        # await queries.drop_table_users(conn)
        await queries.create_table_users(conn)    
        await queries.create_table_machines(conn)
        await queries.create_table_production(conn)
        
    yield
    await app.state.db.close()

# --- FastAPI Initialization ---

server = FastAPI(
    title="Arman Tak System API",
    description="Clean Architecture API with Separate SQL Layer",
    version="3.0.0",
    lifespan=lifespan
)

server.add_exception_handler(DuplicateEntityError, duplicate_entity_exception_handler)
server.add_exception_handler(EntityNotFoundError, entity_not_found_exception_handler)

# --- Pydantic Schemas ---

class MachineCreate(BaseModel):
    machine_name: str = Field(..., examples=["CementBlockMachine"])
    model_year: int = Field(..., examples=[2024])

class ProductionCreate(BaseModel):
    machine_id: int = Field(..., examples=[1], description="ID of the machine")
    amount: int = Field(..., gt=0, examples=[200], description="Production amount must be > 0")
    date: str = Field(..., examples=["2026-07-21"], description="Date formatted YYYY-MM-DD")

class ProductionUpdate(BaseModel):
    record_id: int = Field(..., examples=[1])
    new_amount: int = Field(..., gt=0, examples=[250])

class UserRegister(BaseModel):
    username: str = Field(..., examples=["mahdiar"])
    password: str = Field(..., examples=["secret123"])
    role: str = "operator"

# --- Endpoints ---

@server.get("/", tags=["General"])
async def home():
    return {"message": "Welcome to ARMAN TAK Factory API (Clean SQL Architecture)"}

# 1. Create Machine
@server.post("/machines", status_code=status.HTTP_201_CREATED, tags=["Machines"])
async def create_machine(
    machine: MachineCreate, 
    current_user: str = Depends(get_current_user)
):
    async with server.state.db.acquire() as conn:
        
        db_user = await queries.get_user_by_username(conn, username=current_user)
        
        
        if not db_user or db_user["role"] != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins are allowed to perform this action")
            
        
        new_id = await queries.create_machine(conn, machine_name=machine.machine_name, model_year=machine.model_year)
        return {"status": "success", "machine_id": new_id, "message": "Machine created successfully"}

# 2. Insert Production Log
@server.post("/insert_production", status_code=status.HTTP_201_CREATED, tags=["Production"])
async def add_production_log(record: ProductionCreate, current_user: str = Depends(get_current_user)):
    async with server.state.db.acquire() as conn:
        machine_exists = await queries.check_machine_exists(conn, machine_id=record.machine_id)
        if not machine_exists:
            raise EntityNotFoundError(f"Machine with ID {record.machine_id} does not exist.")
        
        db_user = await queries.get_user_by_username(conn, username=current_user)

        production_id = await queries.insert_production(
            conn, machine_id=record.machine_id, user_id=db_user["id"], amount=record.amount, date=record.date
        )
        return {
            "status": "success",
            "message": "Production record logged successfully",
            "data": {
                "id": production_id, 
                "machine_id": record.machine_id, 
                "user_id": db_user["id"],
                "amount": record.amount, 
                "date": record.date
            }
        }

# 3. Update Production Log
@server.put("/update_production", tags=["Production"])
async def update_production_log(data: ProductionUpdate):
    async with server.state.db.acquire() as conn:
        updated_id = await queries.update_production(conn, new_amount=data.new_amount, record_id=data.record_id)
        if not updated_id:
            raise EntityNotFoundError(f"Record with ID {data.record_id} not found.")

        return {"status": "success", "message": "Record updated successfully"}

# 4. Delete Production Log
@server.delete("/delete_production/{record_id}", tags=["Production"])
async def delete_production_log(record_id: int):
    async with server.state.db.acquire() as conn:
        deleted_id = await queries.delete_production(conn, record_id=record_id)
        if not deleted_id:
            raise EntityNotFoundError(f"Record with ID {record_id} not found.")

        return {"status": "success", "message": "Record deleted successfully"}

# 5. Analytics Endpoint
@server.get("/analytics/{machine_id}", tags=["Analytics"])
async def get_factory_analytics(machine_id: int):
    async with server.state.db.acquire() as conn:
        result = await queries.get_analytics(conn, machine_id=machine_id)
        if not result or result['total_production'] is None:
            raise EntityNotFoundError(f"No production records found for machine ID {machine_id}.")
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
            new_user_id = await queries.register_user(
                conn,
                username=user_data.username,
                password=hashed_pwd,
                role=user_data.role
            )
            return {
                "status": "success",
                "message": "User registered successfully",
                "user_id": new_user_id
            }
        except asyncpg.UniqueViolationError:
            raise DuplicateEntityError("Username already exists. Please choose another username.")

# 7. Login User
@server.post("/login", tags=["Auth"])
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    async with server.state.db.acquire() as conn:
        db_user = await queries.get_user_by_username(conn, username=form_data.username)
        
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not verify_password(form_data.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
        token = create_access_token({"sub": db_user["username"]})
        
        return {"access_token": token, "token_type": "bearer"}

# 8. Read Current User
@server.get("/users/me", tags=["Auth"])
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"message": f"welcome to endpoint {current_user}"}

# 9. Asynchronous Analytics Report Generation (Celery & Redis)

@server.post("/generate_report/{machine_id}", status_code=202, tags=["Analytics"])
async def trigger_analytics_report(machine_id: int):
    
    task = generate_heavy_analytics_report.delay(machine_id)
    
    return {
        "status": "processing",
        "task_id": task.id,
        "message": f"Analytics report generation started in background for machine #{machine_id}."
    }
