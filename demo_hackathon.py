"""
Arc Hackathon Demo - Quick test of the 3D scanning system
"""

import cv2
import numpy as np
from dual_detection_service import DualDetectionService
from arc_scanner import ArcRealTimeScanner

def main():
    print("=== Arc - Image to 3D Model Demo ===")
    print("Hackathon Requirements Test")
    print()
    
    try:
        # Initialize detection service
        print("1. Loading AI models...")
        import os
        wall_model = "wall_elements_specialized.pt" if os.path.exists("wall_elements_specialized.pt") else None
        detector = DualDetectionService(wall_model_path=wall_model)
        print("✓ Object detection ready")
        
        # Initialize scanner
        print("2. Initializing 3D scanner...")
        scanner = ArcRealTimeScanner(detector, camera_index=0)
        print("✓ Real-time scanner ready")
        
        print()
        print("=== DEMO INSTRUCTIONS ===")
        print("1. Point camera at a wall")
        print("2. Press 'S' to capture wall scans")
        print("3. Scan multiple walls (minimum 2)")
        print("4. Press 'R' to generate room model")
        print("5. Press 'Q' to quit")
        print()
        print("Starting camera...")
        
        # Start real-time scanning
        scanner.start_scanning()
        
        print("Demo completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure camera is connected and models are available")

if __name__ == "__main__":
    main()