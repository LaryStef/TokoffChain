from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.api.schemes import SuccessResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create transaction",
    description=(
        "Add transaction to the list of transactions to be saved in next block"
    ),
    responses={
        status.HTTP_201_CREATED: {
            "model": SuccessResponse,
            "description": (
                "Response for successfull transaction creating"
            ),
            "example": {
                "status": status.HTTP_201_CREATED,
                "message": (
                    "Transaction successfully added to the list"
                    "to be saved in next block",
                ),
            },
        },
    },
)
async def create_transaction() -> JSONResponse:
    return JSONResponse(content="")
