from pydantic import BaseModel
from fastapi import Response, status
from mysql.connector import Error, IntegrityError

from database.database import close_db, get_connection
from utils.auth import encryptPass, decryptPass, generateAccessToken, generateRefreshToken

class RegisterUser(BaseModel):
    username: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str


async def register(user : RegisterUser, response: Response):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        hashedPassword = encryptPass(user.password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES ( %s, %s, %s)",
            ( user.username, user.email, hashedPassword),
        )
        conn.commit()
        print("cursor.lastrowid :", cursor.rowcount)
        response.status_code = status.HTTP_201_CREATED
        return {"id": cursor.lastrowid, "user": user}
    except IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "User with this email already exists"}
    except Error as e:
        print("Error:", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
    finally:
        close_db(cursor, conn)

async def login(LoginUser : LoginUser, response: Response):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (LoginUser.email,))
        user = cursor.fetchone()
        print("user :", user,type(user))
        if user:
            if decryptPass(LoginUser.password, user['password']):
                response.status_code = status.HTTP_200_OK
                accessToken = generateAccessToken(user) # generate token for the user
                refreshToken = generateRefreshToken(user) # generate refresh token for the user

                response.set_cookie(
                    key="refresh_token",
                    value=refreshToken,
                    httponly=True,
                    secure=False,      # True in production HTTPS
                    samesite="lax",
                    max_age=7 * 24 * 60 * 60
                )
                return {"message": "Login successful", "accessToken": accessToken, "refreshToken": refreshToken}
            else:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return {"error": "Invalid password"}
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"error": "User not found"}
    except Error as e:
        print("Error:", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
    finally:
        close_db(cursor, conn)