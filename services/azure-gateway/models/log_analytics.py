

class LogAnalyticsConfiguration:
    def __init__(self, configuration):
        account = configuration.account
        azure_log_analytics = configuration.azure_log_analytics

        self.subscription_id = account.get('subscription_id')
        self.log_analytics_base_url = azure_log_analytics.get(
            'log_analytics_base_url')
        self.workspace_id = azure_log_analytics.get('workspace_id')
        self.workspace_name = azure_log_analytics.get('workspace_name')
        self.resource_group = azure_log_analytics.get('resource_group')
        self.management_base_url = azure_log_analytics.get(
            'management_base_url')
        self.log_analytics_resource_scope = azure_log_analytics.get(
            'log_analytics_resource_scope')
        self.management_resource_scope = azure_log_analytics.get(
            'management_resource_scope')
