# from marshmallow import Schema, fields
#
#
# class ItemSchema(Schema):
#     id = fields.Int(dump_only=True)
#     name = fields.Str(dump_only=True)
#     price = fields.Str(required=True)

from ma import ma
from models.item import ItemModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        dump_only = ("id",)
        load_instance = True
