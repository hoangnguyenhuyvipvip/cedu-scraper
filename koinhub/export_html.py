import json

with open("cedehub_design.json", "r", encoding="utf-8") as f:
    data = json.load(f)

messages = data.get("messages", {})
colors = data.get("colors", [])
fonts = data.get("fonts", [])
tokens = data.get("design_tokens", {})

# Tạo ô màu cho mỗi color
color_boxes = ""
for c in colors:
    color_boxes += f"""
    <div class="color-item">
        <div class="color-box" style="background:{c}"></div>
        <span>{c}</span>
    </div>"""

# Tạo bảng design tokens
token_rows = ""
for k, v in tokens.items():
    token_rows += f"<tr><td>{k}</td><td>{v}</td></tr>"

# Tạo danh sách headings
headings_list = "".join([f"<li>{h}</li>" for h in messages.get("headings", [])])

# Tạo danh sách buttons
buttons_list = "".join([f"<span class='badge'>{b}</span>" for b in messages.get("buttons", [])])

# Tạo danh sách fonts
fonts_list = "".join([f"<li>{f}</li>" for f in fonts])

html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Cedehub.io — Design Document</title>
    <style>
        body {{ font-family: sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #0f0f0f; color: #eee; }}
        h1 {{ color: #fff; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        h2 {{ color: #aaa; margin-top: 40px; }}
        .color-grid {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 16px; }}
        .color-item {{ display: flex; flex-direction: column; align-items: center; gap: 6px; }}
        .color-box {{ width: 60px; height: 60px; border-radius: 8px; border: 1px solid #333; }}
        span {{ font-size: 11px; color: #aaa; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
        th, td {{ padding: 8px 12px; border: 1px solid #333; font-size: 13px; text-align: left; }}
        th {{ background: #1a1a1a; color: #fff; }}
        td {{ color: #ccc; }}
        ul {{ line-height: 2; color: #ccc; }}
        .badge {{ display: inline-block; background: #1a1a1a; border: 1px solid #333; border-radius: 20px; padding: 4px 12px; margin: 4px; font-size: 13px; color: #eee; }}
        .hero {{ background: #1a1a1a; border-radius: 12px; padding: 24px; margin: 20px 0; }}
        .hero h3 {{ margin: 0 0 8px; color: #aaa; font-size: 13px; text-transform: uppercase; }}
        .hero p {{ margin: 0; font-size: 22px; font-weight: bold; color: #fff; }}
    </style>
</head>
<body>
    <h1>Cedehub.io — Design Document</h1>

    <div class="hero">
        <h3>Hero Title</h3>
        <p>{messages.get('hero_title', '')}</p>
    </div>

    <h2>Headings</h2>
    <ul>{headings_list}</ul>

    <h2>Buttons / CTAs</h2>
    <div>{buttons_list}</div>

    <h2>Color Palette ({len(colors)} màu)</h2>
    <div class="color-grid">{color_boxes}</div>

    <h2>Typography / Fonts</h2>
    <ul>{fonts_list}</ul>

    <h2>Design Tokens ({len(tokens)} biến)</h2>
    <table>
        <tr><th>Token</th><th>Value</th></tr>
        {token_rows}
    </table>
</body>
</html>"""

with open("cedehub_design.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Đã xuất cedehub_design.html")