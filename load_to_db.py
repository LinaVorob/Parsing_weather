from sqlalchemy.orm import sessionmaker
from selenium.common import NoSuchElementException
from DB import engine, City, QueryParams
from city_coordinate import get_coordinates

Session = sessionmaker(bind=engine)
session = Session()


def is_city_exist(city):
    qur = session.query(City).filter(City.name == city).all()
    if len(qur) == 0:
        return False
    return True


def add_new_city(city):
    try:
        latitude, longitude = get_coordinates(city)

    except NoSuchElementException:

        if not is_city_exist('Error'):
            result = City(
                name='Error',
                latitude=0,
                longitude=0
            )
            session.add(result)
            session.commit()
            raise ValueError


    result = City(
        name=city,
        latitude=latitude,
        longitude=longitude
    )

    session.add(result)
    session.commit()


def city_coordinate(city):
    if not is_city_exist(city):
        add_new_city(city)
    qur = session.query(City.latitude, City.longitude).filter(City.name == city).first()

    return qur


def load_result_to_db(city, error=None):
    result = QueryParams(
        city_id=session.query(City.id).filter(City.name == city).first()[0],
        result='Успешно' if not error else error,
    )
    session.add(result)
    session.commit()
