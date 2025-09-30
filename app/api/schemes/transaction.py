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
        examples=[
            "daa4561fc476bcd85d74d97e0d322b0e56297a76dd0254f9c459f174937"
            "4e65b",
        ],
        min_length=64,
        max_length=64,
    )]
    signature: Annotated[str, Field(
        description="Signature of transaction",
        examples=[
            "30450220046cb66059b69ef5a521a042ee7352b83aac5ba8129338129047cd547"
            "ce24a30022100d68c4db563f4596a0c120fe117ee5c5edf380c54293c1319c1b4"
            "9a8c71f7ac5b",
        ],
        min_length=140,
        max_length=144,
    )]
    public_key: Annotated[str, Field(
        description="Public key for signature validation",
        examples=[
            "-----BEGIN PUBLIC KEY-----MFYwEAYHKoZIzj-----END PUBLIC KEY-----",
        ],
        min_length=174,
        max_length=174,
    )]
