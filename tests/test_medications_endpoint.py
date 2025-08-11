from fastapi.testclient import TestClient
from rcvco.api.app import app

client = TestClient(app)


def test_medications_idempotent():
    r1 = client.post('/api/medications', params={'name':'Aspirina'})
    assert r1.status_code == 200
    items1 = r1.json()['items']
    r2 = client.post('/api/medications', params={'name':'aspirina'})  # case diff
    assert r2.status_code == 200
    items2 = r2.json()['items']
    assert items1 == items2  # no duplicado
    assert len(items2) == 1


def test_medications_delete():
    client.post('/api/medications', params={'name':'Losartan'})
    r = client.delete('/api/medications/losartan')
    assert r.status_code == 200
    assert 'losartan' not in r.json()['items']
