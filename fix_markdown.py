with open("app_pages/about.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace st.markdown(..., unsafe_allow_html=True) with st.html(...)
content = content.replace("st.markdown(f\"\"\"", "st.html(f\"\"\"")
content = content.replace("st.markdown(\"\"\"", "st.html(\"\"\"")
content = content.replace("\"\"\", unsafe_allow_html=True)", "\"\"\")")

with open("app_pages/about.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done.")
