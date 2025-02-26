from sqlmodel import SQLModel, create_engine


DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)