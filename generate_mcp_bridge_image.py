"""
Protocol Geometry - Visual Expression
MCP Bridge: AnythingLLM ↔ VS Code/Cursor/Claude
"""

from PIL import Image, ImageDraw, ImageFont
import math

# Image dimensions - 16:9 ratio for Medium preview
WIDTH = 1600
HEIGHT = 900

# Color palette - technical and restrained
BG_COLOR = (10, 14, 39)  # Deep space blue
PRIMARY_BLUE = (30, 58, 138)  # Structural blue
ACCENT_CYAN = (6, 182, 212)  # Electric cyan
ACCENT_AMBER = (245, 158, 11)  # Warm amber
GRAY_DARK = (55, 65, 81)  # Structural gray
GRAY_LIGHT = (156, 163, 175)  # Secondary gray
TEXT_COLOR = (229, 231, 235)  # Light text

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img, 'RGBA')

# Grid reference (subtle) - systematic approach
grid_alpha = 40
for x in range(0, WIDTH, 100):
    draw.line([(x, 0), (x, HEIGHT)], fill=GRAY_DARK + (grid_alpha,), width=1)
for y in range(0, HEIGHT, 100):
    draw.line([(0, y), (WIDTH, y)], fill=GRAY_DARK + (grid_alpha,), width=1)

# LEFT: AnythingLLM Knowledge Hub (Circle - completeness, repository)
hub_x, hub_y = 300, 450
hub_radius = 150

# Outer circle with gradient effect (multiple circles)
for r in range(hub_radius, hub_radius - 20, -3):
    alpha = int(220 - (hub_radius - r) * 5)
    draw.ellipse([hub_x - r, hub_y - r, hub_x + r, hub_y + r], 
                 fill=PRIMARY_BLUE + (alpha,), 
                 outline=None)

# Circle border
draw.ellipse([hub_x - hub_radius, hub_y - hub_radius, 
              hub_x + hub_radius, hub_y + hub_radius], 
             outline=ACCENT_CYAN, width=4)

# Inner circle (data layers) - dashed effect
inner_r = 100
segments = 24
for i in range(segments):
    if i % 2 == 0:
        angle1 = (i / segments) * 2 * math.pi
        angle2 = ((i + 1) / segments) * 2 * math.pi
        x1 = hub_x + inner_r * math.cos(angle1)
        y1 = hub_y + inner_r * math.sin(angle1)
        x2 = hub_x + inner_r * math.cos(angle2)
        y2 = hub_y + inner_r * math.sin(angle2)
        draw.line([(x1, y1), (x2, y2)], fill=ACCENT_CYAN + (100,), width=2)

# CENTER: MCP Protocol Layer (Hexagon - connection, protocol)
hex_x, hex_y = 800, 450
hex_radius = 100

# Calculate hexagon vertices
hex_vertices = []
for i in range(6):
    angle = math.pi / 3 * i - math.pi / 6
    x = hex_x + hex_radius * math.cos(angle)
    y = hex_y + hex_radius * math.sin(angle)
    hex_vertices.append((x, y))

# Draw filled hexagon
draw.polygon(hex_vertices, fill=ACCENT_AMBER + (230,), outline=ACCENT_CYAN, width=4)

# MCP inner structure (protocol channels)
inner_hex_r = 65
for i in range(6):
    angle = math.pi / 3 * i
    x = hex_x + inner_hex_r * math.cos(angle)
    y = hex_y + inner_hex_r * math.sin(angle)
    draw.line([(hex_x, hex_y), (x, y)], fill=BG_COLOR + (200,), width=3)

# RIGHT: Client Interfaces (Stacked rounded rectangles)
clients = [
    {'name': 'VS Code', 'y': 200},
    {'name': 'Cursor', 'y': 400},
    {'name': 'Claude Desktop', 'y': 600}
]

client_x = 1150
client_width = 350
client_height = 100
corner_radius = 15

for client in clients:
    y = client['y']
    
    # Draw rounded rectangle (simulate with multiple shapes)
    # Fill
    draw.rectangle([client_x + corner_radius, y,
                   client_x + client_width - corner_radius, y + client_height],
                  fill=PRIMARY_BLUE + (220,))
    draw.rectangle([client_x, y + corner_radius,
                   client_x + client_width, y + client_height - corner_radius],
                  fill=PRIMARY_BLUE + (220,))
    
    # Corners
    draw.pieslice([client_x, y, client_x + 2*corner_radius, y + 2*corner_radius],
                  180, 270, fill=PRIMARY_BLUE + (220,))
    draw.pieslice([client_x + client_width - 2*corner_radius, y,
                   client_x + client_width, y + 2*corner_radius],
                  270, 360, fill=PRIMARY_BLUE + (220,))
    draw.pieslice([client_x, y + client_height - 2*corner_radius,
                   client_x + 2*corner_radius, y + client_height],
                  90, 180, fill=PRIMARY_BLUE + (220,))
    draw.pieslice([client_x + client_width - 2*corner_radius,
                   y + client_height - 2*corner_radius,
                   client_x + client_width, y + client_height],
                  0, 90, fill=PRIMARY_BLUE + (220,))
    
    # Border (simplified - just rectangle for clarity)
    draw.rectangle([client_x, y, client_x + client_width, y + client_height],
                  outline=ACCENT_CYAN, width=3)

