import yaml
import re
from typing import Dict, Any, Optional

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

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