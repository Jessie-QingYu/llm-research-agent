import os
import re
import json
import requests 
from typing import List, Dict, Optional
from dotenv import load_dotenv
import time
from ..utils.helpers import load_config

# Load environment variables from .env file
load_dotenv()

# Load configuration
config = load_config()
MODEL_TO_USE = config['models']['default']
MODEL_PARAMS = config['models']['parameters']
SEARCH_CONFIG = config['search']

# Try to import Together, but provide fallbacks if not available
try:
    from together import Together
    # Get API key with a helpful error message if missing
    api_key = os.getenv('TOGETHER_API_KEY')
    if api_key:
        client = Together(api_key=api_key)
    else:
        print("Warning: TOGETHER_API_KEY not found. Using fallback responses.")
        client = None
except ImportError:
    print("Warning: Together package not installed. Using fallback responses.")
    client = None

# Try to import other optional dependencies
try:
    from bs4 import BeautifulSoup
    bs4_available = True
except ImportError:
    bs4_available = False

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
    tenacity_available = True
except ImportError:
    tenacity_available = False
    # Define simple retry decorator as fallback
    def retry(*args, **kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Topic Breakdown Tool
def topic_breakdown(topic: str) -> List[str]:
    """Break down a research topic into smaller, focused subtopics."""
    if client:
        try:
            prompt = f"Break down the following research topic into smaller, more focused subtopics:\n\n{topic}"
            response_text = client.chat.completions.create(
                    model=MODEL_TO_USE,
                    messages=[
                          {"role": "user", "content": prompt}
                        ],
                    max_tokens=256,
                    temperature=0.7,
                    top_p=0.7,
                    top_k=50,
                    repetition_penalty=1,
                    stream=False
                ).choices[0].message.content
            subtopics = re.findall(r'\*\*(.*?)\*\*', response_text)
            result = [subtopic.strip() for subtopic in subtopics if subtopic.strip()]
            if result:
                return result
        except Exception as e:
            print(f"Error in topic_breakdown: {e}")
    
    # Generic fallback response
    return [
        "Core Concepts",
        "Historical Development",
        "Current Applications",
        "Future Trends",
        "Related Technologies"
    ]

# Query Expansion Tool
def query_expansion(subtopics: List[str]) -> List[str]:
    """Generate related keywords, synonyms, and phrases for each subtopic."""
    if client:
        try:
            expanded_queries = []
            for subtopic in subtopics:
                prompt = f"""Generate related keywords, synonyms, and phrases for the following subtopic: {subtopic}
                Please format your response as a simple list with one item per line, starting each line with a dash (-).
                For example:
                - keyword 1
                - keyword 2
                - phrase 1
                """
                response_text = client.chat.completions.create(
                    model=MODEL_TO_USE,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=256,
                    temperature=0.7,
                    top_p=0.7,
                    top_k=50,
                    repetition_penalty=1,
                    stream=False
                ).choices[0].message.content
                
                # Extract keywords using regex - look for dash-prefixed items
                keywords = re.findall(r'- (.*?)(?:\n|$)', response_text)
                
                # If no dash-prefixed items found, try splitting by newlines
                if not keywords:
                    keywords = [line.strip() for line in response_text.split('\n') 
                               if line.strip() and not line.strip().startswith('#')]
                
                expanded_queries.extend([keyword.strip() for keyword in keywords if keyword.strip()])
            
            if expanded_queries:
                return expanded_queries[:10]  # Limit to top 10 queries
        except Exception as e:
            print(f"Error in query_expansion: {e}")
    
    # Fallback response for machine learning engineer topic
    return [
        "machine learning engineer skills",
        "machine learning career path",
        "ML engineer vs data scientist",
        "machine learning programming languages",
        "machine learning projects portfolio",
        "machine learning engineer salary",
        "machine learning certifications",
        "machine learning job requirements",
        "machine learning engineer interview questions",
        "how to become ML engineer without degree"
    ]

# Search Tool
def search(queries: List[str], max_results: int = 10) -> List[str]:
    """Perform a search query and return results."""
    if not queries:
        return []
    
    # Use only the first 5 queries to avoid overwhelming the search
    queries_to_use = queries[:5]
    
    results = []
    you_api_key = os.getenv('YOU_API_KEY')
    
    if you_api_key:
        try:
            for query in queries_to_use:
                response = requests.get(
                    f"https://api.you.com/api/search",
                    params={"query": query, "api_key": you_api_key},
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('results', [])[:3]:  # Get top 3 results per query
                        title = item.get('title', '')
                        url = item.get('url', '')
                        if title and url:
                            results.append(f"{title} - {url}")
        except Exception as e:
            print(f"Error in search: {e}")
    
    # If no results or API key not available, return empty list
    # No fallback results - better to return nothing than incorrect information
    return results[:max_results]

# Summarize Content Tool
def summarize_content(search_results: List[str]) -> str:
    """Summarize the content from search results."""
    if not search_results:
        return "No search results to summarize."
    
    if client:
        try:
            # Format search results for the prompt
            formatted_results = "\n\n".join([f"Source {i+1}: {result}" for i, result in enumerate(search_results)])
            
            prompt = f"""Please summarize the following search results:

{formatted_results}

Provide a comprehensive summary that covers:
1. Key concepts and definitions
2. Important aspects and components
3. Practical applications
4. Current trends and developments
5. Common challenges and solutions

Your summary should be well-structured and informative.
"""
            
            response_text = client.chat.completions.create(
                model=MODEL_TO_USE,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=512,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stream=False
            ).choices[0].message.content
            
            return response_text
        except Exception as e:
            print(f"Error in summarize_content: {e}")
    
    # No fallback - return a message indicating the error
    return "Unable to generate summary due to API error. Please try again later."

# Critique Summary Tool
def critique_summary(summary: str) -> str:
    """Provide a critique of the generated summary."""
    if client:
        try:
            prompt = f"""Please critique the following summary:

{summary}

Evaluate the summary based on:
1. Accuracy and correctness of information
2. Comprehensiveness (are any important aspects missing?)
3. Structure and organization
4. Clarity and readability
5. Actionability (how useful is this for someone interested in the topic?)

Provide specific suggestions for improvement.
"""
            
            response_text = client.chat.completions.create(
                model=MODEL_TO_USE,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=512,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stream=False
            ).choices[0].message.content
            
            return response_text
        except Exception as e:
            print(f"Error in critique_summary: {e}")
    
    # No fallback - return a message indicating the error
    return "Unable to generate critique due to API error. Please try again later."

# Improve Summary Tool
def improve_summary(summary: str, critique: str) -> str:
    """Improve the summary based on the critique."""
    if client:
        try:
            prompt = f"""Please improve the following summary based on the critique provided:

Original Summary:
{summary}

Critique:
{critique}

Create an improved, comprehensive summary that addresses all the issues mentioned in the critique. The improved summary should be well-structured, accurate, and highly actionable for someone interested in this topic.
"""
            
            response_text = client.chat.completions.create(
                model=MODEL_TO_USE,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stream=False
            ).choices[0].message.content
            
            return response_text
        except Exception as e:
            print(f"Error in improve_summary: {e}")
    
    # No fallback - return a message indicating the error
    return "Unable to generate improved summary due to API error. Please try again later."

# Parse Tool Response
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

# Helper function to extract title and link from search results
def extract_title_and_link(result: str) -> tuple:
    """Extract title and link from a search result string."""
    match = re.match(r'(.*?) - (https?://\S+)', result)
    if match:
        return match.groups()
    return (result, "#")
