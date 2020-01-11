from flask import Blueprint, request
from flask_restplus import Api, Resource, fields

from project.api.services import (add_user, get_all_users, get_user_by_email,
                                  get_user_by_id)

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

user = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UserLists(Resource):
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_email(email)
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        add_user(username, email)
        response_object["message"] = f"{email} was added!"
        return response_object, 201

    @api.marshal_with(user, as_list=True)
    def get(self):
        return get_all_users(), 200


class Users(Resource):
    @api.marshal_with(user)
    def get(self, user_id):
        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user, 200


api.add_resource(UserLists, "/users")
api.add_resource(Users, "/users/<int:user_id>")
