def get_text_x(text, font, draw, shape_center):
    """Return the X coordinate to horizontally center text at a given center."""
    # bbox = (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font)
    text_width = bbox[2] - bbox[0]
    return shape_center - (text_width // 2) - bbox[0]


def get_text_y(text, font, draw, shape_center):
    """Return the Y coordinate to vertically center text at a given center."""
    # bbox = (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font)
    text_height = bbox[3] - bbox[1]
    return shape_center - (text_height // 2) - bbox[1]


def get_gear_state(current_frame_data):
    """Map telemetry 'gear_state' to a single-letter display."""
    match current_frame_data["gear_state"]:
        case "GEAR_PARK":
            return "P"
        case "GEAR_DRIVE":
            return "D"
        case "GEAR_REVERSE":
            return "R"
        case "GEAR_NEUTRAL":
            return "N"
        case _:
            return ""


def get_autopilot_state(current_frame_data):
    """Map telemetry 'autopilot_state' to a user-friendly string."""
    match current_frame_data["autopilot_state"]:
        case "TACC":
            return "Cruise"
        case "AUTOSTEER":
            return "Autopilot"
        case "SELF_DRIVING":
            return "Self Driving"
        case _:
            return ""


def get_speed(current_frame_data, args):
    """Convert and format vehicle speed according to CLI unit preference."""
    speed_mps = float(current_frame_data["vehicle_speed_mps"])
    if args.mph:
        speed = speed_mps * 2.237
        speed_unit = "MPH"
    else:
        speed = speed_mps * 3.6
        speed_unit = "KM/H"

    if speed < 0:
        speed = f"{speed*speed:.0f}"
    else:
        speed = f"{speed:.0f}"

    return speed, speed_unit