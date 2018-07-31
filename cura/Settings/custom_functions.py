
from typing import Any, TYPE_CHECKING

from UM.Logger import Logger
from UM.Settings.PropertyEvaluationContext import PropertyEvaluationContext, ContextType
from UM.Settings.SettingFunction import SettingFunction

if TYPE_CHECKING:
    from cura.Settings.CuraContainerStack import CuraContainerStack


def getValue(stack: "CuraContainerStack", name: str, from_container_name: str = None) -> Any:
    container_type_dict = {"user": 0,
                           "quality_changes": 1,
                           "quality": 2,
                           "material": 3,
                           "variant": 4,
                           "definition_changes": 5,
                           "definition": 6}

    idx = container_type_dict[from_container_name]

    context = PropertyEvaluationContext(stack)
    context.context[ContextType.EvaluateFromContainerIndex.value] = idx

    value = stack.getRawProperty(name, "value", context = context, use_next = False)
    if isinstance(value, SettingFunction):
        if context is not None:
            context.pushContainer(stack)
        value = value(stack, context)
        if context is not None:
            context.popContainer()

    Logger.log("d", "------------    stack = [%s]  name = [%s]  from container name = [%s]    container idx = [%s]  result = [%s]",
               stack, name, from_container_name, idx, value)
    return value


__all__ = ["getValue"]
