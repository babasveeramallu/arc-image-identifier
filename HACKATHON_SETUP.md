# Arc - Image to 3D Model | Hackathon Setup

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements_hackathon.txt
```

### 2. Test Core System
```bash
python demo_hackathon.py
```

### 3. Launch Web Demo
```bash
python run_web_demo.py
```
Opens at: http://localhost:8000

## Hackathon Requirements ✅

| Requirement | Implementation | Status |
|------------|----------------|--------|
| Real-time wall scanning | Camera + depth estimation | ✅ |
| Element detection | YOLOv8 (outlets, switches, etc.) | ✅ |
| 3D model generation | Point cloud + mesh reconstruction | ✅ |
| Multi-wall stitching | ICP registration + SLAM | ✅ |
| Texture library | 5 materials (paint, brick, wood, etc.) | ✅ |
| Web app deployment | FastAPI + WebRTC | ✅ |

## Core Components

### 1. Real-time Scanner (`arc_scanner.py`)
- **DepthEstimator**: Intel DPT model for depth maps
- **PointCloudProcessor**: RGB-D to 3D conversion
- **WallStitcher**: Multi-wall registration and room reconstruction
- **ArcRealTimeScanner**: Main scanning pipeline

### 2. Web Interface (`web_app.py`)
- **FastAPI backend**: REST API + WebSocket
- **Camera access**: WebRTC for real-time streaming
- **3D viewer**: Three.js integration
- **Texture system**: Material library

### 3. Object Detection (Existing)
- **Specialized model**: 5 wall elements (outlets, switches, etc.)
- **General model**: 80 COCO classes
- **Dual detection**: Smart overlap removal

## Usage Instructions

### Desktop Demo
1. Run `python demo_hackathon.py`
2. Point camera at wall
3. Press 'S' to capture walls
4. Press 'R' to generate room model
5. Press 'Q' to quit

### Web Demo
1. Run `python run_web_demo.py`
2. Allow camera access in browser
3. Click "Start Camera"
4. Click "Capture Wall" for each wall
5. Click "Generate Room" for 3D model
6. Select textures and download model

## Technical Architecture

```
Camera Feed → Depth Estimation → Point Cloud → Wall Detection
     ↓              ↓               ↓            ↓
Object Detection → 3D Mapping → Registration → Room Model
     ↓              ↓               ↓            ↓
Web Interface → Visualization → Textures → Export (PLY)
```

## Performance Specs

- **Processing**: ~200ms per frame
- **Depth estimation**: Intel DPT (GPU accelerated)
- **Object detection**: YOLOv8 (80%+ accuracy)
- **3D reconstruction**: Open3D Poisson
- **Web latency**: <500ms end-to-end

## Deployment Options

### Option 1: Local Demo (Recommended)
```bash
python run_web_demo.py
# Access at localhost:8000
```

### Option 2: Cloud Deployment
```bash
# Deploy to Railway/Heroku
git push railway main
# Or use Docker
docker build -t arc-scanner .
docker run -p 8000:8000 arc-scanner
```

## File Structure
```
Arc/
├── arc_scanner.py           # Core 3D scanning system
├── web_app.py              # Web interface
├── demo_hackathon.py       # Desktop demo
├── run_web_demo.py         # Web launcher
├── dual_detection_service.py # Object detection (existing)
├── requirements_hackathon.txt # Dependencies
├── static/                 # Web assets
│   └── textures/          # Material library
└── room_model.ply         # Generated 3D model
```

## Troubleshooting

### Camera Issues
- Ensure camera permissions granted
- Try different camera index (0, 1, 2)
- Check if camera is used by other apps

### Model Loading
- Download models on first run (automatic)
- Requires internet for Hugging Face models
- GPU recommended but CPU works

### Performance
- Reduce frame rate if slow (modify `frame_count % 3`)
- Lower depth model resolution
- Use smaller point cloud voxel size

## Demo Video Script

1. **Introduction** (30s)
   - Show web interface
   - Explain real-time scanning concept

2. **Wall Scanning** (60s)
   - Point camera at wall with outlets/switches
   - Show real-time detection overlays
   - Capture multiple walls

3. **3D Reconstruction** (45s)
   - Generate room model
   - Show 3D visualization
   - Apply different textures

4. **Export** (15s)
   - Download PLY model
   - Show file in 3D viewer

## Submission Checklist

- [ ] Working web demo link
- [ ] Demo video (2-3 minutes)
- [ ] Source code ZIP
- [ ] Setup instructions
- [ ] Screenshots

## Contact
Email demo link and files to: yusuf@stickanddot.com

---
**Arc - AI Wall Scanner**  
*Real-time 3D room reconstruction from smartphone camera*