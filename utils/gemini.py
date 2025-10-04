import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def chat_with_gemini_as_astronomy_expert(message: str) -> str:
    prompt = f"You are an expert on exoplanets. Answer clearly and concisely in plain text without markdown: {message}"
    response = model.generate_content(prompt)
    text = response.text or ""
    text = re.sub(r"[*_`#>-]", "", text)
    text = re.sub(r"\n{2,}", "\n", text).strip()

    return text
