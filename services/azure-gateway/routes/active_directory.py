from framework.logger.providers import get_logger
from services.active_directory_service import ActiveDirectoryService
from utilities.meta import MetaBlueprint

active_directory_bp = MetaBlueprint('active_directory_bp', __name__)
logger = get_logger(__name__)


@active_directory_bp.configure('/api/ad/applications', methods=['GET'], auth_scheme='read')
async def get_applications(container):
    service: ActiveDirectoryService = container.resolve(ActiveDirectoryService)

    applications = await service.get_applications()
    return applications
