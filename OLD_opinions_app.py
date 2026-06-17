import csv
from datetime import datetime
import os
from random import randrange

import click
from flask import Flask, abort, flash, redirect, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


DATA_REQUIRED_MESSAGE = 'Обязательное поле'

OPINION_TITLE_MAX_LENGTH = 128

OPINION_TITLE_MIN_LENGTH = 1

OPINION_SOURCE_MAX_LENGTH = 256

OPINION_SOURCE_MIN_LENGTH = 1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Opinion(db.Model):
    """Представляем таблицу Opinion."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(OPINION_TITLE_MAX_LENGTH), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(OPINION_SOURCE_MAX_LENGTH))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))


class OpinionForm(FlaskForm):
    """Описывает форму для модели Opinion."""

    title = StringField(
        'Введите название фильма',
        validators=[
            DataRequired(message=DATA_REQUIRED_MESSAGE),
            Length(OPINION_TITLE_MIN_LENGTH, OPINION_TITLE_MAX_LENGTH)
        ]
    )
    text = TextAreaField(
        'Расскажите свое мнение',
        validators=[DataRequired(message=DATA_REQUIRED_MESSAGE)]
    )
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[
            Length(OPINION_SOURCE_MIN_LENGTH, OPINION_SOURCE_MAX_LENGTH),
            Optional()
        ]
    )
    submit = SubmitField('Добавить')


@app.cli.command('load_opinions')
def load_opinions_command():
    """Загружает мнения в БД из файла opinions.csv."""

    with open('opinions.csv', encoding='utf-8') as file:

        reader = csv.DictReader(file)
        counter = 0

        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            counter += 1

        db.session.commit()
    
    click.echo(f'Загружено мнений: {counter}')

@app.errorhandler(500)
def internal_error(error):
    """Обработчик исключения 500."""
    db.session.rollback()

    return render_template('500.html'), 500

@app.errorhandler(404)
def not_found(error):
    """Обработчик исключения 404."""
    return render_template('404.html'), 404

@app.route('/')
def index_view():
    """Вью-функция, обрабатывающая запросы к главной странице."""
    querycount = Opinion.query.count()

    if not querycount:
        abort(500)

    opinion = Opinion.query.offset(randrange(querycount)).first()

    return render_template('opinion.html', opinion=opinion)

@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    """Вью-функция для добавления нового мнения."""
    form = OpinionForm()

    if form.validate_on_submit():

        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!', 'unique-field')
        
            return render_template('add_opinion.html', form=form)

        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )

        db.session.add(opinion)
        db.session.commit()

        return redirect(url_for('opinion_view', opinion_id=opinion.id))

    return render_template('add_opinion.html', form=form)

@app.route('/opinions/<int:opinion_id>')
def opinion_view(opinion_id):
    """Вью-функция, извекающая один элемент из БД."""
    opinion = Opinion.query.get_or_404(opinion_id)

    return render_template('opinion.html', opinion=opinion)

if __name__ == '__main__':
    app.run()
