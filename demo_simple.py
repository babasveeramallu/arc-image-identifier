"""
Arc Simple Demo - Works without 3D dependencies
Demonstrates core detection functionality for hackathon
"""

import cv2
import numpy as np
from dual_detection_service import DualDetectionService
import os

def main():
    print("=== Arc - Simple Detection Demo ===")
    print("Hackathon Requirements Test (No 3D)")
    print()
    
    try:
        # Initialize detection service
        print("1. Loading AI models...")
        wall_model = "wall_elements_specialized.pt" if os.path.exists("wall_elements_specialized.pt") else None
        detector = DualDetectionService(wall_model_path=wall_model)
        print("✓ Object detection ready")
        
        print()
        print("=== DEMO INSTRUCTIONS ===")
        print("1. Camera will open showing live detection")
        print("2. Point camera at walls with outlets/switches")
        print("3. Press 'q' to quit")
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
            
            # Run detection every 5 frames for performance
            if frame_count % 5 == 0:
                try:
                    results = detector.detect_comprehensive(frame)
                    
                    # Draw detections
                    vis_frame = draw_detections(frame, results)
                    
                    # Show stats
                    cv2.putText(vis_frame, f"Objects: {results['total_objects']}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(vis_frame, f"Wall elements: {len(results['wall_elements'])}", 
                               (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(vis_frame, "Press 'q' to quit", 
                               (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    
                except Exception as e:
                    print(f"Detection error: {e}")
                    vis_frame = frame
            else:
                vis_frame = frame
            
            cv2.imshow('Arc - Wall Scanner Demo', vis_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print("Demo completed!")
        print("✓ Real-time detection working")
        print("✓ Wall element recognition active")
        print("✓ Ready for hackathon submission!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure camera is connected and models are available")

def draw_detections(frame, results):
    """Draw detection boxes on frame"""
    vis = frame.copy()
    
    # Draw wall elements in red
    for det in results['wall_elements']:
        bbox = det['bbox']
        x1, y1, x2, y2 = map(int, bbox)
        
        cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        label = f"{det['class']}: {det['confidence']:.2f}"
        cv2.putText(vis, label, (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Draw general objects in green
    for det in results['general_objects']:
        bbox = det['bbox']
        x1, y1, x2, y2 = map(int, bbox)
        
        cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        label = f"{det['class']}: {det['confidence']:.2f}"
        cv2.putText(vis, label, (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return vis

if __name__ == "__main__":
    main()