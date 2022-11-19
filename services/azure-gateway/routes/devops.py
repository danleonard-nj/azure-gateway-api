from services.devops_service import DevopsService
from utilities.meta import MetaBlueprint

devops_bp = MetaBlueprint('devops_bp', __name__)


@devops_bp.configure('/api/devops/builds/<project>', methods=['GET'], auth_scheme='read')
async def get_builds(container, project):
    service: DevopsService = container.resolve(DevopsService)

    builds = await service.get_builds(
        project=project)
    return builds


@devops_bp.configure('/api/devops/builds/<project>/name/<build_name>', methods=['POST'], auth_scheme='write')
async def trigger_build_by_name(container, project, build_name):
    service: DevopsService = container.resolve(DevopsService)

    builds = await service.trigger_build_by_build_name(
        project=project,
        build_name=build_name)

    return builds
