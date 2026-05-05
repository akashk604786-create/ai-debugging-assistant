import streamlit as st
import sys
import os

# 1. FIX PATH FIRST (Fixes ModuleNotFoundError)
# This allows the imports below to actually find your 'utils' folder.
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../../'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 2. CONFIGURE PAGE (Fixes Bad Message Format)
# Must be called before any other Streamlit UI commands.
st.set_page_config(
    page_title="AI Debugging Assistant",
    page_icon="🔎",
    layout="centered"
)

# 3. IMPORTS
from utils.llm_client import GeminiClient
from utils.debugging_helper import build_debugging_prompt

# 4. CACHE CLIENT (Fixes Connecting Loop)
@st.cache_resource
def get_gemini_client():
    return GeminiClient()

def main():
    st.title("🔧 AI Debugging Assistant")
    st.write("Paste your **Python Code** or **error log**, and I'll help you debug it.")

    user_input = st.text_area(
        "Enter your code or error log below:",
        height=200,
        placeholder="Example:\nprint(\"hello\" + 5)"
    )

    if st.button("🔎 Debug Code"):
        if not user_input or user_input.strip() == "":
            st.warning("Please enter some code or an error message first.")
        else:
            # Using st.empty() prevents the UI from flickering 
            # and keeps the connection stable during long AI calls.
            result_container = st.empty()
            with st.spinner("Analyzing your code..."):
                try:
                    prompt = build_debugging_prompt(user_input)
                    client = get_gemini_client()
                    response = client.ask(prompt)

                    with result_container.container():
                        st.markdown("---")
                        st.subheader("🧠 Debugging Result")
                        st.markdown(response)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()