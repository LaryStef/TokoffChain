import hashlib
import json

from app.api.schemes.transaction import Transaction
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ec import (
    ECDSA,
    EllipticCurvePublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
)

from .exceptions import (
    InvalidHashError,
    InvalidKeyTypeError,
    InvalidSignatureError,
)


def verify_transaction(transaction: Transaction) -> None:
    public_key = load_pem_public_key(transaction.public_key.encode("utf-8"))

    if not isinstance(public_key, EllipticCurvePublicKey):
        raise InvalidKeyTypeError(public_key)

    serialized_transaction = json.dumps({
        "sender": transaction.sender,
        "recipient": transaction.recipient,
        "amount": str(transaction.amount),
        "public_key": transaction.public_key,
    }, sort_keys=True).encode("utf-8")

    expected_hash = hashlib.sha256(serialized_transaction).hexdigest()
    if expected_hash != transaction.hash:
        raise InvalidHashError

    try:
        public_key.verify(
            bytes.fromhex(transaction.signature),
            serialized_transaction,
            ECDSA(hashes.SHA256()),
        )
    except InvalidSignature:
        raise InvalidSignatureError from None
