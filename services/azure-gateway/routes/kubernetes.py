from models.kubernetes import KuberenetesLogRequest
from quart import abort, request
from services.kubernetes_service import KubernetesService
from utilities.meta import MetaBlueprint

kubernetes_bp = MetaBlueprint('kubernetes_bp', __name__)


@kubernetes_bp.configure('/api/aks/pods/images', methods=['GET'], auth_scheme='read')
async def get_pod_images(container):
    kubernetes_service: KubernetesService = container.resolve(
        KubernetesService)

    pods = await kubernetes_service.get_pod_images()
    return pods


@kubernetes_bp.configure('/api/aks/pods/names', methods=['GET'], auth_scheme='read')
async def get_pod_names(container):
    kubernetes_service: KubernetesService = container.resolve(
        KubernetesService)

    pods = await kubernetes_service.get_pods()
    return {'pods': pods}


@kubernetes_bp.configure('/api/aks/<namespace>/<pod>/logs', methods=['GET'], auth_scheme='read')
async def get_logs(container, namespace, pod):
    kubernetes_service: KubernetesService = container.resolve(
        KubernetesService)

    model = KuberenetesLogRequest(
        namespace=namespace,
        pod=pod,
        params=request.args)

    if not model.validate():
        return abort(404)

    logs = await kubernetes_service.get_logs(
        namespace=model.namespace,
        pod=model.pod,
        tail_lines=model.tail)

    return {'logs': logs}
