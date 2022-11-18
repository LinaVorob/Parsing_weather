from flask import render_template, send_file, redirect, url_for, Response
from flask import request
from werkzeug.exceptions import HTTPException

from app import app
from app.forms import CityForm
from load_to_db import load_result_to_db
from parser_weather import parsing_weather
from put_to_excel import write_to_excel

FILENAME = 'Weather.xlsx'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'], )
def index():
    form = CityForm()
    if request.method == 'POST':
        city = request.form['city_name']
        print(city)

        try:
            weather = parsing_weather(city)
            load_result_to_db(city)
            write_to_excel(weather, city)
            return redirect(url_for('send_xlsx'))
        except (TypeError, ValueError):
            load_result_to_db('Error', error='Ошибка')
            return render_template("form.html", form=form)
    return render_template("form.html", form=form)


@app.route('/weather', methods=['GET'])
def send_xlsx():
    try:
        return send_file(FILENAME, as_attachment=True)
    except FileNotFoundError:
        return {'message: file not found'}
