with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

methods_to_delete = [
    'def render_home(self):',
    'def render_about(self):',
    'def render_pricing(self):',
    'def render_faq(self):',
    'def render_testimonials(self):',
    'def render_changelog(self):',
    'def render_analyzer(self):',
    'def render_builder(self):',
    'def render_job_search(self):',
    'def render_feedback_page(self):'
]

new_lines = []
skip = False

for line in lines:
    stripped_line = line.strip()
    
    # Check if we are entering a method to delete
    if any(stripped_line.startswith(m) for m in methods_to_delete):
        skip = True
        continue
        
    # Check if we are entering a new method or class to stop skipping
    if skip and (stripped_line.startswith('def ') or stripped_line.startswith('class ')):
        # Wait, if it's an inner function, it might be indented.
        # But top-level methods of the class are indented by exactly 4 spaces.
        if line.startswith('    def '):
            skip = False

    if not skip:
        new_lines.append(line)

with open("app_clean.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
