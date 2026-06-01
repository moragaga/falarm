"""
Defines a data structure for representing the result of an action performed
by the PublicationManager. This structure contains details about the rows
affected, any encountered errors, and an optional success message.

The structure ensures immutability and provides a utility property to
check if any errors are present.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PublicationManagerActionResult:
    rows: list[dict[str, Any]]
    errors: tuple[str, ...] = ()
    success_message: str | None = None

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)
