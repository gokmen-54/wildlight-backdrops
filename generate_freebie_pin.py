import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_freebie_pin():
    width = 2000
    height = 3000
    pin = Image.new("RGBA", (width, height), (15, 23, 42, 255)) # Dark slate navy

    # Load base backdrop
    base_dir = r"C:\Users\1247617\.gemini\antigravity\scratch\wildlight_showcase"
    backdrop_path = os.path.join(base_dir, "assets", "backdrops", "luxury_christmas_studio.jpg")
    snow_path = os.path.join(base_dir, "assets", "freebie", "Wildlight_Free_4K_Holiday_Snow_Overlay.png")

    if os.path.exists(backdrop_path):
        bg = Image.open(backdrop_path).convert("RGBA")
        # Crop & resize to fit center canvas
        bg_w = 1800
        bg_h = 1350
        bg_resized = bg.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
        
        # Apply snow on right half to show before/after
        if os.path.exists(snow_path):
            snow = Image.open(snow_path).convert("RGBA")
            snow_resized = snow.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
            
            # Composite snow over right half
            mask = Image.new("L", (bg_w, bg_h), 0)
            draw_m = ImageDraw.Draw(mask)
            draw_m.rectangle([bg_w // 2, 0, bg_w, bg_h], fill=255)
            
            snow_composite = Image.composite(snow_resized, Image.new("RGBA", (bg_w, bg_h), (0,0,0,0)), mask)
            bg_combined = Image.alpha_composite(bg_resized, snow_composite)
        else:
            bg_combined = bg_resized

        # Paste onto pin canvas
        pin.paste(bg_combined, (100, 750), bg_combined)

        # Draw a sleek divider line between before and after
        draw = ImageDraw.Draw(pin)
        divider_x = 100 + (bg_w // 2)
        draw.line([(divider_x, 750), (divider_x, 750 + bg_h)], fill=(250, 204, 21, 240), width=6)
        
        # Badges on image
        # BEFORE pill
        draw.rounded_rectangle([150, 780, 420, 860], radius=16, fill=(15, 23, 42, 220), outline=(100, 116, 139, 200), width=3)
        # AFTER pill
        draw.rounded_rectangle([divider_x + 50, 780, divider_x + 500, 860], radius=16, fill=(220, 38, 38, 230), outline=(254, 202, 202, 220), width=3)
    else:
        draw = ImageDraw.Draw(pin)

    # Load system fonts
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 46)
        font_title = ImageFont.truetype("arialbd.ttf", 94)
        font_subtitle = ImageFont.truetype("arial.ttf", 52)
        font_pills = ImageFont.truetype("arialbd.ttf", 42)
        font_features = ImageFont.truetype("arialbd.ttf", 48)
        font_cta = ImageFont.truetype("arialbd.ttf", 64)
    except:
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_pills = ImageFont.load_default()
        font_features = ImageFont.load_default()
        font_cta = ImageFont.load_default()

    draw = ImageDraw.Draw(pin)

    # Top Eyebrow Pill
    draw.rounded_rectangle([500, 100, 1500, 200], radius=50, fill=(185, 28, 28, 255), outline=(252, 165, 165, 255), width=4)
    draw.text((1000, 150), "🎁 100% FREE HOLIDAY GIFT • ZERO COST", font=font_badge, fill=(255, 255, 255, 255), anchor="mm")

    # Big Main Headline
    draw.text((1000, 320), "FREE 4K FALLING SNOW", font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((1000, 440), "PHOTOSHOP OVERLAY PNG", font=font_title, fill=(250, 204, 21, 255), anchor="mm")

    # Subtitle
    draw.text((1000, 560), "Ultra-Sharp Transparent Alpha Channel • Instant Drag & Drop", font=font_subtitle, fill=(203, 213, 225, 255), anchor="mm")
    draw.text((1000, 640), "Transform Portraits into Magical Winter Scenes in 1-Click", font=font_subtitle, fill=(148, 163, 184, 255), anchor="mm")

    # Image Labels
    draw.text((285, 820), "ORIGINAL RAW", font=font_pills, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((divider_x + 275, 820), "+ 4K SNOW OVERLAY", font=font_pills, fill=(255, 255, 255, 255), anchor="mm")

    # Feature Checklist Box below image (2180 to 2580)
    box_top = 2160
    draw.rounded_rectangle([100, box_top, 1900, box_top + 380], radius=24, fill=(30, 41, 59, 200), outline=(51, 65, 85, 255), width=3)
    
    features = [
        "✓ 4000x2667 px Ultra HD Transparent PNG (Works on Any Background)",
        "✓ Compatible with Photoshop, Photoshop Elements, Canva & Procreate",
        "✓ Commercial Studio License Included • Perfect for Holiday Mini-Sessions",
        "✓ Includes Bonus 40% OFF Coupon for Complete 8K Holiday Backdrop Vault"
    ]
    
    for i, feat in enumerate(features):
        color = (250, 204, 21, 255) if i == 3 else (241, 245, 249, 255)
        draw.text((160, box_top + 50 + (i * 80)), feat, font=font_features, fill=color)

    # Bottom Big CTA Button
    cta_top = 2600
    draw.rounded_rectangle([200, cta_top, 1800, cta_top + 180], radius=90, fill=(234, 179, 8, 255), outline=(254, 240, 138, 255), width=5)
    draw.text((1000, cta_top + 90), "DOWNLOAD 100% FREE NOW →", font=font_cta, fill=(15, 23, 42, 255), anchor="mm")

    # Branding footer
    draw.text((1000, 2860), "Wildlight Backdrops • Official 5-Star Etsy Store • Instant Digital Access", font=font_subtitle, fill=(148, 163, 184, 255), anchor="mm")

    out_path = os.path.join(base_dir, "assets", "backdrops", "free_snow_overlay_pinterest_pin.jpg")
    pin.convert("RGB").save(out_path, "JPEG", quality=95)
    print(f"Generated Freebie Pinterest Pin at: {out_path}")

if __name__ == "__main__":
    create_freebie_pin()
