from typing import Dict

from clients.authentication_client import AzureScope
from clients.identity_client import IdentityClient
from framework.configuration import Configuration
from framework.logger.providers import get_logger
from httpx import AsyncClient
from models.auth import AuthClient

logger = get_logger(__name__)


class ActiveDirectoryClient:
    def __init__(
        self,
        configuration: Configuration,
        identity_client: IdentityClient,
        http_client: AsyncClient
    ):
        self._base_url = configuration.active_directory.get(
            'base_url')

        self._identity_client = identity_client
        self._http_client = http_client

    async def _get_headers(
        self
    ) -> Dict:
        logger.info('Fetch auth token for AD')

        token = await self._identity_client.get_token(
            client_name=AuthClient.AzureGatewayApi,
            scope=AzureScope.Graph)

        return {
            'Authorization': f'Bearer {token}'
        }

    async def get_applications(
        self
    ) -> Dict:
        endpoint = f'{self._base_url}/applications'
        logger.info(f'Endpoint: {endpoint}')

        headers = await self._get_headers()
        logger.info(f'Auth headers: {headers}')
        
        data = await self._http_client.get(
            url=f'{self._base_url}/applications',
            headers=headers)
        
        apps = data.json()

        return apps
