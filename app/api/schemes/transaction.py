from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from app.settings import settings


class Transaction(BaseModel):
    sender: Annotated[str, Field(
        description=(
            "Public key for signature validation and wallet address"
            "at the same time in uuid format"
        ),
        examples=["93af6bfa-80e5-4d41-ab5f-d284b733c760"],
        frozen=True,
        pattern=(
            "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}"
            "-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
        ),
    )]
    recipient: Annotated[str, Field(
        description=(
            "Reciever wallet address in uuid format"
        ),
        examples=["93af6bfa-80e5-4d41-ab5f-d284b733c760"],
        frozen=True,
        pattern=(
            "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}"
            "-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
        ),
    )]
    amount: Annotated[Decimal, Field(
        description="Amount of transaction",
        examples=["23.43"],
        ge=settings.MIN_TRANSACTION_SIZE,
        le=settings.MAX_TRANSACTION_SIZE,
        decimal_places=6,
    )]
    hash: Annotated[str, Field(
        description="Hash of transaction",
        examples=["0x1234567890abcdef"],
        min_length=64,
        max_length=64,
    )]
    signature: Annotated[str, Field(
        description="Signature of transaction",
        examples=["0x1234567890abcdef"],
        min_length=140,
        max_length=144,
    )]
    public_key: Annotated[str, Field(
        description="Public key for signature validation",
        examples=["0x1234567890abcdef"],
        min_length=174,
        max_length=174,
    )]
