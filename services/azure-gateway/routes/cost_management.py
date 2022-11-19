from framework.logger.providers import get_logger
from models.cost_management import CostManagementRequest
from quart import request
from services.cost_management_service import CostManagementService
from utilities.meta import MetaBlueprint

cost_management_bp = MetaBlueprint('cost_management_bp', __name__)
logger = get_logger(__name__)


@cost_management_bp.configure('/api/cost/timeframe/daily/groupby/product', methods=['GET'], auth_scheme='read')
async def get_usage(container):
    service: CostManagementService = container.resolve(CostManagementService)

    cost_request = CostManagementRequest(
        _request=request)

    response = await service.get_cost_by_product_data(
        request=cost_request)

    return response
