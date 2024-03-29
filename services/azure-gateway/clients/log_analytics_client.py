from clients.authentication_client import AuthenticationClient
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from httpx import AsyncClient
from models.log_analytics import LogAnalyticsConfiguration

logger = get_logger(__name__)


class LogAnalyticsClient:
    def __init__(
        self,
        configuration: Configuration,
        authentication_client: AuthenticationClient,
        http_client: AsyncClient
    ):
        self._authentication_client = authentication_client
        self._http_client = http_client

        self._configuration = LogAnalyticsConfiguration(
            configuration=configuration)

    async def get_log_analytics_headers(
        self
    ) -> dict:
        logger.info('Getting auth headers')
        token = await self._authentication_client.get_resource_token(
            resource_name=self._configuration.log_analytics_resource_scope
        )

        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    async def get_management_headers(
        self
    ) -> dict:
        logger.info('Getting auth headers')
        token = await self._authentication_client.get_resource_token(
            resource_name=self._configuration.management_resource_scope
        )

        logger.info(
            f'Management Scope Token Request Headers: Resource: {self._configuration.management_resource_scope}')

        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    async def query(
        self,
        query: str
    ) -> dict:
        logger.info(f'Log Analytics Query: {query}')
        body = {
            'query': query
        }

        endpoint = f'{self._configuration.log_analytics_base_url}/v1/workspaces/{self._configuration.workspace_id}/query'

        headers = await self.get_log_analytics_headers()
        logger.info(f'Azure Query Endpoint: {endpoint}')

        response = await self._http_client.post(
            url=endpoint,
            json=body,
            headers=headers)

        return response.json()

    def _get_tables_endpoint(
        self
    ):
        subscription = f'{self._configuration.management_base_url}/subscriptions/{self._configuration.subscription_id}'
        resource = f'{subscription}/resourcegroups/{self._configuration.resource_group}/providers/Microsoft.OperationalInsights'
        return f'{resource}/workspaces/{self._configuration.workspace_name}/tables?api-version=2020-08-01'

    async def get_tables(
        self
    ) -> dict:
        logger.info('Azure Log Tables: Generating endpoint')

        endpoint = self._get_tables_endpoint()
        headers = await self.get_management_headers()
        logger.info(f'Azure Log Tables Endpoint: {endpoint}')

        response = await self._http_client.get(
            url=endpoint,
            headers=headers)

        return response.json()
