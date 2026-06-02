#!/usr/bin/env python3
"""Генерирует брендовые SVG-плейсхолдеры под каждый товар OGR Store."""
import os, re

ASSETS = os.path.join(os.path.dirname(__file__), "assets", "products")
os.makedirs(ASSETS, exist_ok=True)

# (id, category, верхняя подпись, нижняя подпись)
ITEMS = [
    ("ip15-128","iphone","iPhone 15","128 GB"),
    ("ip15-256","iphone","iPhone 15","256 GB"),
    ("ip16-128","iphone","iPhone 16","128 GB"),
    ("ip16-256","iphone","iPhone 16","256 GB"),
    ("ip16p-256","iphone","iPhone 16 Pro","256 GB"),
    ("ip16p-512","iphone","iPhone 16 Pro","512 GB"),
    ("ip16pm-256","iphone","iPhone 16 Pro Max","256 GB"),
    ("ip16pm-1tb","iphone","iPhone 16 Pro Max","1 TB"),
    ("mba13-256","macbook","MacBook Air 13","8/256 GB"),
    ("mba13-512","macbook","MacBook Air 13","16/512 GB"),
    ("mbp14-512","macbook","MacBook Pro 14","16/512 GB"),
    ("mbp14-1tb","macbook","MacBook Pro 14","24/1 TB"),
    ("ipad-air-128","ipad","iPad Air 11","128 GB"),
    ("ipad-air-256","ipad","iPad Air 11","256 GB"),
    ("ipad-pro-256","ipad","iPad Pro 11","256 GB"),
    ("s24-256","samsung","Galaxy S24","256 GB"),
    ("s24u-256","samsung","Galaxy S24 Ultra","256 GB"),
    ("s24u-512","samsung","Galaxy S24 Ultra","512 GB"),
    ("ps5-slim","ps5","PlayStation 5","Slim"),
    ("ps5-pro","ps5","PlayStation 5","Pro"),
    ("aw10-42","watch","Apple Watch S10","42 mm"),
    ("aw10-46","watch","Apple Watch S10","46 mm"),
    ("awu2-49","watch","Apple Watch Ultra 2","49 mm"),
    ("airpods-pro2","acc","AirPods Pro 2","USB-C"),
    ("charger-20w","acc","Apple 20W","USB-C"),
    ("magsafe","acc","MagSafe","Charger"),
    ("case-16pro","acc","Чехол 16 Pro","Silicone"),
]

# крупные иконки устройств (stroke = #C9A24B), исходный viewBox 0 0 100 100,
# (glyph, дополнительный transform для центровки/масштаба под конкретную форму)
GLYPH = {
 "iphone": ('<rect x="35" y="14" width="30" height="72" rx="7"/><line x1="44" y1="79" x2="56" y2="79"/>', ""),
 "macbook":('<rect x="22" y="30" width="56" height="36" rx="3"/><path d="M14 72h72l-6-8H20z"/>', "translate(0,2)"),
 "ipad":   ('<rect x="28" y="16" width="44" height="68" rx="6"/><line x1="44" y1="77" x2="56" y2="77"/>', ""),
 "samsung":('<rect x="35" y="12" width="30" height="76" rx="6"/><line x1="44" y1="81" x2="56" y2="81"/>', ""),
 "ps5":    ('<path d="M22 38h56a16 16 0 0 1 16 16 16 16 0 0 1-16 16H22A16 16 0 0 1 6 54a16 16 0 0 1 16-16z"/><line x1="20" y1="54" x2="32" y2="54"/><line x1="26" y1="48" x2="26" y2="60"/><circle cx="70" cy="48" r="3"/><circle cx="78" cy="56" r="3"/><circle cx="70" cy="60" r="3"/>', "translate(0,4)"),
 "watch":  ('<rect x="34" y="32" width="32" height="36" rx="9"/><path d="M40 32l2-13h16l2 13M40 68l2 13h16l2-13"/>', ""),
 "acc":    ('<path d="M24 56V44a26 26 0 0 1 52 0v12"/><rect x="16" y="54" width="14" height="24" rx="7"/><rect x="70" y="54" width="14" height="24" rx="7"/>', ""),
}

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def svg(cat, top, bot):
    glyph, extra = GLYPH.get(cat, GLYPH["iphone"])
    # центрируем сетку 100x100 в точке (400,300) с масштабом 2.6
    g_transform = f"translate(400,300) scale(2.6) translate(-50,-50) {extra}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
  <defs>
    <radialGradient id="bg" cx="50%" cy="38%" r="75%">
      <stop offset="0%" stop-color="#1C1813"/>
      <stop offset="55%" stop-color="#141210"/>
      <stop offset="100%" stop-color="#0C0B09"/>
    </radialGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F0DBA0"/>
      <stop offset="45%" stop-color="#D9B863"/>
      <stop offset="100%" stop-color="#B68A38"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="#C9A24B" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#C9A24B" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="800" height="800" fill="url(#bg)"/>
  <circle cx="400" cy="300" r="300" fill="url(#glow)"/>
  <rect x="20" y="20" width="760" height="760" rx="28" fill="none" stroke="#C9A24B" stroke-opacity="0.22" stroke-width="1.5"/>
  <g transform="{g_transform}" fill="none" stroke="url(#gold)" stroke-width="2.6"
     stroke-linecap="round" stroke-linejoin="round">{glyph}</g>
  <text x="400" y="600" text-anchor="middle" font-family="Playfair Display, Georgia, serif"
     font-size="46" font-weight="600" fill="url(#gold)">{esc(top)}</text>
  <text x="400" y="648" text-anchor="middle" font-family="Jost, Arial, sans-serif"
     font-size="26" letter-spacing="3" fill="#9C9483">{esc(bot).upper()}</text>
  <text x="400" y="730" text-anchor="middle" font-family="Jost, Arial, sans-serif"
     font-size="22" letter-spacing="6" fill="#6E6657">OGR STORE</text>
</svg>'''

for pid, cat, top, bot in ITEMS:
    with open(os.path.join(ASSETS, f"{pid}.svg"), "w", encoding="utf-8") as f:
        f.write(svg(cat, top, bot))

print(f"Сгенерировано {len(ITEMS)} плейсхолдеров в {ASSETS}")
