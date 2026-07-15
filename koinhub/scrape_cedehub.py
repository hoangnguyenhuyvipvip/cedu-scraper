import requests
from bs4 import BeautifulSoup
import json
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

URL = "https://cedehub.io"

res = requests.get(URL, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# --- Messages ---
messages = {}
messages["hero_title"]   = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
messages["headings"]     = [h.get_text(strip=True) for h in soup.find_all(["h2", "h3"])]
messages["descriptions"] = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
messages["buttons"]      = [b.get_text(strip=True) for b in soup.find_all("a") if b.get_text(strip=True)]

# --- Tìm CSS links ---
css_links = []
for link in soup.find_all("link"):
    href = link.get("href", "")
    if ".css" in href or "stylesheet" in link.get("rel", []):
        if href.startswith("http"):
            css_links.append(href)
        elif href:
            if not href.startswith("/"):
                href = "/" + href
            css_links.append("https://cedehub.io" + href)

print(f"CSS links tìm thấy: {len(css_links)} file")

# --- Lấy màu, font, CSS vars ---
colors = set()
fonts = set()
css_vars = {}

for css_url in css_links:
    try:
        r = requests.get(css_url, headers=headers, timeout=15)
        css_text = r.text
        print(f"Tải CSS: {css_url} ({len(css_text)} chars)")
        colors.update(re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}\b|rgba?\([^)]+\)|hsla?\([^)]+\)', css_text))
        fonts.update(re.findall(r'font-family\s*:\s*([^;}{]+)', css_text))
        for k, v in re.findall(r'(-{2}[\w-]+)\s*:\s*([^;}\n]+)', css_text):
            css_vars[k.strip()] = v.strip()
    except Exception as e:
        print(f"Lỗi: {e}")

# --- Màu từ inline style ---
for tag in soup.find_all(style=True):
    found = re.findall(r'#[0-9a-fA-F]{6}|rgba?\([^)]+\)', tag["style"])
    colors.update(found)

design_tokens = {
    k: v for k, v in css_vars.items()
    if any(x in k.lower() for x in ["color", "font", "radius", "spacing", "shadow", "bg", "text", "border"])
}

result = {
    "messages": messages,
    "colors": sorted(list(colors)),
    "fonts": [f.strip() for f in list(fonts)][:20],
    "design_tokens": design_tokens
}

with open("cedehub_design.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\nDone!")
print(f"- Hero title: {messages['hero_title']}")
print(f"- Headings: {len(messages['headings'])} mục")
print(f"- Buttons: {len(messages['buttons'])} nút")
print(f"- Colors: {len(result['colors'])} màu")
print(f"- Fonts: {len(result['fonts'])} font")
print(f"- Design tokens: {len(design_tokens)} biến")