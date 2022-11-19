from framework.abstractions.abstract_request import RequestContextProvider
from framework.dependency_injection.provider import InternalProvider
from framework.logger.providers import get_logger
from framework.serialization.serializer import configure_serializer
from quart import Quart

from routes.active_directory import active_directory_bp
from routes.authentication import authentication_bp
from routes.container_registry import container_registry_bp
from routes.cost_management import cost_management_bp
from routes.devops import devops_bp
from routes.health import health_bp
from routes.kubernetes import kubernetes_bp
from routes.log_analytics import log_analytics_bp
from utilities.provider import ContainerProvider

app = Quart(__name__)

logger = get_logger(__name__)

configure_serializer(app)

app.register_blueprint(health_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(log_analytics_bp)
app.register_blueprint(container_registry_bp)
app.register_blueprint(kubernetes_bp)
app.register_blueprint(devops_bp)
app.register_blueprint(cost_management_bp)
app.register_blueprint(active_directory_bp)


@app.before_serving
async def startup():
    RequestContextProvider.initialize_provider(
        app=app)

ContainerProvider.initialize_provider()
InternalProvider.bind(ContainerProvider.get_service_provider())


configure_serializer(app)

if __name__ == '__main__':
    app.run(debug=True, port='5091')
