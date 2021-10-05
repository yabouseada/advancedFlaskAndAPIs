from ma import ma
from models.user import UserModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True
