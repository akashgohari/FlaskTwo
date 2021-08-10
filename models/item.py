from db import db


class ItemModel(db.Model):
    __tablename__ = "Items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    @classmethod
    def find_an_item(cls, name):
        return cls.query.filter_by(name=name).first()

    def add_update_item(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_items(cls):
        return cls.query.all()
