#!/usr/bin/env python3
"""
VOS Static HTML Renderer - Simplified Version
This version uses only Python standard library to avoid dependency issues.
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
# Simple YAML Parser (Basic implementation for front-matter)
# ============================================================================

def parse_simple_yaml(yaml_text: str) -> Dict:
    """Parse simple YAML front-matter (supports basic key: value pairs)."""
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
# HTML Template
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
# Core Parser Functions
# ============================================================================

def parse_vos_file(file_path: str) -> Tuple[Optional[Dict], str]:
    """Parse a VOS markdown file with YAML front-matter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract YAML front-matter using strict regex
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if not match:
            # If no YAML front-matter, use default metadata
            return None, markdown_to_html_simple(content)
            
        yaml_data = parse_simple_yaml(match.group(1))
        markdown_data = match.group(2)
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
    if state in ['STABLE', 'VALIDATED']:
        state_class = "badge-stable"
    elif state in ['DRAFT', 'IN_PROGRESS', 'REVIEW']:
        state_class = "badge-progress"
    else:
        state_class = "badge-draft"
    
    # Calculate WTP percentage
    wtp = meta.get('metrics', {}).get('willingness_to_pay', 0)
    wtp_percent = (wtp / 10.0) * 100 if wtp else 0
    
    # Format constraints
    constraints = meta.get('constraints_passed', [])
    constraints_html = ""
    if constraints:
        constraints_html = "<div class='mt-3'><strong>محدودیت‌های تأییدشده:</strong><br>"
        for constraint in constraints:
            constraints_html += f"<span class='badge bg-secondary me-1 mb-1'>{constraint}</span>"
        constraints_html += "</div>"
    
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
                    <div class="mb-2"><i class="bi bi-gear fs-4"></i></div>
                    <div><strong>وضعیت ماشین ران‌تایم</strong></div>
                    <div class="{state_class} mt-2">{state}</div>
                </div>
            </div>
            
            <div class="col-md-3 mb-3">
                <div class="text-center">
                    <div class="mb-2"><i class="bi bi-person-badge fs-4"></i></div>
                    <div><strong>مسئول گام (Owner)</strong></div>
                    <div class="fs-5">{meta.get('owner_agent', 'N/A')}</div>
                </div>
            </div>
            
            <div class="col-md-3 mb-3">
                <div class="text-center">
                    <div class="mb-2"><i class="bi bi-graph-up fs-4"></i></div>
                    <div><strong>تمایل به پرداخت (WTP)</strong></div>
                    <div class="fs-5">{wtp}/10</div>
                    <div class="wtp-bar">
                        <div class="wtp-fill" style="width: {wtp_percent}%"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-md-6">
                <div><strong>امتیاز اطمینان:</strong> {meta.get('metrics', {}).get('confidence_score', 'N/A')}</div>
                <div><strong>درصد تطابق بازار:</strong> {meta.get('metrics', {}).get('market_fit_percentage', 'N/A')}%</div>
            </div>
            <div class="col-md-6">
                <div><strong>آخرین به‌روزرسانی:</strong> {meta.get('last_updated', 'N/A')}</div>
            </div>
        </div>
        
        {constraints_html}
    </div>
    """
    return panel_html

def generate_sidebar_links(base_path: str = ".", active_file: str = "") -> str:
    """Generate sidebar navigation from directory structure."""
    sidebar_html = ""
    
    # Define the main sections to include
    main_sections = [
        "000-Governance-System",
        "00-Principles", 
        "00-System-Spine",
        "01-Vision",
        "02-Problem",
        "03-Validation",
        "04-Product",
        "05-Domain-Model",
        "06-System-Architecture",
        "07-Runtime",
        "08-MVP",
        "09-Launch",
        "10-Learning",
        "11-Customer-Discovery",
        "12-PMF",
        "13-Growth-Strategy",
        "14-GTM",
        "15-AI-Runtime",
        "AI-System",
        "Examples",
        "Templates"
    ]
    
    for section in main_sections:
        section_path = os.path.join(base_path, section)
        if not os.path.exists(section_path):
            continue
            
        # Get markdown files in this section
        md_files = []
        try:
            for item in os.listdir(section_path):
                if item.endswith('.md') and not item.startswith('.'):
                    md_files.append(item)
        except:
            continue
            
        if not md_files:
            continue
            
        # Sort files numerically if possible
        md_files.sort()
        
        section_name = section.replace('-', ' ').title()
        sidebar_html += f"""
        <div class="nav-section">
            <div class="nav-section-title">
                <span>{section_name}</span>
                <span class="toggle-icon">+</span>
            </div>
            <div class="nav-links" style="display: none;">
        """
        
        for md_file in md_files:
            file_path = os.path.join(section, md_file)
            file_name = md_file.replace('.md', '').replace('-', ' ').title()
            is_active = "active" if active_file == file_path else ""
            
            sidebar_html += f"""
                <a href="{file_path.replace('.md', '.html')}" class="nav-link {is_active}">
                    <i class="bi bi-file-text me-2"></i>{file_name}
                </a>
            """
        
        sidebar_html += """
            </div>
        </div>
        """
    
    return sidebar_html

def render_html(meta: Optional[Dict], content: str, sidebar: str, active_file: str = "") -> str:
    """Render complete HTML page."""
    document_title = meta.get('title', 'VOS Document') if meta else "VOS Document"
    generation_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta_panel = generate_meta_panel(meta)
    
    return HTML_TEMPLATE.format(
        document_title=document_title,
        sidebar_links=sidebar,
        generation_time=generation_time,
        meta_panel=meta_panel,
        active_document_content=content
    )

def process_directory(base_path: str = ".", output_dir: str = ".vos-renderer/output") -> None:
    """Process all markdown files in the directory and generate HTML files."""
    print(f"[INFO] Processing directory: {base_path}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all markdown files
    for root, dirs, files in os.walk(base_path):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md') and not file.startswith('.'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_path)
                
                print(f"[INFO] Processing: {relative_path}")
                
                # Parse the file
                meta, content = parse_vos_file(file_path)
                
                # Generate sidebar
                sidebar = generate_sidebar_links(base_path, relative_path)
                
                # Render HTML
                html = render_html(meta, content, sidebar, relative_path)
                
                # Determine output path
                output_path = os.path.join(
                    output_dir, 
                    relative_path.replace('.md', '.html')
                )
                
                # Create subdirectories if needed
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Write HTML file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                
                print(f"[INFO] Generated: {output_path}")
    
    # Create index.html
    print("[INFO] Generating index.html...")
    index_meta = {
        'title': 'VOS Dashboard - Overview',
        'id': 'VOS-DASH-001',
        'state': 'STABLE',
        'owner_agent': 'System',
        'last_updated': datetime.datetime.now().strftime("%Y-%m-%d"),
        'metrics': {
            'confidence_score': 0.95,
            'willingness_to_pay': 9.0,
            'market_fit_percentage': 90
        },
        'constraints_passed': ['C1_VISION_ALIGNMENT', 'C2_DATA_MODEL_VALID']
    }
    
    index_content = """
    <div class="alert alert-success">
        <h4><i class="bi bi-check-circle"></i> سیستم رندرینگ VOS فعال شد</h4>
        <p>سیستم استاتیک رندرینگ HTML برای پلی‌بوک استراتژیک توسعه محصول با موفقیت راه‌اندازی شد.</p>
    </div>
    
    <h2>داشبورد مدیریتی Venture Playbook OS</h2>
    
    <p>این سیستم تمامی اسناد مارک‌داون موجود در پوشه‌های پروژه را به صفحات HTML تعاملی تبدیل می‌کند.</p>
    
    <h3>ویژگی‌های سیستم:</h3>
    <ul>
        <li><strong>پشتیبانی از YAML Front-Matter:</strong> استخراج خودکار متادیتا از اسناد</li>
        <li><strong>ناوبری سلسله‌مراتبی:</strong> دسترسی سریع به تمامی اسناد بر اساس ساختار پوشه‌ها</li>
        <li><strong>پنل وضعیت ماشین:</strong> نمایش وضعیت ران‌تایم، امتیاز اطمینان و سایر متریک‌ها</li>
        <li><strong>رندرینگ فارسی:</strong> رابط کاربری به زبان فارسی با پشتیبانی RTL</li>
        <li><strong>واچ‌داگ فایل:</strong> به‌روزرسانی خودکار با تغییر در اسناد (در حالت نظارت)</li>
    </ul>
    
    <h3>دستورالعمل استفاده:</h3>
    <ol>
        <li>از نوار کناری برای پیمایش بین اسناد استفاده کنید</li>
        <li>هر سند شامل پنل متادیتای کامل می‌باشد</li>
        <li>برای فعال‌سازی حالت نظارت خودکار، از گزینه watch=true در URL استفاده کنید</li>
    </ol>
    
    <div class="alert alert-info">
        <h5><i class="bi bi-info-circle"></i> نکته فنی</h5>
        <p>این سیستم به صورت استاتیک HTML تولید می‌کند و نیازی به سرور بک‌اند ندارد. تمامی فایل‌های تولید شده در پوشه <code>.vos-renderer/output</code> ذخیره می‌شوند.</p>
    </div>
    """
    
    sidebar = generate_sidebar_links(base_path)
    index_html = render_html(index_meta, index_content, sidebar)
    
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"[INFO] Index generated: {os.path.join(output_dir, 'index.html')}")

def watch_directory(base_path: str = ".", interval: int = 5) -> None:
    """Watch directory for changes and regenerate HTML files."""
    print(f"[INFO] Starting file watcher for {base_path} (interval: {interval}s)")
    print("[INFO] Press Ctrl+C to stop")
    
    last_modified = {}
    
    try:
        while True:
            changed = False
            
            # Check all markdown files
            for root, dirs, files in os.walk(base_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if file.endswith('.md') and not file.startswith('.'):
                        file_path = os.path.join(root, file)
                        try:
                            mtime = os.path.getmtime(file_path)
                            if file_path not in last_modified or last_modified[file_path] != mtime:
                                last_modified[file_path] = mtime
                                changed = True
                                print(f"[WATCH] Detected change in: {file_path}")
                        except:
                            continue
            
            if changed:
                print("[WATCH] Changes detected, regenerating HTML...")
                process_directory(base_path)
                print("[WATCH] Regeneration complete")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n[INFO] File watcher stopped by user")

def main():
    """Main entry point for the VOS Static HTML Renderer."""
    import argparse
    
    parser = argparse.ArgumentParser(description='VOS Static HTML Renderer')
    parser.add_argument('--build', action='store_true', help='Build all HTML files from markdown')
    parser.add_argument('--watch', action='store_true', help='Watch for changes and rebuild automatically')
    parser.add_argument('--serve', action='store_true', help='Start a simple HTTP server')
    parser.add_argument('--port', type=int, default=8000, help='Port for HTTP server (default: 8000)')
    parser.add_argument('--output', type=str, default='.vos-renderer/output', help='Output directory')
    
    args = parser.parse_args()
    
    print("[INFO] Initializing VOS Static Builder Pipeline...")
    print("[INFO] Venture Playbook OS - HTML Renderer v1.0")
    
    if args.build or (not args.watch and not args.serve):
        # Build all HTML files
        process_directory(".", args.output)
        print(f"[INFO] Build complete. HTML files saved to: {args.output}")
    
    if args.watch:
        # Start file watcher
        process_directory(".", args.output)  # Initial build
        watch_directory(".", interval=5)
    
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