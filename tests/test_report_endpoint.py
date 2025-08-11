from fastapi.testclient import TestClient
from rcvco.api.app import app

def test_report_endpoint(monkeypatch):
    from rcvco.adapters.llm import factory
    class Dummy:
        def generate_report(self, prompt: str) -> str:
            return "OK"
    monkeypatch.setattr(factory, "_provider_cache", Dummy())
    client = TestClient(app)
    payload = {"pseudo_id":"p1","sexo":"M","edad":60,"labs":[],"medications":[]}
    r = client.post("/api/report", json=payload)
    assert r.status_code == 200
    assert r.json()["report_text"] == "OK"
