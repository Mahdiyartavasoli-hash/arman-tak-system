from fastapi.testclient import TestClient
from server import server  


client = TestClient(server)

def test_read_main():
    
    response = client.get("/docs")
    
    assert response.status_code == 200

def test_create_production_log():
    payload = {
        "machine_name": "Arman_Tak_1",
        "production_amount": 550.0
    }
    
    response = client.post("/insert_production", json=payload)
    
    assert response.status_code == 200
    
    assert response.json()["status"] == "success"  
      