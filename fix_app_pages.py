import glob
import os

# Fix app.py import
with open("app.py", "r", encoding="utf-8") as f:
    app_content = f.read()
app_content = app_content.replace("from pages import ", "from app_pages import ")
with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_content)

# Fix apply_modern_styles in all app_pages
for filepath in glob.glob("app_pages/*.py"):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Check if the import is at the top
    has_import = any("from ui_components import apply_modern_styles" in line for line in lines)
    if not has_import:
        # Check if they import other things from ui_components
        for i, line in enumerate(lines):
            if "from ui_components import hero_section, page_header" in line:
                lines[i] = "from ui_components import hero_section, page_header, apply_modern_styles\n"
                has_import = True
                break
            elif "from ui_components import" in line and not "apply_modern_styles" in line:
                lines[i] = line.strip() + ", apply_modern_styles\n"
                has_import = True
                break
        
        if not has_import:
            lines.insert(0, "from ui_components import apply_modern_styles\n")
            
    # Also we want to ensure any 'from ui_components import apply_modern_styles' inside render() is removed
    # or just let it be, but let's remove it if it's indented
    new_lines = []
    for line in lines:
        if line.strip() == "from ui_components import apply_modern_styles" and line.startswith("    "):
            continue
        new_lines.append(line)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
