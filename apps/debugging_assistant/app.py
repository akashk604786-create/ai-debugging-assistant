import streamlit as st
import sys
import os

# STAGE 1: SET SYSTEM PATH (Fixes ModuleNotFoundError)
# This must run before 'from utils...' so the server knows where the utils folder is.
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../../'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# STAGE 2: IMPORTS
from utils.llm_client import GeminiClient
from utils.debugging_helper import build_debugging_prompt

# STAGE 3: INITIALIZE SESSION (Fixes Bad Message Format)
# This MUST be the first Streamlit command called.
st.set_page_config(
    page_title="AI Debugging Assistant",
    page_icon="🔎",
    layout="centered"
)

# STAGE 4: CACHING (Fixes the Connecting Loop)
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
        if not user_input or user_input.strip() == "":
            st.warning("Please enter some code or an error message first.")
        else:
            # result_container ensures Streamlit has a dedicated spot to write to,
            # which prevents the "Connecting" UI glitch.
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