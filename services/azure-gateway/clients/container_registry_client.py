import base64
from typing import List

from framework.clients.http_client import HttpClient
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
import httpx

logger = get_logger(__name__)


class ContainerRegistryClient:
    def __init__(
        self,
        configuration: Configuration
    ):
        self.__registry_url = configuration.azure_container_registry.get(
            'registry_url')
        self.__registry_username = configuration.azure_container_registry.get(
            'registry_username')
        self.__registry_password = configuration.azure_container_registry.get(
            'registry_password')

    def __get_auth_headers(
        self
    ) -> dict:

        auth_pair = f'{self.__registry_username}:{self.__registry_password}'
        auth_string = base64.b64encode(auth_pair.encode())

        return {
            'Authorization': f'Basic {auth_string.decode()}'
        }

    async def get_repository_list(
        self
    ) -> dict:

        endpoint = self.__registry_url + '/acr/v1/_catalog'
        logger.info(f'Endpoint: {endpoint}')

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(
                url=endpoint,
                headers=self.__get_auth_headers())

        logger.info(f'Response code: {response.status_code}')
        return response.json()

    async def get_manifests(
        self,
        repository_name: str
    ) -> List[dict]:

        endpoint = f'{self.__registry_url}/acr/v1/{repository_name}/_manifests'
        logger.info(f'Endpoint: {endpoint}')

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(
                url=endpoint,
                headers=self.__get_auth_headers(),
                timeout=None)

        logger.info(f'Response code: {response.status_code}')
        return response.json()

    async def delete_manifest(
        self,
        repository: str,
        id: str
    ) -> bool:

        endpoint = f'{self.__registry_url}/v2/{repository}/manifests/{id}'
        logger.info(f'Endpoint: {endpoint}')

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.delete(
                url=endpoint,
                headers=self.__get_auth_headers(),
                timeout=None)

        logger.info(f'Response code: {response.status_code}')
        return True

    async def get_manifest(
        self,
        repository: str,
        id: str
    ) -> bool:

        endpoint = f'{self.__registry_url}/v2/{repository}/manifests/{id}'
        logger.info(f'Endpoint: {endpoint}')

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(
                url=endpoint,
                headers=self.__get_auth_headers(),
                timeout=None)

        logger.info(f'Response code: {response.status_code}')
        return response.json()
