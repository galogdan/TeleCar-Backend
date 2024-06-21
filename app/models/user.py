from pydantic import BaseModel, EmailStr
from app.models.vehicle import Vehicle


class UserRegistration(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    vehicle: Vehicle
    gender: bool


class UserLogin(BaseModel):
    email: str
    password: str
