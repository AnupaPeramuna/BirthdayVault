from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TokenBlocklist(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    jti: so.Mapped[str] = so.mapped_column(sa.String(36), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"<Token {self.jti}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()