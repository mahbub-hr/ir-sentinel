# Orchestrator.py
# @author: mahbub
# This script orchestrates the entire workflow of the IR Sentinel project.
import os
from openai import OpenAI
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pathlib import Path
import time

load_dotenv()  # Load environment variables from .env file


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client_genai = genai.Client()

client_openai = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

PROMPT_DIR = Path(__file__).resolve().parent / "prompt"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OPENAI_OUTPUT_DIR = OUTPUT_DIR / "openai"
GEMINI_OUTPUT_DIR = OUTPUT_DIR / "gemini"
GEMINI_SUMMARY_FILE = GEMINI_OUTPUT_DIR / "summary.txt"
OPENAI_SUMMARY_FILE = OPENAI_OUTPUT_DIR / "summary.txt"
OPENAI_OUTPUT_DIR.mkdir(exist_ok=True)
GEMINI_OUTPUT_DIR.mkdir(exist_ok=True)
USE_SERVICE = "Gemini"
N=30

SUMMARY_FILE = GEMINI_SUMMARY_FILE if USE_SERVICE == "Gemini" else OPENAI_SUMMARY_FILE

def read_prompt_from_file(file_path):
    print(f"Reading prompt from: {file_path}")
    with open(file_path, 'r') as f:
        return f.read()

def write_to_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)

def query_gemini(system_prompt, user_prompt):
    response = client_genai.models.generate_content(
        model="gemini-3-flash-preview", 
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="low"),
            temperature=0.6,
            system_instruction=system_prompt
        ),
        contents=user_prompt
    )
    return response.text

def query_openai(system_prompt, user_prompt):
    response = client_openai.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

system_prompt = read_prompt_from_file(PROMPT_DIR / "system_prompt_uafs.prompt")
session_setup_code_prompt = read_prompt_from_file(PROMPT_DIR / "session_setup_code.prompt")
ksmbd_explainer_prompt = read_prompt_from_file(PROMPT_DIR / "ksmbd_explainer.prompt")
session_setup_context_explainer_prompt = read_prompt_from_file(PROMPT_DIR / "session_setup_context_explainer.prompt")
audit_request_prompt = read_prompt_from_file(PROMPT_DIR / "audit_request.prompt")

prompt = "\n\n".join([
    session_setup_code_prompt,
    ksmbd_explainer_prompt,
    session_setup_context_explainer_prompt,
    audit_request_prompt
])

with open(SUMMARY_FILE, 'w') as f:
    for i in range(N):
        content = None
        try:
            print(f"--- Iteration {i} ---")
            if USE_SERVICE == "Gemini":
                content = query_gemini(system_prompt, prompt)
            else:
                content = query_openai(system_prompt, prompt)

        except Exception as e:
            print(f"Error during generation: {str(e)}")
            time.sleep(20)  # Sleep for a short time before retrying
            continue

        text = content.lower()
        if "use-after-free" in text or "use after free" in text:
            print(f"Use-After-Free vulnerability found in iteration {i}!")
            f.write(f"Use-After-Free vulnerability found in iteration {i}!\n")

        output_file = GEMINI_OUTPUT_DIR / f"output-{i}.txt" if USE_SERVICE == "Gemini" else OPENAI_OUTPUT_DIR / f"output-{i}.txt"
        write_to_file(output_file, content)
        time.sleep(10)  # Sleep for a short time to avoid hitting rate limits