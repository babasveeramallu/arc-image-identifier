"""Main object detection using pre-trained YOLO."""

from ultralytics import YOLO
import cv2
from pathlib import Path

class ObjectDetector:
    """High-accuracy object detector using pre-trained YOLOv8."""
    
    def __init__(self, model_path='yolov8m.pt'):
        """Initialize with pre-trained model (85%+ accuracy)."""
        print(f"Loading model: {model_path}")
        self.model = YOLO(model_path)
        print(f"Model loaded - detects {len(self.model.names)} classes")
    
    def detect(self, image_path, conf_threshold=0.5):
        """Detect objects in image."""
        results = self.model(image_path, conf=conf_threshold)
        
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    'class': self.model.names[int(box.cls[0])],
                    'confidence': float(box.conf[0]),
                    'bbox': box.xyxy[0].tolist()
                })
        
        return detections
    
    def detect_and_save(self, image_path, output_path='result.jpg'):
        """Detect and save annotated image."""
        results = self.model(image_path)
        results[0].save(filename=output_path)
        return self.detect(image_path)

if __name__ == "__main__":
    detector = ObjectDetector()
    
    # Test on sample image
    test_img = Path("training_data/train2017")
    images = list(test_img.glob("*.jpg"))[:1]
    
    if images:
        detections = detector.detect_and_save(str(images[0]), "detection_demo.jpg")
        print(f"\nDetected {len(detections)} objects:")
        for d in detections:
            print(f"  - {d['class']}: {d['confidence']:.2%}")
        print("\nResult saved to: detection_demo.jpg")
