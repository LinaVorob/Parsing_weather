from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired


class CityForm(FlaskForm):
    city_name = TextField('city name', validators=[DataRequired()])
