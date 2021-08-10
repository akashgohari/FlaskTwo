from db import db


class UserModel(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    @classmethod
    def find_by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    def add_update_user(self):
        db.session.add(self)
        db.session.commit()
