import google.generativeai as genai

API_KEY = ""# Use here yoour key

def configure_api():
    genai.configure(api_key=API_KEY)

def gimmini(response):
    configure_api()
    model_name = 'gemini-1.5-flash'  # Update with the correct model name if needed
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(response)

    return response.text  # Ensure this is correct
