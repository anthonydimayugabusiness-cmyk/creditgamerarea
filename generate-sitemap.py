#!/usr/bin/env python3
"""Generate updated sitemap.xml for creditgamerarea.com"""

import os
import glob
from datetime import datetime

BASE_URL = "https://www.creditgamerarea.com"

def get_html_files():
    """Get all HTML files in the site."""
    base_dir = "/root/.openclaw/workspace/triviacaptain-website"
    
    files = []
    
    # Root level HTML files
    root_files = glob.glob(os.path.join(base_dir, "*.html"))
    for f in root_files:
        filename = os.path.basename(f)
        if filename not in ['sitemap.html']:
            files.append(('/', filename))
    
    # Quiz landing pages
    quiz_landing = glob.glob(os.path.join(base_dir, "*-quiz.html"))
    for f in quiz_landing:
        files.append(('/', os.path.basename(f)))
    
    # Blog posts
    blog_files = glob.glob(os.path.join(base_dir, "blog", "*.html"))
    for f in blog_files:
        if os.path.basename(f) != 'index.html':
            files.append(('/blog/', os.path.basename(f)))
    
    # Quiz question pages (just the landing pages, not individual questions)
    quiz_dirs = glob.glob(os.path.join(base_dir, "quiz", "*"))
    for quiz_dir in quiz_dirs:
        if os.path.isdir(quiz_dir):
            quiz_name = os.path.basename(quiz_dir)
            # Add the quiz landing page if it exists
            landing = f"/quiz/{quiz_name}/"
            files.append((f'/quiz/{quiz_name}/', 'index.html'))
    
    return files

def get_priority(path):
    """Determine priority based on page type."""
    if path == '/':
        return '1.0'
    elif 'quizzes' in path or path.endswith('-quiz.html'):
        return '0.8'
    elif '/blog/' in path:
        return '0.7'
    elif '/quiz/' in path:
        return '0.6'
    else:
        return '0.5'

def generate_sitemap():
    """Generate sitemap XML."""
    files = get_html_files()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Add homepage
    xml.append('  <url>')
    xml.append(f'    <loc>{BASE_URL}/</loc>')
    xml.append(f'    <lastmod>{today}</lastmod>')
    xml.append('    <priority>1.0</priority>')
    xml.append('  </url>')
    
    # Add quizzes page
    xml.append('  <url>')
    xml.append(f'    <loc>{BASE_URL}/quizzes/</loc>')
    xml.append(f'    <lastmod>{today}</lastmod>')
    xml.append('    <priority>0.9</priority>')
    xml.append('  </url>')
    
    # Add blog index
    xml.append('  <url>')
    xml.append(f'    <loc>{BASE_URL}/blog/</loc>')
    xml.append(f'    <lastmod>{today}</lastmod>')
    xml.append('    <priority>0.8</priority>')
    xml.append('  </url>')
    
    # Track added URLs to avoid duplicates
    added = {'/', '/quizzes/', '/blog/'}
    
    for path, filename in files:
        if path == '/' and filename == 'index.html':
            continue  # Skip root index
        
        if path == '/' and filename.endswith('-quiz.html'):
            url = f'{BASE_URL}/{filename}'
        elif path == '/blog/':
            url = f'{BASE_URL}/blog/{filename}'
        else:
            continue  # Skip other files for now
        
        if url in added:
            continue
        added.add(url)
        
        priority = get_priority(path + filename)
        
        xml.append('  <url>')
        xml.append(f'    <loc>{url}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append(f'    <priority>{priority}</priority>')
        xml.append('  </url>')
    
    xml.append('</urlset>')
    
    return '\n'.join(xml)

def main():
    """Generate and save sitemap."""
    sitemap = generate_sitemap()
    
    output_path = "/root/.openclaw/workspace/triviacaptain-website/sitemap.xml"
    with open(output_path, 'w') as f:
        f.write(sitemap)
    
    print(f"✅ Sitemap updated: {output_path}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Count URLs
    url_count = sitemap.count('<url>')
    print(f"🔗 URLs: {url_count}")

if __name__ == "__main__":
    main()
