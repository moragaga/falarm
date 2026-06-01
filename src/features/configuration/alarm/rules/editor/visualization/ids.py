from __future__ import annotations


class AlarmRuleVisualizationIds:
    TARGETS_CONTAINER = 'alarm-rule-visualization-targets-container'

    # Se conservan estos IDs por compatibilidad con callbacks/patches previos,
    # pero la visualización final solo usa componentes y subcomponentes Nivel 0.
    ADD_TARGET_BUTTON = 'alarm-rule-visualization-add-target-button'
    TOOL_TYPE = 'alarm-rule-visualization-tool'
    VISUALIZATION_MODE_TYPE = 'alarm-rule-visualization-mode'
    MAIN_COMPONENT_TYPE = 'alarm-rule-visualization-main-component'
    HIGHLIGHT_TARGET_TYPE = 'alarm-rule-visualization-highlight-target'
    POSITION_GROUP_TYPE = 'alarm-rule-visualization-position-group'
    MIN_POSITION_TYPE = 'alarm-rule-visualization-min-position'
    MAX_POSITION_TYPE = 'alarm-rule-visualization-max-position'
    REMOVE_TYPE = 'alarm-rule-visualization-remove'

    AFFECTED_COMPONENTS_TYPE = 'alarm-rule-visualization-affected-components'
    AFFECTED_SUBCOMPONENTS_TYPE = 'alarm-rule-visualization-affected-subcomponents'
