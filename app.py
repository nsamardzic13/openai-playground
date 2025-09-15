import json
import streamlit as st
from openai import OpenAI

with open("config.json") as f:
    config = json.load(f)

client = OpenAI(api_key=st.secrets["api_key"], base_url=config["base_url"])

system_content = """
You are focused on data engineering tasks and you answer in a concise manner.
You do not answer questions that are not related to data engineering or programming. If you do not know the answer, you say 'I don't know'.
You do not make up answers.
You always answer in the english.
You always answer in the format:
If you are asked to write code, you always send only the code differential, not the whole file.
You always answer in markdown format, with code blocks for code.
If not asked, you do not explain the code.
"""

st.title("OpenAI Q&A")

# --- User inputs ---
user_question = st.text_area("Enter your question")
date_guard = st.text_input("Which date is today (yyyy-mm-dd)?", placeholder="Type today's date to enable Run button")

# --- Run button only active if entered ---
can_run = date_guard.strip().lower() == st.secrets["today_date"].strip().lower()
st.write(f"Run button {'enabled' if can_run else 'disabled until you type today date'}")

if st.button("Run", disabled=not can_run):
    if user_question.strip():
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model=config["model"],
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_question},
                ],
                temperature=0.5,
                stream=False,
            )
        st.markdown(response.choices[0].message.content)
    else:
        st.warning("Please enter a question.")
