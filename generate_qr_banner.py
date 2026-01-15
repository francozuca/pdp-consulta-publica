#!/usr/bin/env python3
"""
Script to generate a QR code banner image for PDP Consulta Pública
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
URL = "https://lemon-coast-081b49410.1.azurestaticapps.net/"
MAIN_TEXT = "IMPORTANTE! El futuro de PDP depende de vos"
SUBTEXT = "Votá en la consulta pública a favor de Pueblos del Plata"
DISCLAIMER = "Iniciativa de vecinos de PDP"
OUTPUT_FILE = "src/qr_banner.png"
LOGO_PATH = None  # Set to logo file path if available, e.g., "src/logo.png"

# Image dimensions (portrait orientation)
BANNER_WIDTH = 800
BANNER_HEIGHT = 1200
QR_SIZE = 450  # Increased size
LOGO_SIZE = 200
PADDING = 50

def generate_qr_code(url, size):
    """Generate a QR code image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)
    return qr_img

def create_gradient_background(width, height):
    """Create a gradient background from teal/blue to green"""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    # Colors inspired by the logo: teal/blue at top, green at bottom
    top_color = (70, 150, 180)  # Teal/blue
    bottom_color = (60, 160, 100)  # Green
    
    for y in range(height):
        # Calculate interpolation factor
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        
        for x in range(width):
            pixels[x, y] = (r, g, b)
    
    return img

def load_logo(path, max_size):
    """Load and resize logo if available"""
    if path and os.path.exists(path):
        try:
            logo = Image.open(path)
            # Resize maintaining aspect ratio
            logo.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            return logo
        except Exception as e:
            print(f"Warning: Could not load logo: {e}")
    return None

def get_font(size, bold=False):
    """Try to get a nice font, fallback to default if not available"""
    try:
        if bold:
            # Try common bold fonts
            font_paths = [
                "/System/Library/Fonts/Helvetica.ttc",  # macOS
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
                "C:/Windows/Fonts/arialbd.ttf",  # Windows
            ]
            for path in font_paths:
                if os.path.exists(path):
                    return ImageFont.truetype(path, size)
        else:
            # Try common regular fonts
            font_paths = [
                "/System/Library/Fonts/Helvetica.ttc",  # macOS
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
                "C:/Windows/Fonts/arial.ttf",  # Windows
            ]
            for path in font_paths:
                if os.path.exists(path):
                    return ImageFont.truetype(path, size)
    except:
        pass
    # Fallback to default font
    return ImageFont.load_default()

