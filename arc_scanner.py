"""
Arc Core Scanner - Real-time 3D Wall Detection System
Minimal implementation for hackathon requirements
"""

import cv2
import numpy as np
import torch
from typing import Dict, List, Tuple, Optional
import open3d as o3d
from dataclasses import dataclass
from transformers import DPTImageProcessor, DPTForDepthEstimation


@dataclass
class WallScan:
    frame_id: int
    rgb_image: np.ndarray
    depth_map: np.ndarray
    point_cloud: o3d.geometry.PointCloud
    detections: List[Dict]
    plane_equation: Optional[np.ndarray] = None
    transform: Optional[np.ndarray] = None


class DepthEstimator:
    def __init__(self):
        print("Loading depth model...")
        self.processor = DPTImageProcessor.from_pretrained("Intel/dpt-hybrid-midas")
        self.model = DPTForDepthEstimation.from_pretrained("Intel/dpt-hybrid-midas")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.model.eval()
        print(f"✓ Depth estimator ready ({self.device})")
    
    def estimate(self, image: np.ndarray) -> np.ndarray:
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            depth = outputs.predicted_depth
        
        depth = torch.nn.functional.interpolate(
            depth.unsqueeze(1),
            size=image.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()
        
        depth = depth.cpu().numpy()
        depth = (depth - depth.min()) / (depth.max() - depth.min())
        return depth


class PointCloudProcessor:
    def __init__(self, fx=525.0, fy=525.0):
        self.fx = fx
        self.fy = fy
    
    def depth_to_pointcloud(self, depth: np.ndarray, rgb: np.ndarray) -> o3d.geometry.PointCloud:
        h, w = depth.shape
        cx, cy = w / 2, h / 2
        
        x = np.arange(w)
        y = np.arange(h)
        xv, yv = np.meshgrid(x, y)
        
        z = depth * 1000.0
        x3d = (xv - cx) * z / self.fx
        y3d = (yv - cy) * z / self.fy
        
        points = np.stack([x3d, y3d, z], axis=-1).reshape(-1, 3)
        colors = rgb.reshape(-1, 3) / 255.0
        
        valid = (z.reshape(-1) > 0) & (z.reshape(-1) < 10000)
        points = points[valid]
        colors = colors[valid]
        
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.colors = o3d.utility.Vector3dVector(colors)
        
        return pcd
    
    def extract_wall_plane(self, pcd: o3d.geometry.PointCloud) -> Tuple[o3d.geometry.PointCloud, np.ndarray]:
        plane_model, inliers = pcd.segment_plane(
            distance_threshold=20.0,
            ransac_n=3,
            num_iterations=1000
        )
        
        wall_pcd = pcd.select_by_index(inliers)
        return wall_pcd, plane_model


class WallStitcher:
    def __init__(self):
        self.walls: List[WallScan] = []
        self.global_pcd = o3d.geometry.PointCloud()
        
    def add_wall(self, scan: WallScan):
        self.walls.append(scan)
        
        if len(self.walls) > 1:
            self._register_with_existing(scan)
        
        if scan.transform is not None:
            transformed_pcd = scan.point_cloud.transform(scan.transform)
            self.global_pcd += transformed_pcd
        else:
            self.global_pcd += scan.point_cloud
    
    def _register_with_existing(self, new_scan: WallScan):
        best_fitness = 0
        best_transform = np.eye(4)
        
        for prev_scan in self.walls[:-1]:
            reg_result = o3d.pipelines.registration.registration_icp(
                new_scan.point_cloud,
                prev_scan.point_cloud,
                max_correspondence_distance=100.0,
                init=np.eye(4)
            )
            
            if reg_result.fitness > best_fitness:
                best_fitness = reg_result.fitness
                best_transform = reg_result.transformation
        
        if best_fitness > 0.3:
            new_scan.transform = best_transform
    
    def generate_room_mesh(self) -> o3d.geometry.TriangleMesh:
        if len(self.walls) < 2:
            return None
        
        pcd_down = self.global_pcd.voxel_down_sample(voxel_size=50.0)
        pcd_down.estimate_normals()
        
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd_down, depth=7
        )
        
        return mesh


