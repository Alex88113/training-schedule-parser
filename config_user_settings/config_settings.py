import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, ValidationError, Field

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()


class UserSettings(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    application_key: str = Field(min_length=1)
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
