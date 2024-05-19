
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .config import settings
from .database import engine
from .routers import auth, blog, user
from .schemas import Blog

app = FastAPI()
print('*****************',settings.database_hostname)
print("***************************** APp created")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True, 
    allow_methods = ['*'],
    allow_headers = ['*']
)
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/', tags=['root'])
def hello():
    return {'message': 'Hello from Zahid'}
 