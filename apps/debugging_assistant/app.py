import streamlit as st

# 1. MUST be the absolute first line of code executed to prevent connection loops
st.set_page_config(
    page_title="AI Debugging Assistant",
    page_icon="🔎",
    layout="centered"
)

import sys
import os

# 2. Perform system path modifications and other imports AFTER config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.llm_client import GeminiClient
from utils.debugging_helper import build_debugging_prompt

# 3. Cache the resource to keep the connection stable
@st.cache_resource
def get_gemini_client():
    return GeminiClient()

def main():
    st.title("🔧 AI Debugging Assistant")
    st.write("Paste your **Python Code** or **error log**, and I'll help you debug it.")

    # Input area
    user_input = st.text_area(
        "Enter your code or error log below:",
        height=200,
        placeholder="Example:\nprint(\"hello\" + 5)"
    )

    # Button Logic
    if st.button("🔎 Debug Code"):
        # Check if input is empty or just whitespace
        if not user_input or user_input.strip() == "":
            st.warning("Please enter some code or an error message first.")
        else:
            # The spinner provides visual feedback that the app is working
            with st.spinner("Analyzing your code..."):
                try:
                    # Build the prompt
                    prompt = build_debugging_prompt(user_input)
                    
                    # Get the cached client
                    client = get_gemini_client()
                    
                    # Get the AI response
                    response = client.ask(prompt)

                    # Display the results
                    st.markdown("---")
                    st.subheader("🧠 Debugging Result")
                    st.markdown(response)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()