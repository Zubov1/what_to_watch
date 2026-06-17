from datetime import datetime

from . import db


OPINION_TITLE_MAX_LENGTH = 128

OPINION_TITLE_MIN_LENGTH = 1

OPINION_SOURCE_MAX_LENGTH = 256

OPINION_SOURCE_MIN_LENGTH = 1


class Opinion(db.Model):
    """Представляем таблицу Opinion."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(OPINION_TITLE_MAX_LENGTH), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(OPINION_SOURCE_MAX_LENGTH))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))

    def to_dict(self):
        """Функция для сериализации объектов класса Opinion."""
        return dict(
            added_by = self.added_by,
            id = self.id,
            title = self.title,
            text = self.text,
            source = self.source,
            timestamp = self.timestamp
        )
    
    def from_dict(self, data):
        """Функция для десериализации json в объект класса Opinion."""

        for field in ['title', 'text', 'source', 'added_by']:
            if field in data:
                setattr(self, field, data[field])
