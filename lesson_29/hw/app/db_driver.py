import os
import allure
from psycopg2 import OperationalError
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment variables")

Base = declarative_base()


class TestDataset(Base):
    """ Model for tests. Must be deleted after using. """

    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True)
    function_description = Column(String)
    result = Column(Float)


class Dataset(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    function_description = Column(String)
    result = Column(Float)


# DB handler class
class DatabaseHandler:

    def __init__(self, model):
        try:
            self.model = model
            self.engine = create_engine(DATABASE_URL, echo=False)
            self.db_session = sessionmaker(bind=self.engine)
            Base.metadata.create_all(bind=self.engine)
        except OperationalError as e:
            raise f"Database connection failed: {e}"
        except SQLAlchemyError as e:
            raise f"SQLAlchemy error occurred: {e}"
        except Exception as e:
            raise f"Unexpected error: {e}"


    def add_record(self, function_description, result):
        with self.db_session() as session:
            record = self.model(function_description=function_description, result=result)
            session.add(record)
            session.commit()
            session.refresh(record)

        with allure.step(f"Add record to DB. ID: {record.id}, Description: {function_description}, Result: {result}"):
            pass


    @allure.step("Update record ID: {record_id}, new value={new_function_description}")
    def update_record(self, record_id, new_function_description):
        with self.db_session() as session:
            record = session.get(self.model, record_id)
            if record:
                record.function_description = new_function_description
                session.commit()


    @allure.step("Delete record ID: {record_id}")
    def delete_record(self, record_id):
        with self.db_session() as session:
            record = session.get(self.model, record_id)
            if record:
                session.delete(record)
                session.commit()


    @allure.step("Get all record from DB")
    def list_all_records(self):
        with self.db_session() as session:
            return session.query(self.model).all()


    @allure.step("Retrieve record from DB with ID: {record_id}")
    def get_record(self, record_id):
        with self.db_session() as session:
            return session.get(self.model, record_id)
