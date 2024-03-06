from typing import Dict

from clients.authentication_client import AuthenticationClient
from constants.azure import AzureScope
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from httpx import AsyncClient
from models.cost_management import CostByProductQuery

logger = get_logger(__name__)


class CostManagementClient:
    def __init__(
        self,
        configuration: Configuration,
        auth_client: AuthenticationClient,
        http_client: AsyncClient
    ):
        self._authentication_client = auth_client
        self._http_client = http_client

        self._subscription_id = configuration.account.get(
            'subscription_id')
        self._base_url = configuration.azure_resource_management.get(
            'base_url')

    def _get_management_base_url(
        self
    ) -> str:
        return f'{self._base_url}/subscriptions/{self._subscription_id}'

    async def _get_headers(
        self
    ) -> Dict:

        logger.info(
            f'Fetching Azure auth token for scope: {AzureScope.ManagementDefault}')

        token = await self._authentication_client.get_scoped_token(
            scope=AzureScope.ManagementDefault)

        logger.info(f'Token: {token}')

        return {
            'Authorization': f'Bearer {token}'
        }

    async def get_cost_by_product_data(
        self,
        start_date,
        end_date
    ):
        logger.info(f'Fetching cost management data')
        logger.info(f'StartDate: {start_date}: EndDate: {end_date}')

        cost_by_product_query = CostByProductQuery(
            start_date=start_date,
            end_date=end_date)

        query = cost_by_product_query.get_query()
        logger.info(f'Query: {serialize(query)}')

        base_url = self._get_management_base_url()
        endpoint = f'{base_url}/providers/Microsoft.CostManagement/query?api-version=2021-10-01'

        headers = await self._get_headers()
        logger.info(f'Endpoint: {endpoint}')

        response = await self._http_client.post(
            url=endpoint,
            headers=headers,
            json=query,
            timeout=None)

        logger.info(f'Status: {response.status_code}')
        return response.json()
