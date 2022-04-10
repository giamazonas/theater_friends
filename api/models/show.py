from datetime import datetime
from api.models.db import db

class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    theater = db.Column(db.String(150))
    city = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    cast = db.Column(db.String(450))
    info = db.Column(db.String(450))
    ticket_url = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __repr__(self):
      return f"Show('{self.id}', '{self.title}'"

    def serialize(self):
      show = {s.name: getattr(self, s.name) for s in self.__table__.columns}
      return show