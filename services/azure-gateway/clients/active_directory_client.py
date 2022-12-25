from typing import Dict

import httpx
from framework.configuration import Configuration
from framework.logger.providers import get_logger

from clients.authentication_client import AzureScope
from clients.identity_client import IdentityClient
from models.auth import AuthClient

logger = get_logger(__name__)


class ActiveDirectoryClient:
    def __init__(
        self,
        configuration: Configuration,
        identity_client: IdentityClient
    ):
        self.__base_url = configuration.active_directory.get(
            'base_url')

        self.__identity_client = identity_client

    async def __get_headers(
        self
    ) -> Dict:
        logger.info('Fetch auth token for AD')

        token = await self.__identity_client.get_token(
            client_name=AuthClient.AzureGatewayApi,
            scope=AzureScope.Graph)

        return {
            'Authorization': f'Bearer {token}'
        }

    async def get_applications(
        self
    ) -> Dict:
        endpoint = f'{self.__base_url}/applications'
        logger.info(f'Endpoint: {endpoint}')

        headers = await self.__get_headers()
        logger.info(f'Auth headers: {headers}')

        async with httpx.AsyncClient(timeout=None) as client:
            data = await client.get(
                url=f'{self.__base_url}/applications',
                headers=headers)

        apps = data.json()
        return apps
