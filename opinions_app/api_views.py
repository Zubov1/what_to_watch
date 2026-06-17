from random import randrange

from flask import jsonify, request

from . import app, db
from .exceptions import InvalidAPIUsage
from .models import Opinion
from .views import random_opinion


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    """Функция для создания нового объекта класса Opinion."""
    data = request.get_json()

    opinion = Opinion()
    opinion.from_dict(data)

    db.session.add(opinion)
    db.session.commit()

    return jsonify({'opinion': opinion.to_dict()}), 201

@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    """Функция для получения всего списка объектов из БД."""
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]

    return jsonify({'opinions': opinions_list}), 200

@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    """Функция для получения отдельного объекта."""
    opinion = Opinion.query.get_or_404(id)

    return jsonify({'opinion': opinion.to_dict()}), 200

@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    """Функция для обновления мнения в БД."""
    data = request.get_json()

    opinion = Opinion.query.get_or_404(id)

    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)

    db.session.commit()

    return jsonify({'opinion': opinion.to_dict()}), 200

@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    """Функция для удаления объектов из БД."""
    opinion = Opinion.query.get_or_404(id)

    db.session.delete(opinion)
    db.session.commit()

    return '', 204

@app.route('/api/get-random-opinion/')
def get_random_opinion():
    """Возвращает случайную запись из БД."""
    opinion = random_opinion()

    if not opinion:
        raise InvalidAPIUsage('В Базе Данных нет мнений.', 404)

    return jsonify({'opinion': opinion.to_dict()}), 200
