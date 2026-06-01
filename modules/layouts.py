import cv2 as cv

Region = tuple[int, int, int, int]
LayoutConfig = dict[str, tuple[str, ...] | dict[str, Region]]

# Layout options
FOUR_CAMERA_DEFAULT = {
    "required_cameras": ("front", "back", "left_repeater", "right_repeater"),
    "regions": {
        "front": (276, 0, 728, 546),
        "back": (524, 546, 232, 174),
        "left_repeater": (276, 546, 232, 174),
        "right_repeater": (772, 546, 232, 174),
    },
}


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
