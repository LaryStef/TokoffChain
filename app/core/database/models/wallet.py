from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.models.mixins import CreatedAtMixin, UpdatedAtMixin

from .model import Model


class Wallet(Model, CreatedAtMixin, UpdatedAtMixin):
    address: Mapped[str] = mapped_column(primary_key=True)
    balance: Mapped[Decimal] = mapped_column(
        default=Decimal(0),
        nullable=False,
    )
