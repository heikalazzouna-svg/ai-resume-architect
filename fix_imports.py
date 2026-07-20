import glob

for filepath in glob.glob("pages/*.py"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("hero_section, bento_card, page_header", "hero_section, page_header")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
