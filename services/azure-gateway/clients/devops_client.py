import base64
from typing import Dict

from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from httpx import AsyncClient

logger = get_logger(__name__)


class DevopsClient:
    def __init__(
        self,
        configuration: Configuration,
        http_client: AsyncClient
    ):
        self.__username = configuration.devops.get('username')
        self.__pat = configuration.devops.get('pat')
        self.__organization = configuration.devops.get('organization')
        self.__base_url = configuration.devops.get('base_url')

        self.__http_client = http_client

    def __get_headers(
        self
    ) -> Dict:
        basic_auth = base64.b64encode(
            f'{self.__username}:{self.__pat}'.encode())

        return {
            'Authorization': f'Basic {basic_auth.decode()}',
            'Content-Type': 'application/json'
        }

    async def get_build_definitions(
        self,
        project: str
    ):
        logger.info(f'DevOps: Fetch builds for project: {project}')

        segment = f'{self.__organization}/{project}/_apis/build/definitions?api-version=6.0'
        endpoint = f'{self.__base_url}/{segment}'

        logger.info(f'Endpoint: {endpoint}')
        response = await self.__http_client.get(
            url=endpoint,
            headers=self.__get_headers())

        logger.info(f'Response status: {response.status_code}')
        return response.json().get('value')

    async def trigger_build_by_definition(
        self,
        project,
        definition_id
    ):
        logger.info(
            f"DevOps: triggering build '{definition_id}' in project: {project}")

        data = {
            'definition': {
                'id': definition_id
            }
        }

        headers = self.__get_headers()
        logger.info(headers)

        response = await self.__http_client.post(
            url=f'{self.__base_url}/{self.__organization}/{project}/_apis/build/builds?api-version=6.0',
            json=data,
            headers=headers)

        return response.json()
