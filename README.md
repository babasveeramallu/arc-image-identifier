# Arc - Image to 3D Model Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hackathon](https://img.shields.io/badge/Hackathon-Ready-brightgreen.svg)](https://github.com/)

🏆 **Real-time AI-powered wall scanner that converts smartphone camera input to accurate 3D room models**

Built for hackathon: AI model that scans walls and surface elements in real-time, forming accurate 3D models with automatic multi-wall stitching and texture application.

## 🎆 Hackathon Features

- **📱 Real-time Camera Scanning** - Live wall detection using smartphone/webcam
- **🏠 3D Room Reconstruction** - Multi-wall stitching with automatic corner detection
- **🔌 Element Detection** - AI detection of outlets, switches, windows, doors
- **🎨 Texture Library** - Apply materials (paint, brick, wood, concrete)
- **🌐 Web Interface** - Browser-based demo with WebRTC
- **📥 Model Export** - Download 3D models as PLY files
- **⚡ Real-time Processing** - Sub-second depth estimation and reconstruction

## 🚀 Quick Start (Hackathon Demo)

```bash
# 1. Install dependencies
pip install -r requirements_hackathon.txt

# 2. Test 3D scanning system
python demo_hackathon.py

# 3. Launch web demo
python run_web_demo.py
# Opens at http://localhost:8000
```

### 🎬 Live Demo
**Web App**: Point camera at wall → Capture multiple walls → Generate 3D room model → Apply textures → Download PLY file

## 🔍 Detection + 3D Capabilities

### 🏠 Real-time Wall Scanning
- **Depth Estimation**: Intel DPT model for RGB-to-depth conversion
- **Point Cloud Generation**: 3D reconstruction from camera feed
- **Wall Plane Detection**: RANSAC-based wall surface extraction
- **Multi-wall Stitching**: ICP registration for room completion

### 🔌 Element Detection (Existing)
- **5 Wall Classes**: mirror, thermostat, vent, wall_socket, window_box
- **80 General Classes**: furniture, electronics, etc.
- **Training Data**: 5,002 labeled images
- **Real-time Overlay**: Live detection boxes on camera feed

## Training Your Own Model

### Option 1: Jupyter Notebook (Recommended)
1. Open `YOLO_Training_Final.ipynb` in Jupyter/Colab
2. Upload `arc_training_data.zip` when prompted
3. Run all cells (6-8 hours CPU training)
4. Download trained model

### Option 2: Local Training
```bash
python train_yolo.py
```

## 💻 Usage Examples

### Real-time 3D Scanning
```python
from arc_scanner import ArcRealTimeScanner
from dual_detection_service import DualDetectionService

# Initialize scanner
detector = DualDetectionService()
scanner = ArcRealTimeScanner(detector)

# Start real-time scanning
scanner.start_scanning()
# Press 'S' to capture walls, 'R' for room model
```

### Web Interface
```python
# Launch web demo
python run_web_demo.py

# Features:
# - Real-time camera access
# - Live object detection overlay
# - 3D room model generation
# - Texture application
# - PLY model export
```

### API Usage
```python
# Process single frame
result = scanner.process_frame(camera_frame)
print(f"Detections: {len(result['detections'])}")
print(f"Depth map: {result['depth_map'].shape}")
print(f"Point cloud: {len(result['point_cloud'].points)} points")
```

## Model Performance

| Model Type | Classes | Accuracy | Use Case |
|------------|---------|----------|----------|
| Specialized Wall | 5 | Custom trained | Architectural elements |
| General YOLOv8m | 80 | 80%+ | Everything else |
| Combined System | 85 | Optimal | Complete detection |

## 📁 Project Structure

```
Arc/
├── arc_scanner.py                # 🎆 Core 3D scanning system
├── web_app.py                    # 🌐 Web interface (FastAPI + WebRTC)
├── demo_hackathon.py             # 📹 Desktop demo
├── run_web_demo.py               # 🚀 Web launcher
├── dual_detection_service.py     # Object detection service
├── detect_objects.py             # Simple detection script
├── requirements_hackathon.txt    # 🎆 Hackathon dependencies
├── static/                       # Web assets
│   └── textures/                 # Material library
├── yolo_data/                    # Training dataset (5,002 images)
├── HACKATHON_SETUP.md            # 📝 Setup instructions
└── room_model.ply                # 🏠 Generated 3D model
```

## 🔑 Key Files

- **`arc_scanner.py`** - 🎆 Real-time 3D scanning pipeline (depth + point cloud + stitching)
- **`web_app.py`** - 🌐 Full web interface with camera access and 3D viewer
- **`demo_hackathon.py`** - 📹 Desktop demo for testing
- **`run_web_demo.py`** - 🚀 One-click web demo launcher
- **`dual_detection_service.py`** - Object detection (existing)
- **`HACKATHON_SETUP.md`** - 📝 Complete setup guide

## Training Data

- **Images**: 5,002 high-quality wall images
- **Classes**: 5 specialized architectural elements
- **Format**: YOLO format with bounding boxes
- **Size**: ~1GB compressed (yolo_data.zip)

## Quick Demo

```bash
# Run demo with sample images
python demo_pretrained.py

# Output: detection_result.jpg with bounding boxes
```

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection
- [MiDaS](https://github.com/isl-org/MiDaS) - Depth estimation
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework

## 🎆 Hackathon Implementation

### ✅ Completed (Hackathon Ready)
- [x] **Real-time camera scanning** - Live wall detection
- [x] **3D model generation** - Point cloud to mesh conversion
- [x] **Multi-wall stitching** - ICP registration algorithm
- [x] **Element detection** - 5 wall classes + 80 general objects
- [x] **Web interface** - Browser-based demo
- [x] **Texture system** - Material library with 5 options
- [x] **Model export** - PLY file download

### 🔄 Technical Pipeline
```
Camera → Depth Estimation → Point Cloud → Wall Detection → 3D Model
   ↓           ↓              ↓           ↓           ↓
Object Detection → Real-time Overlay → Multi-wall Stitching → Export
```

## 🏆 Hackathon Submission

**Challenge**: AI model that scans walls and surface elements in real-time, forming accurate 3D models

**Solution**: Arc - Complete real-time wall scanner with:
- 📱 Smartphone camera integration
- 🤖 AI element detection (outlets, switches, etc.)
- 🏠 Multi-wall 3D room reconstruction
- 🎨 Texture application system
- 🌐 Web-based demo interface

**Demo**: `python run_web_demo.py` → http://localhost:8000

**Submission Files**:
- Working prototype (web link)
- Demo video (3-5 minutes)
- Complete source code
- Setup instructions

---

🚀 **Made by Baba Sumukhesh Veeramallu** | Hackathon Ready 🏆
