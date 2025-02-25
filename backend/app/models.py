from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import logging

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)

    def __repr__(self):
        try:
            return '<User {}>'.format(self.username)
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            raise

    def set_password(self, password):
        try:
            self.password_hash = generate_password_hash(password)
        except Exception as e:
            logging.error(f"Error setting user password: {e}")
            raise

    def check_password(self, password):
        try:
            return check_password_hash(self.password_hash, password)
        except Exception as e:
            logging.error(f"Error checking user password: {e}")
            raise


    @classmethod
    def get_user_by_username(cls, username):
        try:
            return cls.query.filter_by(username = username).first()
        except Exception as e:
            logging.error(f"Error getting user by username: {e}")
            raise

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving user to database: {e}")
            raise

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting user from database: {e}")
            raise
    


class TokenBlockList(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    jti: so.Mapped[str] = so.mapped_column(sa.String(36), nullable=False)
    created_at: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))


    def __repr__(self):
        try:
            return f"<Token {self.jti}>"
        except Exception as e:
            logging.error(f"Error getting token in TokenBlockList: {e}")
            raise
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving token to TokenBlockList: {e}")
            raise