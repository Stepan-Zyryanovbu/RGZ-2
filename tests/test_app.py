from app import app

def test_weather_ok():
    client = app.test_client()
    r = client.get("/weather/?city=Amsterdam")
    assert r.status_code == 200
    body = r.get_json()
    assert body["data"]["city"] == "Amsterdam"