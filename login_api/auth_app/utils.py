# auth_app/utils.py

import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()  

SECRET_KEY = os.getenv('API_KEY')


def generate_jwt(email):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
