"""
Arc Simple Demo - Stable detection without blinking
Demonstrates core detection functionality for hackathon
"""

import cv2
import numpy as np
from dual_detection_service import DualDetectionService
import os
from collections import deque

class DetectionStabilizer:
    def __init__(self, history_size=5, confidence_threshold=0.4):
        self.history_size = history_size
        self.confidence_threshold = confidence_threshold
        self.detection_history = deque(maxlen=history_size)
        self.stable_detections = []
    
    def add_detections(self, detections):
        # Filter by confidence
        filtered_dets = [det for det in detections if det['confidence'] >= self.confidence_threshold]
        self.detection_history.append(filtered_dets)
        
        # Get stable detections
        if len(self.detection_history) >= 2:
            self.stable_detections = self._get_stable_detections()
        return self.stable_detections
    
    def _get_stable_detections(self):
        stable = []
        recent_frames = list(self.detection_history)[-3:]
        
        for frame_dets in recent_frames:
            for det in frame_dets:
                if self._is_detection_stable(det, recent_frames) and not self._already_added(det, stable):
                    stable.append(det)
        return stable
    
    def _is_detection_stable(self, detection, frames):
        similar_count = 0
        bbox = detection['bbox']
        class_name = detection['class']
        
        for frame_dets in frames:
            for det in frame_dets:
                if det['class'] == class_name and self._boxes_overlap(bbox, det['bbox']) > 0.5:
                    similar_count += 1
                    break
        return similar_count >= 1  # More sensitive - show after 1 stable frame
    
    def _boxes_overlap(self, box1, box2):
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2
        
        x_min = max(x1_min, x2_min)
        y_min = max(y1_min, y2_min)
        x_max = min(x1_max, x2_max)
        y_max = min(y1_max, y2_max)
        
        if x_max <= x_min or y_max <= y_min:
            return 0.0
        
        intersection = (x_max - x_min) * (y_max - y_min)
        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0
    
    def _already_added(self, detection, stable_list):
        for stable_det in stable_list:
            if (stable_det['class'] == detection['class'] and
                self._boxes_overlap(detection['bbox'], stable_det['bbox']) > 0.7):
                return True
        return False

def main():
    print("=== Arc - Simple Detection Demo ===")
    print("Stable detection without blinking")
    print()
    
    try:
        # Initialize detection service
        print("1. Loading AI models...")
        wall_model = "wall_elements_specialized.pt" if os.path.exists("wall_elements_specialized.pt") else None
        detector = DualDetectionService(wall_model_path=wall_model)
        
        # Initialize stabilizer
        stabilizer = DetectionStabilizer()
        
        print("Object detection ready")
        
        print()
        print("=== DEMO INSTRUCTIONS ===")
        print("1. Camera will open showing stable detection")
        print("2. Point camera at walls with outlets/switches")
        print("3. Press 'q' to quit, 's' to save screenshot")
        print()
        print("Starting camera...")
        
        # Start camera
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            try:
                # Lower confidence for more detections
                results = detector.detect_comprehensive(frame, confidence_threshold=0.3)
                
                # Combine all detections
                all_detections = results['wall_elements'] + results['general_objects']
                
                # Stabilize detections
                stable_detections = stabilizer.add_detections(all_detections)
                
                # Draw stable detections
                vis_frame = draw_detections(frame, stable_detections)
                
                # Show stats
                cv2.putText(vis_frame, f"Stable Objects: {len(stable_detections)}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(vis_frame, "Press 'q' to quit, 's' to save", 
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
            except Exception as e:
                print(f"Detection error: {e}")
                vis_frame = frame
            
            cv2.imshow('Arc - Wall Scanner Demo', vis_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                cv2.imwrite(f'detection_screenshot_{frame_count}.jpg', vis_frame)
                print(f"Screenshot saved: detection_screenshot_{frame_count}.jpg")
        
        cap.release()
        cv2.destroyAllWindows()
        
        print("Demo completed!")
        print("Stable detection working")
        print("No more blinking boxes")
        print("Ready for hackathon submission!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure camera is connected and models are available")

def draw_detections(frame, detections):
    """Draw stable detection boxes"""
    vis = frame.copy()
    
    for det in detections:
        bbox = det['bbox']
        x1, y1, x2, y2 = map(int, bbox)
        
        # Color based on type
        if det.get('type') == 'wall_element':
            color = (0, 0, 255)  # Red for wall elements
            thickness = 3
        else:
            color = (0, 255, 0)  # Green for general objects
            thickness = 2
        
        # Draw thick, stable box
        cv2.rectangle(vis, (x1, y1), (x2, y2), color, thickness)
        
        # Draw filled background for text
        label = f"{det['class']}: {det['confidence']:.2f}"
        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(vis, (x1, y1-text_height-10), (x1+text_width, y1), color, -1)
        
        # Draw text
        cv2.putText(vis, label, (x1, y1-5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return vis

if __name__ == "__main__":
    main()