#!/usr/bin/env python3
"""
VOS Static HTML Renderer - Fixed Version
Fixed YAML parser for nested structures
"""

import os
import re
import datetime
import time
import html
import argparse
import http.server
import socketserver
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# ============================================================================
# Improved Simple YAML Parser (Basic implementation for front-matter)
# ============================================================================

def parse_simple_yaml(yaml_text: str) -> Dict:
    """Parse simple YAML front-matter (supports basic key: value pairs and nested structures)."""
    result = {}
    lines = yaml_text.strip().split('\n')
    
    current_key = None
    current_dict = result
    path = []
    
    for line in lines:
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue
        
        # Count indentation
        indent = len(line) - len(line.lstrip())
        indent_level = indent // 2  # Assuming 2 spaces per level
        
        # Remove extra path levels if we've moved back
        while len(path) > indent_level:
            path.pop()
        
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Remove quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            
            # Navigate to the correct dictionary based on path
            target_dict = result
            for p in path:
                if p in target_dict and isinstance(target_dict[p], dict):
                    target_dict = target_dict[p]
                else:
                    target_dict[p] = {}
                    target_dict = target_dict[p]
            
            if not value:  # Start of a nested dictionary
                target_dict[key] = {}
                path.append(key)
            else:
                # Try to parse basic types
                parsed_value = value
                if value.lower() == 'true':
                    parsed_value = True
                elif value.lower() == 'false':
                    parsed_value = False
                elif value.isdigit():
                    parsed_value = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                    try:
                        parsed_value = float(value)
                    except:
                        pass
                elif value.startswith('[') and value.endswith(']'):
                    # Simple array parsing
                    items = value[1:-1].split(',')
                    parsed_value = [item.strip().strip('"\'') for item in items if item.strip()]
                
                target_dict[key] = parsed_value
                current_key = key
        
        # Handle array items
        elif line.strip().startswith('- '):
            item = line.strip()[2:].strip()
            # Remove quotes if present
            if (item.startswith('"') and item.endswith('"')) or \
               (item.startswith("'") and item.endswith("'")):
                item = item[1:-1]
            
            # Navigate to the correct dictionary based on path
            target_dict = result
            for p in path:
                if p in target_dict and isinstance(target_dict[p], dict):
                    target_dict = target_dict[p]
            
            if current_key and current_key in target_dict:
                if isinstance(target_dict[current_key], list):
                    target_dict[current_key].append(item)
                else:
                    target_dict[current_key] = [item]
    
    return result

# ============================================================================
# Simple Markdown to HTML Converter (same as before)
# ============================================================================

def markdown_to_html_simple(markdown_text: str) -> str:
    """Convert basic markdown to HTML using only standard library."""
    lines = markdown_text.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    code_block_content = []
    current_list_type = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Handle code blocks
        if stripped.startswith('```'):
            if in_code_block:
                # End code block
                escaped_code = html.escape(''.join(code_block_content))
                html_lines.append(f'<pre><code>{escaped_code}</code></pre>')
                code_block_content = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
                if in_list:
                    html_lines.append(f'</{current_list_type}>')
                    in_list = False
            continue
        
        if in_code_block:
            code_block_content.append(line + '\n')
            continue
        
        # Headers (levels 1-6)
        header_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if header_match:
            level = len(header_match.group(1))
            content = header_match.group(2)
            html_lines.append(f'<h{level}>{content}</h{level}>')
            continue
        
        # Horizontal rules
        if re.match(r'^[-*_]{3,}$', stripped):
            html_lines.append('<hr>')
            continue
        
        # Lists
        list_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        if list_match:
            indent = len(list_match.group(1))
            content = list_match.group(2)
            
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
                current_list_type = 'ul'
            
            html_lines.append(f'<li>{content}</li>')
            continue
        
        # Checkboxes
        checkbox_match = re.match(r'^(\s*)[-*+]\s+\[([ xX])\]\s+(.+)$', line)
        if checkbox_match:
            indent = len(checkbox_match.group(1))
            checked = checkbox_match.group(2).lower() == 'x'
            content = checkbox_match.group(3)
            checked_attr = ' checked' if checked else ''
            
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
                current_list_type = 'ul'
            
            html_lines.append(f'<li><input type="checkbox"{checked_attr} disabled> {content}</li>')
            continue
        
        # End of list
        if in_list and not stripped:
            html_lines.append(f'</{current_list_type}>')
            in_list = False
            current_list_type = None
        
        # Links [text](url)
        line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', line)
        
        # Images ![alt](src)
        line = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', line)
        
        # Bold **text** or __text__
        line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', line)
        
        # Italic *text* or _text_
        line = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', line)
        line = re.sub(r'_([^_]+)_', r'<em>\1</em>', line)
        
        # Inline code `code`
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
        
        # Blockquotes
        if stripped.startswith('>'):
            content = stripped[1:].strip()
            html_lines.append(f'<blockquote>{content}</blockquote>')
            continue
        
        # Tables (basic support)
        if '|' in line and not stripped.startswith('|--'):
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells:
                html_lines.append('<tr>')
                for cell in cells:
                    # Check if it's a header row (next line has |--|)
                    if i + 1 < len(lines) and '|--' in lines[i + 1]:
                        html_lines.append(f'<th>{cell}</th>')
                    else:
                        html_lines.append(f'<td>{cell}</td>')
                html_lines.append('</tr>')
            continue
        
        # Table separator
        if '|--' in line:
            continue
        
        # Regular paragraphs
        if stripped:
            html_lines.append(f'<p>{line}</p>')
        elif html_lines and not html_lines[-1] == '<p>&nbsp;</p>':
            html_lines.append('<p>&nbsp;</p>')
    
    # Close any open list
    if in_list:
        html_lines.append(f'</{current_list_type}>')
    
    return '\n'.join(html_lines)

