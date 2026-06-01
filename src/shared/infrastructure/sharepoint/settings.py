"""
Provides a dataclass for SharePoint settings and a method for instantiating
it from an environment configuration.

This module defines a frozen dataclass `SharepointSettings`, which holds
URLs and settings related to SharePoint operations. It includes a method
for generating an instance of the dataclass using data from a provided
environment configuration.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.app.env_configuration import EnvConfiguration


@dataclass(frozen=True)
class SharepointSettings:
    get_endpoint: str = 'https://defaultd96f3d5a3042402a994b05725b2e14.27.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/69f705fa63e54fe0926e497535547a14/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=55o2q_xGNjwQWkes9BV81brxmCCWCrZKwWZqdfs6fM8'
    post_endpoint: str = 'https://defaultd96f3d5a3042402a994b05725b2e14.27.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/05311c3635aa492e9775ae6d19ac117b/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=oyMKQKNCcDzMgHdplOw0kfWkPUNWLZEFB6b-jaUXjDk'
    root_path: str = ''
    headers: dict | None = None

    @classmethod
    def from_env(cls, settings: EnvConfiguration) -> SharepointSettings:
        return cls(
            get_endpoint=cls.get_endpoint,
            post_endpoint=cls.post_endpoint,
            root_path=settings.sharepoint_root_path,
            headers={'app-access-token': settings.secret_key}
        )
