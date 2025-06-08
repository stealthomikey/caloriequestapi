# app/main.py

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from dotenv import load_dotenv
from app.database import Base, engine
from app.routers import auth, redirect, meals, foods, user_action
import os

# load encrypted variabl;es from .env file
load_dotenv()

# intialise the api with description
app = FastAPI(
    title="MDL Showcase API",
    description="Used for the backend logic for the calorie counting app.",
    version="1.0.0",
)

# cors for safe cross-origin requests
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# middleware for cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# session middleware for user sessions
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
        headers=exc.headers,
    )

# error handling
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled Exception: {exc}") # Print for debugging
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred. Please try again later."},
    )

# Include Routers 
app.include_router(redirect.router) # redirect router for auth redirection
app.include_router(auth.router) # auth router for login and logout
app.include_router(meals.router) # meal router for meal logging
app.include_router(foods.router) # food router for foods
app.include_router(user_action.router) # user action router for 

# api base path check
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Nutrition Tracker API is running"}