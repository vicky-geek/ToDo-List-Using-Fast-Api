import time

from dotenv import load_dotenv

load_dotenv() # this will load the environment variables from the .env file and set them in the environment variables of the system

from fastapi import FastAPI, Request
from routes.authRoutes import router as authRouter
from routes.toDoRoutes import router as toDoRouter
from utils.logger import configure_uvicorn_logging, logger

configure_uvicorn_logging()

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s -> %s (%.0fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response

# @app.get('/')
# # @app.get('/hello')   for controller we need to create just after end point declaration if we create controller after two  end point then boths end points controller will be same 
# def read_root():
#     return {"Hello": "World"}

app.include_router(toDoRouter)
app.include_router(authRouter)