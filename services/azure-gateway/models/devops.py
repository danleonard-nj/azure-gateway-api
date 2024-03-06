from framework.serialization import Serializable


class GetBuildByDefinitionRequest(Serializable):
    def __init__(
        self,
        definition_id: int
    ):
        self.definition_id = definition_id

    def to_dict(self) -> dict:
        return {
            'definition': {
                'id': self.definition_id
            }
        }


class BuildDefinition:
    def __init__(self, data):
        self.link = data.get('_links').get('web').get('href')
        self.createdDate = data.get('createdDate')
        self.id = data.get('id')
        self.name = data.get('name')

    def to_dict(self):
        return self.__dict__


class TriggeredBuildResponse:
    def __init__(self, data):
        self.build_number = data.get('buildNumber')
        self.id = data.get('id')
        self.status = data.get('status')

    def to_dict(self):
        return self.__dict__
