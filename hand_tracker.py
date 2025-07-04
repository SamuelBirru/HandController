import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional
import time

class HandTracker:
    """
    Hand tracking and gesture recognition class using MediaPipe.
    
    This class handles:
    - Real-time hand landmark detection
    - Basic gesture recognition
    - Coordinate mapping for DJ controls
    """
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Configure hand detection
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,      # Process video frames
            max_num_hands=2,              # Track up to 2 hands
            min_detection_confidence=0.7, # Minimum confidence for detection
            min_tracking_confidence=0.5   # Minimum confidence for tracking
        )
        
        
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[List]]:
        """
        Process a video frame to detect hand landmarks.
        
        Args:
            frame: Input video frame (BGR format)
            
        Returns:
            Tuple of (processed_frame, landmarks_list)
        """
        # Convert BGR to RGB (MediaPipe expects RGB)
        # Process the frame
        # Convert back to BGR for OpenCV

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        processed_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        landmarks_list = []
        
        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Get hand type if available
                hand_type = "unknown"
                if hasattr(results, 'multi_handedness') and results.multi_handedness:
                    if i < len(results.multi_handedness):
                        handedness = results.multi_handedness[i]
                        if handedness.classification:
                            hand_type = handedness.classification[0].label.lower()
                
                # Draw hand landmarks on frame
                self.mp_drawing.draw_landmarks(
                    processed_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Extract landmark coordinates
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    # Convert to pixel coordinates
                    h, w, _ = frame.shape
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    landmarks.append((x, y))
                
                # Add hand type information to landmarks
                landmarks.append(hand_type) 
                landmarks_list.append(landmarks)
        
        return processed_frame, landmarks_list
    
    def detect_gestures(self, landmarks_list: List[List]) -> dict:
        """
        Detect basic gestures from hand landmarks.
        
        Args:
            landmarks_list: List of hand landmark coordinates with hand type
            
        Returns:
            Dictionary of detected gestures
        """
        gestures = {}
        
        for landmarks in landmarks_list:
            if len(landmarks) < 22:  # Should have 21 landmarks + hand type
                continue
                
            # Extract hand type and landmarks 
            hand_type = landmarks[-1] 
            landmark_coords = landmarks[:-1] 
            
            if hand_type in ["left", "right"]:
                # Swap left and right, MediaPipe detects them in reverse
                if hand_type == "left":
                    hand_type = "right"
                elif hand_type == "right":
                    hand_type = "left"
                hand_id = f"{hand_type}_hand"
                
                # Detect basic gestures
                gestures[hand_id] = {
                    'fist': self._is_fist(landmark_coords),
                    'open_hand': self._is_open_hand(landmark_coords),
                    'pinch': self._is_pinch(landmark_coords),
                    'hand_position': self._get_hand_position(landmark_coords)
                }
        
        return gestures
    
    def _is_fist(self, landmarks: List[Tuple[int, int]]) -> bool:
        """Detect if hand is in a fist position."""
        # Check fingers are curled (except thumb)
        finger_tips = [8, 12, 16, 20] 
        finger_mids = [6, 10, 14, 18]  
        
        curled_fingers = 0
        for tip, mid in zip(finger_tips, finger_mids):
            if landmarks[tip][1] > landmarks[mid][1]:  # Tip below middle joint
                curled_fingers += 1
        
        return curled_fingers >= 4  # At least 4 fingers curled
    
    def _is_open_hand(self, landmarks: List[Tuple[int, int]]) -> bool:
        """Detect if hand is open (fingers extended)."""
        finger_tips = [8, 12, 16, 20]
        finger_mids = [6, 10, 14, 18]
        
        extended_fingers = 0
        for tip, mid in zip(finger_tips, finger_mids):
            if landmarks[tip][1] < landmarks[mid][1]:  
                extended_fingers += 1
        
        return extended_fingers >= 4  # At least 4 fingers extended
    
    def _is_pinch(self, landmarks: List[Tuple[int, int]]) -> bool:
        """Detect pinch gesture (thumb and index finger touching)."""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        # Calculate distance between thumb and index finger
        distance = np.sqrt((thumb_tip[0] - index_tip[0])**2 + (thumb_tip[1] - index_tip[1])**2)
        
        return distance < 30  # Threshold for pinch detection
    
    def _get_hand_position(self, landmarks: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Get the center position of the hand (wrist)."""
        return landmarks[0]  # Wrist position
    
    def release(self):
        """Release resources."""
        self.hands.close() 