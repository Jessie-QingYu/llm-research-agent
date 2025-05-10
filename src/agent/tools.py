import os
import re
import json
import requests 
from typing import List, Dict, Optional
from together import Together 
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key with a helpful error message if missing
api_key = os.getenv('TOGETHER_API_KEY')
if not api_key:
    raise ValueError(
        "TOGETHER_API_KEY not found. Please set this environment variable "
        "or create a .env file with TOGETHER_API_KEY=your_api_key"
    )

# Initialize Together client
client = Together(api_key=api_key)

# Define functions at module level instead of inside a class
def topic_breakdown(topic: str) -> List[str]:
    """Break down a research topic into smaller, focused subtopics.
    
    Args:
        topic (str): The main research topic
        
    Returns:
        List[str]: List of subtopics
    """
    # For testing, return a simple list of subtopics
    return [
        "Intelligent Tutoring Systems (ITS)",
        "Personalized Learning",
        "Automated Grading",
        "Natural Language Processing (NLP) in Education",
        "Virtual Learning Environments (VLEs)"
    ]

def query_expansion(subtopics: List[str]) -> List[str]:
    """Generate related keywords, synonyms, and phrases for each subtopic.
    
    Args:
        subtopics (List[str]): List of subtopics
        
    Returns:
        List[str]: Expanded list of search queries
    """
    # For testing, return a simple list of expanded queries
    return [
        "AI tutoring systems",
        "machine learning in education",
        "personalized learning platforms",
        "adaptive learning technologies",
        "automated essay grading"
    ]

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def search(queries: List[str]) -> List[str]:
    """Perform web searches for the expanded queries.
    
    Args:
        queries (List[str]): List of search queries
        
    Returns:
        List[str]: List of search results with titles and URLs
    """
    # For testing, return mock search results
    return [
        "Intelligent Tutoring Systems: A Review - https://example.com/its-review",
        "The Impact of AI on Education - https://example.com/ai-education-impact",
        "Personalized Learning: Current Status and Future Directions - https://example.com/personalized-learning"
    ]

def summarize_content(content: str) -> str:
    """Generate a concise summary of the provided content.
    
    Args:
        content (str): Content to summarize
        
    Returns:
        str: Generated summary
    """
    # For testing, return a simple summary
    return "AI has numerous applications in education, including intelligent tutoring systems, personalized learning platforms, and automated grading tools."

def critique_summary(summary: str) -> str:
    """Provide a critique of the generated summary.
    
    Args:
        summary (str): Summary to critique
        
    Returns:
        str: Critique and suggestions
    """
    # For testing, return a simple critique
    return "The summary is concise but could benefit from more specific examples and statistics to support the claims."

def improve_summary(summary: str, critique: str) -> str:
    """Improve the summary based on the critique.
    
    Args:
        summary (str): Original summary
        critique (str): Critique and suggestions
        
    Returns:
        str: Improved summary
    """
    # For testing, return an improved summary
    return "AI has transformed education through several key applications: (1) Intelligent tutoring systems that provide personalized guidance to students, (2) Adaptive learning platforms that adjust content based on student performance, and (3) Automated grading tools that save teachers time and provide quick feedback to students."

def parse_tool_response(response: str):
    """Parse the response from a tool call."""
    function_regex = r"<function=(\w+)>(.*?)</function>"
    match = re.search(function_regex, response, re.DOTALL)

    if match:
        function_name = match.group(1)
        function_args = match.group(2)
        try:
            args_dict = json.loads(function_args)
            return {
                "function": function_name,
                "arguments": args_dict
            }
        except json.JSONDecodeError:
            return {
                "function": function_name,
                "arguments": {}
            }
    return None

# You can keep the class for backward compatibility if needed
class ResearchTools:
    topic_breakdown = staticmethod(topic_breakdown)
    query_expansion = staticmethod(query_expansion)
    search = staticmethod(search)
    summarize_content = staticmethod(summarize_content)
    critique_summary = staticmethod(critique_summary)
    improve_summary = staticmethod(improve_summary)
    parse_tool_response = staticmethod(parse_tool_response)
