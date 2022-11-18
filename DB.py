import datetime

from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey, Float, Index, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///weather_result.sqlite')
Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    latitude = Column(Float(), nullable=False)
    longitude = Column(Float(), nullable=False)

    __table_args__ = (UniqueConstraint('latitude', 'longitude', name='coordinates'),)


class QueryParams(Base):
    __tablename__ = 'parameters of queries'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    city_id = Column(ForeignKey('cities.id'), nullable=False)
    date_of_query = Column(DateTime(), default=datetime.datetime.now())
    result = Column(String(200), nullable=False)
    city = relationship("City")


Base.metadata.create_all(engine)
