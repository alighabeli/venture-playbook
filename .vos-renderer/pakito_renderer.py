#!/usr/bin/env python3
"""
VOS Static HTML Renderer - Pakito Version
Specialized version for processing Pakito .md.docx files
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
# Improved YAML Parser for Pakito files
# ============================================================================

def parse_pakito_yaml(yaml_text: str) -> Dict:
    """Parse YAML front-matter from Pakito .md.docx files."""
    result = {}
    lines = yaml_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Remove quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            
            # Try to parse basic types
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                try:
                    value = float(value)
                except:
                    pass
            elif value.startswith('[') and value.endswith(']'):
                # Simple array parsing
                items = value[1:-1].split(',')
                value = [item.strip().strip('"\'') for item in items if item.strip()]
            
            result[key] = value
    
    return result

# ============================================================================
# Simple Markdown to HTML Converter
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
# HTML Template for Pakito
# ============================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پاکیتو - {document_title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <style>
        :root {{
            --pakito-primary: #00a896;
            --pakito-secondary: #028090;
            --pakito-accent: #f0b67f;
            --pakito-light: #f5f5f5;
            --pakito-dark: #05668d;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            color: #333;
        }}
        
        .sidebar {{
            background: linear-gradient(180deg, var(--pakito-primary) 0%, var(--pakito-dark) 100%);
            color: white;
            min-height: 100vh;
            position: fixed;
            right: 0;
            top: 0;
            width: III280px;
            overflow-y: auto;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .main-content {{
            margin-right: 280px;
            padding: 20px;
        }}
        
        .pakito-header {{
            background: white;
            border-bottom: 3px solid var(--pakito-secondary);
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
            background: linear-gradient(135deg, var(--pakito-primary) 0%, var(--pakito-secondary) 100%);
            color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }}
        
        .badge-locked {{
            background-color: #05668d;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
        }}
        
        .badge-draft {{
            background-color: #f0b67f;
            color: #333;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
        }}
        
        .badge-stable {{
            background-color: #00a896;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
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
            border-right-color: var(--pakito-accent);
        }}
        
        .nav-link.active {{
            color: white;
            background-color: rgba(255,255,255,0.1);
            border-right-color: var(--pakito-accent);
            font-weight: 600;
        }}
        
        .generation-time {{
            font-size: 0.9em;
            color: #7f8c8d;
            text-align: left;
            margin-top: 20px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: var(--pakito-dark);
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }}
        
        h1 {{
            border-bottom: 2px solid var(--pakito-primary);
            padding-bottom: 10px;
        }}
        
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background-color: var(--pakito-dark);
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
            background-color: var(--pakito-primary);
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
            border-right-color: var(--pakito-secondary);
            color: #2c3e50;
        }}
        
        .alert-warning {{
            background-color: #fff3cd;
            border-right-color: #f0b67f;
            color: #856404;
        }}
        
        .alert-success {{
            background-color: #d4edda;
            border-right-color: var(--pakito-primary);
            color: #155724;
        }}
        
        .venture-badge {{
            background-color: var(--pakito-accent);
            color: #333;
            padding: -3px 10px;
            border-radius: III15px;
            font-size: 0.9em;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            <h3><i class="bi bi-droplet"></i> پاکیتو - سیستم مدیریتی</h3>
            <p class="mb-0" style="color: rgba(255,255,255,0.7); font-size: 0.9em;">پلتفرم شستشوی هوشمند لباس</p>
        </div>
        
        {sidebar_links}
        
        <div class="generation-time">
            <small><i class="bi bi-clock"></i> آخرین به‌روزرسانی: {generation_time}</small>
        </div>
    </div>
    
    <div class="main-content">
        <div class="pakito-header">
            <h1>{document_title}</h1>
            <p class="lead">پلتفرم شستشوی هوشمند لباس</p>
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
                if (links.style.display === 'none' || links.style.display === '') {{
                    links.style.display = 'block';
                    this.querySelector('.toggle-icon').textContent = '−';
                }} else {{
                    links.style.display = 'none';
                    this.querySelector('.toggle-icon').textContent = '+';
                }}
            }});
        }});
        
        // Set active nav link based on current URL
        const currentPath = window.location.pathname.split('/').pop();
        document.querySelectorAll('.nav-link').forEach(link => {{
            if (link.getAttribute('href') === currentPath || 
                link.textContent.includes(currentPath.replace('.html', ''))) {{
                link.classList.add('active');
            }}
        }});
        
        // Auto-refresh every 30 seconds if in watch mode
        if (window.location.search.includes('watch=true')) {{
            setTimeout(() => {{
                window.location.reload();
            }}, 30000);
        }}
    </script>
</body>
</html>"""

