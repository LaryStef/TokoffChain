from typing import Annotated

from fastapi import status
from pydantic import BaseModel, Field


class _BaseResponse(BaseModel):
    status: Annotated[int, Field(
        description="HTTP status code for response",
        examples=[status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST],
        ge=100,
        le=599,
    )]
    message: Annotated[str, Field(
        description="Additional information about response",
        examples=["Operation completed successfully"],
    )]


class ErrorResponse(_BaseResponse):
    type: Annotated[str, Field(
        description="Type of error",
        examples=["password"],
    )]


class SuccessResponse(_BaseResponse):
    pass