# Connection flows: Knowledge Hub → MCP
flow_width = 3
draw.line([(hub_x + hub_radius, hub_y), (hex_x - hex_radius - 20, hex_y)],
         fill=ACCENT_CYAN + (180,), width=flow_width)

# Arrow head
arrow_tip_x = hex_x - hex_radius - 20
draw.polygon([(arrow_tip_x, hex_y), 
              (arrow_tip_x - 15, hex_y - 8),
              (arrow_tip_x - 15, hex_y + 8)],
             fill=ACCENT_CYAN + (180,))

# Connection flows: MCP → Clients
for client in clients:
    target_y = client['y'] + client_height // 2
    
    # Calculate bezier-like curve with multiple segments
    start_x, start_y = hex_x + hex_radius, hex_y
    end_x, end_y = client_x, target_y
    
    # Draw line
    draw.line([(start_x, start_y), (end_x, end_y)],
             fill=ACCENT_CYAN + (180,), width=flow_width)
    
    # Arrow head at end
    draw.polygon([(end_x, end_y),
                  (end_x - 15, end_y - 8),
                  (end_x - 15, end_y + 8)],
                 fill=ACCENT_CYAN + (180,))

# Accent dots at connection points (data flow markers)
connection_points = [
    (hub_x + hub_radius, hub_y),
    (hex_x - hex_radius - 20, hex_y),
    (hex_x + hex_radius, hex_y)
]
for point in connection_points:
    draw.ellipse([point[0] - 8, point[1] - 8, point[0] + 8, point[1] + 8],
                 fill=ACCENT_AMBER + (200,))

# Typography - minimal, technical annotations
try:
    font_title = ImageFont.truetype("arial.ttf", 48)
    font_label = ImageFont.truetype("arial.ttf", 32)
    font_small = ImageFont.truetype("arial.ttf", 22)
    font_tiny = ImageFont.truetype("arial.ttf", 18)
except:
    font_title = ImageFont.load_default()
    font_label = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_tiny = ImageFont.load_default()

# Title - top
title_text = "Model Context Protocol"
subtitle_text = "Bridging AI Assistants with AnythingLLM"
title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
title_width = title_bbox[2] - title_bbox[0]
draw.text(((WIDTH - title_width) // 2, 50), title_text, fill=TEXT_COLOR, font=font_title)

subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=font_small)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
draw.text(((WIDTH - subtitle_width) // 2, 110), subtitle_text, fill=GRAY_LIGHT, font=font_small)

# Main labels
draw.text((hub_x - 75, hub_y - 10), "AnythingLLM", fill=TEXT_COLOR, font=font_label)
draw.text((hub_x - 70, 750), "Knowledge Base", fill=GRAY_LIGHT, font=font_small)

draw.text((hex_x - 35, hex_y - 15), "MCP", fill=BG_COLOR, font=font_label)
draw.text((hex_x - 60, 780), "Protocol Layer", fill=GRAY_LIGHT, font=font_small)

for client in clients:
    name = client['name']
    y = client['y']
    name_bbox = draw.textbbox((0, 0), name, font=font_label)
    name_width = name_bbox[2] - name_bbox[0]
    draw.text((client_x + (client_width - name_width) // 2, y + 30), 
              name, fill=TEXT_COLOR, font=font_label)

draw.text((client_x + 100, 750), "MCP Clients", fill=GRAY_LIGHT, font=font_small)

# Technical annotation - bottom right
tech_text = "stdio transport / JSON-RPC"
draw.text((WIDTH - 300, HEIGHT - 40), tech_text, fill=GRAY_LIGHT + (150,), font=font_tiny)

# Technical grid references (subtle)
draw.text((20, 20), "00", fill=GRAY_DARK, font=font_tiny)
draw.text((WIDTH - 40, HEIGHT - 40), "16", fill=GRAY_DARK, font=font_tiny)

# Save with high quality
output_path = 'a:/Docker/Meus artigos/anythingllm-mcp-bridge.png'
img.save(output_path, 'PNG', optimize=True, quality=95)
print("✓ Image created: anythingllm-mcp-bridge.png")
print(f"  Resolution: {WIDTH}x{HEIGHT} pixels (16:9)")
print(f"  Philosophy: Protocol Geometry")
