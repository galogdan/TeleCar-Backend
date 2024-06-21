from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserRegistration
from app.core.security import pwd_context
from app.db.db import users_collection
from app.api.auth import verify_token
from app.utils.translation import translate_text, is_hebrew
from app.utils.dmv import is_car_id_valid, is_motorcycle_id_valid
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
import jwt
from app.models.Token import TokenData
import logging
from jose import JWTError, jwt

logger = logging.getLogger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", status_code=status.HTTP_200_OK)
def register_user(user_data: UserRegistration):
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    if users_collection.find_one({"vehicle.carId": user_data.vehicle.carId}):
        raise HTTPException(status_code=400, detail="Car already registered")

    api_record = is_car_id_valid(user_data.vehicle.carId)
    if not api_record:
        api_record_motor = is_motorcycle_id_valid(user_data.vehicle.carId)
        if api_record_motor:
            user_data.vehicle.color = "Motorcycle Not Detailed"
            user_data.vehicle.year = api_record_motor.get('shnat_yitzur')
            user_data.vehicle.brend = translate_text(api_record_motor.get('tozeret_nm'))
            user_data.vehicle.model = translate_text(api_record_motor.get('degem_nm'))
        else:
            raise HTTPException(status_code=400, detail="Invalid car ID")

    else:
        # Translate and update vehicle details from API
        print(api_record.get('tzeva_rechev'))

        print(is_hebrew(api_record.get('tzeva_rechev')))

        user_data.vehicle.color = translate_text(api_record.get('tzeva_rechev'))
        user_data.vehicle.year = api_record.get('shnat_yitzur')
        user_data.vehicle.brend = translate_text(api_record.get('tozeret_nm'))
        user_data.vehicle.model = translate_text(api_record.get('kinuy_mishari'))

    hashed_password = pwd_context.hash(user_data.password)

    user_doc = {
        "email": user_data.email,
        "first_name": user_data.first_name.capitalize(),
        "last_name": user_data.last_name.capitalize(),
        "password": hashed_password,
        "vehicle": user_data.vehicle.dict(),
        "gender": user_data.gender
    }

    try:
        users_collection.insert_one(user_doc)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/profile", response_model=UserRegistration)
def read_user_profile(current_user: str = Depends(verify_token)):
    user_data = users_collection.find_one({"email": current_user})
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRegistration(**user_data)


# Get user by ID
def get_user_by_email(email: str):
    user = users_collection.find_one({"email": email})
    if user is None:
        return None
    return user


def get_current_user(email: str = Depends(verify_token)):
    user = get_user_by_email(email)
    if user is None:
        logging.error(f"User not found: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user