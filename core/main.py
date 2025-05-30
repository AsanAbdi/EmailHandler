from fastapi import FastAPI

from apps.users.apis import router as UserRouter
from config.settings import settings


app = FastAPI()

app.include_router(UserRouter, prefix=settings.API_V1_STR)