import cv2 as cv
import numpy as np
import sys
import pandas as pd
from pathlib import Path

# Import modules
from modules import config
from modules import overlay_renderer
from modules import data_handler
from modules import layouts

CANVAS_WIDTH = config.CANVAS_WIDTH
CANVAS_HEIGHT = config.CANVAS_HEIGHT


def get_video_fps(
    input_path: Path,
    video_data: dict[str, dict[str, str | None]],
) -> tuple[str, float]:
    """Return the first clip timestamp and FPS from a reference video."""
    first_timestamp = sorted(video_data.keys())[0]
    reference_video = data_handler.get_available_video_file(video_data[first_timestamp])
    if reference_video is None:
        sys.exit("FATAL: No reference video file found.")

    reference_video_path = input_path / reference_video
    cap_temp = cv.VideoCapture(reference_video_path)
    if not cap_temp.isOpened():
        sys.exit(
            f"FATAL: Could not open {reference_video_path} to get video properties."
        )

    fps = cap_temp.get(cv.CAP_PROP_FPS)
    cap_temp.release()

    return first_timestamp, fps


def create_video_writer(
    output_path: Path,
    output_filename: str,
    fps: float,
) -> tuple[cv.VideoWriter, Path]:
    """Create and validate the MP4 VideoWriter for the final output."""
    if output_path.exists() and not output_path.is_dir():
        sys.exit(f"Output path '{output_path}' exists but is not a directory.")

    output_path.mkdir(parents=True, exist_ok=True)
    output_filepath = output_path / f"{output_filename}.mp4"

    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    out = cv.VideoWriter(
        output_filepath,
        fourcc,
        fps,
        (CANVAS_WIDTH, CANVAS_HEIGHT),
        isColor=True,
    )

    if not out.isOpened():
        sys.exit(f"FATAL: Could not create output video file: {output_filepath}")

    return out, output_filepath


def open_captures(
    input_path: Path,
    files_info: dict[str, str | None],
    layout: dict[str, tuple[str, ...] | dict[str, layouts.Region]],
) -> dict[str, cv.VideoCapture]:
    """Open VideoCapture objects for the required cameras in a clip group."""
    required_cameras = layout["required_cameras"]

    captures = {}

    for camera_key in required_cameras:
        video_file = files_info.get(camera_key)
        if video_file:
            captures[camera_key] = cv.VideoCapture(input_path / video_file)

    return captures


def process_video(
    captures: dict,
    telemetry_df: pd.DataFrame | None,
    out: cv.VideoWriter,
    input_path: Path,
    video_data: dict[str, dict[str, str | None]],
    settings,
) -> None:
    """Render frames from the selected layout and write them to the output video."""

    for camera_key, capture in captures.items():
        if not capture.isOpened():
            print(f"Cannot open {camera_key} video file")
            return

    frame_index = 0

    reference_camera = settings.layout["required_cameras"][0]

    while True:
        frames = {}

        for camera_key in settings.layout["required_cameras"]:
            ret, frame = captures[camera_key].read()
            if not ret:
                return
            frames[camera_key] = frame

        # Get current frame index
        curr_frame = int(captures[reference_camera].get(cv.CAP_PROP_POS_FRAMES))

        # Create canvas
        canvas = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 3), dtype=np.uint8)

        canvas = layouts.render_layout(canvas, frames, settings.layout)

        # Write text overlay
        if not settings.no_overlay and telemetry_df is not None:
            canvas = overlay_renderer.draw_overlay(
                canvas, curr_frame, telemetry_df, frame_index, settings
            )

        frame_index += 1

        if settings.preview:
            cv.imshow("Preview", canvas)  # Shows the video in a window
            if cv.waitKey(1) & 0xFF == ord("q"):  # Lets you quit by pressing 'q'
                for capture in captures.values():
                    capture.release()
                out.release()
                cv.destroyAllWindows()
                data_handler.remove_generated_csv(input_path, video_data, settings)
                sys.exit("User stopped program.")

        # write frame
        out.write(canvas)


def release_captures(captures: dict[str, cv.VideoCapture]) -> None:
    """Release all open VideoCapture objects."""
    for capture in captures.values():
        capture.release()
