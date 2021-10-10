from flask_restful import Resource
from models import confirmation
from models.confirmation import ConfirmationModel
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema
from time import time


confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        """return confirmation html"""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)

        if not confirmation:
            return {"message": "NOT_FOUND"}, 404

        if confirmation.confirmed:
            return {"message": "ALREADY_CONFIRMED"}, 400

        if confirmation.expired:
            return {"message": "EXPIRED"}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()


class ConfirmationByUser(Resource):
    def get(self, user_id: int):
        """Returns confirmation for a given user"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User Not found"}
        return (
            {
                "current_time": int(time()),
                "confirmation": [
                    confirmation_schema.dump(each)
                    for each in user.confimation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )

    def post(self, user_id: int):
        """resend confirmation email"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User Not found"}

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": "already confirmed"}, 400
                confirmation.force_to_expire()
            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": "resend success"}
        except:

            return {"message": "resend failed"}
