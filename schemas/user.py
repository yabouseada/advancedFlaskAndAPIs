import re
from ma import ma
from models.user import UserModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import pre_dump


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")
        load_instance = True

    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confimation = [user.most_recent_confirmation]
        return user
