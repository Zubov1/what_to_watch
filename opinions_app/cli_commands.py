import csv

import click

from . import app, db
from .models import Opinion


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
