from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_visits_count_up(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DATA_FILE", tmp_path / "visits.txt")
    assert client.get("/visits").json() == {"visits": 1}
    assert client.get("/visits").json() == {"visits": 2}
