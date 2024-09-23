import argparse
import time
import os
from typing import Optional

from fastapi.responses import HTMLResponse, JSONResponse
# import pretty_errors

from fastapi import FastAPI, HTTPException, Request

from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles

from database.connection import init_db

from core.settings import (
    Settings,
    setup_endpoints,
    setup_middleware,
)

from core import  setup 

from starlette.middleware.cors import CORSMiddleware
from middleware.apps.admin.endpoints import API_ADMIN_MODULE
from middleware.apps.product.endpoints import API_PRODUCT_MODULE
from middleware.apps.feedback.endpoints import API_FEEDBACK_MODULE
from middleware.apps.order.endpoints import API_ORDER_MODULE

BUILD_PATH: Optional[str] = f"{os.getcwd()}/frontend/build/static"
INDEX_DIRECTORY: Optional[str] = f"{os.getcwd()}/frontend/build/index.html"

settings = Settings()

allow_origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://10.78.1.48:3000",
    "http://127.0.0.1:8000/"
]

allow_credentials = True
allow_methods = ["*"]
allow_headers = ["*"]

@asynccontextmanager
async def lifespan_context(app: FastAPI):
    await setup() 
    print(f"{settings.application_name} is running")
    await init_db()
    from core import cfg
    print(f"{settings.application_name} is conneting to database {cfg['DATABASE_URL']}")
    await initial_server()
    print(f"{settings.application_name} is starting")
    yield

app = FastAPI(
    title=settings.application_name,
    debug=settings.debug,
    lifespan=lifespan_context
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # Specify allowed origins here
    allow_credentials=allow_credentials,
    allow_methods=allow_methods,  # Allow all methods (GET, POST, etc.)
    allow_headers=allow_headers,  # Allow all headers
)
app.mount("/static", StaticFiles(directory=BUILD_PATH), name="static")

endpoints = []
async def initial_server():

    global endpoints
        
    endpoints.append(("/api_version_1", API_ADMIN_MODULE))
    endpoints.append(("/api_version_1", API_PRODUCT_MODULE ))
    endpoints.append(("/api_version_1", API_FEEDBACK_MODULE))
    endpoints.append(("/api_version_1", API_ORDER_MODULE))
    await setup_endpoints(
        app=app,
        endpoints=endpoints
    )
@app.get(
    "/",
    summary="Home page",
)
async def index():
    return HTMLResponse(
        open(INDEX_DIRECTORY).read()
    )
    
@app.get(
    "/static/{file_path:path}",
    summary="Get static files",
)
async def static(file_path: str):
    return StaticFiles(directory=BUILD_PATH)(file_path)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
  
# @app.get("/{full_path:path}")
# async def catch_all(full_path: str):
#     # Возвращаем index.html для любых запросов, которые не соответствуют API
#     with open(INDEX_DIRECTORY, 'r') as file:
#         return HTMLResponse(content=file.read(), status_code=200)
    

def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser for CLI
    """
    parser = argparse.ArgumentParser(description="Запуск сервера")
    parser.add_argument("--host", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=8000, type=int)
    
    return parser
if __name__ == "__main__":
    """
    If u start server from console
    """
    import uvicorn
    parser = create_parser()
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)