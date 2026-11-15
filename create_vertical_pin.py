import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = r"C:\Users\1247617\.gemini\antigravity\scratch\wildlight_showcase\assets\backdrops"
OUTPUT_PATH = os.path.join(ASSETS_DIR, "mega_holiday_bundle_vertical.jpg")

WIDTH, HEIGHT = 2000, 3000 # 2:3 Pinterest optimal ratio

def get_font(size, bold=False):
    font_paths = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def generate_vertical_pin():
    # Base dark luxury navy canvas
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 30))
    draw = ImageDraw.Draw(canvas)

    # 1. Header Banner
    draw.rectangle([0, 0, WIDTH, 360], fill=(5, 8, 20))
    f_brand = get_font(38, bold=True)
    f_title = get_font(64, bold=True)
    f_sub = get_font(36, bold=False)

    draw.text((WIDTH//2, 80), "WILDLIGHT DIGITAL STUDIO • COMMERCIAL VAULT", fill=(245, 158, 11), font=f_brand, anchor="mm")
    draw.text((WIDTH//2, 180), "HOLIDAY MINI-SESSION BUNDLE", fill=(255, 255, 255), font=f_title, anchor="mm")
    draw.text((WIDTH//2, 270), "8x 8K Luxury Studio Backdrops + 3x Falling Snow Overlays", fill=(203, 213, 225), font=f_sub, anchor="mm")

    # 2. Three Stacked Featured Backdrop Previews
    scenes = [
        ("gingerbread_cottage_studio.jpg", "Whimsical Gingerbread Bakery"),
        ("luxury_christmas_studio.jpg", "Emerald Velvet & Golden Hearth"),
        ("scandi_frosted_fireplace.jpg", "Nordic Scandi Frosted Brick Hearth")
    ]

    img_w, img_h = 1860, 680
    start_y = 400
    gap = 20

    f_badge = get_font(34, bold=True)

    for i, (fname, label) in enumerate(scenes):
        fpath = os.path.join(ASSETS_DIR, fname)
        if os.path.exists(fpath):
            im = Image.open(fpath).convert("RGB")
            im = im.resize((img_w, img_h), Image.Resampling.LANCZOS)
            y_pos = start_y + i * (img_h + gap)
            canvas.paste(im, (70, y_pos))

            # Overlay Badge on each preview
            draw.rectangle([90, y_pos + 20, 90 + 750, y_pos + 85], fill=(15, 23, 42, 230), outline=(245, 158, 11), width=2)
            draw.text((110, y_pos + 33), f"★ {label}", fill=(245, 158, 11), font=f_badge)

    # 3. Bottom Value Callout & CTA Footer
    footer_y = start_y + 3 * (img_h + gap) + 10
    draw.rectangle([0, footer_y, WIDTH, HEIGHT], fill=(5, 8, 20))

    # Floating CTA Box
    cta_box_w, cta_box_h = 1860, 360
    cta_bx, cta_by = 70, footer_y + 40
    draw.rectangle([cta_bx, cta_by, cta_bx + cta_box_w, cta_by + cta_box_h], fill=(15, 23, 42), outline=(16, 185, 129), width=5)

    f_deal_h = get_font(56, bold=True)
    f_deal_sub = get_font(36, bold=False)
    f_cta_btn = get_font(46, bold=True)

    draw.text((WIDTH//2, cta_by + 75), "8000 x 5333 PX • 300 DPI • PHOTOSHOP & CANVA", fill=(255, 255, 255), font=f_deal_h, anchor="mm")
    draw.text((WIDTH//2, cta_by + 160), "Unlimited Commercial Studio License for Client Sessions & Prints", fill=(203, 213, 225), font=f_deal_sub, anchor="mm")

    # Green Button
    btn_w, btn_h = 900, 100
    btn_x = (WIDTH - btn_w)//2
    btn_y = cta_by + 225
    draw.rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], fill=(16, 185, 129))
    draw.text((WIDTH//2, btn_y + 50), "INSTANT DOWNLOAD • $19.99 ➔", fill=(10, 15, 30), font=f_cta_btn, anchor="mm")

    canvas.save(OUTPUT_PATH, "JPEG", quality=92)
    print(f"[PIN-GEN] 2:3 Vertical Pinterest Pin generated: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_vertical_pin()
