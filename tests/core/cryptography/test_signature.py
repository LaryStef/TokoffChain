import hashlib
import json
from decimal import Decimal

import pytest

from app.api.schemes.transaction import Transaction
from app.core.cryptography.exceptions import (
    InvalidHashError,
    InvalidKeyTypeError,
    InvalidSignatureError,
)
from app.core.cryptography.signature import verify_transaction
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ec import (
    ECDSA,
    SECP256K1,
    EllipticCurvePrivateKey,
)
from cryptography.hazmat.primitives.asymmetric.ec import (
    generate_private_key as generate_ec_private_key,
)
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, PSS
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
)
from cryptography.hazmat.primitives.asymmetric.rsa import (
    generate_private_key as generate_rsa_private_key,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)


def _rsa_sign(
    private_key: RSAPrivateKey,
    serialized_transaction: bytes,
) -> bytes:
    return private_key.sign(
        serialized_transaction,
        padding=PSS(mgf=MGF1(hashes.SHA256()), salt_length=PSS.MAX_LENGTH),
        algorithm=hashes.SHA256(),
    )

def _ec_sign(
    private_key: EllipticCurvePrivateKey,
    serialized_transaction: bytes,
) -> bytes:
    return private_key.sign(
        serialized_transaction,
        ECDSA(hashes.SHA256()),
    )


def _sign_transaction(
    sender: str,
    recipient: str,
    amount: str,
    private_key: RSAPrivateKey | EllipticCurvePrivateKey,
) -> Transaction:
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    transaction_json: dict[str, str] = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "public_key": public_key_pem,
    }

    serialized_transaction = json.dumps(
        transaction_json,
        sort_keys=True,
    ).encode("utf-8")
    _hash = hashlib.sha256(serialized_transaction).hexdigest()
    if isinstance(private_key, EllipticCurvePrivateKey):
        signature = _ec_sign(private_key, serialized_transaction)
    else:
        signature = _rsa_sign(private_key, serialized_transaction)

    return Transaction(
        sender=sender,
        recipient=recipient,
        amount=Decimal(amount),
        signature=signature.hex(),
        hash=_hash,
        public_key=public_key_pem,
    )


@pytest.fixture()
def sender() -> str:
    return "93af6bfa-80e5-4d41-ab5f-d284b733c760"


@pytest.fixture()
def recipient() -> str:
    return "38kf6bfa-80e5-4d41-ab5f-d284b733c760"


@pytest.fixture()
def amount() -> str:
    return "1.0"


@pytest.fixture()
def transaction(
    sender: str,
    recipient: str,
    amount: str,
) -> Transaction:
    private_key = generate_ec_private_key(curve=SECP256K1())
    return _sign_transaction(
        sender=sender,
        recipient=recipient,
        amount=amount,
        private_key=private_key,
    )


@pytest.fixture()
def transaction_with_invalid_key_type(
    sender: str,
    recipient: str,
    amount: str,
) -> Transaction:
    private_key = generate_rsa_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return _sign_transaction(
        sender=sender,
        recipient=recipient,
        amount=amount,
        private_key=private_key,
    )


@pytest.fixture()
def transaction_with_invalid_hash(
    transaction: Transaction,
) -> Transaction:
    transaction.hash = "invalid_hash"
    return transaction


@pytest.fixture()
def transaction_with_invalid_signature(
    transaction: Transaction,
) -> Transaction:
    transaction.signature = "invalid_signature"
    return transaction


@pytest.fixture()
def transaction_with_invalid_public_key(
    transaction: Transaction,
) -> Transaction:
    transaction.public_key = "invalid_public_key"
    return transaction


def test_verify_transaction(
    transaction: Transaction,
) -> None:
    verify_transaction(transaction)


def test_verify_transaction_with_invalid_key_type(
    transaction_with_invalid_key_type: Transaction,
) -> None:
    with pytest.raises(InvalidKeyTypeError):
        verify_transaction(transaction_with_invalid_key_type)


def test_verify_transaction_with_invalid_key(
    transaction_with_invalid_key: Transaction,
) -> None:
    with pytest.raises(InvalidSignatureError):
        verify_transaction(transaction_with_invalid_key)


def test_verify_transaction_with_invalid_signature(
    transaction_with_invalid_signature: Transaction,
) -> None:
    with pytest.raises(InvalidSignatureError):
        verify_transaction(transaction_with_invalid_signature)


def test_verify_transaction_with_invalid_hash(
    transaction_with_invalid_hash: Transaction,
) -> None:
    with pytest.raises(InvalidHashError):
        verify_transaction(transaction_with_invalid_hash)
