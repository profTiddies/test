

# ----------------------------HASHING PASSWORD-------------------------
from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"])

def hashPass(pas):
    return context.hash(pas)

def verifyPass(pas , hashedPas):
    return context.verify(pas , hashedPas)
# ------------------------------------------------------------------



