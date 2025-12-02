# Arc - AI Wall Scanner

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Comprehensive AI-powered object detection system that combines specialized wall element detection with general object recognition for complete scene understanding.

## Features

- **Dual Detection System** - Specialized wall elements + 80 general object classes
- **YOLOv8 Models** - Custom trained + pre-trained models for maximum coverage
- **Smart Overlap Removal** - Intelligent deduplication of detections
- **Google Colab Training** - Free GPU training with enhanced notebook
- **Real-time Detection** - Sub-second response times
- **Production Ready** - Clean, optimized codebase

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test dual detection system
python demo_pretrained.py

# Detect objects in specific image
python detect_objects.py
```

## Detection Capabilities

### Specialized Wall Elements (Custom Model)
- **5 Classes**: mirror, thermostat, vent, wall_socket, window_box
- **Training Data**: 5,002 labeled images
- **Accuracy**: Optimized for architectural elements

### General Objects (Pre-trained YOLOv8m)
- **80 Classes**: person, furniture, electronics, vehicles, etc.
- **Coverage**: Anything that might appear on walls
- **Accuracy**: 80%+ on COCO dataset, faster inference

## Training Your Own Model

### Option 1: Google Colab (Recommended)
1. Open `Colab_Training_Enhanced.ipynb` in Google Colab
2. Enable GPU (Runtime → Change runtime type → GPU)
3. Upload `yolo_data.zip` when prompted
4. Run all cells (2-3 hours training)
5. Download both models

### Option 2: Local Training
```bash
python train_yolo.py
```

## Usage Examples

### Dual Detection Service
```python
from dual_detection_service import DualDetectionService

# Initialize with both models
detector = DualDetectionService(
    wall_model_path='wall_elements_specialized.pt',
    general_model_path='yolov8m.pt'
)

# Comprehensive detection
results = detector.detect_comprehensive('image.jpg')
print(f"Total objects: {results['total_objects']}")
print(f"Wall elements: {len(results['wall_elements'])}")
print(f"General objects: {len(results['general_objects'])}")
```

### Simple Detection
```python
from ultralytics import YOLO

# Use YOLOv8m for balanced speed/accuracy
model = YOLO('yolov8m.pt')
results = model('image.jpg')
results[0].show()
```

## Model Performance

| Model Type | Classes | Accuracy | Use Case |
|------------|---------|----------|----------|
| Specialized Wall | 5 | Custom trained | Architectural elements |
| General YOLOv8m | 80 | 80%+ | Everything else |
| Combined System | 85 | Optimal | Complete detection |

## Project Structure

```
Arc/
├── dual_detection_service.py     # Main detection service
├── detect_objects.py             # Object detection script
├── demo_pretrained.py            # Demo with pre-trained model
├── train_yolo.py                 # Training script
├── Colab_Training_Enhanced.ipynb # Google Colab notebook
├── yolo_data/                    # Training dataset
│   ├── images/train/             # 5,002 training images
│   ├── labels/train/             # Label files
│   └── data.yaml                 # Dataset configuration
├── runs/detect/                  # Training results
└── requirements.txt              # Dependencies
```

## Key Files

- **`dual_detection_service.py`** - Combines both models with smart overlap removal
- **`Colab_Training_Enhanced.ipynb`** - Complete training pipeline for Google Colab
- **`yolo_data/`** - 5,002 labeled images for wall element training
- **`detect_objects.py`** - Simple detection script
- **`demo_pretrained.py`** - Quick demo using pre-trained models

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

## Roadmap

- [x] Dual detection system
- [x] Google Colab training
- [x] Smart overlap removal
- [x] 5,002 image dataset
- [x] Enhanced training notebook
- [ ] Real-time video processing
- [ ] Mobile app integration
- [ ] 3D scene reconstruction

---

Made by Baba Sumukhesh Veeramallu
