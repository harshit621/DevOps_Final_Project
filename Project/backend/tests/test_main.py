def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_asset(client):
    payload = {"name": "ThinkPad T14", "category": "Laptop", "serial_number": "SN-1001"}
    response = client.post("/api/assets", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "ThinkPad T14"

def test_list_assets(client):
    client.post("/api/assets", json={"name": "Dell Monitor", "category": "Display", "serial_number": "SN-2002"})
    response = client.get("/api/assets")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_update_asset_status(client):
    create_res = client.post("/api/assets", json={"name": "Raspberry Pi 5", "category": "SBC", "serial_number": "SN-3003"})
    asset_id = create_res.json()["id"]
    update_res = client.put(f"/api/assets/{asset_id}", json={"status": "Assigned"})
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "Assigned"

def test_delete_asset(client):
    create_res = client.post("/api/assets", json={"name": "Cisco Switch", "category": "Network", "serial_number": "SN-4004"})
    asset_id = create_res.json()["id"]
    del_res = client.delete(f"/api/assets/{asset_id}")
    assert del_res.status_code == 204
    get_res = client.get("/api/assets")
    assert len(get_res.json()) == 0