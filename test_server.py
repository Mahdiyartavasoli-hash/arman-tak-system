

async def test_read_home(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to ARMAN TAK Factory API (Clean SQL Architecture)"}



async def test_read_docs(async_client):
    response = await async_client.get("/docs")
    assert response.status_code == 200


async def test_create_production_invalid_data(async_client):
    payload = {
        "machine_id": 1,
        "amount": -50,  
        "date": "2026-07-21"
    }

    response = await async_client.post("/insert_production", json = payload)
    response.status_code == 422


async def test_create_production_success(async_client):
   
    login_data = {
        "username": "mahdiar",
        "password": "secret123"
    }

    login_res = await async_client.post("/login", data=login_data)
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "machine_id": 1,
        "amount": 100,
        "date": "2026-07-25"
    }

    response = await async_client.post("/insert_production", json=payload, headers=headers)
    assert response.status_code == 201   
    res_json = response.json()
    assert res_json["status"] == "success"
    assert "data" in res_json
    assert res_json["data"]["amount"] == 100
    assert res_json["data"]["machine_id"] == 1