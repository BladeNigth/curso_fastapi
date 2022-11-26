from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from main import app
from app.db.models import Base
from app.hashing import Hash
from app.db.database import get_db
import time

db_path = os.path.join(os.path.dirname(__file__), 'test.db')
db_uri = "sqlite:///{}".format(db_path)
SQLALCHEMY_DATABASE_URL = db_uri
engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine_test)

cliente = TestClient(app)

user = {
        "username": "prueba",
        "password": "prueba12"
    }


def insertar_usuario_prueba():
    password_hash = Hash.hash_password('prueba12')
    engine_test.execute(
        f"""
        INSERT INTO usuario(username,password,nombre,apellido,direccion,telefono,correo)
        values('prueba','{password_hash}','prueba_nombre','prueba_apellido','prueba_direccion',1212,'prueba@gmail.com')
        """
    )


insertar_usuario_prueba()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_crear_usuario():
    time.sleep(2)
    usuario = {
        "username": "hector",
        "password": "root",
        "nombre": "hector",
        "apellido": "emilio",
        "direccion": "calle 5",
        "telefono": 3107401216,
        "correo": "hector@gmail.com",
        "creacion": "2022-11-26T11:54:00.570779"
    }

    response = cliente.post('/user/', json=usuario)
    assert response.status_code == 401

    response_token = cliente.post('/login/', data=user)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"
    headers = {
        "Authorization": f"Bearer {response_token.json()['access_token']}"
    }
    response = cliente.post('/user/', json=usuario, headers=headers)
    assert response.status_code == 201
    assert response.json()["Respuesta"] == "Usuario creado satisfactoriamente!!"


def test_obtener_usuarios():
    response_token = cliente.post('/login/', data=user)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"
    headers = {
        "Authorization": f"Bearer {response_token.json()['access_token']}"
    }
    response = cliente.get('/user/', headers=headers)
    assert len(response.json()) == 2


def test_obtener_usuario():
    response_token = cliente.post('/login/', data=user)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"
    headers = {
        "Authorization": f"Bearer {response_token.json()['access_token']}"
    }
    response = cliente.post('/user/1', headers=headers)
    assert response.json()["username"] == "prueba"


def test_delete_usuario():
    response_token = cliente.post('/login/', data=user)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"
    headers = {
        "Authorization": f"Bearer {response_token.json()['access_token']}"
    }
    response = cliente.delete('/user/2', headers=headers)
    assert response.json()


def test_actualizar_usuario():
    usuario = {
        "username": "prueba_actualizado",
    }
    response = cliente.patch('/user/1',json=usuario)
    assert response.json()


def test_no_encuentra_usuario():
    usuario = {
        "username": "prueba_actualizado",
    }
    response = cliente.patch('/user/12', json=usuario)
    print()
    assert response.json()["detail"] == "No existe el Usuario con el id 12, por lo tanto no se puede actualizar"

def test_delete_database():
    test_db_path = os.path.join(os.path.dirname(__file__), 'test.db')
    os.remove(test_db_path)
