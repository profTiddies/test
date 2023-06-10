
from pydantic import BaseModel , EmailStr

# ----------------------------USER---------------------------------
class createUser(BaseModel):
    email : EmailStr
    passw : str

class returnUser(BaseModel):
    email : EmailStr
    id : int
# ------------------------------------------------------------------


# ----------------------------POST---------------------------------
class createPost(BaseModel):
    title : str
    content : str


class Post(BaseModel):
    id : int
    title : str
    content : str
    votes : int

class postUser(BaseModel):
    email : EmailStr
    id : int

class returnPost(BaseModel):
    post : Post
    user : postUser
# ------------------------------------------------------------------


# ----------------------------VOTE-------------------------
class requestVote(BaseModel):
    post_id : int
    flag : int
# ------------------------------------------------------------------





