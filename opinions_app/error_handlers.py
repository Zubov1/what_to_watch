from flask import jsonify, render_template

from . import app, db
from .exceptions import InvalidAPIUsage


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обработчик исключения в работе с API."""
    return jsonify(error.to_dict()), error.status_code

@app.errorhandler(500)
def internal_error(error):
    """Обработчик исключения 500."""
    db.session.rollback()

    return render_template('500.html'), 500

@app.errorhandler(404)
def not_found(error):
    """Обработчик исключения 404."""
    return render_template('404.html'), 404
