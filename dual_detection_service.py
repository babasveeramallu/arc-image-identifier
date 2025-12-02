"""Dual detection service combining specialized wall elements + general object detection."""

import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Any

class DualDetectionService:
    """Combines specialized wall detection with general object detection."""
    
    def __init__(self, wall_model_path: str, general_model_path: str = None):
        """Initialize both detection models."""
        self.wall_model = YOLO(wall_model_path)
        self.general_model = YOLO(general_model_path or 'yolov8m.pt')
        
        # Wall-specific classes
        self.wall_classes = ['mirror', 'thermostat', 'vent', 'wall_socket', 'window_box_(for_plants)']
        
        print("✓ Dual detection service initialized")
    
    def detect_comprehensive(self, image_path: str, confidence_threshold: float = 0.5) -> Dict[str, Any]:
        """Perform comprehensive detection using both models."""
        
        # Run wall-specific detection
        wall_results = self.wall_model(image_path, conf=confidence_threshold)
        
        # Run general object detection
        general_results = self.general_model(image_path, conf=confidence_threshold)
        
        # Combine results
        combined_detections = self._combine_detections(wall_results[0], general_results[0])
        
        return {
            "total_objects": len(combined_detections),
            "wall_elements": self._filter_wall_elements(combined_detections),
            "general_objects": self._filter_general_objects(combined_detections),
            "all_detections": combined_detections,
            "image_size": wall_results[0].orig_shape
        }
    
    def _combine_detections(self, wall_result, general_result) -> List[Dict]:
        """Combine detections from both models, removing duplicates."""
        detections = []
        
        # Add wall-specific detections
        if wall_result.boxes is not None:
            for box in wall_result.boxes:
                detection = {
                    "class_name": self.wall_classes[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist(),
                    "type": "wall_element"
                }
                detections.append(detection)
        
        # Add general detections
        if general_result.boxes is not None:
            for box in general_result.boxes:
                detection = {
                    "class_name": general_result.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist(),
                    "type": "general_object"
                }
                detections.append(detection)
        
        # Remove overlapping detections (keep higher confidence)
        detections = self._remove_overlaps(detections)
        
        return detections
    
    def _remove_overlaps(self, detections: List[Dict], iou_threshold: float = 0.5) -> List[Dict]:
        """Remove overlapping detections, keeping higher confidence ones."""
        if len(detections) <= 1:
            return detections
        
        # Sort by confidence (descending)
        detections.sort(key=lambda x: x["confidence"], reverse=True)
        
        filtered = []
        for detection in detections:
            bbox1 = detection["bbox"]
            
            # Check if this detection overlaps with any already filtered detection
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
        
        # Calculate intersection
        x_min = max(x1_min, x2_min)
        y_min = max(y1_min, y2_min)
        x_max = min(x1_max, x2_max)
        y_max = min(y1_max, y2_max)
        
        if x_max <= x_min or y_max <= y_min:
            return 0.0
        
        intersection = (x_max - x_min) * (y_max - y_min)
        
        # Calculate union
        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0
    
    def _filter_wall_elements(self, detections: List[Dict]) -> List[Dict]:
        """Filter only wall-specific elements."""
        return [d for d in detections if d["type"] == "wall_element"]
    
    def _filter_general_objects(self, detections: List[Dict]) -> List[Dict]:
        """Filter only general objects."""
        return [d for d in detections if d["type"] == "general_object"]
    
    def visualize_detections(self, image_path: str, detections: List[Dict], output_path: str = None):
        """Visualize all detections on the image."""
        image = cv2.imread(image_path)
        
        # Color coding: wall elements = red, general objects = blue
        colors = {"wall_element": (0, 0, 255), "general_object": (255, 0, 0)}
        
        for detection in detections:
            bbox = detection["bbox"]
            x1, y1, x2, y2 = map(int, bbox)
            
            color = colors[detection["type"]]
            
            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{detection['class_name']}: {detection['confidence']:.2f}"
            cv2.putText(image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        if output_path:
            cv2.imwrite(output_path, image)
        
        return image

# Example usage
if __name__ == "__main__":
    # Initialize service
    detector = DualDetectionService(
        wall_model_path="wall_elements_specialized.pt",
        general_model_path="yolov8x_general.pt"
    )
    
    # Perform detection
    results = detector.detect_comprehensive("test_image.jpg")
    
    print(f"Total objects detected: {results['total_objects']}")
    print(f"Wall elements: {len(results['wall_elements'])}")
    print(f"General objects: {len(results['general_objects'])}")