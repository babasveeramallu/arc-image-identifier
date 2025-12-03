"""
Simple Web Demo - Works without Open3D
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import cv2
import numpy as np
import json
import base64
from dual_detection_service import DualDetectionService

app = FastAPI(title="Arc Detection Demo")

# Initialize detector
detector = DualDetectionService()

@app.get("/")
async def root():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>Arc Detection Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        video { width: 640px; height: 480px; border: 2px solid #333; }
        .controls { margin: 20px 0; }
        button { padding: 10px 20px; margin: 5px; font-size: 16px; }
        .results { margin: 20px 0; padding: 10px; background: #f5f5f5; }
        canvas { border: 2px solid #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Arc - AI Detection Demo</h1>
        <p>Real-time object detection for wall elements</p>
        
        <video id="video" autoplay playsinline></video>
        <br>
        <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
        
        <div class="controls">
            <button onclick="startCamera()">Start Camera</button>
            <button onclick="captureFrame()">Detect Objects</button>
        </div>
        
        <div class="results" id="results">
            Ready to detect objects...
        </div>
    </div>

    <script>
        let video, canvas, ctx;
        
        async function startCamera() {
            video = document.getElementById('video');
            canvas = document.getElementById('canvas');
            ctx = canvas.getContext('2d');
            
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: 'environment', width: 640, height: 480 }
                });
                video.srcObject = stream;
                document.getElementById('results').textContent = 'Camera started - click Detect Objects';
            } catch (err) {
                document.getElementById('results').textContent = 'Camera access failed: ' + err.message;
            }
        }
        
        async function captureFrame() {
            if (!video) {
                alert('Start camera first');
                return;
            }
            
            // Draw video frame to canvas
            ctx.drawImage(video, 0, 0, 640, 480);
            
            // Convert to blob
            canvas.toBlob(async (blob) => {
                const formData = new FormData();
                formData.append('file', blob, 'frame.jpg');
                
                document.getElementById('results').textContent = 'Processing...';
                
                try {
                    const response = await fetch('/detect', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    displayResults(result);
                } catch (err) {
                    document.getElementById('results').textContent = 'Detection failed: ' + err.message;
                }
            }, 'image/jpeg', 0.8);
        }
        
        function displayResults(result) {
            const resultsDiv = document.getElementById('results');
            
            let html = '<h3>Detection Results:</h3>';
            
            if (result.wall_elements && result.wall_elements.length > 0) {
                html += '<h4>Wall Elements Found:</h4><ul>';
                result.wall_elements.forEach(det => {
                    html += `<li>${det.class} (${(det.confidence * 100).toFixed(1)}%)</li>`;
                });
                html += '</ul>';
            }
            
            if (result.general_objects && result.general_objects.length > 0) {
                html += '<h4>General Objects:</h4><ul>';
                result.general_objects.slice(0, 5).forEach(det => {
                    html += `<li>${det.class} (${(det.confidence * 100).toFixed(1)}%)</li>`;
                });
                if (result.general_objects.length > 5) {
                    html += `<li>... and ${result.general_objects.length - 5} more</li>`;
                }
                html += '</ul>';
            }
            
            html += `<p><strong>Total Objects:</strong> ${result.total_objects}</p>`;
            
            resultsDiv.innerHTML = html;
        }
    </script>
</body>
</html>
    """)

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    """Detect objects in uploaded image"""
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return {"error": "Could not decode image"}
    
    # Detect objects
    results = detector.detect_comprehensive(frame)
    
    return {
        "wall_elements": results.get('wall_elements', []),
        "general_objects": results.get('general_objects', []),
        "total_objects": results.get('total_objects', 0),
        "success": True
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Arc Detection Demo...")
    print("Open: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)