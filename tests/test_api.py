import os
from dotenv import load_dotenv
from together import Together

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('TOGETHER_API_KEY')
print(f"API key found: {'Yes' if api_key else 'No'}")

# Model to use
MODEL_TO_USE = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

try:
    # Initialize client
    client = Together(api_key=api_key)
    
    print(f"Trying with model: {MODEL_TO_USE}")
    
    # Simple completion
    response = client.chat.completions.create(
        model=MODEL_TO_USE,
        messages=[
            {"role": "user", "content": "Hello, how are you?"}
        ],
        max_tokens=128,
        temperature=0.7
    )
    
    print("Response received:")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"Error: {e}")