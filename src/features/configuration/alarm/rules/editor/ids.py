from __future__ import annotations


class AlarmRuleEditorIds:
    HEADER = 'alarm-rule-editor-header'
    ORIGINAL_STORE = 'alarm-rule-editor-original-store'
    DRAFT_STORE = 'alarm-rule-editor-draft-store'
    VALIDATION_STORE = 'alarm-rule-editor-validation-store'
    DIRTY_STORE = 'alarm-rule-editor-dirty-store'
    TABS = 'alarm-rule-editor-tabs'
    TAB_CONTENT = 'alarm-rule-editor-tab-content'
    SAVE_BUTTON = 'alarm-rule-editor-save-button'
    CANCEL_BUTTON = 'alarm-rule-editor-cancel-button'

class AlarmRuleEditorTabs:
    IDENTITY = 'identity'
    MANAGEMENT = 'management'
    ESCALATION = 'escalation'
    VISUALIZATION = 'visualization'
    SUMMARY = 'summary'

    ALL = (
        IDENTITY,
        MANAGEMENT,
        ESCALATION,
        VISUALIZATION,
        SUMMARY,
    )
