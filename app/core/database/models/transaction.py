from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.models.mixins.created_at import CreatedAtMixin
from app.core.database.models.model import Model
from app.settings import settings


class Transaction(Model, CreatedAtMixin):
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    sender: Mapped[str] = mapped_column(String(36), nullable=False)
    recipient: Mapped[str] = mapped_column(String(36), nullable=False)
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
