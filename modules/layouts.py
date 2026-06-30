from typing import Mapping, TypedDict

import cv2 as cv

Region = tuple[int, int, int, int]


class LayoutConfig(TypedDict):
    name: str
    required_cameras: tuple[str, ...]
    reference_camera: str
    regions: dict[str, Region]

FOUR_CAMERA_KEYS = ("front", "back", "left_repeater", "right_repeater")
SIX_CAMERA_KEYS = (
    "front",
    "back",
    "left_repeater",
    "right_repeater",
    "left_pillar",
    "right_pillar",
)
ALL_CAMERA_KEYS = SIX_CAMERA_KEYS

# Prefer the main camera clips when probing video properties or extracting SEI.
CAMERA_REFERENCE_PREFERENCE = (
    "front",
    "back",
    "left_repeater",
    "right_repeater",
    "left_pillar",
    "right_pillar",
)

# Layout options
FOUR_CAMERA_DEFAULT: LayoutConfig = {
    "name": "default_four_camera",
    "required_cameras": FOUR_CAMERA_KEYS,
    "reference_camera": "front",
    "regions": {
        "front": (276, 0, 728, 546),
        "back": (524, 546, 232, 174),
        "left_repeater": (276, 546, 232, 174),
        "right_repeater": (772, 546, 232, 174),
    },
}

SIX_CAMERA_DEFAULT: LayoutConfig = {
    "name": "default_six_camera",
    "required_cameras": SIX_CAMERA_KEYS,
    "reference_camera": "front",
    "regions": {
        "left_pillar": (1, 0, 426, 360),
        "front": (427, 0, 426, 360),
        "right_pillar": (853, 0, 426, 360),
        "left_repeater": (1, 360, 426, 360),
        "back": (427, 360, 426, 360),
        "right_repeater": (853, 360, 426, 360),
    },
}


def _missing_cameras(files_info: Mapping[str, str | None], camera_keys: tuple[str, ...]) -> list[str]:
    return [camera_key for camera_key in camera_keys if not files_info.get(camera_key)]


def _has_any_pillar_camera(files_info: Mapping[str, str | None]) -> bool:
    return bool(files_info.get("left_pillar") or files_info.get("right_pillar"))


def select_default_layout(video_data: Mapping[str, Mapping[str, str | None]]) -> LayoutConfig:
    """Select the default layout for a complete four-camera or six-camera input set."""
    if not video_data:
        raise ValueError("No Tesla dashcam files found in the input directory.")

    six_camera_missing = {
        timestamp: _missing_cameras(files_info, SIX_CAMERA_KEYS)
        for timestamp, files_info in video_data.items()
    }
    four_camera_missing = {
        timestamp: _missing_cameras(files_info, FOUR_CAMERA_KEYS)
        for timestamp, files_info in video_data.items()
    }

    all_six_camera = all(not missing for missing in six_camera_missing.values())
    all_four_camera = all(not missing for missing in four_camera_missing.values())
    any_pillar_cameras = any(
        _has_any_pillar_camera(files_info) for files_info in video_data.values()
    )

    if all_six_camera:
        return SIX_CAMERA_DEFAULT

    if all_four_camera and not any_pillar_cameras:
        return FOUR_CAMERA_DEFAULT

    messages = ["Input contains mixed or incomplete TeslaCam camera sets."]

    incomplete_six = {
        timestamp: missing
        for timestamp, missing in six_camera_missing.items()
        if missing
    }
    if incomplete_six:
        messages.append("")
        messages.append("For the six-camera layout, these timestamps are missing:")
        for timestamp in sorted(incomplete_six):
            messages.append(f"- {timestamp}: {', '.join(incomplete_six[timestamp])}")

    incomplete_four = {
        timestamp: missing
        for timestamp, missing in four_camera_missing.items()
        if missing
    }
    if incomplete_four:
        messages.append("")
        messages.append("For the four-camera layout, these timestamps are missing:")
        for timestamp in sorted(incomplete_four):
            messages.append(f"- {timestamp}: {', '.join(incomplete_four[timestamp])}")

    raise ValueError("\n".join(messages))


def get_reference_camera(layout_config: LayoutConfig) -> str:
    """Return the layout's preferred reference camera."""
    reference_camera = layout_config.get("reference_camera")
    if isinstance(reference_camera, str):
        return reference_camera

    required_cameras = layout_config["required_cameras"]
    return required_cameras[0]


def place_frame(canvas, frame, region: Region) -> None:
    """Resize a frame and place it into the specified canvas region."""
    x, y, width, height = region
    resized_frame = cv.resize(frame, (width, height), interpolation=cv.INTER_LANCZOS4)
    canvas[y : y + height, x : x + width] = resized_frame


def render_layout(
    canvas,
    frames: dict[str, object],
    layout_config: LayoutConfig = FOUR_CAMERA_DEFAULT,
):
    """Render all frames defined by a layout config onto the canvas."""
    for camera_key, region in layout_config["regions"].items():
        frame = frames[camera_key]
        place_frame(canvas, frame, region)

    return canvas
