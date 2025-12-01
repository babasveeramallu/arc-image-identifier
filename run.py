#!/usr/bin/env python3
"""
Arc - AI Wall Scanner
Production launcher script with automatic port detection and proper error handling.
"""

import sys
import os
from pathlib import Path
import uvicorn
import socket

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def find_free_port(start_port=8000):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    return start_port

def check_dependencies():
    """Check if required dependencies are installed."""
    required = ['fastapi', 'uvicorn', 'pydantic', 'cv2', 'numpy']
    missing = []
    
    for package in required:
        try:
            if package == 'cv2':
                __import__('cv2')
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    return True

def main():
    """Main entry point."""
    if not check_dependencies():
        sys.exit(1)
    
    try:
        from src.api.main import app
        
        port = int(os.getenv("PORT", find_free_port(8000)))
        host = os.getenv("HOST", "0.0.0.0")
        debug = os.getenv("DEBUG", "false").lower() == "true"
        
        print("=" * 70)
        print("Arc - AI Wall Scanner")
        print("=" * 70)
        print(f"Server: http://localhost:{port}")
        print(f"API Docs: http://localhost:{port}/docs")
        print(f"API Reference: http://localhost:{port}/redoc")
        print(f"Health Check: http://localhost:{port}/health")
        print("=" * 70)
        print()
        print("Open the URL in your browser to start scanning")
        print("Press Ctrl+C to stop the server")
        print("=" * 70)
        print()
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="debug" if debug else "info",
            access_log=True,
            reload=debug
        )
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're in the project directory")
        print("Try: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nArc server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