# ============================================================================
# Core Parser Functions for Pakito
# ============================================================================

def parse_pakito_file(file_path: str) -> Tuple[Optional[Dict], str]:
    """Parse a Pakito .md.docx file with YAML front-matter."""
    try:
        import zipfile
        import xml.etree.ElementTree as ET
        
        # Check if file is a .docx (Word) file
        if file_path.lower().endswith('.docx'):
            # Read .docx file as ZIP archive
            with zipfile.ZipFile(file_path, 'r') as docx:
                # Get the document.xml file
                xml_content = docx.read('word/document.xml').decode('utf-8')
                
                # Extract text between <w:t> tags (Word text elements)
                import re
                text_parts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', xml_content)
                content = '\n'.join(text_parts)
                
                # Also try to get text from paragraphs
                if not content.strip():
                    # Alternative: extract all text between > and <
                    text_parts = re.findall(r'>([^<]+)<', xml_content)
                    content = '\n'.join([t.strip() for t in text_parts if t.strip()])
        else:
            # For regular text files
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # Extract YAML front-matter - Pakito format
        # First try: ---yaml--- format
        match = re.match(r'^---(.*?)---(.*)$', content, re.DOTALL)
        if not match:
            # Second try: ---\nyaml\n---\n format
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
            if not match:
                # If no YAML front-matter, use default metadata
                return None, markdown_to_html_simple(content)
        
        yaml_data = parse_pakito_yaml(match.group(1).strip())
        markdown_data = match.group(2).strip()
        html_body = markdown_to_html_simple(markdown_data)
        return yaml_data, html_body
    except Exception as e:
        print(f"[ERROR] Failed to parse {file_path}: {e}")
        return None, f"<div class='alert alert-warning'>Error parsing document: {str(e)}</div>"

def generate_meta_panel(meta: Optional[Dict]) -> str:
    """Generate metadata panel HTML from YAML front-matter."""
    if not meta:
        return "<div class='alert alert-info'>No metadata available for this document.</div>"
    
    # Determine state badge class
    state = meta.get('state', 'UNKNOWN')
    if state in ['LOCKED', 'STABLE']:
        state_class = "badge-locked"
    elif state in ['DRAFT', 'IN_PROGRESS', 'REVIEW']:
        state_class = "badge-draft"
    else:
        state_class = "badge-stable"
    
    # Get venture name
    venture_name = meta.get('venture_name', 'پاکیتو')
    
    panel_html = f"""
    <div class="meta-panel">
        <div class="row">
            <div class="col-md-3 mb-3">
                <div class="text-center">
                    <div class="mb-2"><i class="bi bi-file-text fs-4"></i></div>
                    <div><strong>شناسه سند</strong></div>
                    <div class="fs-5">{meta.get('id', 'N/A')}</div>
                </div>
            </div>
            
            <div class="col-md-3 mb-3">
                <div class="text-center">
                    <div class="mb-2"><i class="bi bi-lock fs-4"></i></div>
                    <div><strong>وضعیت سند</strong></div>
                    <div class="{state_class} mt-2">{state}</div>
                </div>
            </div>
            
            <div class="col-md-3 mb-3">
                <div class="text-center">
                    <div class="mb-2"><i class="bi bi-building fs-4"></i></div>
                    <div><strong>ونچر</strong></div>
                    <div class="fs-5">{venture_name}</div>
                </div>
            </div>
            
            <div class="col-md-3 mb-3">
                <div class="text-center">
                    <div class="mb-2"><i class="bi bi-calendar fs-4"></i></div>
                    <div><strong>آخرین به‌روزرسانی</strong></div>
                    <div class="fs-5">{meta.get('last_updated', 'N/A')}</div>
                </div>
            </div>
        </div>
    </div>
    """
    return panel_html

