from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmConfigDiagnostic:
    diagnostic_id: str
    created_at: str
    family_key: str
    rule_key: str
    severity: str
    error_code: str
    error_message: str
    source_section: str
    blocking: bool
    status: str
