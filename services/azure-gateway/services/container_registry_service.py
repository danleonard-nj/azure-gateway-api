from typing import Dict
from clients.container_registry_client import ContainerRegistryClient
from framework.logger.providers import get_logger

logger = get_logger(__name__)


class ContainerRegistryService:
    def __init__(
        self,
        client: ContainerRegistryClient
    ):
        self.__client = client

    async def get_repositories(
        self
    ) -> Dict:
        logger.info(f'ACR: Fetch repository list')

        result = await self.__client.get_repository_list()
        return result

    async def get_manifests(
        self,
        repository_name: str
    ) -> Dict:
        logger.info(f'ACR: Fetch manifests: {repository_name}')

        result = await self.__client.get_manifests(
            repository_name=repository_name)
        return result

    async def get_manifest(
        self,
        repository: str,
        id: str
    ) -> bool:
        logger.info(f'ACR: Fetch manifest: {repository}: {id}')

        result = await self.__client.get_manifest(
            repository=repository,
            id=id)

        return result

    async def delete_manifest(
        self,
        repository: str,
        id: str
    ) -> bool:
        logger.info(f'ACR: Delete manifest: {repository}: {id}')

        result = await self.__client.delete_manifest(
            repository=repository,
            id=id)
        return result
