"""
Arc Detection Demo - Works without Open3D
Real-time object detection for hackathon submission
"""

import cv2
import numpy as np
from dual_detection_service import DualDetectionService
import time

def main():
    print("=== Arc Detection Demo ===")
    print("Real-time Wall Element Detection")
    print("Press 'q' to quit, 's' to save screenshot")
    
    # Initialize detector
    detector = DualDetectionService()
    
    # Start camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process every 3rd frame for performance
        if frame_count % 3 == 0:
            # Detect objects
            results = detector.detect_comprehensive(frame)
            
            # Draw detections
            display_frame = frame.copy()
            
            # Draw all detections
            for category, detections in results.items():
                if category in ['total_objects', 'all_detections'] or not isinstance(detections, list):
                    continue
                    
                color = (0, 255, 0) if 'wall' in category else (255, 0, 0)
                
                for det in detections:
                    x1, y1, x2, y2 = map(int, det['bbox'])
                    
                    # Draw box
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Draw label
                    label = f"{det['class']} ({det['confidence']:.2f})"
                    cv2.putText(display_frame, label, (x1, y1-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Show stats
            total_objects = len(results.get('all_detections', []))
            wall_elements = len(results.get('wall_elements', []))
            
            cv2.putText(display_frame, f"Objects: {total_objects}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(display_frame, f"Wall Elements: {wall_elements}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Arc Detection Demo', display_frame)
        
        frame_count += 1
        
        # Handle keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f"detection_demo_{int(time.time())}.jpg"
            cv2.imwrite(filename, display_frame)
            print(f"Screenshot saved: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("Demo completed!")

if __name__ == "__main__":
    main()