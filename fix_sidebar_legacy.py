with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

import re

# Remove the call to self.show_repo_notification()
for i in range(len(lines)):
    if 'self.show_repo_notification()' in lines[i]:
        lines[i] = ""

# Find and delete the function definition
start_idx = -1
for i in range(len(lines)):
    if 'def show_repo_notification(self):' in lines[i]:
        start_idx = i
        break

if start_idx != -1:
    end_idx = start_idx
    # Find the end of the function (where the next def starts, or end of file)
    while end_idx + 1 < len(lines) and 'def ' not in lines[end_idx + 1]:
        end_idx += 1
    
    for i in range(start_idx, min(end_idx + 1, len(lines))):
        lines[i] = ""

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
