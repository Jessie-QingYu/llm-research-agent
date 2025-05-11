import os
import sys
from dotenv import load_dotenv
import requests

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Load environment variables
load_dotenv()

# import from src
from src.agent.research_agent import ResearchAgent

def main():
    # Get API key from environment
    api_key = os.getenv('TOGETHER_API_KEY')
    if not api_key:
        print("ERROR: TOGETHER_API_KEY not found. Please set this environment variable.")
        print("You can get an API key from https://api.together.xyz/settings/api-keys")
        return
        
    # Initialize the research agent
    agent = ResearchAgent()
    
    # Define research topic
    topic = "the drugs for RAS inhibitors"
    
    # Execute research
    result = agent.research(topic)
    
    # Print results
    print(f"Research Results for: {topic}\n")
    print(result)

if __name__ == "__main__":
    main()