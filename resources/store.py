from flask_restful import Resource
from models.store import StoreModel
from schemas.store import StoreSchema

NAME_ALREADY_EXISTS = "A STORE WITH NAME '{}' ALREADY EXISTS"
ERROR_INSERTING = "AN ERROR OCURRED WHILE INSERTING THE STORE"
STORE_NOT_FOUND = "STORE NOT FOUND"
STORE_DELETED = "STORE DELETED"

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {"message": STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 404

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": STORE_DELETED}

        return {"message": STORE_NOT_FOUND}


class StoreList(Resource):
    @classmethod
    def get(cls):

        return {"stores": store_list_schema.dump(StoreModel.find_all())}
