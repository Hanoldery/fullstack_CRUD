import os
from datetime import date, datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
import jwt
from sqlalchemy.ext.associationproxy import association_proxy


db = SQLAlchemy()

# TODO: Remplacer les **_type_back par **_type_tmp
# TODO: Mettre unique ou l'enlever, mais se decider
# TODO: Se décider sur les noms des tables


def datetime_handler(dt):
    if isinstance(dt, (datetime, date)):
        return dt.isoformat()
    # raise TypeError("Unknown type")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=True)
    admin = db.Column(db.Boolean, unique=False, nullable=False)
    confirmed = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def encode_auth_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            os.environ.get('SECRET_KEY'),
            algorithm='HS256'
        )

    def decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, os.environ.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User(id=%r, title='%s', email='%s', password='%s', admin=%s, confirmed=%s)>" % (
            self.id, self.title, self.email, self.password, 'true' if self.admin else 'false', 'true' if self.confirmed else 'false')

