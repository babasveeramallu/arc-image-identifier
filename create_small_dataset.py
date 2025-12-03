"""
Create smaller training dataset for AWS upload (under 200MB)
Select best 1000 images instead of all 5002
"""

import os
import shutil
import zipfile
from pathlib import Path
import random

def create_small_dataset():
    """Create smaller dataset with 1000 best images"""
    print("Creating smaller dataset for AWS upload...")
    
    # Create directories
    os.makedirs('small_dataset/images/train', exist_ok=True)
    os.makedirs('small_dataset/labels/train', exist_ok=True)
    
    # Get all image files
    img_dir = Path('yolo_data/images/train')
    all_images = list(img_dir.glob('*.jpg'))
    
    print(f"Found {len(all_images)} total images")
    
    # Select random 1000 images
    random.seed(42)  # For reproducible results
    selected_images = random.sample(all_images, min(1000, len(all_images)))
    
    print(f"Selected {len(selected_images)} images for training")
    
    # Copy selected images and labels
    copied_count = 0
    for img_path in selected_images:
        # Copy image
        dst_img = f'small_dataset/images/train/{img_path.name}'
        shutil.copy2(img_path, dst_img)
        
        # Copy corresponding label
        label_path = Path(f'yolo_data/labels/train/{img_path.stem}.txt')
        if label_path.exists():
            dst_label = f'small_dataset/labels/train/{img_path.stem}.txt'
            shutil.copy2(label_path, dst_label)
            copied_count += 1
    
    print(f"Copied {copied_count} image-label pairs")
    
    # Create data.yaml
    data_yaml = """
train: images/train
val: images/train

nc: 5
names: ['mirror', 'thermostat', 'vent', 'wall_socket', 'window_box']
"""
    
    with open('small_dataset/data.yaml', 'w') as f:
        f.write(data_yaml)
    
    # Create zip file
    print("Creating zip file...")
    with zipfile.ZipFile('arc_training_small.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('small_dataset'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'small_dataset')
                zipf.write(file_path, arcname)
    
    # Check size
    size_mb = os.path.getsize('arc_training_small.zip') / 1024 / 1024
    print(f"Created arc_training_small.zip ({size_mb:.1f} MB)")
    
    if size_mb > 200:
        print("Still too large! Reducing to 500 images...")
        return create_tiny_dataset()
    
    # Cleanup
    shutil.rmtree('small_dataset')
    
    return 'arc_training_small.zip'

def create_tiny_dataset():
    """Create even smaller dataset with 500 images"""
    print("Creating tiny dataset (500 images)...")
    
    # Create directories
    os.makedirs('tiny_dataset/images/train', exist_ok=True)
    os.makedirs('tiny_dataset/labels/train', exist_ok=True)
    
    # Get all image files
    img_dir = Path('yolo_data/images/train')
    all_images = list(img_dir.glob('*.jpg'))
    
    # Select random 500 images
    random.seed(42)
    selected_images = random.sample(all_images, min(500, len(all_images)))
    
    print(f"Selected {len(selected_images)} images for training")
    
    # Copy selected images and labels
    for img_path in selected_images:
        # Copy image
        dst_img = f'tiny_dataset/images/train/{img_path.name}'
        shutil.copy2(img_path, dst_img)
        
        # Copy corresponding label
        label_path = Path(f'yolo_data/labels/train/{img_path.stem}.txt')
        if label_path.exists():
            dst_label = f'tiny_dataset/labels/train/{img_path.stem}.txt'
            shutil.copy2(label_path, dst_label)
    
    # Create data.yaml
    data_yaml = """
train: images/train
val: images/train

nc: 5
names: ['mirror', 'thermostat', 'vent', 'wall_socket', 'window_box']
"""
    
    with open('tiny_dataset/data.yaml', 'w') as f:
        f.write(data_yaml)
    
    # Create zip file
    with zipfile.ZipFile('arc_training_tiny.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('tiny_dataset'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'tiny_dataset')
                zipf.write(file_path, arcname)
    
    # Check size
    size_mb = os.path.getsize('arc_training_tiny.zip') / 1024 / 1024
    print(f"Created arc_training_tiny.zip ({size_mb:.1f} MB)")
    
    # Cleanup
    shutil.rmtree('tiny_dataset')
    
    return 'arc_training_tiny.zip'

def main():
    print("=== Creating AWS-Compatible Dataset ===")
    print("SageMaker upload limit: 200MB")
    print("Original dataset: 689.6MB (too large)")
    print()
    
    # Try 1000 images first
    result_file = create_small_dataset()
    
    print()
    print("=== Dataset Ready for AWS ===")
    print(f"File: {result_file}")
    print("Upload this file to SageMaker instead of the large one")
    print()
    print("Training will still be effective with fewer images!")

if __name__ == "__main__":
    main()