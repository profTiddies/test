from fastapi import APIRouter , status , HTTPException , Depends
from app.database import conn , cursor
from datetime import datetime , timedelta
import app.schemas as schemas , app.utils as utils

from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from jose import jwt , JWTError

authRouter = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# ----------------------------CREATE ACCESS TOKEN-------------------------
def create_access_token(data : dict = {}):
    toEncode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode["exp"] = expire

    encoded_jwt = jwt.encode(toEncode , SECRET_KEY , algorithm=ALGORITHM)
    return encoded_jwt
# ------------------------------------------------------------------


# ----------------------------VERIFY ACCESS TOKEN-------------------------
def verify_access_token(token : str):
    try:
        return jwt.decode(token , SECRET_KEY , algorithms=ALGORITHM)
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid Credentials")
# ------------------------------------------------------------------


# ----------------------------GET CURRENT USER-------------------------
def get_current_user(token : str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)

    currentUserId = payload["user_id"]

    return currentUserId
# ------------------------------------------------------------------



# ----------------------------LOG IN-------------------------
@authRouter.post("/login")
def login(formData : OAuth2PasswordRequestForm = Depends()):
    
    cursor.execute("""
    select * from users
    where email = %s""",
    (formData.username,)
    )

    result = cursor.fetchone()

    if result == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credentials")
    
    result = dict(result)

    if not utils.verifyPass(formData.password , result["passw"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credentials")

    jwt_token = create_access_token({"user_id" : result["id"]})

    return {
        "token" : jwt_token,
        "token_type" : "bearer"
        }
# ------------------------------------------------------------------


