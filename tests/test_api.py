import os
from dotenv import load_dotenv
from together import Together

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('TOGETHER_API_KEY')
print(f"API key found: {'Yes' if api_key else 'No'}")

try:
    # Initialize client
    client = Together(api_key=api_key)
    
    # Simple completion
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",  # Try a different model
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
    
    # Try with direct API call
    import requests
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "max_tokens": 128,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            json=data
        )
        print(f"Direct API call status: {response.status_code}")
        print(response.json())
    except Exception as e2:
        print(f"Direct API call error: {e2}")