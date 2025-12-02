# Setup Instructions

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd arc-wall-scanner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download models** (auto-downloads on first run)
   ```bash
   python demo_pretrained.py
   ```

## Training Data

The training dataset (5,002 images, ~1.75GB) is not included in this repo due to size limits.

**To get training data:**
- Contact the repository owner
- Or use your own dataset in YOLO format

**Training data structure:**
```
yolo_data/
├── images/train/     # 5,002 training images
├── labels/train/     # 5,002 label files  
└── data.yaml         # Dataset configuration
```

## Models

Models are downloaded automatically:
- **yolov8m.pt** - General detection (80 classes)
- **Custom trained model** - Wall elements (5 classes)

## File Structure

```
arc-wall-scanner/
├── dual_detection_service.py     # Main detection service
├── detect_objects.py             # Simple detection script
├── demo_pretrained.py            # Demo script
├── train_yolo.py                 # Training script
├── Colab_Training_Enhanced.ipynb # Google Colab training
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

## Usage

```bash
# Quick demo
python demo_pretrained.py

# Detect objects in image
python detect_objects.py

# Train custom model (requires yolo_data/)
python train_yolo.py
```