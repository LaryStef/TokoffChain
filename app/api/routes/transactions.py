from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.api.schemes import SuccessResponse
from app.api.schemes.response import ErrorResponse
from app.api.schemes.transaction import Transaction
from app.core.encryption.exceptions import InvalidTransactionError
from app.core.encryption.signature import verify_transaction

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
                    "to be saved in the next block",
                ),
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Response for invalid transaction data",
            "example": {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": (
                    "Invalid signature or hash."
                    "Make sure you use right pair of keys, algorithm, encoding"
                    "and elliptic curve cryptography for transaction sign"
                ),
                "type": "Invalid transaction",
            },
        },
    },
)
async def create_transaction(transaction: Transaction) -> JSONResponse:
    try:
        verify_transaction(transaction)
    except InvalidTransactionError:
        return JSONResponse(
            content=ErrorResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message=(
                    "Invalid signature or hash."
                    "Make sure you use right pair of keys, algorithm, encoding"
                    "and elliptic curve cryptography for transaction sign"
                ),
                type="Invalid signature",
            ).model_dump_json(),
        )
    return JSONResponse(
        content=SuccessResponse(
            status=status.HTTP_201_CREATED,
            message=(
                "Transaction successfully added to the list"
                "to be saved in the next block"
            ),
        ).model_dump_json(),
    )
