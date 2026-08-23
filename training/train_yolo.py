"""Train YOLO for object detection on wall elements."""

import json
import shutil
from pathlib import Path
from ultralytics import YOLO

def convert_coco_to_yolo(json_path, img_dir, output_dir="yolo_data"):
    """Convert COCO format to YOLO format."""
    
    with open(json_path) as f:
        data = json.load(f)
    
    output_path = Path(output_dir)
    (output_path / "images" / "train").mkdir(parents=True, exist_ok=True)
    (output_path / "labels" / "train").mkdir(parents=True, exist_ok=True)
    
    # Category mapping
    categories = {cat['id']: idx for idx, cat in enumerate(data['categories'])}
    cat_names = [cat['name'] for cat in sorted(data['categories'], key=lambda x: categories[x['id']])]
    
    # Group annotations by image
    img_dict = {img['id']: img for img in data['images']}
    ann_by_img = {}
    for ann in data['annotations']:
        img_id = ann['image_id']
        if img_id not in ann_by_img:
            ann_by_img[img_id] = []
        ann_by_img[img_id].append(ann)
    
    print(f"Converting {len(ann_by_img)} images...")
    converted = 0
    
    for img_id, anns in ann_by_img.items():
        if img_id not in img_dict:
            continue
        
        img_info = img_dict[img_id]
        if 'file_name' in img_info:
            img_name = img_info['file_name']
        elif 'coco_url' in img_info:
            img_name = img_info['coco_url'].split('/')[-1]
        else:
            img_name = f"{str(img_id).zfill(12)}.jpg"
        
        src_img = Path(img_dir) / img_name
        if not src_img.exists():
            continue
        
        # Copy image
        dst_img = output_path / "images" / "train" / img_name
        shutil.copy(src_img, dst_img)
        
        # Create YOLO label file
        label_file = output_path / "labels" / "train" / f"{src_img.stem}.txt"
        
        img_w = img_info.get('width', 640)
        img_h = img_info.get('height', 480)
        
        with open(label_file, 'w') as f:
            for ann in anns:
                bbox = ann['bbox']  # [x, y, width, height]
                cat_id = categories[ann['category_id']]
                
                # Convert to YOLO format (normalized center x, center y, width, height)
                x_center = (bbox[0] + bbox[2] / 2) / img_w
                y_center = (bbox[1] + bbox[3] / 2) / img_h
                width = bbox[2] / img_w
                height = bbox[3] / img_h
                
                f.write(f"{cat_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        converted += 1
        if converted % 100 == 0:
            print(f"  Converted {converted} images...")
    
    # Create data.yaml
    yaml_content = f"""
train: {output_path.absolute()}/images/train
val: {output_path.absolute()}/images/train

nc: {len(cat_names)}
names: {cat_names}
"""
    
    with open(output_path / "data.yaml", 'w') as f:
        f.write(yaml_content)
    
    print(f"\nConverted {converted} images")
    print(f"Classes: {cat_names}")
    print(f"Data saved to: {output_path}")
    
    return str(output_path / "data.yaml")

def train_yolo(data_yaml, epochs=2):
    """Train YOLO model."""
    
    print("\nInitializing YOLOv8m (medium - pre-trained with 85%+ accuracy)...")
    model = YOLO('yolov8m.pt')
    
    print(f"\nTraining for {epochs} epochs with optimized hyperparameters...")
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=320,  # Standard size for better accuracy
        batch=8,  # Smaller batch for YOLOv8m on CPU
        device='cpu',
        patience=5,  # Stop early if no improvement
        save=True,
        project='runs/detect',
        name='wall_elements',
        # Optimized hyperparameters
        lr0=0.01,  # Higher initial learning rate
        lrf=0.01,  # Final learning rate
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3,
        warmup_momentum=0.8,
        box=7.5,  # Box loss weight
        cls=0.5,  # Class loss weight
        dfl=1.5,  # DFL loss weight
        hsv_h=0.015,  # HSV-Hue augmentation
        hsv_s=0.7,  # HSV-Saturation augmentation
        hsv_v=0.4,  # HSV-Value augmentation
        degrees=10,  # Rotation augmentation
        translate=0.1,  # Translation augmentation
        scale=0.5,  # Scale augmentation
        mosaic=1.0,  # Mosaic augmentation
        mixup=0.1  # Mixup augmentation
    )
    
    print("\nTraining complete!")
    print(f"Best model saved to: runs/detect/wall_elements/weights/best.pt")
    
    return model

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python train_yolo.py <annotations.json> <images_dir>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    img_dir = sys.argv[2]
    
    # Convert data
    data_yaml = convert_coco_to_yolo(json_path, img_dir)
    
    # Train YOLO
    model = train_yolo(data_yaml, epochs=25)
    
    print("\nTo use the model:")
    print("  from ultralytics import YOLO")
    print("  model = YOLO('runs/detect/wall_elements/weights/best.pt')")
    print("  results = model('image.jpg')")
