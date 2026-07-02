from collections.abc import Callable
from dataclasses import dataclass

from modules import layouts


@dataclass
class RenderSettings:
    no_overlay: bool
    mph: bool
    preview: bool
    keep_csv: bool
    layout: layouts.LayoutConfig
    telemetry_prompt: Callable[[], bool] | None = None
