from framework.crypto.hashing import sha256
from framework.validators.nulls import none_or_whitespace


class CacheKey:
    @staticmethod
    def get_auth_resource_token_cache_key(resource_name):
        token_name = sha256(f'resource-{resource_name}')
        return f'azure-gateway-token-{token_name}'

    @staticmethod
    def get_auth_scoped_token_cache_key(scope):
        token_name = sha256(f'scope-{scope}')
        return f'azure-gateway-token-{token_name}'

    @staticmethod
    def auth_token(
        client: str,
        scope: str = None
    ) -> str:
        if not none_or_whitespace(scope):
            hashed_scope = sha256(scope)
            return f'auth-{client}-{hashed_scope}'
        return f'auth-{client}'
