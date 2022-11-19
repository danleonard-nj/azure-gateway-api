from framework.logger.providers import get_logger
from quart import request
from services.container_registry_service import ContainerRegistryService
from utilities.meta import MetaBlueprint

container_registry_bp = MetaBlueprint('container_registry_bp', __name__)

logger = get_logger(__name__)


@container_registry_bp.configure('/api/acr/repositories', methods=['GET'], auth_scheme='read')
async def get_repositories(container):
    registry_service: ContainerRegistryService = container.resolve(
        ContainerRegistryService)

    response = await registry_service.get_repositories()
    return response


@container_registry_bp.configure('/api/acr/manifests', methods=['GET'], auth_scheme='read')
async def get_manifests(container):
    registry_service: ContainerRegistryService = container.resolve(
        ContainerRegistryService)

    repository = request.args.get('repository_name')

    if not repository:
        raise Exception('Repository cannot be null')

    response = await registry_service.get_manifests(
        repository_name=repository)

    return response


@container_registry_bp.configure('/api/acr/manifests', methods=['DELETE'], auth_scheme='write')
async def delete_manifest(container):
    registry_service: ContainerRegistryService = container.resolve(
        ContainerRegistryService)

    repository = request.args.get('repository_name')
    manifest = request.args.get('manifest_id')

    if not repository:
        raise Exception('Repository_name cannot be null')
    if not repository:
        raise Exception('Manifest_id cannot be null')

    response = await registry_service.delete_manifest(
        repository=repository,
        id=manifest)

    return {'result': response}
