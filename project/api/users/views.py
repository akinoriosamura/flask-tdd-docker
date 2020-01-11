from flask import Blueprint, request
from flask_restplus import Api, Resource, fields, Namespace

from project.api.services import (
    add_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
)

users_namespace = Namespace("users")

user = users_namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UserLists(Resource):
    @users_namespace.expect(user, validate=True)
    @users_namespace.response(201, "<user_email> was added!")  # new
    @users_namespace.response(400, "Sorry. That email already exists.")  # new
    def post(self):
        """Creates a new user."""
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

    @users_namespace.marshal_with(user, as_list=True)
    def get(self):
        """Returns all users."""
        return get_all_users(), 200


class Users(Resource):
    @users_namespace.marshal_with(user)
    @users_namespace.response(200, "Success")  # new
    @users_namespace.response(404, "User <user_id> does not exist")  # new
    def get(self, user_id):
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return user, 200


users_namespace.add_resource(UserLists, "")  # updated
users_namespace.add_resource(Users, "/<int:user_id>")  # updated