class ArcRealTimeScanner:
    def __init__(self, object_detector, camera_index: int = 0):
        self.object_detector = object_detector
        self.depth_estimator = DepthEstimator()
        self.pcd_processor = PointCloudProcessor()
        self.stitcher = WallStitcher()
        
        self.camera = cv2.VideoCapture(camera_index)
        self.frame_count = 0
        self.scanning = False
        
        print("✓ Arc Scanner initialized")
    
    def start_scanning(self):
        self.scanning = True
        print("Scanning... Press 'q' to stop, 's' to save wall, 'r' for room model")
        
        while self.scanning:
            ret, frame = self.camera.read()
            if not ret:
                break
            
            result = self.process_frame(frame)
            vis_frame = self._visualize_results(frame, result)
            cv2.imshow('Arc Scanner', vis_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.scanning = False
            elif key == ord('s'):
                self._save_current_wall(result)
            elif key == ord('r'):
                self._generate_room_model()
        
        self.camera.release()
        cv2.destroyAllWindows()
    
    def process_frame(self, frame: np.ndarray) -> Dict:
        self.frame_count += 1
        
        # Object detection
        detections = self.object_detector.detect_comprehensive(frame)
        
        # Depth estimation (every 3rd frame)
        depth_map = None
        point_cloud = None
        wall_plane = None
        
        if self.frame_count % 3 == 0:
            depth_map = self.depth_estimator.estimate(frame)
            point_cloud = self.pcd_processor.depth_to_pointcloud(depth_map, frame)
            
            if len(point_cloud.points) > 100:
                point_cloud, wall_plane = self.pcd_processor.extract_wall_plane(point_cloud)
        
        return {
            'frame': frame,
            'detections': detections,
            'depth_map': depth_map,
            'point_cloud': point_cloud,
            'wall_plane': wall_plane
        }
    
    def _save_current_wall(self, result: Dict):
        if result['point_cloud'] is None:
            print("No point cloud available")
            return
        
        scan = WallScan(
            frame_id=self.frame_count,
            rgb_image=result['frame'],
            depth_map=result['depth_map'],
            point_cloud=result['point_cloud'],
            detections=result['detections'],
            plane_equation=result['wall_plane']
        )
        
        self.stitcher.add_wall(scan)
        print(f"✓ Wall {len(self.stitcher.walls)} saved")
    
    def _generate_room_model(self):
        print("Generating room model...")
        mesh = self.stitcher.generate_room_mesh()
        
        if mesh:
            o3d.io.write_triangle_mesh("room_model.ply", mesh)
            print("✓ Room model saved to room_model.ply")
            o3d.visualization.draw_geometries([mesh])
        else:
            print("Need at least 2 walls")
    
    def _visualize_results(self, frame: np.ndarray, result: Dict) -> np.ndarray:
        vis = frame.copy()
        
        # Draw object detections - handle both list and dict formats
        detections_data = result['detections']
        
        if isinstance(detections_data, dict):
            # Extract all detections from dict
            all_dets = []
            if 'wall_elements' in detections_data:
                all_dets.extend(detections_data['wall_elements'])
            if 'general_objects' in detections_data:
                all_dets.extend(detections_data['general_objects'])
        else:
            all_dets = detections_data
        
        # Draw boxes
        for det in all_dets:
            bbox = det['bbox']
            x1, y1, x2, y2 = map(int, bbox)
            
            # Color code: wall elements = red, general = green
            color = (0, 0, 255) if det.get('type') == 'wall_element' else (0, 255, 0)
            
            cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)
            
            label = f"{det['class']}: {det['confidence']:.2f}"
            cv2.putText(vis, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Overlay depth
        if result['depth_map'] is not None:
            depth_colored = cv2.applyColorMap(
                (result['depth_map'] * 255).astype(np.uint8),
                cv2.COLORMAP_PLASMA
            )
            vis = cv2.addWeighted(vis, 0.7, depth_colored, 0.3, 0)
        
        # Instructions
        cv2.putText(vis, "Press 'S' to save wall, 'R' for room model, 'Q' to quit",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(vis, f"Walls saved: {len(self.stitcher.walls)}",
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return vis


if __name__ == "__main__":
    from dual_detection_service import DualDetectionService
    import os
    
    # Initialize detector with optional wall model
    wall_model = "wall_elements_specialized.pt" if os.path.exists("wall_elements_specialized.pt") else None
    detector = DualDetectionService(wall_model_path=wall_model)
    
    # Create scanner
    scanner = ArcRealTimeScanner(detector)
    
    # Start scanning
    scanner.start_scanning()