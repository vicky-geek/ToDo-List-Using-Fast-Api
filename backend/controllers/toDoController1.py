from pydantic import BaseModel
from fastapi import Response, status
from mysql.connector import Error, IntegrityError

from database.database import close_db, get_connection
from utils.logger import logger


class item(BaseModel):
    task: str
    priority: int
    description: str | None = None


class ToDo(BaseModel):
    item: item


async def getToDos(response: Response):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, task, priority, description FROM todos")
        rows = cursor.fetchall()
        response.status_code = status.HTTP_200_OK
        return {"data": rows}
    except Error as e:
        print("Error:", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
    finally:
        close_db(cursor, conn)


async def addToDo(ToDo: ToDo, response: Response):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO todos (task, priority, description) VALUES ( %s, %s, %s)",
            ( ToDo.item.task, ToDo.item.priority, ToDo.item.description),
        )
        conn.commit()
        logger.info("cursor.lastrowid : %s", cursor.rowcount)
        response.status_code = status.HTTP_201_CREATED
        return {"id": cursor.lastrowid, "item": ToDo.item}
    except IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "ToDo with this id already exists"}
    except Error as e:
        print("Error:", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
    finally:
        close_db(cursor, conn)


async def getToDoById(id: int, response: Response):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, task, priority, description FROM todos WHERE id = %s",
            (id,),
        )
        row = cursor.fetchone()

        if not row:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "ToDo not found"}

        response.status_code = status.HTTP_200_OK
        return row
    except Error as e:
        print("Error:", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
    finally:
        close_db(cursor, conn)


async def updateToDoById(id: int, ToDo: ToDo, response: Response):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE id = %s", (id,))
        if not cursor.fetchone():
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "ToDo not found"}

        cursor.execute(
            "UPDATE todos SET task = %s, priority = %s, description = %s WHERE id = %s",
            (ToDo.item.task, ToDo.item.priority, ToDo.item.description, id),
        )
        conn.commit()

        response.status_code = status.HTTP_200_OK
        return {"id": id, "item": ToDo.item}
    except Error as e:
        print("Error:", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
    finally:
        close_db(cursor, conn)


async def deleteToDoById(id: int, response: Response):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE id = %s", (id,))
        if not cursor.fetchone():
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "ToDo not found"}

        cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
        conn.commit()

        response.status_code = status.HTTP_200_OK
        return {"message": "ToDo deleted successfully"}
    except Error as e:
        print("Error:", e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
    finally:
        close_db(cursor, conn)
