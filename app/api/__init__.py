from fastapi import APIRouter

from .routes import transactions

api: APIRouter = APIRouter(prefix="/api")
api.include_router(transactions.router)

__all__ = ["api"]
