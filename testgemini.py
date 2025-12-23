from dotenv import load_dotenv
import os, google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEN_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
print(model.generate_content("Say hello from Gemini!").text)
