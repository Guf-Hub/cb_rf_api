# from typing import Annotated, List, Union


# from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    # Depends,
    Security,
)

# from api_v1.db.session import get_async_session
from api_v1.auth.service import is_valid_token

TokenDep = Security(is_valid_token)
