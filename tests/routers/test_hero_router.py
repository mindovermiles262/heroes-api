from fastapi.testclient import TestClient
from sqlmodel import Session

from models.hero_model import Hero

valid_body = { "name": "Test Hero Valid", "secret_name": "THV" }
incomplete_body = { "name": "Test Hero Incomplete" }
invalid_body = { "name": "Test Hero Invalid", "secret_name": {"status": "invalid"} }

def _valid_hero():
    return Hero(name="Test Hero Read Valid 1", secret_name="THRV1")

def _valid_hero_2():
    return Hero(name="Test Hero Read Valid 2", secret_name="THRV2", age=2)

# Test Hero Create takes in a Pytest Client Fixture, which is connected to
# the test database (see conftest.py). Then creates a new hero and asserts
# it's been created as it should.
def test_hero_create(fxt_client: TestClient): 
    resp = fxt_client.post('/heroes', json=valid_body)
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data['name'] == valid_body['name']
    assert resp_data['secret_name'] == valid_body['secret_name']
    assert resp_data['age'] is None
    assert resp_data['id'] is not None


def test_hero_create_incomplete(fxt_client: TestClient):
    resp = fxt_client.post('/heroes', json=incomplete_body)
    assert resp.status_code == 422


def test_hero_create_invalid(fxt_client: TestClient):
    resp = fxt_client.post('/heroes', json=invalid_body)
    assert resp.status_code == 422

def test_read_heroes(fxt_session: Session, fxt_client: TestClient):
    hero_1 = _valid_hero()
    hero_2 = _valid_hero_2()

    fxt_session.add(hero_1)
    fxt_session.add(hero_2)
    fxt_session.commit()

    resp = fxt_client.get("/heroes")
    data = resp.json()

    assert resp.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] == hero_1.age
    assert data[0]["id"] == hero_1.id
    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert data[1]["id"] == hero_2.id



def test_read_hero(fxt_session: Session, fxt_client: TestClient):
    hero = _valid_hero()
    fxt_session.add(hero)
    fxt_session.commit()

    response = fxt_client.get(f"/heroes/{hero.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero.name
    assert data["secret_name"] == hero.secret_name
    assert data["age"] == hero.age
    assert data["id"] == hero.id


def test_update_hero(fxt_session: Session, fxt_client: TestClient):
    hero = _valid_hero()
    fxt_session.add(hero)
    fxt_session.commit()

    response = fxt_client.patch(f"/heroes/{hero.id}", json={"name": "Update Name"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Update Name"
    assert data["secret_name"] == hero.secret_name
    assert data["age"] is None
    assert data["id"] == hero.id