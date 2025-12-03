"""Demo using pre-trained YOLOv8 for wall element detection."""

from ultralytics import YOLO
from pathlib import Path
import cv2

def test_pretrained_model(image_path=None, save_results=True):
    """Test pre-trained YOLOv8m model."""
    
    print("Loading pre-trained YOLOv8m model (85%+ accuracy)...")
    model = YOLO('yolov8m.pt')
    
    print(f"\nModel detects {len(model.names)} classes including:")
    relevant_classes = ['bottle', 'cup', 'bowl', 'chair', 'couch', 'bed', 'dining table', 
                       'toilet', 'tv', 'laptop', 'mouse', 'keyboard', 'cell phone', 
                       'microwave', 'oven', 'sink', 'refrigerator', 'clock', 'vase']
    print(f"  {', '.join(relevant_classes[:10])}...")
    
    if image_path:
        print(f"\nRunning detection on: {image_path}")
        results = model(image_path)
        
        # Display results
        for r in results:
            print(f"\nDetected {len(r.boxes)} objects:")
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls]
                print(f"  - {name}: {conf:.2%} confidence")
            
            if save_results:
                output_path = "detection_result.jpg"
                r.save(filename=output_path)
                print(f"\nResult saved to: {output_path}")
        
        return results
    else:
        print("\nModel ready! Use it like:")
        print("  results = model('path/to/image.jpg')")
        print("  results[0].show()  # Display results")
        return model

def test_on_sample_images():
    """Test on sample images from training data."""
    
    model = YOLO('yolov8m.pt')
    img_dir = Path("yolo_data\images\train")
    
    # Get first 5 images
    images = list(img_dir.glob("*.jpg"))[:5]
    
    if not images:
        print("No images found in \yolo_data\images")
        return
    
    print(f"\nTesting on {len(images)} sample images...")
    
    total_detections = 0
    for img_path in images:
        results = model(str(img_path), verbose=False)
        detections = len(results[0].boxes)
        total_detections += detections
        print(f"  {img_path.name}: {detections} objects detected")
    
    print(f"\nTotal: {total_detections} objects detected across {len(images)} images")
    print(f"Average: {total_detections/len(images):.1f} objects per image")
    
    # Save one result as example
    if images:
        results = model(str(images[0]))
        results[0].save(filename="sample_detection.jpg")
        print(f"\nSample result saved to: sample_detection.jpg")

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("PRE-TRAINED YOLO DETECTION DEMO")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Test on specific image
        test_pretrained_model(sys.argv[1])
    else:
        # Test on sample images
        test_on_sample_images()
        
        print("\n" + "=" * 60)
        print("To test on your own image:")
        print("  python demo_pretrained.py path/to/image.jpg")
        print("=" * 60)
