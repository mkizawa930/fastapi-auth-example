from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False},
)

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestSessionLocal = scoped_session(TestSession)


async def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
