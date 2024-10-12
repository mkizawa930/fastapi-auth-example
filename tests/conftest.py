from typing import AsyncGenerator
from api import models
import pytest
from sqlalchemy.orm import Session
from tests.database import TestSessionLocal, test_engine
from tests.testutils.db.seed import create_users


async def get_test_db() -> AsyncGenerator[Session, None]:
    db = TestSessionLocal()
    models.Base.metadata.create_all(test_engine)
    create_users(db)
    try:
        yield db
    finally:
        db.close()
