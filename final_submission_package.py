"""
FINAL SUBMISSION PACKAGE - Automated setup and test
Run this to prepare everything for hackathon submission
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run command and show result"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"PASS {description} completed")
            return True
        else:
            print(f"FAIL {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"FAIL {description} error: {e}")
        return False

def check_file_exists(filepath, description):
    """Check if critical file exists"""
    if Path(filepath).exists():
        print(f"PASS {description}")
        return True
    else:
        print(f"FAIL {description} MISSING")
        return False

def test_import(module, description):
    """Test if module can be imported"""
    try:
        __import__(module)
        print(f"PASS {description}")
        return True
    except ImportError:
        print(f"FAIL {description} - pip install {module}")
        return False

def main():
    print("=" * 60)
    print("ARC HACKATHON - FINAL SUBMISSION PACKAGE")
    print("=" * 60)
    
    # 1. Check critical files
    print("\n1. CHECKING CRITICAL FILES...")
    files_ok = all([
        check_file_exists("dual_detection_service.py", "Dual detection service"),
        check_file_exists("arc_scanner.py", "Arc scanner"),
        check_file_exists("web_app.py", "Web application"),
        check_file_exists("demo_hackathon.py", "Demo script"),
        check_file_exists("run_web_demo.py", "Web launcher"),
        check_file_exists("setup_static.py", "Static setup script"),
        check_file_exists("requirements_hackathon.txt", "Requirements file")
    ])
    
    # 2. Test critical imports
    print("\n2. TESTING IMPORTS...")
    imports_ok = all([
        test_import("ultralytics", "YOLO"),
        test_import("cv2", "OpenCV"),
        test_import("numpy", "NumPy"),
        test_import("torch", "PyTorch"),
        test_import("fastapi", "FastAPI")
    ])
    
    # 3. Setup static files
    print("\n3. SETTING UP STATIC FILES...")
    static_ok = run_command("python setup_static.py", "Static files setup")
    
    # 4. Test detection service
    print("\n4. TESTING DETECTION SERVICE...")
    detection_ok = run_command(
        'python -c "from dual_detection_service import DualDetectionService; d=DualDetectionService(); print(\\"Detection works!\\")"',
        "Detection service test"
    )
    
    # 5. Check static directories
    print("\n5. CHECKING STATIC DIRECTORIES...")
    static_dirs_ok = all([
        check_file_exists("static", "Static directory"),
        check_file_exists("static/textures", "Textures directory"),
        check_file_exists("static/models", "Models directory")
    ])
    
    # 6. Summary
    print("\n" + "=" * 60)
    print("SUBMISSION READINESS SUMMARY")
    print("=" * 60)
    
    all_checks = [
        ("Critical Files", files_ok),
        ("Python Imports", imports_ok),
        ("Static Setup", static_ok),
        ("Detection Service", detection_ok),
        ("Static Directories", static_dirs_ok)
    ]
    
    for check_name, status in all_checks:
        print(f"{check_name}: {'PASS' if status else 'FAIL'}")
    
    overall_status = all(status for _, status in all_checks)
    
    print("\n" + "=" * 60)
    
    if overall_status:
        print("READY FOR SUBMISSION!")
        print("\nNext steps:")
        print("1. Test demo: python demo_hackathon.py")
        print("2. Test web: python run_web_demo.py")
        print("3. Record demo video")
        print("4. Submit to hackathon!")
        print("\nGitHub: https://github.com/babasveeramallu/arc-image-identifier.git")
    else:
        print("SOME ISSUES FOUND")
        print("\nFix the failed checks above before submitting")
        print("Most issues can be resolved by installing missing packages:")
        print("pip install ultralytics opencv-python torch fastapi uvicorn")
    
    print("=" * 60)

if __name__ == "__main__":
    main()