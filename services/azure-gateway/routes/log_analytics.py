from framework.logger.providers import get_logger
from quart import request
from services.log_analytics_service import LogAnalyticsService
from utilities.meta import MetaBlueprint

log_analytics_bp = MetaBlueprint('log_analytics_bp', __name__)

logger = get_logger(__name__)


@log_analytics_bp.configure('/api/logs/query', methods=['POST'], auth_scheme='read')
async def post_query(container):
    log_service = container.resolve(LogAnalyticsService)

    logger.info('gateway: post_query')
    body = await request.get_json()

    if not body or not body.get('query'):
        raise Exception('query cannot be null')

    response = await log_service.query(
        query=body.get('query'))

    return response


@log_analytics_bp.configure('/api/logs/tables', methods=['GET'], auth_scheme='read')
async def get_tables(container):
    log_service = container.resolve(LogAnalyticsService)

    logger.info('gateway: get_tables')
    response = await log_service.get_tables()
    return response
