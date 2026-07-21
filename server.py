from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# --- Database Connection Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mahdiar_user:my_secure_password@127.0.0.1:5433/arman_tak_db")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Table: factory_managers
    cur.execute("""
        CREATE TABLE IF NOT EXISTS factory_managers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            role VARCHAR(50) NOT NULL
        );
    """)
    
    # 2. Table: machines
    cur.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id SERIAL PRIMARY KEY,
            machine_name VARCHAR(100) NOT NULL,
            model_year INTEGER
        );
    """)

    # 3. Table: production
    cur.execute("""
        CREATE TABLE IF NOT EXISTS production (
            id SERIAL PRIMARY KEY,
            machine_id INTEGER REFERENCES machines(id) ON DELETE CASCADE,
            amount INTEGER NOT NULL,
            date VARCHAR(50) NOT NULL
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

# --- FastAPI Initialization ---
server = FastAPI(
    title="Arman Tak System API",
    description="Enterprise API for Managing Factory Machines and Production Logs",
    version="1.0.0"
)

@server.on_event("startup")
def startup_event():
    init_db()

# --- Pydantic Schemas for Request Validation ---
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

# --- Routes / Endpoints ---

@server.get("/", tags=["General"])
def home():
    return {"message": "Welcome to ARMAN TAK Factory API"}

# 1. Create a Machine (Prerequisite for logging production)
@server.post("/machines", status_code=status.HTTP_201_CREATED, tags=["Machines"])
def create_machine(machine: MachineCreate):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO machines (machine_name, model_year) VALUES (%s, %s) RETURNING id;",
            (machine.machine_name, machine.model_year)
        )
        new_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        return {"status": "success", "machine_id": new_id, "message": "Machine created successfully"}
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()

# 2. Insert Production Log (Validated against machines table)
@server.post("/insert_production", status_code=status.HTTP_201_CREATED, tags=["Production"])
def add_production_log(record: ProductionCreate):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Foreign Key Existence Check
        cur.execute("SELECT id FROM machines WHERE id = %s;", (record.machine_id,))
        if not cur.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Machine with ID {record.machine_id} does not exist."
            )

        # Insert Production
        cur.execute(
            "INSERT INTO production (machine_id, amount, date) VALUES (%s, %s, %s) RETURNING id;",
            (record.machine_id, record.amount, record.date)
        )
        production_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        return {
            "status": "success",
            "message": "Production record logged successfully",
            "data": {"id": production_id, "machine_id": record.machine_id, "amount": record.amount, "date": record.date}
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if conn: conn.close()

# 3. Update Production Log
@server.put("/update_production", tags=["Production"])
def update_production_log(data: ProductionUpdate):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE production SET amount = %s WHERE id = %s RETURNING id;", (data.new_amount, data.record_id))
        updated = cur.fetchone()
        
        if not updated:
            raise HTTPException(status_code=404, detail=f"Record with ID {data.record_id} not found.")

        conn.commit()
        cur.close()
        return {"status": "success", "message": "Record updated successfully"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()

# 4. Delete Production Log
@server.delete("/delete_production/{record_id}", tags=["Production"])
def delete_production_log(record_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM production WHERE id = %s RETURNING id;", (record_id,))
        deleted = cur.fetchone()

        if not deleted:
            raise HTTPException(status_code=404, detail=f"Record with ID {record_id} not found.")

        conn.commit()
        cur.close()
        return {"status": "success", "message": "Record deleted successfully"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()

# 5. Analytics Endpoint
@server.get("/analytics/{machine_id}", tags=["Analytics"])
def get_factory_analytics(machine_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT SUM(amount) as total_production, AVG(amount) as average_production FROM production WHERE machine_id = %s;",
            (machine_id,)
        )
        result = cur.fetchone()
        cur.close()

        if not result or result['total_production'] is None:
            raise HTTPException(status_code=404, detail="No production records found for this machine.")

        return {
            "machine_id": machine_id,
            "total_production": result['total_production'],
            "average_production": round(float(result['average_production']), 2)
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()