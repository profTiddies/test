
from fastapi import APIRouter , status , HTTPException , Depends
from app.database import cursor , conn
import app.auth as auth , app.schemas as schemas , app.utils as utils

postRouter = APIRouter(tags=["Posts"])

# ----------------------------GET ALL POSTS-------------------------
@postRouter.get("/posts" , response_model=list[schemas.returnPost])
def getAllPosts(limit : int = 100 , search : str = ''):

    cursor.execute("""
    select p.id, p.title, p.content, p.user_id, u.email , count(v.user_id) as votes
    from posts p 
    left join users u on p.user_id = u.id
    left join votes v on p.id = v.post_id
    where p.title like %s
    group by p.id, p.title, p.content, p.user_id, u.email
    limit %s""",
    (f"%{search}%",limit)
    )

    result = cursor.fetchall()
    
    out = []

    for i in result:
        i = dict(i)

        post = schemas.Post(
            id = i["id"],
            title = i["title"],
            content = i["content"],
            votes = i["votes"]
            )

        user = schemas.postUser(
            id = i["user_id"],
            email = i["email"]
        )

        out.append(schemas.returnPost(
            post = post,
            user = user
        ))
    
    return out
# ------------------------------------------------------------------


# ----------------------------GET SPECIFIC POST-------------------------
@postRouter.get("/posts/{id}" , response_model=schemas.returnPost)
def getSpecificPost(id : int, current_user : int = Depends(auth.get_current_user)):

    cursor.execute("""
    select p.id, p.title, p.content, p.user_id, u.email , count(v.user_id) as votes
    from posts p 
    left join users u on p.user_id = u.id
    left join votes v on p.id = v.post_id
    where p.id = %s
    group by p.id, p.title, p.content, p.user_id, u.email""",
    (id,)
    )

    result = cursor.fetchone()
    
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Post not found")

    result = dict(result)

    post = schemas.Post(
        id = result["id"],
        title = result["title"],
        content = result["content"],
        votes = result["votes"]
        )

    user = schemas.postUser(
        id = result["user_id"],
        email = result["email"]
    )

    return schemas.returnPost(
        post = post,
        user = user
    )
# ------------------------------------------------------------------


# ----------------------------CREATE POST-------------------------
@postRouter.post("/posts" , response_model=schemas.returnPost)
def createPost(data : schemas.createPost, current_user : int = Depends(auth.get_current_user)):

    cursor.execute("""
    insert into posts(title , content , user_id) values
    (%s , %s , %s)
    returning *""",
    (data.title , data.content , current_user)
    )

    result = cursor.fetchone()
    conn.commit()

    return result
# ------------------------------------------------------------------


# ----------------------------DELETE POST-------------------------
@postRouter.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id : int , current_user : int = Depends(auth.get_current_user)):

    cursor.execute("""
    select user_id from posts
    where id = %s""",
    (id,)
    )

    postToDelete = cursor.fetchone()
    if postToDelete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Post not found")
    
    postToDelete = dict(postToDelete)
    if postToDelete["user_id"] != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Allowed")

    cursor.execute("""
    delete from posts
    where user_id = %s and id = %s""",
    (current_user , id)
    )

    conn.commit()
# ------------------------------------------------------------------
