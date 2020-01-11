from flask import Blueprint
from flask_restplus import Api, Resource, Namespace

ping_namespace = Namespace("ping")


class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "deploy sucess!!!!!!!!!!1"}


ping_namespace.add_resource(Ping, "")