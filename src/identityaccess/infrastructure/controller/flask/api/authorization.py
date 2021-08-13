from flask import current_app, request, jsonify, make_response
from flask_restx import Namespace, Resource
from identityaccess.application.service.authorize import (
    Authorize as AuthorizationService,
    AuthorizeCommand,
    AuthorizationError
)

from identityaccess import InvalidRequestParamsException
from http import HTTPStatus


authorization_ns = Namespace(
    'authorization',
    description='Authorizing access to a resource using access token',
    path="/identityaccess/api/v1"
)


@authorization_ns.errorhandler(AuthorizationError)
def handle_authorization_error(error):
    return {
       "message": error.message,
       "code": error.code,
       "status": HTTPStatus.UNAUTHORIZED
   }, HTTPStatus.UNAUTHORIZED, {'WWW-Authenticate': 'Bearer realm="Identity & Access API", charset="UTF-8"'}


@authorization_ns.errorhandler(InvalidRequestParamsException)
def handle_value_error(error):
    return {
        "message": error.message,
        "code": error.code,
        "status": HTTPStatus.BAD_REQUEST
    }, HTTPStatus.BAD_REQUEST


@authorization_ns.route("/authorize")
class Authorize(Resource):
    def post(self):
        params = request.get_json()
        headers = request.headers

        authorization_service: AuthorizationService = current_app.container.get(
            'identityaccess.application.service.authorize.authorize'
        )

        authorization_service.authorize(
            AuthorizeCommand(
                params.get('tenant_id'),
                headers.get('Authorization'),
                params.get('scope')
            )
        )

        return make_response('', HTTPStatus.OK)

