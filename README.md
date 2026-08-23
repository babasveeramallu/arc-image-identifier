# Arc — Real-Time AI Room Scanner

Arc converts a smartphone or webcam feed into a 3D room model in real time. It combines wall-element object detection (YOLOv8) with monocular depth estimation (MiDaS/DPT) and point-cloud stitching to reconstruct rooms without any specialized hardware.

## Why I built this

Built for a hackathon focused on AI-powered spatial understanding: scan a room and its surface elements (outlets, switches, windows, doors) using nothing but a camera, and produce an accurate, textured 3D model. The interesting problem wasn't detection — YOLO is well understood — it was fusing per-frame object detection with depth estimation and stitching multiple walls into one coherent, correctly-scaled model in real time.

## How it works

```
Camera feed -> Depth estimation (MiDaS/DPT) -> Point cloud generation
                     |
        Wall-element detection (YOLOv8) -> Real-time overlay
                     |
     Wall plane detection (RANSAC) -> Multi-wall stitching (ICP)
                     |
              Textured 3D model -> PLY export
```

- **Depth Estimation**: Intel DPT model, RGB frame to dense depth map
- **Object Detection**: YOLOv8, 5 custom wall-element classes (mirror, thermostat, vent, wall socket, window box) + 80 general COCO classes
- **3D Reconstruction**: RANSAC wall-plane extraction, ICP registration to stitch multiple walls into one room
- **Interface**: FastAPI backend, browser-based WebRTC camera capture, live detection overlay, PLY model export

## Quick start

```bash
pip install -r requirements.txt
python run_web_demo.py
```

Opens at `http://localhost:8000`. Point your camera at a wall, capture multiple walls, generate the 3D room model, apply a texture, and export as a `.ply` file.

## Project structure

```
arc-image-identifier/
├── run_web_demo.py             # Entry point — starts the server and opens the browser
├── web_app.py                  # FastAPI backend + web interface
├── arc_scanner.py              # Real-time scanning pipeline (depth + point cloud + stitching)
├── dual_detection_service.py   # Object detection service (wall elements + general objects)
├── detect_objects.py           # YOLOv8 detection wrapper
├── requirements.txt
├── scripts/
│   └── setup_static.py         # One-time setup for texture assets
├── training/
│   ├── train_yolo.py           # Custom wall-element model training
│   └── YOLO_Training_Final.ipynb
├── static/                     # Web assets and texture library
└── docs/                       # Screenshots and result images
```

## Training data

The custom wall-element model was trained on 5,002 labeled images (5 classes: mirror, thermostat, vent, wall socket, window box). Training data is not included in this repo. See `training/train_yolo.py` for the training pipeline.

## Limitations

- Multi-wall stitching accuracy depends on overlap between captured frames; sparse capture produces gaps
- Depth estimation is monocular, so absolute scale is approximate without a reference object
- Tested primarily on well-lit indoor rooms; low-light and reflective surfaces reduce detection accuracy

## Tech stack

Python, FastAPI, YOLOv8 (Ultralytics), Intel DPT (depth estimation), Open3D (point cloud + ICP), WebRTC

---

Built by Baba Sumukhesh Veeramallu
