
import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import settings

try:
    conn = psycopg2.connect(
        host=settings.DATABASE_HOST, 
        database=settings.DATABASE_DATABSE, 
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        cursor_factory=RealDictCursor
    )

    cursor = conn.cursor()
    print("Connected to Database")

except Exception as error:
    print("Connection Failed")
    print(error)



