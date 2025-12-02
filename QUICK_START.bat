@echo off
echo === Arc - Image to 3D Model Setup ===
echo.

echo 1. Installing dependencies...
pip install ultralytics opencv-python numpy torch fastapi uvicorn Pillow -q

echo 2. Setting up static assets...
python setup_static.py

echo 3. Testing detection system...
python -c "from dual_detection_service import DualDetectionService; print('Detection ready')"

echo.
echo === Setup Complete! ===
echo.
echo Choose demo to run:
echo 1. python demo_simple.py      - Simple camera demo (no 3D)
echo 2. python run_web_demo.py     - Full web interface
echo.
pause