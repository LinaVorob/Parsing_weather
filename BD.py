import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///weather_result.sqlite')
Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    latitude = Column(Float(), nullable=False)
    longitude = Column(Float(), nullable=False)


class QueryParams(Base):
    __tablename__ = 'parameters of queries'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    city_id = Column(ForeignKey('cities.id'), nullable=False)
    date_of_query = Column(DateTime(), default=datetime.datetime.now())
    result = Column(Boolean(), nullable=False)
    city = relationship("City")


# Вопросы:
# 1. Что подразумевается под "световым днем"?
# 2. Какие входные данные нужно записывать?

Base.metadata.create_all(engine)
