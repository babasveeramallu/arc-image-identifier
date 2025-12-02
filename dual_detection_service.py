"""Fixed DualDetectionService - Works with or without custom wall model"""

from ultralytics import YOLO
from typing import List, Dict, Any
import os
import numpy as np

class DualDetectionService:
    """Combines specialized wall detection with general object detection."""
    
    def __init__(self, wall_model_path: str = None, general_model_path: str = None):
        """
        Initialize detection models.
        
        Args:
            wall_model_path: Path to custom wall model (optional)
            general_model_path: Path to general model (defaults to yolov8m.pt)
        """
        # Use custom wall model if available, otherwise use general model for everything
        if wall_model_path and os.path.exists(wall_model_path):
            print(f"Loading custom wall model: {wall_model_path}")
            self.wall_model = YOLO(wall_model_path)
            self.has_wall_model = True
            self.wall_classes = ['mirror', 'thermostat', 'vent', 'wall_socket', 'window_box']
        else:
            print("No custom wall model found, using general model only")
            self.wall_model = None
            self.has_wall_model = False
            self.wall_classes = []
        
        # General model (always available)
        self.general_model = YOLO(general_model_path or 'yolov8m.pt')
        
        print("✓ Dual detection service initialized")
    
    def detect_comprehensive(self, image, confidence_threshold: float = 0.5) -> Dict[str, Any]:
        """Perform comprehensive detection using available models."""
        
        detections = []
        
        # Run wall-specific detection if available
        if self.has_wall_model:
            wall_results = self.wall_model(image, conf=confidence_threshold, verbose=False)
            if wall_results[0].boxes is not None:
                for box in wall_results[0].boxes:
                    detections.append({
                        "class": self.wall_classes[int(box.cls)],
                        "confidence": float(box.conf),
                        "bbox": box.xyxy[0].tolist(),
                        "type": "wall_element"
                    })
        
        # Run general object detection
        general_results = self.general_model(image, conf=confidence_threshold, verbose=False)
        if general_results[0].boxes is not None:
            for box in general_results[0].boxes:
                detections.append({
                    "class": general_results[0].names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist(),
                    "type": "general_object"
                })
        
        # Remove overlaps
        detections = self._remove_overlaps(detections)
        
        return {
            "total_objects": len(detections),
            "wall_elements": [d for d in detections if d["type"] == "wall_element"],
            "general_objects": [d for d in detections if d["type"] == "general_object"],
            "all_detections": detections
        }
    
    def _remove_overlaps(self, detections: List[Dict], iou_threshold: float = 0.5) -> List[Dict]:
        """Remove overlapping detections, keeping higher confidence ones."""
        if len(detections) <= 1:
            return detections
        
        detections.sort(key=lambda x: x["confidence"], reverse=True)
        
        filtered = []
        for detection in detections:
            bbox1 = detection["bbox"]
            overlaps = False
            
            for filtered_detection in filtered:
                bbox2 = filtered_detection["bbox"]
                iou = self._calculate_iou(bbox1, bbox2)
                
                if iou > iou_threshold:
                    overlaps = True
                    break
            
            if not overlaps:
                filtered.append(detection)
        
        return filtered
    
    def _calculate_iou(self, bbox1: List[float], bbox2: List[float]) -> float:
        """Calculate Intersection over Union (IoU) between two bounding boxes."""
        x1_min, y1_min, x1_max, y1_max = bbox1
        x2_min, y2_min, x2_max, y2_max = bbox2
        
        x_min = max(x1_min, x2_min)
        y_min = max(y1_min, y2_min)
        x_max = min(x1_max, x2_max)
        y_max = min(y1_max, y2_max)
        
        if x_max <= x_min or y_max <= y_min:
            return 0.0
        
        intersection = (x_max - x_min) * (y_max - y_min)
        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0


if __name__ == "__main__":
    # Test with optional wall model
    import os
    
    wall_model = "wall_elements_specialized.pt" if os.path.exists("wall_elements_specialized.pt") else None
    
    detector = DualDetectionService(wall_model_path=wall_model)
    
    print(f"Wall model loaded: {detector.has_wall_model}")
    print(f"Ready for detection!")