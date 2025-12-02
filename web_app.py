"""
Arc Web App - FastAPI backend for real-time scanning
"""

from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import cv2
import numpy as np
import json
import base64
from io import BytesIO
from PIL import Image
import asyncio
from dual_detection_service import DualDetectionService
from arc_scanner import DepthEstimator, PointCloudProcessor, WallStitcher
import open3d as o3d

app = FastAPI(title="Arc - Image to 3D Model")

# Initialize services
detector = DualDetectionService()
depth_estimator = DepthEstimator()
pcd_processor = PointCloudProcessor()
stitcher = WallStitcher()

# Texture library
TEXTURES = {
    "white_paint": {"type": "solid", "color": "#FFFFFF"},
    "beige_paint": {"type": "solid", "color": "#F5F5DC"},
    "brick_red": {"type": "pattern", "url": "/static/textures/brick.jpg"},
    "wood_oak": {"type": "pattern", "url": "/static/textures/wood.jpg"},
    "concrete": {"type": "pattern", "url": "/static/textures/concrete.jpg"},
}

@app.get("/")
async def root():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>Arc - Wall Scanner</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .scanner { position: relative; display: inline-block; }
        video { width: 640px; height: 480px; border: 2px solid #333; }
        .overlay { position: absolute; top: 0; left: 0; pointer-events: none; }
        .detection-box { position: absolute; border: 2px solid #00ff00; background: rgba(0,255,0,0.2); }
        .controls { margin: 20px 0; }
        button { padding: 10px 20px; margin: 5px; font-size: 16px; }
        .status { margin: 10px 0; font-weight: bold; }
        .texture-picker { margin: 20px 0; }
        .texture-btn { padding: 10px; margin: 5px; border: 2px solid #ccc; cursor: pointer; }
        .texture-btn.active { border-color: #007bff; }
        #viewer { width: 640px; height: 480px; border: 2px solid #333; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Arc - AI Wall Scanner</h1>
        
        <div class="scanner">
            <video id="video" autoplay playsinline></video>
            <div class="overlay" id="overlay"></div>
        </div>
        
        <div class="controls">
            <button onclick="startScanning()">Start Camera</button>
            <button onclick="captureWall()">Capture Wall</button>
            <button onclick="generateRoom()">Generate Room</button>
            <button onclick="downloadModel()">Download Model</button>
        </div>
        
        <div class="status" id="status">Ready to scan</div>
        
        <div class="texture-picker">
            <h3>Select Texture:</h3>
            <div id="textures"></div>
        </div>
        
        <div id="viewer"></div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let video, canvas, ws;
        let scanning = false;
        let wallCount = 0;
        let selectedTexture = 'white_paint';
        
        // Initialize textures
        const textures = {
            "white_paint": {"type": "solid", "color": "#FFFFFF"},
            "beige_paint": {"type": "solid", "color": "#F5F5DC"},
            "brick_red": {"type": "pattern", "url": "/static/textures/brick.jpg"},
            "wood_oak": {"type": "pattern", "url": "/static/textures/wood.jpg"},
            "concrete": {"type": "pattern", "url": "/static/textures/concrete.jpg"}
        };
        
        function initTextures() {
            const container = document.getElementById('textures');
            Object.keys(textures).forEach(name => {
                const btn = document.createElement('div');
                btn.className = 'texture-btn';
                btn.textContent = name.replace('_', ' ');
                btn.onclick = () => selectTexture(name);
                container.appendChild(btn);
            });
        }
        
        function selectTexture(name) {
            selectedTexture = name;
            document.querySelectorAll('.texture-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }
        
        async function startScanning() {
            video = document.getElementById('video');
            
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: 'environment', width: 640, height: 480 }
                });
                video.srcObject = stream;
                
                // Start WebSocket for real-time processing
                ws = new WebSocket('ws://localhost:8000/ws');
                ws.onmessage = handleDetections;
                
                scanning = true;
                document.getElementById('status').textContent = 'Scanning...';
                
                // Send frames periodically
                setInterval(sendFrame, 200); // 5 FPS
                
            } catch (err) {
                console.error('Camera error:', err);
                document.getElementById('status').textContent = 'Camera access failed';
            }
        }
        
        function sendFrame() {
            if (!scanning || !video) return;
            
            const canvas = document.createElement('canvas');
            canvas.width = 640;
            canvas.height = 480;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, 640, 480);
            
            canvas.toBlob(blob => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    const reader = new FileReader();
                    reader.onload = () => {
                        ws.send(reader.result);
                    };
                    reader.readAsArrayBuffer(blob);
                }
            }, 'image/jpeg', 0.8);
        }
        
        function handleDetections(event) {
            const data = JSON.parse(event.data);
            const overlay = document.getElementById('overlay');
            overlay.innerHTML = '';
            
            // Draw detection boxes
            if (data.detections) {
                Object.values(data.detections).flat().forEach(det => {
                    const box = document.createElement('div');
                    box.className = 'detection-box';
                    box.style.left = det.bbox[0] + 'px';
                    box.style.top = det.bbox[1] + 'px';
                    box.style.width = (det.bbox[2] - det.bbox[0]) + 'px';
                    box.style.height = (det.bbox[3] - det.bbox[1]) + 'px';
                    box.textContent = det.class;
                    overlay.appendChild(box);
                });
            }
        }
        
        async function captureWall() {
            const response = await fetch('/capture-wall', { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                wallCount++;
                document.getElementById('status').textContent = `Wall ${wallCount} captured`;
            }
        }
        
        async function generateRoom() {
            document.getElementById('status').textContent = 'Generating room model...';
            
            const response = await fetch('/generate-room', { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                document.getElementById('status').textContent = 'Room model generated';
                loadRoomModel(result.model_url);
            }
        }
        
        function loadRoomModel(url) {
            // Simple Three.js viewer
            const container = document.getElementById('viewer');
            container.innerHTML = '';
            
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, 640/480, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer();
            
            renderer.setSize(640, 480);
            container.appendChild(renderer.domElement);
            
            // Load model (simplified - would need proper PLY loader)
            const geometry = new THREE.BoxGeometry(2, 2, 2);
            const material = new THREE.MeshBasicMaterial({ 
                color: textures[selectedTexture].color || 0x00ff00 
            });
            const cube = new THREE.Mesh(geometry, material);
            scene.add(cube);
            
            camera.position.z = 5;
            
            function animate() {
                requestAnimationFrame(animate);
                cube.rotation.x += 0.01;
                cube.rotation.y += 0.01;
                renderer.render(scene, camera);
            }
            animate();
        }
        
        async function downloadModel() {
            window.open('/download-model', '_blank');
        }
        
        // Initialize
        initTextures();
    </script>
</body>
</html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive image data
            data = await websocket.receive_bytes()
            
            # Convert to numpy array
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is not None:
                # Process frame
                detections = detector.detect_comprehensive(frame)
                
                # Send results
                await websocket.send_text(json.dumps({
                    "detections": detections,
                    "status": "processed"
                }))
                
    except Exception as e:
        print(f"WebSocket error: {e}")

@app.post("/scan-frame")
async def scan_frame(file: UploadFile = File(...)):
    """Process uploaded frame"""
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Object detection
    detections = detector.detect_comprehensive(frame)
    
    # Depth estimation
    depth_map = depth_estimator.estimate(frame)
    
    # Generate point cloud
    point_cloud = pcd_processor.depth_to_pointcloud(depth_map, frame)
    
    return {
        "detections": detections,
        "depth_available": True,
        "point_count": len(point_cloud.points)
    }

@app.post("/capture-wall")
async def capture_wall():
    """Capture current wall scan"""
    # This would store the current scan
    # For demo, just increment counter
    return {"success": True, "wall_id": len(stitcher.walls) + 1}

@app.post("/generate-room")
async def generate_room():
    """Generate complete room model"""
    try:
        mesh = stitcher.generate_room_mesh()
        
        if mesh:
            # Save mesh
            o3d.io.write_triangle_mesh("static/room_model.ply", mesh)
            return {"success": True, "model_url": "/static/room_model.ply"}
        else:
            return {"success": False, "error": "Need at least 2 walls"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/download-model")
async def download_model():
    """Download room model file"""
    return FileResponse(
        "static/room_model.ply",
        media_type="application/octet-stream",
        filename="room_model.ply"
    )

@app.get("/textures")
async def get_textures():
    """Get available textures"""
    return TEXTURES

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)