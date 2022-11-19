from framework.clients.cache_client import CacheClientAsync
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from models.auth import AzureAuthConfiguration, AzureScope

from clients.identity_client import IdentityClient

logger = get_logger(__name__)


class AuthenticationClient:
    def __init__(
        self,
        configuration: Configuration,
        cache_client: CacheClientAsync,
        identity_client: IdentityClient
    ):
        self.__cache_client = cache_client
        self.__identity_client = identity_client

        self.__azure_auth = AzureAuthConfiguration(
            data=configuration.azure_auth)

    async def get_scoped_token(self, scope) -> str:
        logger.info('Fetching Azure scoped auth token')

        cache_key = self._get_scoped_token_cache_key(
            scope=scope)
        logger.info(f'Cache key: {cache_key}')

        cached_token = await self.__cache_client.get_cache(
            key=cache_key)

        if cached_token is not None:
            logger.info('Returning cached token')
            return cached_token

        logger.info(f'Fethching token from identity client')
        logger.info(f'Scope: {scope}')

        token = await self.__identity_client.get_token(
            client_name='azure-gateway-api',
            scope=scope)

        logger.info(f'Token: {token}')

        await self.__cache_client.set_cache(
            key=cache_key,
            value=token,
            ttl=60)

        return token

    async def get_resource_token(self, resource_name):
        logger.info('Fetching Azure resource auth token')

        cache_key = self._get_resource_token_cache_key(
            resource_name=resource_name)

        logger.info(f'Attempting fetch from cache at key: {cache_key}')
        cached_token = await self.__cache_client.get_cache(
            key=cache_key)

        if cached_token is not None:
            logger.info('Cache hit, returning cached auth token')
            return cached_token

        logger.info(f'Scope: {self.__azure_auth.auth_scope}')
        logger.info(f'Resource: {resource_name}')

        client_request = self.__identity_client.get_client(
            client_name='azure-gateway-api')

        client_request['scope'] = AzureScope.ARM

        logger.info(f'Client request: {serialize(client_request)}')

        token = await self.__identity_client.send_token_request(
            request=client_request)

        logger.info(f'Token: {token}')

        await self.__cache_client.set_cache(
            key=cache_key,
            value=token,
            ttl=60)

        return token

    def _get_resource_token_cache_key(self, resource_name):
        return f'azure-resource-token:{resource_name}'

    def _get_scoped_token_cache_key(self, scope):
        return f'azure-scoped-token:{scope}'
