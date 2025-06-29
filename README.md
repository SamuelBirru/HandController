# Hand-Controlled Virtual DJ Controller

A computer vision project that allows you to control a virtual DJ controller using hand gestures captured through your webcam.

## Features
- Real-time hand tracking using MediaPipe
- Gesture recognition for DJ controls
- Visual feedback interface with real-time gesture display
- Keyboard automation for Mixxx DJ software integration
- Multiple gesture mappings for different DJ functions

## Setup Instructions

1. **Install Python 3.12, Python 3.13 is not compatible with mediapipe** 
2. **Install dependencies:**
   ```bash
   pip install -r dependencies.txt
   ```
3. **Run the application:**
   ```bash
   python test_mixxx_hand_control.py
   ```
   Or for hand tracking only:
   ```bash
   python test_hand_tracking.py
   ```

## How It Works

 Hand Tracking
- Uses MediaPipe to detect 21 hand landmarks in real-time
- Tracks hand position, finger positions, and gestures
- Processes video feed from your webcam

 Gesture Mappings
- **Crossfader:** Pinching index with thumb on left and right hand moves crossfader left/right respectively
- **Play/Pause:** Open/closed fist
- **More on the Way!**
