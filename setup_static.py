"""
Setup static directory with textures for web demo
Run this before launching web app: python setup_static.py
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

def create_static_structure():
    """Create necessary directories"""
    dirs = [
        "static",
        "static/textures",
        "static/models"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created {dir_path}/")

def generate_texture_placeholder(name, color, size=(512, 512)):
    """Generate placeholder texture images"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Add texture name
    try:
        from PIL import ImageFont
        font = ImageFont.load_default()
    except:
        font = None
    
    # Center text
    text = name.replace('_', ' ').upper()
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
        draw.text(position, text, fill=(255, 255, 255), font=font)
    
    return img

def create_brick_texture():
    """Create brick pattern"""
    img = Image.new('RGB', (512, 512))
    draw = ImageDraw.Draw(img)
    
    # Brick colors
    brick_color = (180, 65, 50)
    mortar_color = (200, 200, 200)
    
    img.paste(brick_color, (0, 0, 512, 512))
    
    # Draw mortar lines
    brick_height = 64
    brick_width = 128
    mortar_width = 8
    
    for y in range(0, 512, brick_height + mortar_width):
        draw.rectangle([0, y, 512, y + mortar_width], fill=mortar_color)
        
    offset = 0
    for y in range(0, 512, brick_height + mortar_width):
        for x in range(offset, 512, brick_width + mortar_width):
            draw.rectangle([x, y, x + mortar_width, y + brick_height], fill=mortar_color)
        offset = brick_width // 2 if offset == 0 else 0
    
    return img

def create_wood_texture():
    """Create wood grain pattern"""
    img = Image.new('RGB', (512, 512))
    pixels = img.load()
    
    # Wood colors
    base_color = (139, 90, 43)
    
    for x in range(512):
        for y in range(512):
            # Add grain variation
            variation = int(20 * np.sin(x / 10) * np.cos(y / 50))
            r = max(0, min(255, base_color[0] + variation))
            g = max(0, min(255, base_color[1] + variation))
            b = max(0, min(255, base_color[2] + variation))
            pixels[x, y] = (r, g, b)
    
    return img

def create_concrete_texture():
    """Create concrete pattern"""
    img = Image.new('RGB', (512, 512))
    pixels = img.load()
    
    # Concrete gray
    base_color = (128, 128, 128)
    
    # Add noise
    np.random.seed(42)
    for x in range(512):
        for y in range(512):
            noise = np.random.randint(-30, 30)
            gray = max(0, min(255, base_color[0] + noise))
            pixels[x, y] = (gray, gray, gray)
    
    return img

def generate_all_textures():
    """Generate all texture files"""
    textures = {
        'brick.jpg': create_brick_texture(),
        'wood.jpg': create_wood_texture(),
        'concrete.jpg': create_concrete_texture(),
        'white_paint.jpg': generate_texture_placeholder('white_paint', (255, 255, 255)),
        'beige_paint.jpg': generate_texture_placeholder('beige_paint', (245, 245, 220)),
    }
    
    for filename, img in textures.items():
        path = f"static/textures/{filename}"
        img.save(path, quality=95)
        print(f"Created {path}")

def create_placeholder_model():
    """Create placeholder 3D model file"""
    # Simple PLY file with a cube
    ply_content = """ply
format ascii 1.0
element vertex 8
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
element face 12
property list uchar int vertex_indices
end_header
-1 -1 -1 200 200 200
1 -1 -1 200 200 200
1 1 -1 200 200 200
-1 1 -1 200 200 200
-1 -1 1 200 200 200
1 -1 1 200 200 200
1 1 1 200 200 200
-1 1 1 200 200 200
3 0 1 2
3 0 2 3
3 4 5 6
3 4 6 7
3 0 4 5
3 0 5 1
3 1 5 6
3 1 6 2
3 2 6 7
3 2 7 3
3 3 7 4
3 3 4 0
"""
    
    with open("static/models/placeholder.ply", 'w') as f:
        f.write(ply_content)
    
    print("Created static/models/placeholder.ply")

def main():
    print("=== Setting up Arc Web Demo Static Files ===\n")
    
    print("1. Creating directory structure...")
    create_static_structure()
    
    print("\n2. Generating texture images...")
    generate_all_textures()
    
    print("\n3. Creating placeholder 3D model...")
    create_placeholder_model()
    
    print("\nSetup complete!")
    print("\nYou can now run: python run_web_demo.py")

if __name__ == "__main__":
    main()