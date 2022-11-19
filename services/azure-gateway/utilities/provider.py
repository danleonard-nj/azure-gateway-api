from clients.active_directory_client import ActiveDirectoryClient
from clients.authentication_client import AuthenticationClient
from clients.container_registry_client import ContainerRegistryClient
from clients.cost_management_client import CostManagementClient
from clients.devops_client import DevopsClient
from clients.identity_client import IdentityClient
from clients.kubernetes_client import KubernetesClient
from clients.log_analytics_client import LogAnalyticsClient
from clients.usage_client import UsageClient
from framework.abstractions.abstract_request import RequestContextProvider
from framework.auth.azure import AzureAd
from framework.auth.configuration import AzureAdConfiguration
from framework.clients.cache_client import CacheClientAsync
from framework.clients.http_client import HttpClient
from framework.configuration.configuration import Configuration
from quart import Quart
from services.active_directory_service import ActiveDirectoryService
from services.container_registry_service import ContainerRegistryService
from services.cost_management_service import CostManagementService
from services.devops_service import DevopsService
from services.kubernetes_service import KubernetesService
from services.log_analytics_service import LogAnalyticsService
from services.usage_service import UsageService
from framework.di.service_collection import ServiceCollection
from framework.di.static_provider import ProviderBase


class AdRole:
    READ = 'AzureGateway.Read'
    WRITE = 'AzureGateway.Write'
    IDENTITY = 'AzureGateway.Identity'


def configure_azure_ad(container):
    configuration = container.resolve(Configuration)

    # Hook the Azure AD auth config into the service
    # configuration
    ad_auth: AzureAdConfiguration = configuration.ad_auth
    azure_ad = AzureAd(
        tenant=ad_auth.tenant_id,
        audiences=ad_auth.audiences,
        issuer=ad_auth.issuer)

    azure_ad.add_authorization_policy(
        name='read',
        func=lambda t: AdRole.READ in t.get('roles'))

    azure_ad.add_authorization_policy(
        name='write',
        func=lambda t: AdRole.WRITE in t.get('roles'))

    azure_ad.add_authorization_policy(
        name='identity',
        func=lambda t: AdRole.IDENTITY in t.get('roles'))

    azure_ad.add_authorization_policy(
        name='default',
        func=lambda t: True)

    return azure_ad


class ContainerProvider(ProviderBase):
    @classmethod
    def configure_container(cls):
        container = ServiceCollection()
        container.add_singleton(Configuration)
        container.add_singleton(IdentityClient)

        container.add_singleton(
            dependency_type=AzureAd,
            factory=configure_azure_ad)

        container.add_singleton(AuthenticationClient)
        container.add_singleton(ContainerRegistryClient)
        container.add_singleton(IdentityClient)
        container.add_transient(KubernetesClient)
        container.add_singleton(LogAnalyticsClient)
        container.add_singleton(UsageClient)
        container.add_singleton(CacheClientAsync)
        container.add_singleton(DevopsClient)
        container.add_singleton(CostManagementClient)
        container.add_singleton(ActiveDirectoryClient)

        container.add_transient(ContainerRegistryService)
        container.add_transient(KubernetesService)
        container.add_transient(LogAnalyticsService)
        container.add_transient(UsageService)
        container.add_transient(DevopsService)
        container.add_transient(CostManagementService)
        container.add_singleton(ActiveDirectoryService)

        return container


def add_container_hook(app: Quart):
    def inject_container():
        RequestContextProvider.initialize_provider(
            app=app)

    app.before_request_funcs.setdefault(
        None, []).append(
            inject_container)
