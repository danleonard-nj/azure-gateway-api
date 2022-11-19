from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from framework.serialization import Serializable

from framework.clients.http_client import HttpClient
from clients.authentication_client import AzureScope

from clients.identity_client import IdentityClient


logger = get_logger(__name__)


class ActiveDirectoryClient:
    def __init__(
        self,
        identity_client: IdentityClient
    ):
        self.__http_client = HttpClient()
        self.__identity_client = identity_client

        self.__base_url = 'https://graph.microsoft.com/v1.0'

    async def __get_headers(self):
        token = await self.__identity_client.get_token(
            client_name='azure-gateway-api',
            scope=AzureScope.GRAPH)

        return {
            'Authorization': f'Bearer {token}'
        }

    async def get_applications(self):
        data = await self.__http_client.get(
            url=f'{self.__base_url}/applications',
            headers=(await self.__get_headers()))

        apps = data.json()
        return apps
