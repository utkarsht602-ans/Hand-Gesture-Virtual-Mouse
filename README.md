# AI Hand Gesture Virtual Mouse

A Python project that lets you control your computer's mouse using hand gestures captured by your webcam. It uses MediaPipe to detect hand landmarks and PyAutoGUI to move the cursor, click, and scroll.

## Features

- **Cursor movement:** Move your index fingertip inside the highlighted active area to move the mouse cursor.
- **Left click:** Bring your thumb and index fingertip close together (pinch gesture).
- **Right click:** Bring your thumb and middle fingertip close together.
- **Scrolling:** Raise your index and middle fingers while folding the ring and little fingers, then move your hand vertically.
- **Live hand tracking:** Displays detected hand landmarks and gesture status in the camera window.
- **Quit:** Press `Q` while the camera window is active.

## Requirements

- Python 3.9 or a compatible version supported by your installed dependencies
- A working webcam
- Camera permission enabled for Python / your terminal or IDE

## Libraries Used

- `opencv-python` (`cv2`) — webcam access, image processing, and display
- `mediapipe` — hand landmark detection and tracking
- `pyautogui` — mouse movement, clicking, and scrolling
- `numpy` — coordinate mapping and scroll calculations
- Python standard libraries: `time` and `math`

## Installation

1. **Download or clone this project** and open its folder in a terminal.
2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv .venv
   ```

3. **Activate the environment:**

   Windows PowerShell:
   ```powershell
   .venv\\Scripts\\Activate.ps1
   ```

   Windows Command Prompt:
   ```bat
   .venv\\Scripts\\activate.bat
   ```

   macOS / Linux:
   ```bash
   source .venv/bin/activate
   ```

4. **Install the required libraries:**

   ```bash
   python -m pip install opencv-python mediapipe pyautogui numpy
   ```

## How to Run

Save the Python script as `project.py` (or use your existing filename), then run:

```bash
python project.py
```

A window named **AI Hand Gesture Virtual Mouse** should open and show the webcam feed. Keep your hand visible to the camera and use the gestures listed below.

## Gesture Controls

| Action | Gesture |
|---|---|
| Move cursor | Move your index fingertip inside the green rectangle |
| Left click | Pinch thumb and index fingertip together |
| Right click | Pinch thumb and middle fingertip together |
| Scroll | Raise index and middle fingers, fold ring and little fingers, then move your hand up or down |
| Exit | Focus the camera window and press `Q` |

## Configuration

The following constants near the top of `project.py` can be adjusted to tune the controls:

| Setting | Default | Purpose |
|---|---:|---|
| `CAMERA_INDEX` | `0` | Webcam device index |
| `FRAME_REDUCTION` | `100` | Defines the inset active area in the camera frame |
| `SMOOTHING` | `5` | Higher values smooth cursor movement but make it slower |
| `CLICK_DISTANCE` | `35` | Distance threshold for pinch clicks, in camera pixels |
| `CLICK_COOLDOWN` | `0.45` | Minimum time between repeated clicks, in seconds |
| `SCROLL_SENSITIVITY` | `3` | Limits scroll step size |
| `SHOW_LANDMARKS` | `True` | Shows MediaPipe hand landmarks |

Adjust these values if the cursor feels too sensitive or gestures trigger too often. The best values can vary with camera resolution, lighting, and hand position.

## Troubleshooting

- **Camera will not open:** Close other apps using the webcam, check camera permissions, and try another `CAMERA_INDEX` if you have multiple cameras.
- **No hand detected:** Improve lighting, keep your hand fully in frame, and avoid covering your fingertips.
- **Cursor is too shaky:** Increase `SMOOTHING` slightly. Higher values make movement smoother but slower.
- **Clicks trigger too often or not often enough:** Adjust `CLICK_DISTANCE` and `CLICK_COOLDOWN`.
- **Installation fails:** Check your Python version and install packages in a virtual environment. MediaPipe support can vary by Python version and operating system.
- **Scroll does not work reliably:** Hold only the index and middle fingers up, fold the ring and little fingers, and move your hand vertically.

## Safety Notes

- This program controls the real mouse and can click on items on your computer. Close sensitive windows before testing.
- PyAutoGUI's fail-safe is enabled. Moving the mouse to the top-left corner of the screen can trigger its fail-safe.
- Use this project in a safe workspace and stop it by pressing `Q` in the camera window.

## How It Works

1. OpenCV reads frames from the webcam and mirrors the preview.
2. MediaPipe detects one hand and returns hand landmark coordinates.
3. The index fingertip coordinates are mapped from the highlighted camera area to the screen dimensions.
4. Cursor smoothing reduces sudden jumps.
5. Distances between fingertips identify left- and right-click pinches.
6. The index/middle-finger pose and vertical hand movement control scrolling.
7. OpenCV displays the camera feed, hand landmarks, and current gesture status.

## Limitations

- The script tracks one hand at a time.
- Gesture thresholds may need tuning for different users, webcams, and lighting.
- Cursor movement only occurs while the index fingertip is inside the highlighted active area.
- The script uses basic landmark-position rules, so unusual hand angles may affect gesture recognition.

## Future Improvements

- Add a settings panel to adjust thresholds without editing code.
- Add additional gestures such as drag-and-drop.
- Improve gesture detection using more robust pose checks.
- Add support for selecting a different camera from the interface.

## License

No license is specified for this project. Add a license file if you intend to share or distribute the code publicly.
