import unittest

from framework.di.static_provider import InternalProvider

from clients.kubernetes_client import KubernetesClient
from utilities.provider import ContainerProvider


class KubernetesClientTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        ContainerProvider.initialize_provider()
        InternalProvider.bind(ContainerProvider.get_service_provider())
        self.service_provider = ContainerProvider.get_service_provider()

    def get_client(
        self
    ) -> KubernetesClient:
        return self.service_provider.resolve(
            KubernetesClient)

    async def test_get_pods(self):
        client = self.get_client()

        response = await client.get_pods()

        self.assertIsNotNone(response)

    async def test_get_pod_images(self):
        client = self.get_client()

        response = await client.get_pod_images()

        self.assertIsNotNone(response)

    async def test_get_logs(self):
        client = self.get_client()

        pods = await client.get_pods()
        pod_name = pods[0].get('name')
        namespace = pods[0].get('namespace')

        response = await client.get_logs(
            namespace=namespace,
            pod=pod_name)

        self.assertIsNotNone(response)
