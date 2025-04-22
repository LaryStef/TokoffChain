import hashlib
import json
from decimal import Decimal

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ec import (
    ECDSA,
    SECP256K1,
    EllipticCurvePrivateKey,
)
from cryptography.hazmat.primitives.asymmetric.ec import (
    generate_private_key as generate_ec_private_key,
)
from cryptography.hazmat.primitives.asymmetric.rsa import (
    generate_private_key as generate_rsa_private_key,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)

from app.api.schemes.transaction import Transaction
from app.core.encryption.exceptions import (
    InvalidHashError,
    InvalidKeyError,
    InvalidKeyTypeError,
    InvalidSignatureError,
)
from app.core.encryption.signature import verify_transaction


@pytest.fixture()
def sender() -> str:
    return "1d8b39b0-9b67-44ca-888b-d064b75e216a"


@pytest.fixture()
def recipient() -> str:
    return "2f165c1e-981a-4f39-bcc7-92f36d894851"


@pytest.fixture()
def amount() -> str:
    return "1.0"


@pytest.fixture()
def ec_private_key() -> EllipticCurvePrivateKey:
    return generate_ec_private_key(curve=SECP256K1())


@pytest.fixture()
def transaction(
    sender: str,
    recipient: str,
    amount: str,
    ec_private_key: EllipticCurvePrivateKey,
) -> Transaction:
    public_key = ec_private_key.public_key()

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
    signature = ec_private_key.sign(
        serialized_transaction,
        ECDSA(hashes.SHA256()),
    )

    return Transaction(
        sender=sender,
        recipient=recipient,
        amount=Decimal(amount),
        signature=signature.hex(),
        hash=_hash,
        public_key=public_key_pem,
    )


@pytest.fixture()
def transaction_with_invalid_key_type(transaction: Transaction) -> Transaction:
    private_key = generate_rsa_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    transaction.public_key = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")
    return transaction


@pytest.fixture()
def transaction_with_invalid_hash(
    transaction: Transaction,
) -> Transaction:
    transaction.hash = "0"*64
    return transaction


@pytest.fixture()
def transaction_with_invalid_signature(
    transaction: Transaction,
) -> Transaction:
    fake_signature = "0"*71
    transaction.signature = fake_signature.encode("utf-8").hex()
    return transaction


@pytest.fixture()
def transaction_with_invalid_key(
    transaction: Transaction,
) -> Transaction:
    transaction.public_key = "0"*174
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
    with pytest.raises(InvalidKeyError):
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
