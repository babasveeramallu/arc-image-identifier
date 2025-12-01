# Google Colab Training Instructions

## OPTION 1: Upload yolo_data.zip (FASTEST - Recommended)

### Step 1: Create yolo_data.zip on your computer
1. Go to folder: `c:\Users\sumuk\Documents\Personal\PythonProjects\Hackathon\Arc - Image to Model Tool`
2. Right-click on `yolo_data` folder → Send to → Compressed (zipped) folder
3. Name it `yolo_data.zip` (should be ~500MB-1GB, much smaller than training_data.zip)

### Step 2: Open Google Colab
1. Go to https://colab.research.google.com
2. Click "New Notebook"
3. Go to Runtime → Change runtime type → Select "T4 GPU" → Save

### Step 3: Paste and run these code cells ONE BY ONE

**Cell 1: Install dependencies**
```python
!pip install ultralytics opencv-python -q
```

**Cell 2: Upload yolo_data.zip**
```python
from google.colab import files
uploaded = files.upload()  # Click "Choose Files" and select yolo_data.zip
```

**Cell 3: Unzip the data**
```python
!unzip -q yolo_data.zip
!ls yolo_data/
```

**Cell 4: Train the model (30 epochs, ~30-45 minutes)**
```python
from ultralytics import YOLO

# Load pre-trained model
model = YOLO('yolov8m.pt')

# Train
results = model.train(
    data='yolo_data/data.yaml',
    epochs=30,
    batch=16,
    imgsz=640,
    device=0,  # GPU
    project='runs/detect',
    name='colab_training',
    patience=10,
    save=True,
    plots=True
)

print("Training complete!")
print(f"Best model saved at: runs/detect/colab_training/weights/best.pt")
```

**Cell 5: Download the trained model**
```python
from google.colab import files
files.download('runs/detect/colab_training/weights/best.pt')
files.download('runs/detect/colab_training/results.png')
```

---

## OPTION 2: Use Google Drive (if upload fails)

### Step 1: Upload yolo_data.zip to Google Drive
1. Go to https://drive.google.com
2. Upload `yolo_data.zip` to your Drive (wait for upload to complete)

### Step 2: Open Google Colab and paste these cells

**Cell 1: Mount Google Drive**
```python
from google.colab import drive
drive.mount('/content/drive')
```

**Cell 2: Install and unzip**
```python
!pip install ultralytics opencv-python -q
!cp /content/drive/MyDrive/yolo_data.zip .
!unzip -q yolo_data.zip
!ls yolo_data/
```

**Cell 3-5: Same as Option 1 (cells 4-5)**

---

## Expected Results
- Training time: 30-45 minutes on GPU
- Expected accuracy: 65-75% mAP50
- Files downloaded: `best.pt` (your trained model) and `results.png` (training graphs)

## After Training
1. Download `best.pt` from Colab
2. Copy it to your project folder
3. Use it in `detect_objects.py` by changing model path to `best.pt`
