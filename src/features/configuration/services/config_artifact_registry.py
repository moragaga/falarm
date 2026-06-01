"""
This module defines classes and functions for managing the configuration artifact
registry. These artifacts represent administrative feature definitions, utilized
to organize and encapsulate configurations for navigation, alarm management,
and KPI systems.

Classes
-------
ConfigArtifactRegistry
    A dataclass encapsulating a collection of admin definitions.

Functions
---------
build_config_artifact_registry
    Constructs and returns an instance of ConfigArtifactRegistry populated
    with predefined admin definitions.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.features.admin_framework.models import AdminDefinition
from src.features.configuration.alarm.components_n0.definition import (
    ALARM_COMPONENTS_N0_ADMIN_DEFINITION,
)
from src.features.configuration.alarm.family.definition import ALARM_FAMILY_ADMIN_DEFINITION
from src.features.configuration.alarm.rules.definition import ALARM_RULES_ADMIN_DEFINITION
from src.features.configuration.alarm.tools.definition import ALARM_TOOLS_ADMIN_DEFINITION

from ..admin_panels.navigation.groups.definition import NAVIGATION_GROUPS_ADMIN_DEFINITION
from ..admin_panels.navigation.links.definition import (
    NAVIGATION_LINKS_ADMIN_DEFINITION,
)


@dataclass(frozen=True)
class ConfigArtifactRegistry:
    definitions: tuple[AdminDefinition, ...]

    def get_definitions(self) -> tuple[AdminDefinition, ...]:
        return self.definitions


def build_config_artifact_registry() -> ConfigArtifactRegistry:
    return ConfigArtifactRegistry(
        definitions=(
            NAVIGATION_LINKS_ADMIN_DEFINITION,
            NAVIGATION_GROUPS_ADMIN_DEFINITION,
            ALARM_FAMILY_ADMIN_DEFINITION,
            ALARM_TOOLS_ADMIN_DEFINITION,
            ALARM_COMPONENTS_N0_ADMIN_DEFINITION,
            ALARM_RULES_ADMIN_DEFINITION,
        )
    )
