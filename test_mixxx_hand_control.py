import cv2
import numpy as np
import time
import sys

from hand_tracker import HandTracker
from mixxx_controller import MixxxController

def main():
    """
    Hand-controlled DJ controller for Mixxx.
    
    This will:
    1. Open your webcam for real-time hand tracking
    2. Send keyboard shortcuts to Mixxx
    3. Control Mixxx with hand gestures
    """
    
    print("Hand-Controlled Mixxx DJ Controller")
    print("=" * 60)
    
    # Initialize hand tracker
    tracker = HandTracker()
    
    # Initialize Mixxx controller
    print("Initializing Mixxx keyboard controller...")
    mixxx = MixxxController()
    
    # Check controller connection
    if mixxx.is_connected:
        print("Mixxx controller ready! Use hand gestures to control Mixxx.")
        print("Make sure Mixxx is running and is the active window.")
        print("The controller will send keyboard shortcuts to Mixxx.")
        print("Press 'q' to quit the hand controller.")
    else:
        print("Mixxx controller not connected.")
        print("Make sure Mixxx is running.")
        print("You can still test hand tracking without Mixxx control.")
    
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
    cv2.namedWindow('Hand-Controlled Mixxx', cv2.WINDOW_NORMAL)
    
    # Set initial window size
    cv2.resizeWindow('Hand-Controlled Mixxx', 800, 600)
    
    print("Webcam opened successfully!")
    print("Starting hand tracking...")
    print("Controls:")
    print("- Left hand: Left deck controls")
    print("- Right hand: Right deck controls")
    print("- Fist: Play/Pause")
    print("- Pinch: Crossfader control (hold pinch to move crossfader)")
    print("- Press 'q' to quit")
    print("=" * 60)
    
    frame_count = 0
    start_time = time.time()
    fps_counter = 0
    fps_start_time = time.time()
    fps = 0.0
    
    # Track previous states to detect triggers
    previous_play_pause_left = False
    previous_play_pause_right = False
    
    # Track pinch states for crossfader control
    left_pinch_active = False
    right_pinch_active = False
    
    # Add rate limiting for pinch gestures to reduce lag
    last_left_pinch_time = 0
    last_right_pinch_time = 0
    
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
        
        # Handle Mixxx controls
        if mixxx.is_connected:
            # Process each hand's gestures individually
            for hand_id, hand_gestures in gestures.items():
                if hand_id == "left_hand":
                    # Left hand controls left deck
                    # Handle play/pause for left deck
                    left_hand_fist = hand_gestures.get('fist', False)
                    current_play_pause_left = left_hand_fist
                    if current_play_pause_left and not previous_play_pause_left:
                        mixxx.handle_play_pause(True, 'left')
                    previous_play_pause_left = current_play_pause_left
                    
                    # Handle crossfader control for left deck
                    left_hand_pinch = hand_gestures.get('pinch', False)
                    current_time = time.time()
                    
                    if left_hand_pinch and not left_pinch_active:
                        # Pinch started - move crossfader left 
                        mixxx.send_key('g')
                        left_pinch_active = True
                        last_left_pinch_time = current_time
                    elif left_hand_pinch and left_pinch_active:
                        # Pinch held
                        if current_time - last_left_pinch_time > 0.2:  # Only every 200ms
                            mixxx.send_key('g')
                            last_left_pinch_time = current_time
                    elif not left_hand_pinch and left_pinch_active:
                        # Pinch ended
                        left_pinch_active = False
                    
                elif hand_id == "right_hand":
                    # Right hand controls right deck
                    # Handle play/pause for right deck
                    right_hand_fist = hand_gestures.get('fist', False)
                    current_play_pause_right = right_hand_fist
                    if current_play_pause_right and not previous_play_pause_right:
                        mixxx.handle_play_pause(True, 'right')
                    previous_play_pause_right = current_play_pause_right
                    
                    right_hand_pinch = hand_gestures.get('pinch', False)
                    current_time = time.time()
                    
                    if right_hand_pinch and not right_pinch_active:
                        # Pinch started 
                        mixxx.send_key('h')
                        right_pinch_active = True
                        last_right_pinch_time = current_time
                    elif right_hand_pinch and right_pinch_active:
                        # Pinch held
                        if current_time - last_right_pinch_time > 0.2:  # Only every 200ms
                            mixxx.send_key('h')
                            last_right_pinch_time = current_time
                    elif not right_hand_pinch and right_pinch_active:
                        # Pinch ended
                        right_pinch_active = False
        
        # Display information on frame
        y_offset = 30
        cv2.putText(processed_frame, "Hand-Controlled Mixxx", (10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show performance metrics
        y_offset += 30
        cv2.putText(processed_frame, f"FPS: {fps:.1f} | Process Time: {process_time:.1f}ms", 
                   (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Show Mixxx status
        y_offset += 30
        if mixxx.is_connected:
            status = mixxx.get_status()
            cv2.putText(processed_frame, f"Mixxx: Connected | Playing: {status['playing']}", 
                       (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        else:
            cv2.putText(processed_frame, "Mixxx: Not Connected", 
                       (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
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
                    elif gesture == 'hand_position':
                        cv2.putText(processed_frame, f"  {gesture}: {value}", (20, y_offset), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
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
        
        # Show volume controls
       
        
        # Show pinch states
        left_pinch_color = (0, 255, 0) if left_pinch_active else (128, 128, 128)
        right_pinch_color = (0, 255, 0) if right_pinch_active else (128, 128, 128)
        
        cv2.putText(processed_frame, f"Left Pinch: {'ACTIVE' if left_pinch_active else 'OFF'}", 
                   (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, left_pinch_color, 1)
        y_offset += 15
        
        cv2.putText(processed_frame, f"Right Pinch: {'ACTIVE' if right_pinch_active else 'OFF'}", 
                   (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, right_pinch_color, 1)
        y_offset += 15
        
        # Show instructions
        cv2.putText(processed_frame, "Press 'q' to quit, 'f' for fullscreen, 'r' to reset", 
                   (10, processed_frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
        
        # Display the frame
        cv2.imshow('Hand-Controlled Mixxx', processed_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('f'):
            # Toggle fullscreen
            cv2.setWindowProperty('Hand-Controlled Mixxx', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        elif key == ord('r'):
            # Reset window size
            cv2.resizeWindow('Hand-Controlled Mixxx', 800, 600)
    
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
    mixxx.cleanup()
    print("Test completed!")

if __name__ == "__main__":
    main() 