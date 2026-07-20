import ast
import os
import re

with open("app.py", "r", encoding="utf-8") as f:
    source = f.read()

tree = ast.parse(source)

methods_to_extract = {
    'render_home': 'home.py',
    'render_about': 'about.py',
    'render_pricing': 'pricing.py',
    'render_faq': 'faq.py',
    'render_testimonials': 'testimonials.py',
    'render_changelog': 'changelog.py',
    'render_analyzer': 'analyzer.py',
    'render_builder': 'builder.py',
    'render_job_search': 'job_search.py',
    'render_feedback_page': 'feedback_page.py'
}

imports_header = """import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime
import io
import time
import traceback
from PIL import Image

from ui_components import hero_section, bento_card, page_header
from config.branding import APP_NAME, FOUNDER_NAME, SOCIAL_LINKS, FOUNDER_TITLE, FOUNDER_BIO
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS
from config.job_roles import JOB_ROLES
from config.database import save_resume_data, save_analysis_data
from utils.resume_parser import extract_text_from_pdf, extract_text_from_docx
from utils.docx_generator import create_docx_resume

"""

class_node = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'ResumeApp')

extracted_names = []

for node in class_node.body:
    if isinstance(node, ast.FunctionDef) and node.name in methods_to_extract:
        filename = methods_to_extract[node.name]
        extracted_names.append(node.name)
        
        # Get the source of the method
        method_source = ast.get_source_segment(source, node)
        
        # Indentation fix: remove 4 spaces
        lines = method_source.split('\n')
        fixed_lines = []
        for line in lines:
            if line.startswith('    '):
                fixed_lines.append(line[4:])
            else:
                fixed_lines.append(line)
        
        method_source = '\n'.join(fixed_lines)
        
        # Replace signature "def render_X(self):" with "def render(app):"
        method_source = re.sub(rf'def {node.name}\(self\):', 'def render(app):', method_source)
        
        # Replace `self.` with `app.`
        method_source = re.sub(r'\bself\.', 'app.', method_source)
        
        with open(os.path.join("pages", filename), "w", encoding="utf-8") as out_f:
            out_f.write(imports_header + method_source + "\n")
            
        print(f"Extracted {node.name} to pages/{filename}")

# Now, we should also remove these methods from app.py
# and update app.py to import them.

new_body = []
for node in class_node.body:
    if not (isinstance(node, ast.FunctionDef) and node.name in methods_to_extract):
        new_body.append(node)

# We cannot easily unparse with comments preserved in Python 3.11 ast.unparse
# So we just print the names we extracted.
