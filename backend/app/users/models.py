import logging
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(256), index=True,
                                                unique=True, nullable=False)
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
    def get_user_by_email(cls, email):
        try:
            return cls.query.filter_by(email = email).first()
        except Exception as e:
            logging.error(f"Error getting user by email: {e}")
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
    