from clients.log_analytics_client import LogAnalyticsClient
from framework.logger.providers import get_logger

logger = get_logger(__name__)


class LogAnalyticsService:
    def __init__(
        self,
        client: LogAnalyticsClient
    ):
        self.__client = client

    async def query(
        self,
        query: str
    ) -> dict:
        logger.info(f'Azure Log Query: Request: {query}')
        response = await self.__client.query(
            query=query)

        return response

    async def get_tables(
        self
    ) -> dict:
        logger.info(f'Fetching Azure Log Tables')

        response = await self.__client.get_tables()
        return response
