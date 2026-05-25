# Tesla Dashcam Telemetry Viewer

Processes Tesla dashcam MP4 files and accompanying CSV telemetry files to produce a combined multi-camera video with real-time telemetry overlay.

---

## Features
* **Multi-cam Sync**: Automatically stitches Front, Rear, and Side Repeater clips into a single frame.
* **Batch Processing**: Ability to add multiple sets of clips to be processed into one large video automatically in order of timestamp.
* **Telemetry Overlay**: Real-time visualization of:
	* Speed
	* Gear selection
	* Steering wheel angle
	* Turn signal state
	* Accelerator pedal position
	* Brake pedal state
	* Self driving state

## Layout

![Screenshot of example output layout](example.png)


## Prerequisites
1. **Python 3.10+**: Check version with `python --version` in a terminal window.
2. **MP4 codec support**: OpenCV needs MP4 encoding support to write the output video. Installing FFmpeg is recommended if MP4 output fails.

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/JeandreRoux/tesla-dashcam-telemetry-viewer.git
   cd tesla-dashcam-telemetry-viewer
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   **macOS/Linux**:
   ```bash
   source .venv/bin/activate
   ```

   **Windows**:
   ```powershell
   .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```

5. **Install FFmpeg (if needed)**:

   **Windows**:
   ```powershell
   winget install ffmpeg
   ```

   **macOS**:
   ```bash
   brew install ffmpeg
   ```

   **Linux (Ubuntu/Debian)**:
   ```bash
   sudo apt update && sudo apt install ffmpeg
   ```

## Input Files

The default layout requires all four Tesla dashcam camera files for each timestamp:

```text
YYYY-MM-DD_HH-MM-SS-front.mp4
YYYY-MM-DD_HH-MM-SS-back.mp4
YYYY-MM-DD_HH-MM-SS-left_repeater.mp4
YYYY-MM-DD_HH-MM-SS-right_repeater.mp4
```

Telemetry can be read from embedded SEI data when available. You can also provide a matching CSV manually:

```text
YYYY-MM-DD_HH-MM-SS.csv
```

## Usage

1. **Run the script**
```bash
python main.py --input /path/to/teslacam/clips --output /path/to/save/video
```

2. **Optional Arguments**
* `--no-overlay`: Disables the telemetry overlay and only produces the multi-camera stitched video.
* `--mph`: Sets the speed units to MPH. Default is KM/H.
* `--preview`: Enables render preview while videos are being processed. Will cause processing to take slightly longer.
* `--keep-csv`: Keeps generated `csv` data file, instead of just deleting it after use.

## Future Roadmap
* **Layout Presets**: Choose from focused, grid, and single-camera export layouts.
* **Camera Selection**: Include only the camera angles needed for each output.
* **Desktop App**: Provide a graphical interface for selecting clips, configuring exports, and previewing results.
* **G-Force Indicator**: Visualize acceleration, braking, and cornering forces from embedded accelerometer telemetry.
* **Location Info**: Show heading and GPS coordinates, with room for future mapping features.

## Troubleshooting
* Not all Tesla-generated dashcam clips contain SEI data. Only clips recorded on Tesla firmware 2025.44.25 or later and HW3 or above contain SEI data. If car is parked, SEI data may not be present.
If no SEI metadata is found, ensure your dashcam footage meets these requirements.
* If there is an error with data extraction and you meet the SEI data requirements above, you can extract the data manually via the [Tesla SEI Explorer](https://teslamotors.github.io/dashcam/sei_explorer.html) and place the `csv` file in the input directory before starting the program.