# ============================================================================
# HTML Template (same as before)
# ============================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VOS Dashboard - {document_title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <style>
        :root {{
            --vos-primary: #2c3e50;
            --vos-secondary: #3498db;
            --vos-accent: #e74c3c;
            --vos-light: #ecf0f1;
            --vos-dark: #1a252f;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            color: #333;
        }}
        
        .sidebar {{
            background: linear-gradient(180deg, var(--vos-primary) 0%, var(--vos-dark) 100%);
            color: white;
            min-height: 100vh;
            position: fixed;
            right: 0;
            top: 0;
            width: 280px;
            overflow-y: auto;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .main-content {{
            margin-right: 280px;
            padding: 20px;
        }}
        
        .vos-header {{
            background: white;
            border-bottom: 3px solid var(--vos-secondary);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        
        .document-card {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }}
        
        .meta-panel {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }}
        
        .badge-stable {{
            background-color: #27ae60;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
        }}
        
        .badge-progress {{
            background-color: #f39c12;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
        }}
        
        .badge-draft {{
            background-color: #95a5a6;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
        }}
        
        .wtp-bar {{
            height: 10px;
            background-color: rgba(255,255,255,0.3);
            border-radius: 5px;
            margin-top: 10px;
            overflow: hidden;
        }}
        
        .wtp-fill {{
            height: 100%;
            background-color: #2ecc71;
            border-radius: 5px;
        }}
        
        .sidebar-header {{
            padding: 25px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .nav-section {{
            padding: 15px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .nav-section-title {{
            padding: 10px 20px;
            font-weight: 600;
            color: rgba(255,255,255,0.9);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-section-title:hover {{
            background-color: rgba(255,255,255,0.1);
        }}
        
        .nav-links {{
            padding-right: 30px;
        }}
        
        .nav-link {{
            display: block;
            padding: 8px 20px;
            color: rgba(255,255,255,0.7);
            text-decoration: none;
            border-right: 3px solid transparent;
            transition: all 0.3s;
        }}
        
        .nav-link:hover {{
            color: white;
            background-color: rgba(255,255,255,0.05);
            border-right-color: var(--vos-secondary);
        }}
        
        .nav-link.active {{
            color: white;
            background-color: rgba(255,255,255,0.1);
            border-right-color: var(--vos-accent);
            font-weight: 600;
        }}
        
        .generation-time {{
            font-size: 0.9em;
            color: #7f8c8d;
            text-align: left;
            margin-top: 20px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: var(--vos-primary);
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }}
        
        h1 {{
            border-bottom: 2px solid var(--vos-secondary);
            padding-bottom: 10px;
        }}
        
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        table th {{
            background-color: var(--vos-primary);
            color: white;
            padding: 12px;
            text-align: right;
        }}
        
        table td {{
            padding: 10px;
            border: 1px solid #ddd;
        }}
        
        table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        .alert {{
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            border-right: 5px solid;
        }}
        
        .alert-info {{
            background-color: #e8f4fd;
            border-right-color: #3498db;
            color: #2c3e50;
        }}
        
        .alert-warning {{
            background-color: #fff3cd;
            border-right-color: #f39c12;
            color: #856404;
        }}
        
        .alert-success {{
            background-color: #d4edda;
            border-right-color: #27ae60;
            color: #155724;
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            <h3><i class="bi bi-diagram-3"></i> داشبورد مدیریتی VOS</h3>
            <p class="mb-0" style="color: rgba(255,255,255,0.7); font-size: 0.9em;">سیستم عملیاتی پلی‌بوک استراتژیک</p>
        </div>
        
        {sidebar_links}
        
        <div class="generation-time">
            <small><i class="bi bi-clock"></i> آخرین به‌روزرسانی: {generation_time}</small>
        </div>
    </div>
    
    <div class="main-content">
        <div class="vos-header">
            <h1>{document_title}</h1>
            <p class="lead">پلی‌بوک استراتژیک توسعه محصول</p>
            <div class="d-flex align-items-center">
                <i class="bi bi-arrow-repeat me-2"></i>
                <span>آخرین به‌روزرسانی خودکار: {generation_time}</span>
            </div>
        </div>
        
        {meta_panel}
        
        <div class="document-card">
            {active_document_content}
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Toggle navigation sections
        document.querySelectorAll('.nav-section-title').forEach(title => {{
            title.addEventListener('click', function() {{
                const links = this.nextElementSibling;
               