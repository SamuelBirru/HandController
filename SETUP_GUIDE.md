# Hand DJ Controller Setup Guide

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download and Start Mixxx** 
    https://mixxx.org/download/

3. **Run the hand controller**:
   ```bash
   python test_mix;xx_hand_control.py
   ```

4. **Make Mixxx the active window**

5. **Use hand gestures** to control Mixxx!

## How It Works

The hand controller automatically sends keyboard shortcuts to Mixxx. **No manual mapping required!** The controller uses Mixxx's official default keyboard shortcuts:

### Official Mixxx Default Keyboard Shortcuts Used:

| Control | Left Deck | Right Deck |
|---------|-----------|------------|
| Play/Pause | `D` | `L` |
| Cue | `F` | `;` |
| Crossfader Left | `G` | - |
| Crossfader Right | `H` | - |
| Hot Cue 1 | `Z` | `M` |
| Hot Cue 2 | `X` | `,` |
| Hot Cue 3 | `C` | `.` |
| Hot Cue 4 | `V` | `/` |
| 4-Beat Loop | `Q` | `U` |
| Halve Loop | `W` | `I` |
| Double Loop | `E` | `O` |
| Bass Kill | `B` | `N` |
| Effects | `5` | `0` |
| Tempo Up | `F2` | `F6` |
| Tempo Down | `F1` | `F5` |

## Hand Gestures

- **Left hand**: Controls left deck
- **Right hand**: Controls right deck
- **Pinch gesture**: Controlls crossfader for each deck
- **Fist**: Play/Pause

## Troubleshooting

### If keyboard shortcuts don't work:

1. **Check Mixxx keyboard preferences**:
   - Open Mixxx
   - Go to `Preferences` > `Keyboard`
   - Make sure the shortcuts listed above are enabled
   - If they're different, you can either:
     - Change Mixxx shortcuts to match the defaults above, OR
     - Update the shortcuts in `mixxx_controller.py`

2. **Verify Mixxx is the active window**:
   - Click on Mixxx to make it the active window
   - The hand controller sends keys to whatever window is active

3. **Test keyboard shortcuts manually**:
   - Click on Mixxx
   - Press `D` - left deck should play/pause
   - Press `L` - right deck should play/pause
   - If these don't work, check Mixxx keyboard preferences

### If hand tracking doesn't work:

1. **Check webcam**:
   - Make sure your webcam is not being used by another application
   - Try closing other video applications

2. **Check lighting**:
   - Ensure good lighting for hand detection
   - Avoid bright backlighting

3. **Check hand position**:
   - Keep hands clearly visible to the camera
   - Avoid rapid movements

## Testing the Controller

You can test the keyboard controller separately:

```bash
python mixxx_controller.py
```

This will send test commands to Mixxx to verify the shortcuts work.

## Safety Features

- **Failsafe**: Move your mouse to any corner of the screen to stop the controller
- **Pause**: Press `q` in the hand controller window to quit

## Customization

If you want to use different keyboard shortcuts:

1. Open `mixxx_controller.py`
2. Find the `keyboard_mappings` dictionary
3. Change the key values to match your preferred shortcuts
4. Make sure to update Mixxx preferences to match

## Requirements

- Python 3.8.12, newest version of python will not work
- Webcam
- Mixxx DJ software
- Good lighting for hand tracking

## Have Fun! 