from django.core.exceptions import ValidationError
from passlib.context import CryptContext

import requests

from . import QUERY_BALANCER_HOST, ACTIVE_REPLICATOR_HOST

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def __verifyPassword(password, hashed_password):
    return PWD_CONTEXT.verify(password, hashed_password)

def __getPasswordHash(password):
    return PWD_CONTEXT.hash(password)

def getUser(username: str):
    q = f"SELECT users.username, users.password FROM users WHERE users.username = '{username}';"

    print("ssssssss")

    resp = requests.post(f"http://{QUERY_BALANCER_HOST}:8080/query", json={"q": q})

    print(resp.json())

    return resp.json()

def registerUser(username: str, name: str, password: str):
    ps = __getPasswordHash(password)
    
    com = f"INSERT INTO users (username, name, password) VALUES ({username}, {name}, {ps});"

    resp = requests.post(f"http://{ACTIVE_REPLICATOR_HOST}:8080/run", json={"com": com})

    return "SUCCESS"
