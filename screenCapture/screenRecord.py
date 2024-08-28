import keyboard
import mss
import cv2
import numpy as np
import time
import inputs
import json
import threading
from inputs import get_gamepad

class ScreenControllerRecorder:
    def __init__(self):
        self.recording = False
        self.frame_data = []
        self.current_frame = 0
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[0]  # Use the primary monitor
        self.controller_thread = None

    def detect_controller(self):
        try:
            controller = inputs.devices.gamepads[0]
            print(f"Controller detected: {controller}")
            return True
        except:
            print("No controller found")
            return False
        

    def start_recording(self):
        if not self.detect_controller():
            return
        self.recording = True
        self.frame_data = []
        self.current_frame = 0
        self.controller_thread = threading.Thread(target=self.capture_controller_input)
        self.controller_thread.start()
        print("Recording started. Press Alt+P again to stop.")

    def stop_recording(self):
        self.recording = False
        if self.controller_thread:
            self.controller_thread.join()
        self.save_data()
        print("Recording stopped. Data saved.")

    def capture_controller_input(self):
        while self.recording:
            events = get_gamepad()
            for event in events:
                if event.ev_type != 'Sync':
                    self.frame_data[self.current_frame-1]['inputs'].append(f'{event.code} {event.state}')

    def capture_frame(self):
        screenshot = np.array(self.sct.grab(self.monitor))
        gray = cv2.cvtColor(screenshot, cv2.COLOR_RGBA2GRAY)
        return gray

    def capture(self):
        img = self.capture_frame()
        inputs = 
    def save_data(self):
        with open('recording_data.json', 'w') as f:
            json.dump(self.frame_data, f)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (self.monitor['width'], self.monitor['height']), isColor=False)
        
        for frame in self.frame_data:
            out.write(cv2.imread(frame['image'], cv2.IMREAD_GRAYSCALE))
        
        out.release()

    def run(self):
        print("Press Alt+P to start/stop recording.")
        while True:
            if keyboard.is_pressed('alt+p'):
                if not self.recording:
                    self.start_recording()
                else:
                    self.stop_recording()
                time.sleep(0.5)  # Prevent multiple toggles
            
            if self.recording:
                frame = self.capture_frame()
                frame_filename = f'frame_{self.current_frame}.jpg'
                # cv2.imwrite(frame_filename, frame)
                self.frame_data.append({'frame': self.current_frame, 'image': frame_filename, 'inputs': []})
                self.current_frame += 1
            
            time.sleep(1/30)  # Capture at 30 FPS

if __name__ == "__main__":
    recorder = ScreenControllerRecorder()
    recorder.run()