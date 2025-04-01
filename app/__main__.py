import uvicorn
from fastapi import FastAPI

from app.api import api
from app.settings import settings

app = FastAPI()
app.include_router(api)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
