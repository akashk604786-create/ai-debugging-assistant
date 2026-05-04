import sys
import os
import json
import difflib
import re
import streamlit as st

# ✅ MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="AI Debugging Assistant",
    page_icon="🧠",
    layout="centered"
)

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from utils.llm_client import GeminiClient
from utils.debugging_helper import build_debugging_prompt


# ---------------- CLEAN RESPONSE ----------------
def clean_code(text):
    if not text:
        return ""

    text = re.sub(r"```[a-zA-Z]*", "", text)
    text = text.replace("```", "")
    text = text.replace("\\n", "\n")
    text = text.replace('\\"', '"')

    return text.strip()


# ---------------- EXTRACT JSON ----------------
def extract_json(response):
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        json_str = response[start:end]
        return json.loads(json_str)
    except:
        return None


# ---------------- MAIN APP ----------------
def main():

    # ✅ Fix horizontal scroll
    st.markdown(
        """
        <style>
        .stApp {
            overflow-x: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ✅ Prevent refresh loop
    if "result" not in st.session_state:
        st.session_state.result = None

    # ---- Header ----
    st.markdown(
        """
        <h1 style='text-align: center;'>🧠 AI Debugging Assistant</h1>
        <p style='text-align: center; color: grey;'>
        Paste your Python code or error logs and get instant debugging help.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---- Input ----
    st.subheader("📥 Input Code / Error")

    user_input = st.text_area(
        "Enter your code or error:",
        height=220,
        placeholder="Example:\nprint(Hello World)"
    )

    debug_clicked = st.button("🔍 Debug")

    if not user_input:
        st.info("👆 Enter your code above and click Debug to get started.")

    # ---- Debug ----
    if debug_clicked:
        if not user_input.strip():
            st.warning("⚠️ Please enter some code or error message.")
            return

        with st.spinner("⚡ Analyzing your code..."):
            try:
                prompt = build_debugging_prompt(user_input)
                client = GeminiClient()
                response = client.ask(prompt)

                # ✅ Store result
                st.session_state.result = response

            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ API limit reached. Please try again later.")
                elif "API key expired" in str(e) or "API_KEY_INVALID" in str(e):
                    st.error("🔑 API key expired. Please generate a new one.")
                else:
                    st.error("⚠️ AI service error. Please try again.")

                st.stop()  # ✅ Prevent infinite reload

    # ---- Show Result ----
    if st.session_state.result:
        response = st.session_state.result

        st.markdown("---")
        st.subheader("🧠 Debugging Result")
        st.success("✅ Analysis Complete")

        data = extract_json(response)

        if not data:
            st.error("⚠️ Failed to parse response. Try again.")
            return

        # ---- Explanation ----
        with st.expander("🧠 Explanation", expanded=True):
            st.markdown(data.get("explanation", "No explanation provided."))

        # ---- Error ----
        with st.expander("❌ Error"):
            st.warning(data.get("error", "No error detected."))

        # ---- Line ----
        line = data.get("line", "")
        if line:
            with st.expander("📍 Possible Error Location"):
                st.warning(f"⚠️ {line}")

        # ---- Fix ----
        raw_fix = data.get("fix", "")
        fix_code = clean_code(raw_fix)

        with st.expander("🔧 Fix"):
            st.code(
                fix_code if fix_code else "No fix available.",
                language="python",
                line_numbers=True
            )

        # ---- Diff ----
        if fix_code:
            original = user_input.strip().splitlines()
            fixed = fix_code.splitlines()

            diff = difflib.unified_diff(
                original,
                fixed,
                fromfile="Original",
                tofile="Fixed",
                lineterm=""
            )

            diff_text = "\n".join(diff)

            with st.expander("🔄 Code Difference"):
                st.code(diff_text, language="diff")

        # ---- Tips ----
        with st.expander("💡 Tips"):
            tips = data.get("tips", "")
            if isinstance(tips, list):
                for t in tips:
                    st.markdown(f"- {t}")
            else:
                st.markdown(tips or "No additional tips.")

    # ---- Footer ----
    st.markdown(
        """
        <hr>
        <p style='text-align:center; color:grey; font-size:12px;'>
        Built by Akash Kumar • AI Debugging Assistant 🚀
        </p>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()