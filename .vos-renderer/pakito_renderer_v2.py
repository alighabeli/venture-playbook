#!/usr/bin/env python3
"""
VOS Static HTML Renderer - Version 2 for Pakito Markdown Files
This version reads from Pakito-md directory instead of Pakito directory
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
import shutil
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
                value = float(value)
            elif value.startswith('[') and value.endswith(']'):
                # Simple list parsing
                items = value[1:-1].split(',')
                value = [item.strip().strip('"\'') for item in items if item.strip()]
            
            result[key] = value
    
    return result

# ============================================================================
# Simple Markdown to HTML Converter
# ============================================================================

def markdown_to_html_simple(markdown_text: str) -> str:
    """Convert markdown to HTML using simple regex-based parsing."""
    if not markdown_text.strip():
        return "<p>No content available.</p>"
    
    lines = markdown_text.split('\n')
    html_lines = []
    in_list = False
    current_list_type = None
    
    for line in lines:
        stripped = line.strip()
        
        # Empty lines
        if not stripped:
            if in_list:
                html_lines.append(f'</{current_list_type}>')
                in_list = False
                current_list_type = None
            else:
                html_lines.append('')
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
        
        # Images ![alt](url)
        line = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" class="img-fluid">', line)
        
        # Bold **text** or __text__
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'__(.+?)__', r'<strong>\1</strong>', line)
        
        # Italic *text* or _text_
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
        line = re.sub(r'_(.+?)_', r'<em>\1</em>', line)
        
        # Code `code`
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
        
        # Paragraphs
        if not any([
            line.startswith('<h'),
            line.startswith('<hr'),
            line.startswith('<ul'),
            line.startswith('<li'),
            line.startswith('</ul'),
            line.startswith('<img'),
            line.startswith('<a ')
        ]):
            html_lines.append(f'<p>{line}</p>')
        else:
            html_lines.append(line)
    
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
            margin-bottom: 20px;
        }}
        
        .meta-panel {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }}
        
        .badge-stable {{
            background-color: #28a745;
            color: white;
        }}
        
        .badge-progress {{
            background-color: #ffc107;
            color: #212529;
        }}
        
        .badge-draft {{
            background-color: #6c757d;
            color: white;
        }}
        
        .nav-section {{
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding: 10px 0;
        }}
        
        .nav-section-title {{
            font-weight: bold;
            padding: 8px 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-section-title:hover {{
            background-color: rgba(255,255,255,0.1);
        }}
        
        .nav-links {{
            padding-right: 25px;
        }}
        
        .nav-link {{
            display: block;
            padding: 8px 15px;
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            border-radius: 5px;
            margin-bottom: 2px;
        }}
        
        .nav-link:hover {{
            background-color: rgba(255,255,255,0.1);
            color: white;
        }}
        
        .nav-link.active {{
            background-color: var(--vos-secondary);
            color: white;
        }}
        
        .progress {{
            height: 10px;
            margin-top: 5px;
        }}
        
        @media (max-width: 768px) {{
            .sidebar {{
                position: relative;
                width: 100%;
                min-height: auto;
            }}
            
            .main-content {{
                margin-right: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="p-4">
            <h4 class="mb-4">
                <i class="bi bi-diagram-3"></i>
                داشبورد مدیریتی VOS
            </h4>
            
            {sidebar_links}
        </div>
    </div>
    
    <div class="main-content">
        <div class="vos-header">
            <h1 class="h3 mb-2">
                <i class="bi bi-journal-bookmark"></i>
                پلی‌بوک استراتژیک توسعه محصول
            </h1>
            <p class="text-muted mb-0">
                <i class="bi bi-clock"></i>
                آخرین به‌روزرسانی خودکار: {generation_time}
            </p>
        </div>
        
        <div class="row">
            <div class="col-md-9">
                {active_document_content}
            </div>
            <div class="col-md-3">
                {meta_panel}
            </div>
        </div>
    </div>

    <script>
        // Toggle sidebar sections
        document.addEventListener('DOMContentLoaded', function() {{
            const sectionTitles = document.querySelectorAll('.nav-section-title');
            sectionTitles.forEach(title => {{
                title.addEventListener('click', function() {{
                    const links = this.nextElementSibling;
                    const icon = this.querySelector('.toggle-icon');
                    
                    if (links.style.display === 'none' || links.style.display === '') {{
                        links.style.display = 'block';
                        icon.textContent = '-';
                    }} else {{
                        links.style.display = 'none';
                        icon.textContent = '+';
                    }}
                }});
            }});
            
            // Auto-expand active section
            const activeLink = document.querySelector('.nav-link.active');
            if (activeLink) {{
                const section = activeLink.closest('.nav-section');
                if (section) {{
                    const title = section.querySelector('.nav-section-title');
                    const links = section.querySelector('.nav-links');
                    const icon = title.querySelector('.toggle-icon');
                    
                    links.style.display = 'block';
                    icon.textContent = '-';
                }}
            }}
        }});
    </script>
</body>
</html>
"""

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
            <div class="col-md-12 mb-3">
                <div class="card">
                    <div class="card-header bg-light">
                        <h6 class="mb-0"><i class="bi bi-info-circle"></i> اطلاعات سند</h6>
                    </div>
                    <div class="card-body">
                        <div class="mb-2">
                            <strong>شناسه سند:</strong><br>
                            <code>{meta.get('id', 'N/A')}</code>
                        </div>
                        
                        <div class="mb-2">
                            <strong>وضعیت ماشین ران‌تایم:</strong><br>
                            <span class="badge {state_class}">{state}</span>
                        </div>
                        
                        <div class="mb-2">
                            <strong>مسئول گام (Owner):</strong><br>
                            {meta.get('owner_agent', 'N/A')}
                        </div>
                        
                        <div class="mb-2">
                            <strong>تمایل به پرداخت (WTP):</strong><br>
                            {wtp}/10
                            <div class="progress">
                                <div class="progress-bar bg-success" role="progressbar" 
                                     style="width: {wtp_percent}%" 
                                     aria-valuenow="{wtp_percent}" 
                                     aria-valuemin="0" 
                                     aria-valuemax="100">
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-2">
                            <strong>آخرین به‌روزرسانی:</strong><br>
                            {meta.get('last_updated', 'N/A')}
                        </div>
                        
                        {constraints_html}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return panel_html

