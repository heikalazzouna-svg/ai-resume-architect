with open("app_pages/about.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

if not any("apply_modern_styles" in line and "import" in line for line in lines):
    lines.insert(1, "from ui_components import apply_modern_styles\n")

with open("app_pages/about.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
