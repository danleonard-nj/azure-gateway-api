

class AzureScope:
    ARM = 'https://management.core.windows.net/.default'
    GRAPH = 'https://graph.microsoft.com/.default'


class AzureAuthConfiguration:
    def __init__(self, data):
        self.auth_scope = data.get('auth_scope')
        self.base_url = data.get('auth_base_url')
        self.tenant_id = data.get('tenant_id')
        self.az_admin_client_id = data.get(
            'azure_admin_client')
        self.az_admin_client_secret = data.get(
            'azure_admin_secret')
