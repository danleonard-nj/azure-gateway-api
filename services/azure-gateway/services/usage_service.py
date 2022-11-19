from clients.usage_client import UsageClient
from framework.logger.providers import get_logger

logger = get_logger(__name__)


class UsageService:
    def __init__(
        self,
        client: UsageClient
    ):
        self.__client = client

    async def get_usage(
        self,
        start_date: str,
        end_date: str
    ):
        logger.info(
            f'Get Azure Usage: Start Date: {start_date}: End Date: {end_date}')

        response = await self.__client.get_usage(
            start_date=start_date,
            end_date=end_date)

        return response
