import streamlit as st
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

# ===== UI ===========
st.title("AI Translator App")
st.divider()
st.markdown("## Translate text to any language.")


language_to_translate = st.selectbox(
    label="Language to translate to:",
    options=["English", "Spanish", "French", "Japanese"]
)

text_to_translate = st.text_area("Paste text here:")

translate_btn = st.button("Translate")


# Models
groq_llm = ChatGroq(model="llama3-8b-8192")
openai_llm = ChatOpenAI()

# Chat Prompt Template
chat_prompt_template = ChatPromptTemplate.from_messages(
    [("system", "You're a professional translator. You task is to translate the following text to {language}"), ("user", "{text}")
    ]
)

prompt = chat_prompt_template.invoke({
    "language": language_to_translate,
    "text": text_to_translate
})


if translate_btn and text_to_translate.strip() != "":
    placeholder = st.empty()
    full_translation = ""
    
    for chunk in groq_llm.stream(prompt):
        print(chunk)
        full_translation += chunk.content
        placeholder.text(full_translation)
    st.balloons()

elif translate_btn:
    st.error("Please provide the text to translate.")