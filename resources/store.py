from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name:str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return{'message':'Store not found'},404
        
    def post(self,name:str):
        if StoreModel.find_by_name(name):
            return{'message':"A store with name '{}' already exists".format(name)},404
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return{'message':'An error ocurred while creating the store.'},500

        return store.json(),201
    def delete(self,name:str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return{'message':'Store deleted'}

        return {'message':'There is no store with this name'}


class StoreList(Resource):
    def get(slef):

        return {'stores':[store.json() for store in StoreModel.find_all()]}
        