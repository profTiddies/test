from fastapi import APIRouter , status , HTTPException , Depends
from app.database import cursor , conn

import app.auth as auth , app.schemas as schemas , app.utils as utils

voteRouter = APIRouter()

@voteRouter.post("/vote")
def votePost(data : schemas.requestVote , current_user : int = Depends(auth.get_current_user)):

    if data.flag not in (0 , 1):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail="Invalid Flag")



    # ----------------------------CHECK IF POST EXIST-------------------------
    cursor.execute("""
    select * from posts
    where id = %s""",
    (data.post_id,)
    )

    result = cursor.fetchone()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Post not found")
    # ------------------------------------------------------------------



    # ----------------------------MAIN LOGIC-------------------------
    cursor.execute("""
    select * from votes
    where user_id = %s and post_id = %s""",
    (current_user , data.post_id)
    )

    result = cursor.fetchone()

    if result == None:
        if data.flag == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Vote doen't exist")
        
        else:
            cursor.execute("""
            insert into votes(user_id , post_id) values
            (%s , %s)
            returning *""",
            (current_user , data.post_id)
            )

            insertedResult = cursor.fetchone()
            conn.commit()

            return {"message" : "Vodted"}
    
    else:
        if data.flag == 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="Already Voted")
        
        else:
            cursor.execute("""
            delete from votes
            where user_id = %s and post_id = %s
            returning *""",
            (current_user , data.post_id)
            )

            deletedResult = cursor.fetchone()
            conn.commit()

            return {"message" : "Unvoted"}
    # ------------------------------------------------------------------
        




