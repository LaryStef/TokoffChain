from cryptography.hazmat.primitives.asymmetric.types import (
    PrivateKeyTypes,
    PublicKeyTypes,
)


class InvalidKeyTypeError(Exception):
    def __init__(self, key: PublicKeyTypes | PrivateKeyTypes) -> None:
        super().__init__(
            f"Invalid key type: {type(key)}."
            "EllipticCurvePublicKey expected",
        )


class InvalidKeyError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Invalid public key.",
        )


class InvalidSignatureError(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid signature. The transaction is not valid.")


class InvalidHashError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Invalid hash."
            "The transaction hash does not match the expected hash.",
        )
