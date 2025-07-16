from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'joao',
            'email': 'joao@joaoa.com',
            'password': 'joao123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'joao',
        'email': 'joao@joaoa.com',
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'joao',
                'email': 'joao@joaoa.com',
            }
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'joao',
        'email': 'joao@joaoa.com',
    }


def test_read_user_should_return_user_not_found(client):
    response = client.get('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not Found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Maria',
            'email': 'maria@joaoa.com',
            'password': 'maria12',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Maria',
        'email': 'maria@joaoa.com',
    }


def test_update_user_should_return_user_not_found(client):
    response = client.put(
        '/users/666',
        json={
            'username': 'Maria',
            'email': 'maria@joaoa.com',
            'password': 'maria12',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not Found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}


def test_delete_user_should_return_user_not_found(client):
    response = client.delete('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not Found'}
