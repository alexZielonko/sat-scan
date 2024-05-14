from app import app

import pytest


@pytest.fixture
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Sat Scan" in response.data


def test_healthcheck(client):
    response = client.get("/health-check")
    assert response.status_code == 200
    assert b"Success" in response.data
