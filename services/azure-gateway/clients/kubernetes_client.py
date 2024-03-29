from typing import Dict

import httpx
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger

logger = get_logger(__name__)


class KubernetesClient:
    def __init__(
        self,
        configuration: Configuration
    ):
        self._base_url = configuration.azure_kubernetes.get(
            'host_url')
        self._token = configuration.azure_kubernetes.get(
            'token')
        self._cert_path = configuration.azure_kubernetes.get(
            'certificate_path')

    def __get_headers(
        self
    ) -> dict:
        return {
            'Authorization': f'Bearer {self._token}'
        }

    async def _get_pods(
        self
    ) -> dict:
        logger.info(f'Fetching pods')

        async with httpx.AsyncClient(verify=self._cert_path) as client:
            response = await client.get(
                url=f'{self._base_url}/api/v1/pods',
                headers=self.__get_headers(),
                timeout=None)

            return response.json()

    async def get_pods(
        self
    ) -> dict:
        pods = await self._get_pods()

        results = []
        for pod in pods.get('items', []):

            metadata = pod.get('metadata', dict())
            results.append({
                'name': metadata.get('name'),
                'namespace': metadata.get('namespace')
            })

        return results

    async def get_pod_images(
        self
    ) -> dict:

        pods = await self._get_pods()

        images = [
            x.get('spec').get('containers')[0].get('image')
            for x in pods.get('items')
        ]

        return {
            'pods': images
        }

    async def get_logs(
        self,
        namespace,
        pod,
        tail_lines=100
    ):

        async with httpx.AsyncClient(verify=self._cert_path) as client:
            response = await client.get(
                url=f'{self._base_url}/api/v1/namespaces/{namespace}/pods/{pod}/log?tailLines={tail_lines}',
                headers=self.__get_headers(),
                timeout=None)

            return response.text
