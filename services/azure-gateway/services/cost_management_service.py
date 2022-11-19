from clients.cost_management_client import CostManagementClient
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from models.cost_management import CostManagementData, CostManagementRequest

logger = get_logger(__name__)


class CostManagementService:
    def __init__(
        self,
        client: CostManagementClient
    ):
        self.__client = client

    async def get_cost_by_product_data(
        self,
        request: CostManagementRequest
    ):
        logger.info(
            f'Get cost management data: {serialize(request.to_dict())}')

        result = await self.__client.get_cost_by_product_data(
            start_date=request.start_date,
            end_date=request.end_date)

        logger.info('Parsing cost management data')
        cost_management_data = CostManagementData(
            data=result)

        data = cost_management_data.get_dict()

        return {
            'data': data
        }
