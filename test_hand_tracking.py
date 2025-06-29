import cv2
import numpy as np
import time
import sys
from hand_tracker import HandTracker

def test_hand_tracker_initialization():
    """Test if HandTracker initializes correctly."""
    try:
        tracker = HandTracker()
        print(" HandTracker initialization: PASSED")
        tracker.release()
        return True
    except Exception as e:
        print(f" HandTracker initialization: FAILED - {e}")
        return False

def test_gesture_detection():
    """Test gesture detection with mock landmarks."""
    try:
        tracker = HandTracker()
        
        # Create mock landmarks for different gestures
        # Mock fist landmarks (fingers curled)
        fist_landmarks = [(100, 100)] * 21  # Simplified mock data
        fist_landmarks[8] = (100, 150)   # Index tip below middle
        fist_landmarks[12] = (100, 160)  # Middle tip below middle
        fist_landmarks[16] = (100, 170)  # Ring tip below middle
        fist_landmarks[20] = (100, 180)  # Pinky tip below middle
        
        # Mock open hand landmarks (fingers extended)
        open_landmarks = [(100, 100)] * 21
        open_landmarks[8] = (100, 50)    # Index tip above middle
        open_landmarks[12] = (100, 40)   # Middle tip above middle
        open_landmarks[16] = (100, 30)   # Ring tip above middle
        open_landmarks[20] = (100, 20)   # Pinky tip above middle
        
        # Test gesture detection
        gestures = tracker.detect_gestures([fist_landmarks, open_landmarks])
        
        print("Gesture detection: PASSED")
        tracker.release()
        return True
    except Exception as e:
        print(f"Gesture detection: FAILED - {e}")
        return False

def test_dj_controls():
    """Test DJ control mapping."""
    try:
        tracker = HandTracker()
        
        # Test empty gestures
        empty_controls = tracker.get_dj_controls({})
        assert 'volume_left' in empty_controls
        assert 'volume_right' in empty_controls
        
        # Test with mock gestures
        mock_gestures = {
            'hand_0': {
                'open_hand': True,
                'pinch': False,
                'hand_position': (100, 200)
            }
        }
        
        controls = tracker.get_dj_controls(mock_gestures)
        print(" DJ controls mapping: PASSED")
        tracker.release()
        return True
    except Exception as e:
        print(f" DJ controls mapping: FAILED - {e}")
        return False

def run_unit_tests():
    """Run all unit tests."""
    print("Running Unit Tests...")
    print("=" * 50)
    
    tests = [
        test_hand_tracker_initialization,
        test_gesture_detection,
        test_dj_controls
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    return passed == total

def main():
    """
    Enhanced test script to demonstrate hand tracking.
    
    This will:
    1. Run unit tests
    2. Open your webcam for real-time testing
    3. Show detected gestures and DJ controls
    4. Provide performance metrics
    """
    
    print("Hand-Controlled DJ Controller - Enhanced Test Mode")
    print("=" * 60)
    
    # Run unit tests first
    if not run_unit_tests():
        print("Some unit tests failed. Continuing with live test..")
    
    print("\nStarting Live Camera Test..")
    print("Controls:")
    print("- Open hand: Volume control")
    print("- Pinch gesture: Cue point")
    print("- Fist: Play/Pause")
    print("- Pointing: Scratch control")
    print("- Press 'q' to quit, 's' to save screenshot")
    print("=" * 60)
    
    # Initialize hand tracker
    tracker = HandTracker()
    
    
  
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam!")
        print("Make sure your webcam is connected and not in use by another application.")
        return
    
    # Set webcam properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Create a resizable window
    cv2.namedWindow('Hand-Controlled DJ Controller', cv2.WINDOW_NORMAL)
    
    # Set initial window size
    cv2.resizeWindow('Hand-Controlled DJ Controller', 800, 600)
    
    print("Webcam opened successfully!")
    print("Starting hand tracking...")
    print("Press 'f' for fullscreen, 'r' to reset window size")
    
    frame_count = 0
    start_time = time.time()
    fps_counter = 0
    fps_start_time = time.time()
    fps = 0.0  # Initialize fps variable
    
    # Track previous play/pause state to detect triggers
    previous_play_pause = False
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame!")
            break
        
        frame_count += 1
        fps_counter += 1
        
        # Calculate FPS every second
        if time.time() - fps_start_time >= 1.0:
            fps = fps_counter / (time.time() - fps_start_time)
            fps_counter = 0
            fps_start_time = time.time()
        
        # Process frame for hand tracking
        process_start = time.time()
        processed_frame, landmarks_list = tracker.process_frame(frame)
        process_time = (time.time() - process_start) * 1000  # Convert to ms
        
        # Detect gestures
        gestures = tracker.detect_gestures(landmarks_list if landmarks_list else [])
        
        # Debug: Print detected hands
        if gestures:
            print(f"Detected hands: {list(gestures.keys())}")
        
        # Get DJ controls
        dj_controls = tracker.get_dj_controls(gestures)
       
        # Display information on frame
        y_offset = 30
        cv2.putText(processed_frame, "Hand-Controlled DJ Controller", (10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show performance metrics
        y_offset += 30
        cv2.putText(processed_frame, f"FPS: {fps:.1f} | Process Time: {process_time:.1f}ms", 
                   (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Show detected gestures
        y_offset += 30
        if gestures:
            cv2.putText(processed_frame, "Detected Gestures:", (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_offset += 25
            
            for hand_id, hand_gestures in gestures.items():
                cv2.putText(processed_frame, f"{hand_id}:", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_offset += 20
                
                for gesture, value in hand_gestures.items():
                    if isinstance(value, bool):
                        color = (0, 255, 0) if value else (128, 128, 128)
                        status = "ON" if value else "OFF"
                        cv2.putText(processed_frame, f"  {gesture}: {status}", (20, y_offset), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                        y_offset += 15
        else:
            cv2.putText(processed_frame, "No hands detected", (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
            y_offset += 30
        
        # Show DJ controls
        y_offset += 20
        cv2.putText(processed_frame, "DJ Controls:", (10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        y_offset += 25
        
        
        
        # Show instructions
        cv2.putText(processed_frame, "Press 'q' to quit, 's' to save screenshot, 'f' for fullscreen, 'r' to reset", 
                   (10, processed_frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
        
        # Display the frame
        cv2.imshow('Hand-Controlled DJ Controller', processed_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save screenshot
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"dj_controller_screenshot_{timestamp}.png"
            cv2.imwrite(filename, processed_frame)
            print(f"Screenshot saved: {filename}")
        elif key == ord('f'):
            # Toggle fullscreen
            cv2.setWindowProperty('Hand-Controlled DJ Controller', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        elif key == ord('r'):
            # Reset window size
            cv2.resizeWindow('Hand-Controlled DJ Controller', 800, 600)
    
    # Calculate and display final statistics
    total_time = time.time() - start_time
    avg_fps = frame_count / total_time if total_time > 0 else 0
    
    print("\n Test Statistics:")
    print(f"   Total frames processed: {frame_count}")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Average FPS: {avg_fps:.1f}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    tracker.release()
    print("Test completed!")

if __name__ == "__main__":
    main() 