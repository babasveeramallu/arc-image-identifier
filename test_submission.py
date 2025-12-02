"""
Pre-submission test - Run this before submitting!
Checks all critical components work
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test all critical imports"""
    print("1. Testing imports...")
    
    required = {
        'torch': 'PyTorch',
        'cv2': 'OpenCV',
        'transformers': 'Transformers',
        'open3d': 'Open3D',
        'ultralytics': 'Ultralytics YOLO',
        'fastapi': 'FastAPI',
        'numpy': 'NumPy'
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} MISSING")
            missing.append(module)
    
    if missing:
        print(f"\nInstall missing: pip install {' '.join(missing)}")
        return False
    
    return True

def test_models():
    """Test model loading"""
    print("\n2. Testing models...")
    
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8m.pt')
        print("  ✓ YOLOv8m loaded")
        
        # Test inference
        import numpy as np
        test_img = np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8)
        results = model(test_img, verbose=False)
        print("  ✓ YOLO inference works")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Model test failed: {e}")
        return False

def test_depth_estimation():
    """Test depth estimator"""
    print("\n3. Testing depth estimation...")
    
    try:
        from transformers import DPTImageProcessor, DPTForDepthEstimation
        import torch
        import numpy as np
        
        processor = DPTImageProcessor.from_pretrained("Intel/dpt-hybrid-midas")
        model = DPTForDepthEstimation.from_pretrained("Intel/dpt-hybrid-midas")
        
        print("  ✓ DPT model loaded")
        
        # Test inference
        test_img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        inputs = processor(images=test_img, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        print("  ✓ Depth estimation works")
        return True
        
    except Exception as e:
        print(f"  ✗ Depth estimation failed: {e}")
        return False

def test_dual_detection():
    """Test dual detection service"""
    print("\n4. Testing dual detection service...")
    
    try:
        from dual_detection_service import DualDetectionService
        import numpy as np
        
        # Test without custom model
        detector = DualDetectionService(wall_model_path=None)
        print("  ✓ Dual detection initialized")
        
        # Test detection
        test_img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        results = detector.detect_comprehensive(test_img)
        
        print(f"  ✓ Detection works (found {results['total_objects']} objects in test image)")
        return True
        
    except Exception as e:
        print(f"  ✗ Dual detection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scanner():
    """Test arc scanner (without camera)"""
    print("\n5. Testing arc scanner...")
    
    try:
        from arc_scanner import DepthEstimator, PointCloudProcessor
        import numpy as np
        
        depth_est = DepthEstimator()
        pcd_proc = PointCloudProcessor()
        
        print("  ✓ Scanner components initialized")
        
        # Test depth estimation
        test_img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        depth = depth_est.estimate(test_img)
        
        print(f"  ✓ Depth map generated: {depth.shape}")
        
        # Test point cloud
        pcd = pcd_proc.depth_to_pointcloud(depth, test_img)
        print(f"  ✓ Point cloud generated: {len(pcd.points)} points")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Scanner test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_static_files():
    """Check static files exist"""
    print("\n6. Checking static files...")
    
    required_dirs = ['static', 'static/textures', 'static/models']
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} MISSING")
            all_exist = False
    
    if not all_exist:
        print("\nRun: python setup_static.py")
        return False
    
    return True

def test_camera():
    """Test camera access"""
    print("\n7. Testing camera access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("  ⚠ Camera not available (OK for demo without camera)")
            return True
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            print(f"  ✓ Camera works: {frame.shape}")
            return True
        else:
            print("  ⚠ Camera opened but couldn't read frame")
            return True
            
    except Exception as e:
        print(f"  ⚠ Camera test failed: {e} (OK for static demo)")
        return True

def main():
    print("=" * 60)
    print("ARC PRE-SUBMISSION TEST")
    print("=" * 60)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Models", test_models),
        ("Depth Estimation", test_depth_estimation),
        ("Dual Detection", test_dual_detection),
        ("Scanner", test_scanner),
        ("Static Files", test_static_files),
        ("Camera", test_camera)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\nUnexpected error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_critical = all(passed for name, passed in results[:5])  # First 5 are critical
    
    print("\n" + "=" * 60)
    
    if all_critical:
        print("✓ ALL CRITICAL TESTS PASSED")
        print("\nYou're ready to:")
        print("1. Run demo: python demo_hackathon.py")
        print("2. Launch web: python run_web_demo.py")
        print("3. Record demo video")
        print("4. Submit!")
    else:
        print("✗ SOME CRITICAL TESTS FAILED")
        print("\nFix issues before submitting!")
    
    print("=" * 60)

if __name__ == "__main__":
    main()