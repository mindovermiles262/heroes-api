import pytest

from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool

from db.database import get_session
from main import app


# sqlite_filename = "db/heros_test.sqlite3"
# sqlite_url = f"sqlite:///{sqlite_filename}"
# Creates an in memory sqlite database. Requires poolclass=StaticPool option.
sqlite_url = "sqlite://"
connect_args  = {"check_same_thread": False}

# Create a Pytest Fixture named "fxt_session". This is responsible for creating
# and migration the test database, then yields a DB Session.
@pytest.fixture(name="fxt_session")
def fixture_session():
    test_engine = create_engine(
        sqlite_url,
        echo=True,
        connect_args=connect_args,
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


# The Pytest Fixture "fxt_client" uses a pytest fixture database session to 
# create the necessary dependency overrides, then creates the TestClient which
# is connected to the test database.
@pytest.fixture(name="fxt_client")
def fixture_client(fxt_session: Session):
    def get_session_override():
        return fxt_session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
