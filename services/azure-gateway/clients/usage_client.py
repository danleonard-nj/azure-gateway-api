from typing import Dict

from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from httpx import AsyncClient

from clients.authentication_client import AuthenticationClient

logger = get_logger(__name__)


# TODO: Deprecated, remove and use cost managment
class UsageClient:
    def __init__(
        self,
        configuration: Configuration,
        auth_client: AuthenticationClient,
        http_client: AsyncClient
    ):
        self.__authentication_client = auth_client
        self.__http_client = http_client

        self.__usage_base_url = configuration.azure_usage.get(
            'usage_base_url')
        self.__scope = configuration.azure_usage.get(
            'scope')
        self.__subscription_id = configuration.account.get(
            'subscription_id')

    async def get_headers(
        self
    ) -> Dict:
        token = await self.__authentication_client.get_scoped_token(
            scope=self.__scope)

        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def get_usage_endpoint(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        subscription = f'{self.__usage_base_url}/subscriptions/{self.__subscription_id}'
        resource = f'{subscription}/providers/Microsoft.Consumption/usageDetails'
        usage = f"{resource}?api-version=2021-01-01&$filter=properties/usageDate"

        return f"{usage} ge '{start_date}' and properties/usageDate le '{end_date}'"

    async def get_usage(
        self,
        start_date: str,
        end_date: str
    ):
        logger.info('Fetching Azure usage data')

        endpoint = self.get_usage_endpoint(
            start_date=start_date,
            end_date=end_date)

        headers = await self.get_headers()
        logger.info(f'Azure endpoint: {endpoint}')

        response = await self.__http_client.get(
            url=endpoint,
            headers=headers)

        logger.info(f'Usage Response Status: {response.status_code}')
        return response.json()
