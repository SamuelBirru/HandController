import time
import pyautogui
from typing import Optional, Dict, Any

class MixxxController:
    """
    Keyboard automation controller for Mixxx DJ software.
    Sends keyboard shortcuts to control Mixxx directly.
    """
    
    def __init__(self):
        self.is_connected = True  # Always connected since we use keyboard
        self.current_volume_left = 0.5
        self.current_volume_right = 0.5
        self.is_playing = False
        self.simulation_mode = False
        
        # Mixxx default keyboard shortcuts
        self.keyboard_mappings = {
            # Playback controls
            'play_pause_left': 'd',           # Playback Deck 1
            'play_pause_right': 'l',          # Playback Deck 2
            'cue_left': 'f',                  # Cue Deck 1
            'cue_right': ';',                 # Cue Deck 2
            
            # Tempo controls
            'tempo_down_left': 'f1',          # Tempo Adjust Down Deck 1
            'tempo_up_left': 'f2',            # Tempo Adjust Up Deck 1
            'tempo_down_right': 'f5',         # Tempo Adjust Down Deck 2
            'tempo_up_right': 'f6',           # Tempo Adjust Up Deck 2
            
            # Loop controls
            'loop_4beat_left': 'q',           # Activate 4 Beat Loop Deck 1
            'loop_4beat_right': 'u',          # Activate 4 Beat Loop Deck 2
            'loop_halve_left': 'w',           # Halve Beat Loop Size Deck 1
            'loop_halve_right': 'i',          # Halve Beat Loop Size Deck 2
            'loop_double_left': 'e',          # Double Beat Loop Size Deck 1
            'loop_double_right': 'o',         # Double Beat Loop Size Deck 2
            
            # Hot cues
            'hotcue_1_left': 'z',             # Set Hot cue 1 Deck 1
            'hotcue_1_right': 'm',            # Set Hot cue 1 Deck 2
            'hotcue_2_left': 'x',             # Set Hot cue 2 Deck 1
            'hotcue_2_right': ',',            # Set Hot cue 2 Deck 2
            'hotcue_3_left': 'c',             # Set Hot cue 3 Deck 1
            'hotcue_3_right': '.',            # Set Hot cue 3 Deck 2
            'hotcue_4_left': 'v',             # Set Hot cue 4 Deck 1
            'hotcue_4_right': '/',            # Set Hot cue 4 Deck 2
            
            # Bass kill
            'bass_kill_left': 'b',            # Bass Kill Deck 1
            'bass_kill_right': 'n',           # Bass Kill Deck 2
            
            # Effects
            'effects_left': '5',              # Activate/Disable Effects Unit Deck 1
            'effects_right': '0',             # Activate/Disable Effects Unit Deck 2
        }
        
        # Configure pyautogui for safety
        pyautogui.FAILSAFE = True  # Move mouse to corner to stop
        pyautogui.PAUSE = 0.01      # Small delay between actions
        
        print("Keyboard controller ready")
        print("Make sure Mixxx is running and is the active window")
        print("The controller will send keyboard shortcuts to Mixxx")
        print("Using official Mixxx default keyboard shortcuts")
    
    def send_key(self, key: str, press_time: float = 0.1):
        """Send a keyboard key to Mixxx."""
        try:
            if self.simulation_mode:
                print(f"SIMULATION: Pressed key '{key}'")
            else:
                pyautogui.press(key)
                print(f"Sent key: {key}")
        except Exception as e:
            print(f"Failed to send key '{key}': {e}")
    
    
    def handle_play_pause(self, play_pause_triggered: bool, deck: str = 'left'):
        """Handle play/pause gesture for specified deck."""
        if play_pause_triggered:
            key = self.keyboard_mappings[f'play_pause_{deck}']
            self.send_key(key)
            self.is_playing = not self.is_playing
            status = "Playing" if self.is_playing else "Paused"
            print(f"Mixxx {deck} deck: {status}")
    
 
    
    def get_status(self) -> Dict[str, Any]:
        """Get current controller status."""
        return {
            'connected': self.is_connected,
            'controller_type': 'keyboard',
            'simulation_mode': self.simulation_mode,
            'playing': self.is_playing,
            'volume_left': self.current_volume_left,
            'volume_right': self.current_volume_right
        }
    
    def cleanup(self):
        """Clean up controller."""
        print(" Keyboard controller closed")

# Test function
if __name__ == "__main__":
    print(" Mixxx Keyboard Controller Test")
    print("=" * 50)
    
    controller = MixxxController()
    
    if controller.is_connected:
        print("\n Testing keyboard commands...")
        print("Make sure Mixxx is running and is the active window!")
        print("The test will send keyboard shortcuts to Mixxx")
        print("Using official Mixxx default keyboard shortcuts")
        
        # Wait a moment for user to switch to Mixxx
        time.sleep(3)
        
        # Test play/pause
        controller.handle_play_pause(True, 'left')
        time.sleep(1)
        controller.handle_play_pause(True, 'right')
        time.sleep(1)
        
        print("\n Keyboard test completed!")
        print(" Check Mixxx to see if the controls are working")
    else:
        print("\n Cannot test - controller not connected")
    
    controller.cleanup()