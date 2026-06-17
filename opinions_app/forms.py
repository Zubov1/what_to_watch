from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .models import (
    OPINION_TITLE_MAX_LENGTH,
    OPINION_TITLE_MIN_LENGTH,
    OPINION_SOURCE_MAX_LENGTH,
    OPINION_SOURCE_MIN_LENGTH
)


DATA_REQUIRED_MESSAGE = 'Обязательное поле'

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
    images = MultipleFileField(
        validators=[
            FileAllowed(
                ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
                message=(
                    'Выберите файлы с расширением '
                    '.jpg, .jpeg, .png, .gif или .bmp'
                )
            ),
        ]
    )
    submit = SubmitField('Добавить')
