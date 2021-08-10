from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource

from models.item import ItemModel
from schemas.item import ItemSchema

_item_schema = ItemSchema()
_item_list_schema = ItemSchema(many=True)


class Item(Resource):

    @classmethod
    @jwt_required()
    def get(cls, name):
        item = ItemModel.find_an_item(name)
        if item:
            return {"item": _item_schema.dump(item)}, 200
        return {"message": "Item not found"}

    @jwt_required(fresh=True)
    def post(self, name):
        json_data = request.get_json()
        json_data["name"] = name
        item = _item_schema.load(json_data)
        item_exist = ItemModel.find_an_item(name)
        if item_exist:
            return {"message": "Item already present"}
        item.add_update_item()
        return {"item": _item_schema.dump(item)}, 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, name):
        item = ItemModel.find_an_item(name)
        if item:
            item.delete_item()
            return {"message": "Item deleted successfully"}
        return {"message": "Item not present"}

    @jwt_required(fresh=True)
    def put(self, name):
        item = ItemModel.find_an_item(name)
        json_data = request.get_json()
        if item:
            item.price = json_data["price"]
        else:
            json_data["name"] = name
            item = _item_schema.load(json_data)
        item.add_update_item()


class ItemList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        items = _item_list_schema.dump(ItemModel.get_all_items())
        user_id = get_jwt().get('jti')
        if items:
            return {"items": items if user_id else [item["name"] for item in items]}
        return {"message": "No items present"}
