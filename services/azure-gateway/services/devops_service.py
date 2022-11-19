

from clients.devops_client import DevopsClient
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from framework.utilities.pinq import first
from models.devops import BuildDefinition, TriggeredBuildResponse

logger = get_logger(__name__)


class DevopsService:
    def __init__(
        self,
        client: DevopsClient
    ):
        self.__client = client

    async def get_builds(
        self,
        project
    ):
        logger.info(f'Get builds for project: {project}')

        result = await self.__client.get_build_definitions(
            project=project)

        logger.info('Parsing build definition models')
        models = [
            BuildDefinition(data=_build)
            for _build in result
        ]

        logger.info('Parsing response models from definitions')
        results = [
            model.to_dict()
            for model in models
        ]

        return {'definitions': results}

    async def trigger_build_by_definition_id(
        self,
        project: str,
        definition_id: str
    ):
        logger.info(
            f"Triggering build definition '{definition_id}' in project {project}")

        response = await self.__client.trigger_build_by_definition(
            project=project,
            definition_id=definition_id)

        model = TriggeredBuildResponse(
            data=response)

        logger.info(f'Triggered build: {model.build_number}')
        return model.to_dict()

    async def trigger_build_by_build_name(
        self,
        project,
        build_name
    ):
        logger.info(f"Triggering build '{build_name}' in project {project}")

        logger.info('Fetching build definitions')
        definitions = await self.__client.get_build_definitions(
            project=project)

        definition_models = [
            BuildDefinition(data=_build)
            for _build in definitions]

        definition = first(
            items=definition_models,
            func=lambda x: x.name == build_name)

        if definition is None:
            raise Exception(
                f"No build with the name '{build_name}' exists in project '{project}'")

        logger.info(
            f'Build definition found: {serialize(definition.to_dict())}')

        response = await self.__client.trigger_build_by_definition(
            project=project,
            definition_id=definition.id)

        model = TriggeredBuildResponse(
            data=response)

        logger.info(f'Triggered build: {model.build_number}')
        return model.to_dict()
