from decimal import Decimal
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Transaction


async def create_transaction(
    session: AsyncSession,
    *,
    sender: str,
    recipient: str,
    amount: Decimal,
    fee: Decimal,
    block_id: str,
    status: Literal["Success", "Fail"],
    signature: str,
) -> None:
    session.add(
        Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
            fee=fee,
            block_id=block_id,
            status=status,
            signature=signature,
        ),
    )
    await session.commit()