def generate_sidebar_links_pakito(base_path: str = "Pakito-md", active_file: str = "") -> str:
    """Generate sidebar navigation from Pakito-md directory structure."""
    sidebar_html = ""
    
    if not os.path.exists(base_path):
        print(f"[ERROR] Directory {base_path} does not exist")
        return "<div class='alert alert-danger'>Pakito-md directory not found</div>"
    
    # Get all markdown files in Pakito-md
    md_files = []
    try:
        for item in os.listdir(base_path):
            if item.endswith('.md') and not item.startswith('.'):
                md_files.append(item)
    except Exception as e:
        print(f"[ERROR] Failed to list files in {base_path}: {e}")
        return f"<div class='alert alert-danger'>Error reading directory: {str(e)}</div>"
    
    if not md_files:
        return "<div class='alert alert-warning'>No markdown files found in Pakito-md</div>"
    
    # Sort files by numeric prefix
    md_files.sort()
    
    # Group files by category based on filename patterns
    categories = {
        "اصول و چشم‌انداز": [],
        "تحلیل و تحقیق": [],
        "محصول و معماری": [],
        "عملیات و مالی": [],
        "استراتژی و رشد": []
    }
    
    for md_file in md_files:
        filename = md_file.lower()
        
        if any(x in filename for x in ['principle', 'vision', 'system']):
            categories["اصول و چشم‌انداز"].append(md_file)
        elif any(x in filename for x in ['problem', 'market', 'analysis']):
            categories["تحلیل و تحقیق"].append(md_file)
        elif any(x in filename for x in ['product', 'user', 'data', 'architecture']):
            categories["محصول و معماری"].append(md_file)
        elif any(x in filename for x in ['operation', 'financial', 'logistic', 'contingency', 'learning']):
            categories["عملیات و مالی"].append(md_file)
        elif any(x in filename for x in ['pmf', 'growth', 'strategy', 'gtm']):
            categories["استراتژی و رشد"].append(md_file)
        else:
            categories["اصول و چشم‌انداز"].append(md_file)
    
    # Generate sidebar HTML for each category
    for category_name, files in categories.items():
        if not files:
            continue
        
        sidebar_html += f"""
        <div class="nav-section">
            <div class="nav-section-title">
                <span>{category_name}</span>
                <span class="toggle-icon">+</span>
            </div>
            <div class="nav-links" style="display: none;">
        """
        
        for md_file in sorted(files):
            file_path = os.path.join(base_path, md_file)
            # Remove numeric prefix and extension for display
            file_name = md_file.replace('.md', '')
            # Remove leading numbers and dashes
            file_name = re.sub(r'^\d+-', '', file_name)
            file_name = file_name.replace('-', ' ').title()
            
            is_active = "active" if active_file == file_path else ""
            
            sidebar_html += f"""
                <a href="{md_file.replace('.md', '.html')}" class="nav-link {is_active}">
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

# ============================================================================
# Main Processing Functions
# ============================================================================

def process_pakito_files():
    """Process all markdown files in Pakito-md directory and generate HTML."""
    input_dir = "Pakito-md"
    output_dir = "pakito-output-v2"
    
    if not os.path.exists(input_dir):
        print(f"[ERROR] Input directory {input_dir} does not exist")
        return False
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all markdown files
    md_files = []
    for item in os.listdir(input_dir):
        if item.endswith('.md') and not item.startswith('.'):
            md_files.append(item)
    
    if not md_files:
        print("[WARNING] No markdown files found in Pakito-md")
        return False
    
    print(f"[INFO] Processing {len(md_files)} markdown files from {input_dir}")
    
    # Process each file
    for md_file in sorted(md_files):
        input_path = os.path.join(input_dir, md_file)
        output_file = md_file.replace('.md', '.html')
        output_path = os.path.join(output_dir, output_file)
        
        print(f"[INFO] Processing: {md_file}")
        
        # Parse the markdown file
        meta, html_content = parse_vos_file(input_path)
        
        # Generate sidebar for this file
        sidebar = generate_sidebar_links_pakito(input_dir, input_path)
        
        # Render complete HTML
        html = render_html(meta, html_content, sidebar, input_path)
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[INFO]   -> Generated: {output_file}")
    
    # Generate dashboard/index page
    print("[INFO] Generating dashboard page...")
    dashboard_meta = {
        'title': 'VOS Pakito Dashboard - Overview',
        'id': 'VOS-PAKITO-DASH-001',
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
    
    dashboard_content = """
    <div class="alert alert-success">
        <h4><i class="bi bi-check-circle"></i> سیستم رندرینگ VOS برای پاکیتو فعال شد</h4>
        <p>سیستم استاتیک رندرینگ HTML برای مستندات پاکیتو با موفقیت راه‌اندازی شد.</p>
    </div>
    
    <h2>داشبورد مدیریتی پاکیتو (Pakito)</h2>
    
    <p>این سیستم تمامی اسناد مارک‌داون پاکیتو را به صفحات HTML تعاملی تبدیل می‌کند.</p>
    
    <h3>ویژگی‌های سیستم:</h3>
    <ul>
        <li><strong>پشتیبانی از YAML Front-Matter:</strong> استخراج خودکار متادیتا از اسناد</li>
        <li><strong>ناوبری دسته‌بندی شده:</strong> دسترسی سریع به اسناد بر اساس موضوع</li>
        <li><strong>پنل وضعیت ماشین:</strong> نمایش وضعیت ران‌تایم، امتیاز اطمینان و سایر متریک‌ها</li>
        <li><strong>رندرینگ فارسی:</strong> رابط کاربری به زبان فارسی با پشتیبانی RTL</li>
    </ul>
    
    <h3>آمار پروژه پاکیتو:</h3>
    <div class="row">
        <div class="col-md-3">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title"><i class="bi bi-folder"></i> اسناد</h5>
                    <p class="card-text fs-3">""" + str(len(md_files)) + """</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title"><i class="bi bi-check-circle"></i> وضعیت</h5>
                    <p class="card-text fs-3">فعال</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title"><i class="bi bi-calendar"></i> تاریخ</h5>
                    <p class="card-text fs-3">""" + datetime.datetime.now().strftime("%Y-%m-%d") + """</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title"><i class="bi bi-code-slash"></i> فرمت</h5>
                    <p class="card-text fs-3">Markdown</p>
                </div>
            </div>
        </div>
    </div>
    
    <h3>دستورات سریع:</h3>
    <div class="alert alert-warning">
        <h5><i class="bi bi-terminal"></i> دستورات ترمینال</h5>
        <pre><code># تولید تمامی فایل‌های HTML
