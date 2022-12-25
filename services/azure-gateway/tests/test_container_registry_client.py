import unittest

from framework.di.static_provider import InternalProvider

from clients.container_registry_client import ContainerRegistryClient
from utilities.provider import ContainerProvider


class ContainerRegistryClientTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        ContainerProvider.initialize_provider()
        InternalProvider.bind(ContainerProvider.get_service_provider())
        self.service_provider = ContainerProvider.get_service_provider()

    def get_client(
        self
    ) -> ContainerRegistryClient:
        return self.service_provider.resolve(
            ContainerRegistryClient)

    async def test_get_repository_list(self):
        client = self.get_client()

        response = await client.get_repository_list()

        self.assertIsNotNone(response)

    async def test_get_manifests(self):
        client = self.get_client()

        repos = await client.get_repository_list()
        test_repo = repos.get('repositories')[0]

        manifests = await client.get_manifests(
            repository_name=test_repo)

        self.assertIsNotNone(manifests)

    async def test_get_manifest(self):
        client = self.get_client()

        repos = await client.get_repository_list()
        test_repo = repos.get('repositories')[0]

        manifests = await client.get_manifests(
            repository_name=test_repo)
        test_manifest = manifests.get('manifests')[0]
        test_manifest_id = test_manifest.get('digest')

        manifest = await client.get_manifest(
            repository=test_repo,
            id=test_manifest_id)

        self.assertIsNotNone(manifest)
