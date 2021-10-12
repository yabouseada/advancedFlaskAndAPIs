from blacklist import BLACKLIST
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager
from ma import ma
from models import confirmation
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import (
    UserRegister,
    UserReview,
    User,
    UserLogin,
    TokenRefresh,
    UserLogout,
)
from resources.confirmation import ConfirmationByUser, Confirmation

from db import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "PC"
# app.config['JWT_BLACKLIST_ENABLED']=True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)  # /auth


@jwt.additional_claims_loader
def additional_claims(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(_decrypted_header, _decrypted_body):
    return _decrypted_body["jti"] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback(_decrypted_header, _decrypted_body):
    return jsonify({"description": "Token has expired", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return "WTF?"


@jwt.unauthorized_loader
def missing_token_callback(error):
    return "Unauthorised token"


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(_decrypted_header, _decrypted_body):
    return "Not Fresh token"


@jwt.revoked_token_loader
def revoked_token_callback(_decrypted_header, _decrypted_body):
    return "revoked token"


api.add_resource(UserRegister, "/register")
api.add_resource(UserReview, "/review")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/itemlist")
api.add_resource(StoreList, "/storelist")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Confirmation, "/confirmation/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/cofirmation/user/<int:user_id>")
if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
