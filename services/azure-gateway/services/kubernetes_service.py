from clients.kubernetes_client import KubernetesClient
from framework.logger.providers import get_logger

logger = get_logger(__name__)


class KubernetesService:
    def __init__(
        self,
        client: KubernetesClient
    ):
        self.__client = client

    async def get_pod_images(
        self
    ):
        logger.info(f'AKS: get pod images')

        pods = await self.__client.get_pod_images()
        return pods

    async def get_pods(
        self
    ):
        logger.info(f'AKS: get pods')

        pods = await self.__client.get_pods()
        return pods

    async def get_logs(
        self,
        namespace: str,
        pod: str,
        tail_lines: int
    ):
        logger.info(
            f'AKS: Get pod logs for pod: {namespace}:{pod}')

        logs = await self.__client.get_logs(
            namespace=namespace,
            pod=pod,
            tail_lines=tail_lines or 100)

        log_lines = logs.split('\n')
        log_lines.reverse()

        return log_lines
