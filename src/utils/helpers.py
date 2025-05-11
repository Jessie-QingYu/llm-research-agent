import yaml
import re
from typing import Dict, Any, Optional
import os

def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml file."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        # Return default config
        return {
            'models': {
                'default': "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                'parameters': {
                    'max_tokens': 256,
                    'temperature': 0.7,
                    'top_p': 0.7,
                    'top_k': 50,
                    'repetition_penalty': 1
                }
            },
            'search': {
                'max_results': 10,
                'timeout': 30
            },
            'cache': {
                'enabled': True,
                'expiry': 3600
            }
        }

def parse_tool_response(response: str) -> Optional[Dict[str, str]]:
    """Parse the response from LLM tools."""
    function_regex = r"<function=(\w+)>"
    match = re.search(function_regex, response)
    
    if match:
        return {"function": match.group(1)}
    return None

def extract_title_and_link(result: str) -> tuple[Optional[str], Optional[str]]:
    """Extract title and link from search result."""
    match = re.match(r'(.*?) - (https?://\S+)', result)
    if match:
        return match.groups()
    return None, None