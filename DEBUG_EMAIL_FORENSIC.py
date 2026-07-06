#!/usr/bin/env python3
"""
Forensic analysis of the email HTML being sent to Resend.
This script will:
1. Generate the exact HTML
2. Validate structure
3. Check image URLs
4. Detect unsupported CSS
5. Find HTML errors
"""

import re
import sys
import os
from pathlib import Path

# Set UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

# Add files directory to path
sys.path.insert(0, str(Path(__file__).parent / "files"))

# Import email service
from app.services.email import ResendEmailService

def print_section(title):
    """Print formatted section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def step1_print_html():
    """STEP 1: Print the exact HTML that gets sent."""
    print_section("STEP 1: EXACT HTML SENT TO RESEND")

    service = ResendEmailService()
    html = service._get_welcome_email_html("Test User")

    # Print to file instead
    with open('DEBUG_EMAIL_OUTPUT.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML written to DEBUG_EMAIL_OUTPUT.html ({len(html)} characters)")
    return html

def step2_validate_html(html):
    """STEP 2: Validate HTML structure."""
    print_section("STEP 2: HTML STRUCTURE VALIDATION")

    errors = []
    warnings = []

    # Check for unclosed tags
    tag_pairs = {
        '<html': '</html>',
        '<head': '</head>',
        '<body': '</body>',
        '<table': '</table>',
        '<tr': '</tr>',
        '<td': '</td>',
        '<img': None,  # self-closing
        '<meta': None,  # self-closing
        '<style': '</style>',
    }

    for open_tag, close_tag in tag_pairs.items():
        open_count = html.count(open_tag)
        if close_tag:
            close_count = html.count(close_tag)
            if open_count != close_count:
                errors.append(f"{open_tag}: {open_count} opens, {close_count} closes (MISMATCH)")
        else:
            print(f"OK {open_tag}: {open_count} self-closing tags found")

    # Check for orphaned divs
    div_count = html.count('<div')
    div_close_count = html.count('</div>')
    if div_count != div_close_count:
        errors.append(f"<div>: {div_count} opens, {div_close_count} closes")
    if div_count > 0:
        warnings.append(f"ALERT: Found {div_count} <div> tags - Gmail may strip these")

    # Check for tbody
    tbody_count = html.count('<tbody')
    if tbody_count == 0:
        warnings.append("No <tbody> found - some tables may not have tbody (acceptable in email)")

    # Report errors
    if errors:
        print("ERRORS FOUND:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("OK All tags properly closed")

    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")

    return len(errors) == 0

def step3_verify_images(html):
    """STEP 3: Verify every image URL."""
    print_section("STEP 3: IMAGE VERIFICATION")

    # Find all img tags
    img_pattern = r'<img[^>]*src="([^"]+)"[^>]*>'
    images = re.findall(img_pattern, html)

    if not images:
        print("ERROR: No images found in email!")
        return False

    print(f"Found {len(images)} image(s):\n")

    for i, url in enumerate(images, 1):
        print(f"{i}. {url}")

        # Validate URL
        if url.startswith('data:'):
            print("   WARNING: Base64 data URI - not ideal for Gmail")
        elif url.startswith('cid:'):
            print("   ERROR: CID URL (embedded) - Gmail may not support")
        elif url.startswith('http://'):
            print("   WARNING: HTTP (not HTTPS) - insecure")
        elif url.startswith('https://'):
            print("   OK HTTPS URL")
        elif url.startswith('/'):
            print("   ERROR: Relative URL - must be absolute")
        else:
            print("   ? Unknown URL format")

        # Check file extension
        if url.endswith('.png'):
            print("   OK PNG format")
        elif url.endswith('.jpg') or url.endswith('.jpeg'):
            print("   OK JPG format")
        elif url.endswith('.svg'):
            print("   WARNING: SVG format - not ideal for all email clients")
        elif url.endswith('.gif'):
            print("   OK GIF format")
        else:
            print("   ? Unknown format")

    return len(images) > 0

def step4_check_size(html):
    """STEP 4: Check HTML size."""
    print_section("STEP 4: HTML SIZE")

    size_bytes = len(html.encode('utf-8'))
    size_kb = size_bytes / 1024

    print(f"Total HTML size: {size_kb:.2f} KB ({size_bytes:,} bytes)")

    if size_kb > 100:
        print(f"WARNING: Size exceeds 100KB ({size_kb:.2f}KB)")
        print("  Some email clients clip messages at 102KB")
        return False
    else:
        print("OK Size is acceptable")

    return True

def step5_find_forbidden_css(html):
    """STEP 5: Search for unsupported CSS."""
    print_section("STEP 5: FORBIDDEN CSS DETECTION")

    forbidden = {
        'display:flex': 'Flexbox not supported in many email clients',
        'display:grid': 'Grid not supported in email clients',
        'position:absolute': 'Absolute positioning not supported',
        'position:fixed': 'Fixed positioning not supported',
        'filter:': 'CSS filters not supported',
        'backdrop-filter': 'Backdrop filters not supported',
        '--': 'CSS variables not supported',
        'animation': 'CSS animations not supported',
        ':hover': 'Hover pseudo-classes not supported',
        ':focus': 'Focus pseudo-classes not supported',
        'transition': 'CSS transitions not supported',
    }

    found_issues = []

    for css_prop, description in forbidden.items():
        # Look in style attributes
        pattern = f'style="[^"]*{re.escape(css_prop)}'
        matches = re.findall(pattern, html, re.IGNORECASE)

        if matches:
            found_issues.append((css_prop, description, len(matches)))

    if found_issues:
        print("FORBIDDEN CSS FOUND:\n")
        for prop, desc, count in found_issues:
            print(f"  - {prop}: {count} occurrence(s)")
            print(f"    {desc}\n")
        return False
    else:
        print("OK No forbidden CSS found")
        return True

def step6_verify_inline_css(html):
    """STEP 6: Verify inline CSS on critical elements."""
    print_section("STEP 6: INLINE CSS VERIFICATION")

    critical_elements = {
        '<img': 'Images must have inline styles',
        '<table': 'Tables must have inline styles',
        '<button': 'Buttons must have inline styles',
        '<a': 'Links must have inline styles',
    }

    issues = []

    for tag, description in critical_elements.items():
        # Find all occurrences
        pattern = f'{re.escape(tag)}[^>]*>'
        matches = re.findall(pattern, html, re.IGNORECASE)

        for match in matches:
            if 'style=' not in match and tag != '<a':  # Some links may not need styles
                issues.append((tag, match[:60], description))

    if issues:
        print("ELEMENTS WITHOUT INLINE STYLES:\n")
        for tag, snippet, desc in issues:
            print(f"  {tag}...")
            print(f"    {desc}")
            print(f"    Found: {snippet}...\n")
        return False
    else:
        print("OK All critical elements have inline styles")
        return True

def step7_check_div_usage(html):
    """Check for <div> usage which Gmail Android strips."""
    print_section("STEP 7: DIV TAG ANALYSIS")

    divs = re.findall(r'<div[^>]*>', html)

    if divs:
        print(f"CRITICAL: Found {len(divs)} <div> tag(s)")
        print("\nGmail Android will strip these:\n")
        for i, div in enumerate(divs, 1):
            print(f"  {i}. {div}")

        print("\nWARNING: Each <div> will be removed, breaking layout")
        return False
    else:
        print("OK No <div> tags found")
        return True

def step8_check_responsive(html):
    """Check for responsive design."""
    print_section("STEP 8: RESPONSIVE DESIGN")

    if '@media' not in html:
        print("WARNING: No @media queries found")
        return False

    print("OK @media queries found")

    # Check for max-width: 600px
    if 'max-width: 600' in html or 'max-width:600' in html:
        print("OK Max-width: 600px found")
        return True
    else:
        print("WARNING: Max-width: 600px not found - mobile may break")
        return False

if __name__ == '__main__':
    html = step1_print_html()

    step2_validate_html(html)
    step3_verify_images(html)
    step4_check_size(html)
    step5_find_forbidden_css(html)
    step6_verify_inline_css(html)
    step7_check_div_usage(html)
    step8_check_responsive(html)

    print_section("FORENSIC ANALYSIS COMPLETE")
    print("Review the findings above to identify root causes.")
