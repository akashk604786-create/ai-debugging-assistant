import streamlit as st
import sys
import os

# 1. THE PATH FIX: Keeps your imports working on the cloud server
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../../'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 2. CLEAN IMPORTS
from utils.llm_client import GeminiClient
from utils.debugging_helper import build_debugging_prompt

# 3. PAGE CONFIG: Must be the very first st command
st.set_page_config(page_title="AI Debugging Assistant", page_icon="🔧")

def main():
    st.title("🔧 AI Debugging Assistant")
    st.write("Professional Python debugging powered by Gemini.")

    user_input = st.text_area("Input Code or Error Log:", height=200)

    if st.button("🔎 Debug Code"):
        if not user_input.strip():
            st.warning("Please enter code to analyze.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    client = GeminiClient()
                    prompt = build_debugging_prompt(user_input)
                    response = client.ask(prompt)
                    
                    st.markdown("---")
                    st.subheader("🧠 Debugging Result")
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

if __name__ == "__main__":
    main()