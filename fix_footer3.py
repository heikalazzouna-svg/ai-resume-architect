with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# Delete lines containing the star button
start_idx = -1
for i, line in enumerate(lines):
    if "# Add GitHub star button" in line:
        start_idx = i
        break

if start_idx != -1:
    end_idx = start_idx
    while end_idx < len(lines):
        if 'Star this repo' in lines[end_idx]:
            end_idx += 5
            break
        end_idx += 1
    
    for i in range(start_idx, min(end_idx, len(lines))):
        lines[i] = ""

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
