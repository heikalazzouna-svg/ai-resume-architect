import glob

for filepath in glob.glob("pages/*.py"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("from utils.docx_generator import create_docx_resume\n", "")
    content = content.replace("from utils.docx_generator import create_docx_resume", "")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
