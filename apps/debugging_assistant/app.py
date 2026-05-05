import streamlit as st

# MUST stay at the very top
st.set_page_config(page_title="AI Debugging Assistant", page_icon="🔎")

import sys
import os
from utils.llm_client import GeminiClient
from utils.debugging_helper import build_debugging_prompt

@st.cache_resource
def get_client():
    return GeminiClient()

def main():
    st.title("🔧 AI Debugging Assistant")
    
    user_input = st.text_area("Enter code:", placeholder="print('hello')")

    if st.button("🔎 Debug Code"):
        if not user_input.strip():
            st.warning("Please enter code.")
        else:
            # Using a clear container helps Streamlit manage the UI state better
            result_container = st.empty()
            with st.spinner("Analyzing..."):
                try:
                    client = get_client()
                    prompt = build_debugging_prompt(user_input)
                    response = client.ask(prompt)
                    
                    with result_container.container():
                        st.markdown("---")
                        st.subheader("🧠 Debugging Result")
                        st.markdown(response)
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()