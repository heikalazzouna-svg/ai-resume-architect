with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

bad_fstring = """            print(
    f"Email input value: {
        st.session_state.get(
            'email_input',
             '')}")"""

good_fstring = "            print(f\"Email input value: {st.session_state.get('email_input', '')}\")"

content = content.replace(bad_fstring, good_fstring)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
