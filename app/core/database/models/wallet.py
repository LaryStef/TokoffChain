from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.mixins import CreatedAtMixin, UpdatedAtMixin

from .model import Model

if TYPE_CHECKING:
    from .transaction import Transaction


class Wallet(Model, CreatedAtMixin, UpdatedAtMixin):
    address: Mapped[str] = mapped_column(primary_key=True)
    balance: Mapped[Decimal] = mapped_column(
        default=Decimal(0),
        nullable=False,
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="wallet",
        lazy="selectin",
    )
