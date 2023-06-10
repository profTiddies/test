
from fastapi import status , HTTPException , APIRouter , Depends
from app.database import conn , cursor
import app.auth as auth , app.schemas as schemas , app.utils as utils

userRouter = APIRouter(
    prefix = "/users",
    tags = ["Users"]
    )

# ----------------------------GET ALL USER-------------------------
@userRouter.get("/" , status_code=status.HTTP_200_OK , response_model=list[schemas.returnUser])
def getAllUser(current_user : str = Depends(auth.get_current_user)):

    cursor.execute("""select * from users""")
    
    result = cursor.fetchall()

    return result
# ------------------------------------------------------------------


# ----------------------------GET SPECIFIC USER-------------------------
@userRouter.get("/{id}" , status_code = status.HTTP_200_OK , response_model=schemas.returnUser)
def getSpecificUser(id : int , current_user : str = Depends(auth.get_current_user)):

    cursor.execute("""
    select * from users
    where id = %s""",
    (id,)
    )

    result = cursor.fetchone()

    if result == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail="Not Found")

    return result
# ------------------------------------------------------------------


# ----------------------------CREATE USER-------------------------
@userRouter.post("/")
def createUser(data : schemas.createUser):

    hashedPass = utils.hashPass(data.passw)
    
    cursor.execute("""
    insert into users(email , passw) 
    values(%s , %s)
    returning *""", 
    (data.email , hashedPass)
    )

    conn.commit()

    result = cursor.fetchone()
    return result
# ------------------------------------------------------------------



