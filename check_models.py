import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
if not key:
    print("[ERROR] GOOGLE_API_KEY not found in .env")
    exit(1)

print(f"[OK] Found Key: {key[:5]}...{key[-5:]}")

try:
    print("Querying available models...")
    try:
        from google.ai.generativelanguage_v1beta import ModelServiceClient
        client = ModelServiceClient(client_options={"api_key": key})
        models = [m.name for m in client.list_models() if "generateContent" in m.supported_generation_methods]
        for m in sorted(models):
            print(f"- {m}")
    except ImportError:
        import google.generativeai as genai
        genai.configure(api_key=key)
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                print(f"- {m.name}")
except Exception as e:
    print(f"[ERROR] Error listing models: {e}")