def generate_pakito_sidebar(base_path: str = "Pakito", active_file: str = "") -> str:
    """Generate sidebar navigation for Pakito files."""
    sidebar_html = ""
    
    # Get all .md.docx files in Pakito directory
    md_files = []
    try:
        for item in os.listdir(base_path):
            if item.endswith('.md.docx') and not item.startswith('.'):
                md_files.append(item)
    except:
        return "<div class='nav-section'><div class='nav-section-title'>خطا در خواندن فایل‌ها</div></div>"
    
    if not md_files:
        return "<div class='nav-section'><div class='nav-section-title'>فایلی یافت نشد</div></div>"
    
    # Sort files numerically
    md_files.sort()
    
    sidebar_html += """
    <div class="nav-section">
        <div class="nav-section-title">
            <span>مستندات پاکیتو</span>
            <span class="toggle-icon">+</span>
        </div>
        <div class="nav-links" style="display: none;">
    """
    
    for md_file in md_files:
        file_path = os.path.join(base_path, md_file)
        # Extract document number and name
        file_name = md_file.replace('.md.docx', '')
        # Parse number and title
        parts = file_name.split('-', 1)
        if len(parts) == 2:
            doc_num = parts[0]
            doc_title = parts[1].replace('-', ' ')
        else:
            doc_num = ""
            doc_title = file_name.replace('-', ' ')
        
        is_active = "active" if active_file == file_path else ""
        
        sidebar_html += f"""
            <a href="{md_file.replace('.md.docx', '.html')}" class="nav-link {is_active}">
                <i class="bi bi-file-text me-2"></i>{doc_num} - {doc_title}
            </a>
        """
    
    sidebar_html += """
        </div>
    </div>
    """
    
    return sidebar_html

def render_pakito_html(meta: Optional[Dict], content: str, sidebar: str, active_file: str = "") -> str:
    """Render complete HTML page for Pakito."""
    document_title = meta.get('title', 'سند پاکیتو') if meta else "سند پاکیتو"
    generation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta_panel = generate_meta_panel(meta)
    
    return HTML_TEMPLATE.format(
        document_title=document_title,
        sidebar_links=sidebar,
        generation_time=generation_time,
        meta_panel=meta_panel,
        active_document_content=content
    )

