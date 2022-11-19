from quart import Blueprint, request
from clients.authentication_client import AuthenticationClient

from framework.handlers.response_handler_async import response_handler
from framework.auth.wrappers.azure_ad_wrappers import azure_ad_authorization

from utilities.meta import MetaBlueprint


authentication_bp = MetaBlueprint('authentication_bp', __name__)


@authentication_bp.configure('/api/authentication/scoped', methods=['POST'], auth_scheme='identity')
async def scoped_token(container):
    authentication_client: AuthenticationClient = container.resolve(
        AuthenticationClient)
    payload = await request.get_json()

    if not payload:
        raise Exception('Request cannot be null')
    if not payload.get('scope'):
        raise Exception('Scope is required')

    token = await authentication_client.get_scoped_token(
        scope=payload.get('scope'))

    if not token:
        raise Exception('Failed to fetch azure token')

    return {
        'token': token
    }


@authentication_bp.configure('/api/authentication/resource', methods=['POST'], auth_scheme='identity')
async def resource_token(container):
    authentication_client: AuthenticationClient = container.resolve(
        AuthenticationClient)
    payload = await request.get_json()

    if not payload:
        raise Exception('Request cannot be null')
    if not payload.get('resource'):
        raise Exception('Resource is required')

    token = await authentication_client.get_resource_token(
        resource_name=payload.get('resource'))

    if not token:
        raise Exception('Failed to fetch azure token')

    return {
        'token': token
    }
