import unittest

from framework.di.static_provider import InternalProvider

from clients.active_directory_client import ActiveDirectoryClient
from utilities.provider import ContainerProvider


class ActiveDirectoryClientTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        ContainerProvider.initialize_provider()
        InternalProvider.bind(ContainerProvider.get_service_provider())
        self.service_provider = ContainerProvider.get_service_provider()

    def get_client(
        self
    ) -> ActiveDirectoryClient:
        return self.service_provider.resolve(
            ActiveDirectoryClient)

    async def test_get_pods(self):
        client = self.get_client()

        response = await client.get_applications()

        self.assertIsNotNone(response)
