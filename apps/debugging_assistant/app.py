import sys
import os
# Ensure the root directory is in the path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from utils.llm_client import GeminiClient
from utils.debugging_helper import build_debugging_prompt

# This decorator ensures the GeminiClient is only initialized once
# It stays in memory, making the app much more responsive
@st.cache_resource
def get_gemini_client():
    return GeminiClient()

def main():
    # Page configuration
    st.set_page_config(
        page_title="AI Debugging Assistant",
        page_icon="🔎",
        layout="centered"
    )

    st.title("🔧 AI Debugging Assistant")
    st.write("Paste your **Python Code** or **error log**, and I'll help you debug it.")

    # Input area
    user_input = st.text_area(
        "Enter your code or error log below:",
        height=200,
        placeholder="Example:\nprint(hello + 6)"
    )

    # Button Logic
    if st.button("🔎 Debug Code"):
        # Check if input is empty or just whitespace
        if not user_input or user_input.strip() == "":
            st.warning("Please enter some code or an error message first.")
        else:
            with st.spinner("Analyzing your code..."):
                try:
                    # 1. Build the prompt using your helper
                    prompt = build_debugging_prompt(user_input)
                    
                    # 2. Get the cached client (instead of re-initializing)
                    client = get_gemini_client()
                    
                    # 3. Get the AI response
                    response = client.ask(prompt)

                    # 4. Display the results
                    st.markdown("---")
                    st.subheader("🧠 Debugging Result")
                    st.markdown(response)

                except Exception as e:
                    # Catch and display any API or logic errors
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()