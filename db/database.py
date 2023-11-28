from sqlmodel import create_engine, Session, SQLModel

sqlite_filename = "db/heros.sqlite3"
sqlite_url = f"sqlite:///{sqlite_filename}"
connect_args  = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session