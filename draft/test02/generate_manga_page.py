#!/usr/bin/env python3
"""Manga Page Layout Generator

Generates HTML for manga pages with dynamic panel boxes based on specified dimensions.
"""

import json
from pathlib import Path


def generate_manga_page_html(
    page_width: int = 834,
    page_height: int = 1194,
    padding: int = 10,
    panels: list = None
) -> str:
    """Generate HTML for a manga page with dynamic panel boxes.
    
    Args:
        page_width: Page width in pixels
        page_height: Page height in pixels
        padding: Padding around page content in pixels
        panels: List of panel definitions with top, left, width, height, and optional background
    
    Returns:
        HTML string for the manga page
    """
    if panels is None:
        panels = [
            {"top": 10, "left": 10, "width": page_width - 20, "height": 380, "background": "linear-gradient(to bottom, #87CEEB, #f0f0f0)"},
            {"top": 410, "left": 10, "width": 290, "height": 290, "background": "linear-gradient(to bottom, #ffcccc, #fff)"},
            {"top": 410, "left": 310, "width": page_width - 320, "height": 290, "background": "linear-gradient(to bottom, #fff, #e0f7fa)"},
            {"top": 720, "left": 10, "width": page_width - 20, "height": 190, "background": None},
            {"top": 930, "left": 10, "width": 190, "height": 244, "background": "linear-gradient(to bottom, #fff, #e0f7fa)"},
            {"top": 930, "left": 210, "width": page_width - 220, "height": 244, "background": None},
        ]
    
    # Calculate panel positions
    for panel in panels:
        panel.setdefault("background", "linear-gradient(to bottom, #87CEEB, #f0f0f0)")
    
    # Generate CSS
    css = f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: #f0f0f0;
            padding: 20px;
            font-family: 'Quicksand', 'Poppins', sans-serif;
        }}
        
        .manga-container {{
            width: {page_width}px;
            height: {page_height}px;
            margin: 0 auto;
            background: white;
            padding: {padding}px;
            position: relative;
        }}
        
        .manga-page {{
            width: {page_width}px;
            height: {page_height}px;
            background: #fff;
            border: 2px solid #000;
            border-radius: 8px;
            position: relative;
            overflow: hidden;
        }}
        
        .panel {{
            position: absolute;
            border: 2px solid #000;
            border-radius: 4px;
            overflow: hidden;
            background: #f5f5f5;
        }}
        
        .panel img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}
        
        .dialog-bubble {{
            position: absolute;
            background: white;
            padding: 12px 16px;
            border-radius: 20px;
            border: 2px solid #000;
            font-size: 14px;
            font-weight: bold;
            max-width: 80%;
            z-index: 10;
        }}
        
        .dialog-bubble::after {{
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            border-width: 10px 10px 0;
            border-style: solid;
            border-color: #000 transparent;
        }}
        
        .thinking-bubble {{
            position: absolute;
            background: white;
            padding: 8px;
            border-radius: 50%;
            border: 2px solid #000;
            font-size: 12px;
            z-index: 10;
        }}
        
        .thinking-bubble::before {{
            content: 'o  o  o';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            color: #666;
        }}
        
        .panel-label {{
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .motion-lines {{
            position: absolute;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(90deg, transparent 0%, #ff6b6b 50%, transparent 100%),
                repeating-linear-gradient(0deg, transparent 0, transparent 10px, #ff6b6b 10px, #ff6b6b 20px);
            opacity: 0.3;
            animation: motion 0.5s infinite linear;
        }}
        
        @keyframes motion {{
            0% {{ background-position: 0 0, 0 0; }}
            100% {{ background-position: 20px 0, 20px 0; }}
        }}
        
        @media (max-width: 768px) {{
            .manga-page {{
                width: 100%;
                height: auto;
                overflow-y: scroll;
            }}
        }}
    """
    
    # Generate panel CSS rules
    panel_css = ""
    for i, panel in enumerate(panels):
        panel_css += f"""
        /* Panel {i+1} */
        .panel-{i+1} {{
            top: {panel['top']}px;
            left: {panel['left']}px;
            width: {panel['width']}px;
            height: {panel['height']}px;
        }}
        """
    
    # Generate HTML body
    html_body = f"""        <div class="manga-page">
            <!-- Panel 1: Establishing shot -->
            <div class="panel panel-1">
                <span class="panel-label">1</span>
                <div style="width: 100%; height: 100%; background: {panels[0]['background']};"></div>
            </div>
            
            <!-- Panel 2: Scared close-up -->
            <div class="panel panel-2">
                <span class="panel-label">2</span>
                <div style="width: 100%; height: 100%; background: {panels[1]['background']};"></div>
            </div>
            
            <!-- Panel 3: Determined face -->
            <div class="panel panel-3">
                <span class="panel-label">3</span>
                <div style="width: 100%; height: 100%; background: {panels[2]['background']};"></div>
            </div>
            
            <!-- Panel 4: Wide action -->
            <div class="panel panel-4">
                <span class="panel-label">4</span>
                <div class="motion-lines" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></div>
            </div>
            
            <!-- Panel 5: Tall action shot -->
            <div class="panel panel-5">
                <span class="panel-label">5</span>
                <div style="width: 100%; height: 100%; background: {panels[4]['background']};"></div>
            </div>
            
            <!-- Panel 6: Motion lines -->
            <div class="panel panel-6">
                <span class="panel-label">6</span>
                <div class="motion-lines" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></div>
            </div>
        </div>
    """
    
    # Generate full HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manga Storyboard - Zachary Lost in City</title>
    <style>
{css}
{panel_css}
    </style>
</head>
<body>
    <div class="manga-container">
        <h1 class="manga-title" style="text-align: center; color: #000; font-size: 2rem; margin-bottom: 20px; font-weight: bold;">Zachary's Adventure</h1>
        
{html_body}
    </div>
</body>
</html>"""
    
    return html


if __name__ == "__main__":
    # Generate manga page HTML
    html = generate_manga_page_html()
    
    # Save to file
    output_path = Path("/opt/data/manga/draft/test02/manga_storyboard.html")
    output_path.write_text(html)
    print(f"Generated HTML saved to {output_path}")
