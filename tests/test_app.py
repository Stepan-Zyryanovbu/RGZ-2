import os, sys

# добавляем корень проекта в sys.path, чтобы работало и локально, и в Actions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


def test_weather_ok():
    client = app.test_client()
    r = client.get("/weather/?city=Amsterdam")
    assert r.status_code == 200
