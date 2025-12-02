"""
Launch Arc Web Demo for Hackathon Submission
"""

import subprocess
import webbrowser
import time
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required = ['torch', 'transformers', 'open3d', 'fastapi', 'uvicorn']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements_hackathon.txt")
        return False
    
    return True

def main():
    print("=== Arc - Image to 3D Model Web Demo ===")
    print("Hackathon Submission - Real-time Wall Scanner")
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if models exist
    if not os.path.exists("wall_elements_specialized.pt"):
        print("Warning: Custom wall model not found")
        print("Using pre-trained YOLOv8 only")
    
    print("Starting web server...")
    print("Demo will open at: http://localhost:8000")
    print()
    print("Features available:")
    print("✓ Real-time camera scanning")
    print("✓ Wall element detection (outlets, switches, etc.)")
    print("✓ Depth estimation and 3D reconstruction")
    print("✓ Multi-wall stitching")
    print("✓ Texture application")
    print("✓ 3D model export")
    print()
    
    try:
        # Start web server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "web_app:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
        
        # Wait a moment then open browser
        time.sleep(3)
        webbrowser.open("http://localhost:8000")
        
        print("Web demo running! Press Ctrl+C to stop")
        process.wait()
        
    except KeyboardInterrupt:
        print("\nStopping demo...")
        process.terminate()
    except Exception as e:
        print(f"Error starting demo: {e}")

if __name__ == "__main__":
    main()