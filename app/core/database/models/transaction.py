from decimal import Decimal
from uuid import uuid4

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.mixins.created_at import CreatedAtMixin
from app.core.database.models.model import Model
from app.settings import settings

from .wallet import Wallet


class Transaction(Model, CreatedAtMixin):
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default_factory=uuid4,
    )
    sender: Mapped[str] = mapped_column(
        ForeignKey(Wallet.address),
        nullable=False,
    )
    recipient: Mapped[str] = mapped_column(
        ForeignKey(Wallet.address),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=settings.NUMBER_PRECISION,
            scale=settings.NUMBER_SCALE,
            asdecimal=True,
        ),
        nullable=False,
    )
    fee: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=settings.NUMBER_PRECISION,
            scale=settings.NUMBER_SCALE,
            asdecimal=True,
        ),
        nullable=False,
    )
    block_id: Mapped[str] = mapped_column(String(36), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    signature: Mapped[str] = mapped_column(String(128), nullable=False)
    wallet: Mapped[Wallet] = relationship(
        back_populates="transactions",
        lazy="selectin",
    )

    def __init__(
        self,
        *,
        sender: str,
        recipient: str,
        amount: Decimal,
        fee: Decimal,
        block_id: str,
        status: str,
        signature: str,
    ) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee
        self.block_id = block_id
        self.status = status
        self.signature = signature
