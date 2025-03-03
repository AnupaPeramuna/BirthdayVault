import datetime
import logging
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.extensions import db

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