import uvicorn
from fastapi import FastAPI

from app.settings import settings

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
