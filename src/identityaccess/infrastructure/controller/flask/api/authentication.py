from flask import current_app, request, jsonify, make_response
from flask_restx import Namespace, Resource
from identityaccess.application.service.authenticate import Authenticate as AuthenticateService, AuthenticateCommand, AuthenticationError
from identityaccess import InvalidRequestParamsException
from http import HTTPStatus


authentication_ns = Namespace(
    "authentication",
    description="User authentication",
    path="/identityaccess/api/v1"
)


@authentication_ns.errorhandler(AuthenticationError)
def handle_authentication_error(error):
    return {
       "message": error.message,
       "code": error.code,
       "status": HTTPStatus.FORBIDDEN
   }, HTTPStatus.FORBIDDEN


@authentication_ns.errorhandler(InvalidRequestParamsException)
def handle_value_error(error):
    return {
        "message": error.message,
        "code": error.code,
        "status": HTTPStatus.BAD_REQUEST
    }, HTTPStatus.BAD_REQUEST


@authentication_ns.route("/authenticate")
class Authenticate(Resource):
    def post(self):
        params = request.get_json()

        authentication_service: AuthenticateService = current_app.container.get(
            "identityaccess.application.service.authenticate.authenticate"
        )

        response = authentication_service.authenticate(
            AuthenticateCommand(
                params.get("tenant_id"),
                params.get("username"),
                params.get("password")
            )
        )

        return make_response(
            jsonify(access_token=response.access_token, token_type=response.token_type),
            HTTPStatus.OK
        )

