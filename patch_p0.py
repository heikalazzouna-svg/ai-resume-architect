import os

with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

builder_save_idx = next((i for i, line in enumerate(lines) if 'save_resume_data(resume_data)' in line), None)
if builder_save_idx:
    indent = lines[builder_save_idx][:lines[builder_save_idx].find('save_resume_data')]
    lines[builder_save_idx] = indent + 'if save_builder_consent:\n' + indent + '    save_resume_data(resume_data)\n'
    
    gen_btn_idx = builder_save_idx
    while 'st.form_submit_button' not in lines[gen_btn_idx] and gen_btn_idx > 0:
        gen_btn_idx -= 1
    if gen_btn_idx > 0:
        lines.insert(gen_btn_idx, '                        save_builder_consent = st.checkbox("Save my resume data to the platform database (optional - requires your consent)", key="builder_save_consent")\n')

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
