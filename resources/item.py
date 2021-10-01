from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.orm import query
from models.item import ItemModel
from typing import Dict, List

BLANK_ERROR = "'{}'CANNOT BE BLANK"
ITEM_NOT_FOUND = "ITEM NOT FOUND"
ITEM_ALREADY_EXIST = "ITEM WITH  NAME '{}' ALREADY EXISTS"
ITEM_DELETED = "ITEM DELETED"
ITEM_WAS_NOT_INSERTED = "AN ERROR OCURRED WHILE TRYING TO INSERT THE ITEM"


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format("price")
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=BLANK_ERROR.format("store_id")
    )

    @classmethod
    # @jwt_required()
    def get(cls, name: str):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    # @jwt_required(fresh=True)
    def post(cls, name: str):

        if ItemModel.find_by_name(name):
            return {"message": ITEM_ALREADY_EXIST.format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": ITEM_WAS_NOT_INSERTED}, 500

        return item.json(), 201

    @classmethod
    # @jwt_required()
    def delete(cls, name: str):
        # claims = get_jwt()
        # if not claims==['is_admin']:
        # return {'message':'Admin previlege required'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}
        return {"message": ITEM_NOT_FOUND}

    @classmethod
    def put(cls, name: str):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)

        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {"items": items}, 200
        return {
            "items": [item["name"] for item in items],
            "message": "More data avaliable if you log in",
        }
        # return{'items':list(map(lambda x :x.json(),ItemModel.query.all()))} #same as first
