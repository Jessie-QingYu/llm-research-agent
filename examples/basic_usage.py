import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# import from src
from src.agent.research_agent import ResearchAgent

def main():
    # Initialize the research agent
    agent = ResearchAgent()
    
    # Define research topic
    topic = "Applications of Artificial Intelligence in Education"
    
    # Execute research
    result = agent.research(topic)
    
    # Print results
    print(f"Research Results for: {topic}\n")
    print(result)

if __name__ == "__main__":
    main()