def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def create_banner():
    """Create the banner image with QR code and text"""
    # Create base image with gradient background
    img = create_gradient_background(BANNER_WIDTH, BANNER_HEIGHT)
    draw = ImageDraw.Draw(img)
    
    # Load logo if available
    logo = load_logo(LOGO_PATH, LOGO_SIZE)
    
    # Calculate vertical layout
    current_y = PADDING
    
    # Add logo at the top (centered)
    if logo:
        logo_x = (BANNER_WIDTH - logo.width) // 2
        # Create a white/light background circle or rounded rectangle for logo
        logo_bg_size = logo.width + 40
        logo_bg = Image.new('RGBA', (logo_bg_size, logo_bg_size), (255, 255, 255, 200))
        mask = Image.new('L', (logo_bg_size, logo_bg_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([(0, 0), (logo_bg_size, logo_bg_size)], fill=255)
        logo_bg.putalpha(mask)
        
        logo_bg_x = (BANNER_WIDTH - logo_bg_size) // 2
        img.paste(logo_bg, (logo_bg_x, current_y), logo_bg)
        logo_x = (BANNER_WIDTH - logo.width) // 2
        logo_y = current_y + 20
        img.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)
        current_y += logo_bg_size + PADDING
    
    # Load fonts
    main_font_size = 42
    subtext_font_size = 28
    disclaimer_font_size = 18
    main_font = get_font(main_font_size, bold=False)  # Changed to regular (not bold)
    subtext_font = get_font(subtext_font_size, bold=False)
    disclaimer_font = get_font(disclaimer_font_size, bold=False)
    
    # Draw main text (centered)
    main_text_lines = wrap_text(MAIN_TEXT, main_font, BANNER_WIDTH - (PADDING * 2))
    text_height_total = sum([main_font.getbbox(line)[3] - main_font.getbbox(line)[1] + 10 
                             for line in main_text_lines]) - 10
    
    text_start_y = current_y
    y_offset = text_start_y
    
    for line in main_text_lines:
        bbox = main_font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (BANNER_WIDTH - text_width) // 2
        
        # Draw text with white outline for better visibility
        for adj in range(-2, 3):
            for adj2 in range(-2, 3):
                if adj != 0 or adj2 != 0:
                    draw.text((text_x + adj, y_offset + adj2), line, 
                             fill='white', font=main_font)
        draw.text((text_x, y_offset), line, fill='white', font=main_font)
        y_offset += text_height + 10
    
    current_y = y_offset + PADDING
    
    # Draw subtext (centered, below main text)
    subtext_lines = wrap_text(SUBTEXT, subtext_font, BANNER_WIDTH - (PADDING * 2))
    subtext_y_offset = current_y
    
    for line in subtext_lines:
        bbox = subtext_font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (BANNER_WIDTH - text_width) // 2
        
        # Draw text with subtle white outline for better visibility
        for adj in range(-1, 2):
            for adj2 in range(-1, 2):
                if adj != 0 or adj2 != 0:
                    draw.text((text_x + adj, subtext_y_offset + adj2), line, 
                             fill='white', font=subtext_font)
        draw.text((text_x, subtext_y_offset), line, fill='white', font=subtext_font)
        subtext_y_offset += text_height + 8
    
    current_y = subtext_y_offset + PADDING * 2
    
    # Generate QR code
    qr_img = generate_qr_code(URL, QR_SIZE)
    
    # Add white background for QR code
    qr_bg_size = QR_SIZE + 30
    qr_bg = Image.new('RGB', (qr_bg_size, qr_bg_size), color='white')
    qr_bg_x = (BANNER_WIDTH - qr_bg_size) // 2
    qr_bg_y = current_y
    img.paste(qr_bg, (qr_bg_x, qr_bg_y))
    
    # Paste QR code (centered)
    qr_x = (BANNER_WIDTH - QR_SIZE) // 2
    qr_y = current_y + 15
    img.paste(qr_img, (qr_x, qr_y))
    
    current_y = qr_y + QR_SIZE + PADDING
    
    # Draw disclaimer (centered, at bottom)
    bbox = disclaimer_font.getbbox(DISCLAIMER)
    disclaimer_width = bbox[2] - bbox[0]
    disclaimer_x = (BANNER_WIDTH - disclaimer_width) // 2
    disclaimer_y = BANNER_HEIGHT - PADDING - (bbox[3] - bbox[1]) - 10
    
    # Draw disclaimer with subtle background
    disclaimer_bg_padding = 10
    disclaimer_bg_height = bbox[3] - bbox[1] + 10
    disclaimer_bg_width = disclaimer_width + disclaimer_bg_padding * 2
    
    # Create semi-transparent background
    disclaimer_bg = Image.new('RGBA', (disclaimer_bg_width, disclaimer_bg_height), (255, 255, 255, 200))
    disclaimer_bg_x = (BANNER_WIDTH - disclaimer_bg_width) // 2
    img.paste(disclaimer_bg, (disclaimer_bg_x, disclaimer_y - 5), disclaimer_bg)
    
    draw.text((disclaimer_x, disclaimer_y), DISCLAIMER, fill='#333333', font=disclaimer_font)
    
    # Save image
    img.save(OUTPUT_FILE, 'PNG')
    print(f"Banner image created successfully: {OUTPUT_FILE}")
    print(f"QR Code URL: {URL}")
    print(f"Main text: {MAIN_TEXT}")
    print(f"Disclaimer: {DISCLAIMER}")
    if logo:
        print(f"Logo included: {LOGO_PATH}")

if __name__ == "__main__":
    create_banner()
