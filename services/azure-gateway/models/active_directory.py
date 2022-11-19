from framework.serialization import Serializable


class ActiveDirectoryApp(Serializable):
    @property
    def application_id(self):
        return self.__data.get('id')

    @property
    def application_name(self):
        return self.__data.get('displayName')

    @property
    def identifier_uri(self):
        if any(self.__data.get('identifierUris', [])):
            return self.__data.get('identifierUris')[0]

    @property
    def default_scope(self):
        if (self.identifier_uri is not None
                and self.identifier_uri != ''):
            return f'{self.identifier_uri}/.default'

    @property
    def roles(self):
        return self.__data.get('appRoles')

    def __init__(self, data):
        self.__data = data

    def to_dict(self):
        return {
            'application_id': self.application_id,
            'application_name': self.application_name,
            'identifier_uri': self.identifier_uri,
            'default_scope': self.default_scope,
            'roles': self.roles
        }
