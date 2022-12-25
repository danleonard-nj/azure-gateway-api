from framework.clients.cache_client import CacheClientAsync
from framework.logger.providers import get_logger

from clients.identity_client import IdentityClient
from models.auth import AuthClient, AzureScope
from models.cache import CacheKey

logger = get_logger(__name__)


class AuthenticationClient:
    def __init__(
        self,
        cache_client: CacheClientAsync,
        identity_client: IdentityClient
    ):
        self.__cache_client = cache_client
        self.__identity_client = identity_client

    async def get_scoped_token(
        self,
        scope: str
    ) -> str:

        logger.info(f'Fetching scoped token: {scope}')

        cache_key = CacheKey.get_auth_scoped_token_cache_key(
            scope=scope)
        logger.info(f'Cache key: {cache_key}')

        cached_token = await self.__cache_client.get_cache(
            key=cache_key)

        if cached_token is not None:
            logger.info(f'Returning cached token: {cache_key}')
            return cached_token

        token = await self.__identity_client.get_token(
            client_name='azure-gateway-api',
            scope=scope)

        logger.info(f'Token: {token}')

        await self.__cache_client.set_cache(
            key=cache_key,
            value=token,
            ttl=60)

        return token

    async def get_resource_token(
        self,
        resource_name: str
    ):
        logger.info(f'Fetching resource token: {resource_name}')

        cache_key = CacheKey.get_auth_resource_token_cache_key(
            resource_name=resource_name)

        logger.info(f'Cache key: {cache_key}')
        cached_token = await self.__cache_client.get_cache(
            key=cache_key)

        if cached_token is not None:
            logger.info(f'Returning cached token: {cached_token}')
            return cached_token

        token = await self.__identity_client.get_token(
            client_name=AuthClient.AzureGatewayApi,
            scope=AzureScope.Arm)

        logger.info(f'Token: {token}')

        await self.__cache_client.set_cache(
            key=cache_key,
            value=token,
            ttl=60)

        return token
