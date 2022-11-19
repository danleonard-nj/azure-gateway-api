from typing import List

from clients.active_directory_client import ActiveDirectoryClient
from models.active_directory import ActiveDirectoryApp


class ActiveDirectoryService:
    def __init__(
        self,
        client: ActiveDirectoryClient
    ):
        self.__client: ActiveDirectoryClient = client

    async def get_applications(
        self
    ) -> List[ActiveDirectoryApp]:
        data = await self.__client.get_applications()

        apps = [
            ActiveDirectoryApp(data=app)
            for app in data.get('value')
        ]

        return apps
