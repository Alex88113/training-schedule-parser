import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, ValidationError

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()


class UserSettings(BaseModel):
    username: str
    password: str
    application_key: str
    id_city: None = None

user_data = {
    'username': os.getenv('TOP_USERNAME'),
    'password': os.getenv('PASSWORD'),
    'application_key': os.getenv('APPLICATION_KEY'),
    'id_city': None
}

try:
    settings = UserSettings(**user_data)

except ValidationError as error:
    print(error)
