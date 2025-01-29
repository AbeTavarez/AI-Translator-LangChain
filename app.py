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

# UI Select-box - user will pick the language to translate to
language_to_translate = st.selectbox(
    label="Language to translate to:",
    options=["English", "Spanish", "French", "Japanese"] # <- add more languages
)

# UI Text Area - user will paste the text in here
text_to_translate = st.text_area("Paste text here:")

# UI Button - user will press the button when they're ready to translate the text
translate_btn = st.button("Translate")


# Models, You can try different models:
groq_llm = ChatGroq(model="llama3-8b-8192")
openai_llm = ChatOpenAI()

# Chat Prompt Template - A reusable prompt template that we can just pass the language and text to translate 
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You're a professional translator. You task is to translate the following text to {language}"), ("user", "{text}")
    ]
)

# Prompt from the prompt template gets invoke with the actual text and language to translate 
prompt = chat_prompt_template.invoke({
    "language": language_to_translate,
    "text": text_to_translate
})

# If the button is press and the text area is not empty then we start translating.
if translate_btn and text_to_translate.strip() != "":
    placeholder = st.empty() # empty placeholder for the translation
    full_translation = "" # string to concatenate the chunks of text from the model
    
    # we stream the response from the model
    for chunk in groq_llm.stream(prompt):
        print(chunk)
        full_translation += chunk.content # concat each chunk
        placeholder.text(full_translation) # show concatenated string in the UI
    st.balloons() # <- balloons just for fun!

elif translate_btn:
    st.error("Please provide the text to translate.")