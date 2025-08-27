#!/usr/bin/env python3
"""
Create a simple logo for Kommo widget with exact dimensions 130x100px
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_logo():
    # Create image with exact dimensions Kommo requires
    width, height = 130, 100
    
    # Create a new image with white background
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Add a border
    draw.rectangle([0, 0, width-1, height-1], outline='#007bff', width=2)
    
    # Add text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        # Fallback to basic font
        font = ImageFont.load_default()
    
    # Add "AI" text
    text = "AI"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center the text
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text with blue color
    draw.text((x, y), text, fill='#007bff', font=font)
    
    # Add "Chat" text below
    text2 = "Chat"
    text2_bbox = draw.textbbox((0, 0), text2, font=font)
    text2_width = text2_bbox[2] - text2_bbox[0]
    text2_height = text2_bbox[3] - text2_bbox[1]
    
    # Center the second text
    x2 = (width - text2_width) // 2
    y2 = y + text_height + 5
    
    # Draw second text
    draw.text((x2, y2), text2, fill='#007bff', font=font)
    
    # Save the image
    output_path = "widgets/shared/images/logo.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path, "PNG")
    
    print(f"✅ Logo created successfully at: {output_path}")
    print(f"📏 Dimensions: {width}x{height} pixels (Kommo requirement)")
    print(f"🎨 Simple AI Chat logo with blue border and text")
    
    return output_path

if __name__ == "__main__":
    try:
        create_simple_logo()
    except Exception as e:
        print(f"❌ Error creating logo: {e}")
        print("💡 Try installing Pillow: pip install Pillow")