python3 .vos-renderer/pakito_renderer_v2.py --build

# راه‌اندازی سرور محلی
python3 .vos-renderer/pakito_renderer_v2.py --serve --port 8080</code></pre>
    </div>
    """
    
    dashboard_sidebar = generate_sidebar_links_pakito(input_dir)
    dashboard_html = render_html(dashboard_meta, dashboard_content, dashboard_sidebar)
    
    dashboard_path = os.path.join(output_dir, "pakito-dashboard.html")
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    print(f"[INFO] Dashboard generated: {dashboard_path}")
    print(f"[INFO] Total files generated: {len(md_files) + 1}")
    print(f"[INFO] Output directory: {output_dir}")
    
    return True

def serve_files(port: int = 8080):
    """Serve generated HTML files using a simple HTTP server."""
    output_dir = "pakito-output-v2"
    
    if not os.path.exists(output_dir):
        print(f"[ERROR] Output directory {output_dir} does not exist. Run with --build first.")
        return
    
    os.chdir(output_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"[INFO] Serving files from {output_dir} at http://localhost:{port}")
        print(f"[INFO] Dashboard: http://localhost:{port}/pakito-dashboard.html")
        print("[INFO] Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Server stopped by user")
        finally:
            httpd.server_close()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="VOS Static HTML Renderer for Pakito Markdown Files")
    parser.add_argument("--build", action="store_true", help="Build all HTML files from Pakito-md")
    parser.add_argument("--serve", action="store_true", help="Serve generated files via HTTP")
    parser.add_argument("--port", type=int, default=8080, help="Port for HTTP server (default: 8080)")
    
    args = parser.parse_args()
    
    if args.build:
        success = process_pakito_files()
        if success:
            print("[SUCCESS] Build completed successfully")
        else:
            print("[ERROR] Build failed")
            sys.exit(1)
    
    if args.serve:
        serve_files(args.port)
    
    if not args.build and not args.serve:
        parser.print_help()

if __name__ == "__main__":
    import sys
    main()