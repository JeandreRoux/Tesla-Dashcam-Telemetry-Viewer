from dataclasses import dataclass


@dataclass
class RenderSettings:
    no_overlay: bool
    mph: bool
    preview: bool
    keep_csv: bool
    layout: dict
