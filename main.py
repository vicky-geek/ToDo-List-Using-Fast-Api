from dotenv import load_dotenv

load_dotenv() # this will load the environment variables from the .env file and set them in the environment variables of the system

from fastapi import FastAPI
from routes.authRoutes import router as authRouter
from routes.toDoRoutes import router as toDoRouter

app = FastAPI()

# @app.get('/')
# # @app.get('/hello')   for controller we need to create just after end point declaration if we create controller after two  end point then boths end points controller will be same 
# def read_root():
#     return {"Hello": "World"}

app.include_router(toDoRouter)
app.include_router(authRouter)