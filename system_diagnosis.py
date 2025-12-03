#!/usr/bin/env python3
"""
Arc System Diagnosis - Check all components
"""

import sys
import os
import subprocess
import importlib
import traceback

def check_python():
    """Check Python version"""
    print("=== PYTHON VERSION ===")
    print(f"Python: {sys.version}")
    print(f"Executable: {sys.executable}")
    return sys.version_info >= (3, 8)

def check_files():
    """Check required files exist"""
    print("\n=== FILE CHECK ===")
    required_files = [
        'run_web_demo.py',
        'web_app.py', 
        'dual_detection_service.py',
        'arc_scanner.py',
        'requirements_hackathon.txt'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing.append(file)
    
    return len(missing) == 0

def check_dependencies():
    """Check Python packages"""
    print("\n=== DEPENDENCY CHECK ===")
    required_packages = [
        'torch', 'torchvision', 'ultralytics', 'transformers',
        'open3d', 'numpy', 'cv2', 'PIL', 'fastapi', 'uvicorn'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'cv2':
                importlib.import_module('cv2')
            elif package == 'PIL':
                importlib.import_module('PIL')
            else:
                importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package} - {e}")
            missing.append(package)
    
    return missing

def check_models():
    """Check model files"""
    print("\n=== MODEL CHECK ===")
    
    # Check YOLOv8 model
    if os.path.exists('yolov8m.pt'):
        print("✓ yolov8m.pt (general model)")
    else:
        print("✗ yolov8m.pt - will download automatically")
    
    # Check custom wall model
    if os.path.exists('wall_elements_specialized.pt'):
        print("✓ wall_elements_specialized.pt (custom model)")
    else:
        print("⚠ wall_elements_specialized.pt - using general model only")
    
    return True

def test_imports():
    """Test critical imports"""
    print("\n=== IMPORT TEST ===")
    
    try:
        from dual_detection_service import DualDetectionService
        print("✓ DualDetectionService")
    except Exception as e:
        print(f"✗ DualDetectionService - {e}")
        return False
    
    try:
        from arc_scanner import DepthEstimator, PointCloudProcessor
        print("✓ Arc Scanner components")
    except Exception as e:
        print(f"✗ Arc Scanner - {e}")
        return False
    
    try:
        import fastapi
        import uvicorn
        print("✓ Web framework")
    except Exception as e:
        print(f"✗ Web framework - {e}")
        return False
    
    return True

def test_detection():
    """Test object detection"""
    print("\n=== DETECTION TEST ===")
    
    try:
        from dual_detection_service import DualDetectionService
        import numpy as np
        
        # Create test image
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Initialize detector
        detector = DualDetectionService()
        
        # Test detection
        results = detector.detect_comprehensive(test_image)
        print("✓ Object detection working")
        print(f"  Detected classes: {list(results.keys())}")
        
        return True
        
    except Exception as e:
        print(f"✗ Detection test failed - {e}")
        traceback.print_exc()
        return False

def test_web_server():
    """Test if web server can start"""
    print("\n=== WEB SERVER TEST ===")
    
    try:
        # Try importing web app
        import web_app
        print("✓ Web app imports successfully")
        
        # Check if port 8000 is available
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print("⚠ Port 8000 already in use")
        else:
            print("✓ Port 8000 available")
        
        return True
        
    except Exception as e:
        print(f"✗ Web server test failed - {e}")
        return False

def run_diagnosis():
    """Run complete system diagnosis"""
    print("🔍 ARC SYSTEM DIAGNOSIS")
    print("=" * 50)
    
    results = {}
    
    # Run all checks
    results['python'] = check_python()
    results['files'] = check_files()
    results['dependencies'] = len(check_dependencies()) == 0
    results['models'] = check_models()
    results['imports'] = test_imports()
    results['detection'] = test_detection()
    results['web_server'] = test_web_server()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 DIAGNOSIS SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for check, status in results.items():
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {check.replace('_', ' ').title()}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    # Recommendations
    print("\n🔧 RECOMMENDATIONS:")
    
    if not results['dependencies']:
        print("1. Install missing dependencies:")
        print("   pip install -r requirements_hackathon.txt")
    
    if not results['detection']:
        print("2. Detection system needs fixing")
        print("   Check dual_detection_service.py")
    
    if not results['web_server']:
        print("3. Web server issues detected")
        print("   Check web_app.py imports")
    
    if passed == total:
        print("✅ System is ready! Try:")
        print("   python run_web_demo.py")
    else:
        print("❌ Fix issues above before running demo")
    
    return passed == total

if __name__ == "__main__":
    success = run_diagnosis()
    sys.exit(0 if success else 1)