def process_pakito_directory(base_path: str = "Pakito", output_dir: str = ".vos-renderer/pakito-output") -> None:
    """Process all Pakito .md.docx files and generate HTML files."""
    # Convert relative path to absolute if needed
    if not os.path.isabs(base_path):
        # Try to find Pakito directory relative to current directory
        possible_paths = [
            base_path,
            f"../{base_path}",
            f"../../{base_path}",
            os.path.join(os.path.dirname(__file__), f"../{base_path}")
        ]
        
        for path in possible_paths:
            if os.path.exists(path) and os.path.isdir(path):
                base_path = os.path.abspath(path)
                break
    
    print(f"[INFO] Processing Pakito directory: {base_path}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all .md.docx files
    md_files = []
    try:
        for item in os.listdir(base_path):
            if item.endswith('.md.docx') and not item.startswith('.'):
                md_files.append(item)
    except Exception as e:
        print(f"[ERROR] Failed to list files in {base_path}: {e}")
        return
    
    if not md_files:
        print("[INFO] No .md.docx files found in Pakito directory")
        return
    
    # Sort files
    md_files.sort()
    
    for md_file in md_files:
        file_path = os.path.join(base_path, md_file)
        print(f"[INFO] Processing: {md_file}")
        
        # Parse the file
        meta, content = parse_pakito_file(file_path)
        
        # Generate sidebar
        sidebar = generate_pakito_sidebar(base_path, file_path)
        
        # Render HTML
        html = render_pakito_html(meta, content, sidebar, file_path)
        
        # Determine output path
        output_path = os.path.join(
            output_dir, 
            md_file.replace('.md.docx', '.html')
        )
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[INFO] Generated: {output_path}")
    
    # Create pakito-dashboard.html
    print("[INFO] Generating pakito-dashboard.html...")
    dashboard_meta = {
        'title': 'داشبورد مدیریتی پاکیتو',
        'id': 'PAKITO-DASH-001',
        'state': 'LOCKED',
        'venture_name': 'Pakito',
        'last_updated': datetime.datetime.now().strftime("%Y-%m-%d")
    }
    
    dashboard_content = """
    <div class="alert alert-success">
        <h4><i class="bi bi-check-circle"></i> سیستم رندرینگ پاکیتو فعال شد</h4>
        <p>سیستم استاتیک رندرینگ HTML برای مستندات پاکیتو با موفقیت راه‌اندازی شد.</p>
    </div>
    
    <h2>داشبورد مدیریتی پاکیتو</h2>
    
    <p>پلتفرم شستشوی هوشمند لباس با رویکرد ونچر پلی‌بوک</p>
    
    <h3>ویژگی‌های سیستم:</h3>
    <ul>
        <li><strong>پشتیبانی از YAML Front-Matter:</strong> استخراج خودکار متادیتا از اسناد</li>
        <li><strong>ناوبری سلسله‌مراتبی:</strong> دسترسی سریع به تمامی مستندات پاکیتو</li>
        <li><strong>پنل وضعیت سند:</strong> نمایش وضعیت LOCKED، DRAFT، STABLE</li>
        <li><strong>رندرینگ فارسی:</strong> رابط کاربری به زبان فارسی با پشتیبانی RTL</li>
        <li><strong>قالب اختصاصی پاکیتو:</strong> طراحی با رنگ‌های برند پاکیتو</li>
    </ul>
    
    <h3>مستندات موجود:</h3>
    <div class="row">
    """
    
    # Add document cards
    for i, md_file in enumerate(md_files[:6]):
        file_name = md_file.replace('.md.docx', '')
        parts = file_name.split('-', 1)
        if len(parts) == 2:
            doc_num = parts[0]
            doc_title = parts[1].replace('-', ' ')
        else:
            doc_num = ""
            doc_title = file_name.replace('-', ' ')
        
        dashboard_content += f"""
        <div class="col-md-4 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title"><i class="bi bi-file-text"></i> {doc_title}</h5>
                    <p class="card-text">شناسه: {doc_num}</p>
                    <a href="{md_file.replace('.md.docx', '.html')}" class="btn btn-outline-primary">مشاهده سند</a>
                </div>
            </div>
        </div>
        """
    
    dashboard_content += """
    </div>
    
    <div class="alert alert-info">
        <h5><i class="bi bi-info-circle"></i> نکته فنی</h5>
        <p>این سیستم به صورت استاتیک HTML تولید می‌کند و نیازی به سرور بک‌اند ندارد. تمامی فایل‌های تولید شده در پوشه <code>.vos-renderer/pakito-output</code> ذخیره می‌شوند.</p>
    </div>
    """
    
    sidebar = generate_pakito_sidebar(base_path)
    dashboard_html = render_pakito_html(dashboard_meta, dashboard_content, sidebar)
    
    # Write dashboard to output directory
    dashboard_output_path = os.path.join(output_dir, 'pakito-dashboard.html')
    with open(dashboard_output_path, 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    # Also write to project root
    with open("pakito-dashboard.html", 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    print(f"[INFO] Dashboard generated: pakito-dashboard.html")
    print(f"[INFO] Pakito build complete. HTML files saved to: {output_dir}")

def main():
    """Main entry point for the Pakito HTML Renderer."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Pakito Static HTML Renderer')
    parser.add_argument('--build', action='store_true', help='Build all HTML files from Pakito .md.docx files')
    parser.add_argument('--serve', action='store_true', help='Start a simple HTTP server')
    parser.add_argument('--port', type=int, default=8081, help='Port for HTTP server (default: 8081)')
    parser.add_argument('--output', type=str, default='.vos-renderer/pakito-output', help='Output directory')
    
    args = parser.parse_args()
    
    print("[INFO] Initializing Pakito Static Builder Pipeline...")
    print("[INFO] Pakito - HTML Renderer v1.0")
    
    if args.build or not args.serve:
        # Build all HTML files
        process_pakito_directory("Pakito", args.output)
        print(f"[INFO] Build complete. HTML files saved to: {args.output}")
    
    if args.serve:
        # Start HTTP server
        import http.server
        import socketserver
        
        os.chdir(args.output)
        
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", args.port), handler) as httpd:
            print(f"[INFO] HTTP server started at http://localhost:{args.port}")
            print("[INFO] Serving files from:", os.path.abspath("."))
            print("[INFO] Press Ctrl+C to stop the server")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n[INFO] HTTP server stopped")

if __name__ == "__main__":
    main()
