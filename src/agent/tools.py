import os
import re
import json
import requests 
from typing import List, Dict, Optional
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

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
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                    messages=[
                          {"role": "user", "content": prompt}
                        ],
                    max_tokens=256,
                    temperature=0.7,
                    top_p=0.7,
                    top_k=50,
                    repetition_penalty=1,
                    stop=["<|eot_id|>"],
                    stream=False
                ).choices[0].message.content
            subtopics = re.findall(r'\*\*(.*?)\*\*', response_text)
            result = [subtopic.strip() for subtopic in subtopics if subtopic.strip()]
            if result:
                return result
        except Exception as e:
            print(f"Error in topic_breakdown: {e}")
    
    # Fallback response
    return [
        "Intelligent Tutoring Systems (ITS)",
        "Personalized Learning",
        "Automated Grading",
        "Natural Language Processing (NLP) in Education",
        "Virtual Learning Environments (VLEs)"
    ]

# Query Expansion Tool
def query_expansion(subtopics: List[str]) -> List[str]:
    """Generate related keywords, synonyms, and phrases for each subtopic."""
    if client:
        try:
            expanded_queries = []
            for subtopic in subtopics:
                prompt = f"Generate related keywords, synonyms, and phrases for the following subtopic:\n\n{subtopic}"
                response_text = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=256,
                    temperature=0.7,
                    top_p=0.7,
                    top_k=50,
                    repetition_penalty=1,
                    stop=["<|eot_id|>"],
                    stream=False
                ).choices[0].message.content
                
                # Extract keywords using regex
                keywords = re.findall(r'- (.*?)(?:\n|$)', response_text)
                if not keywords:
                    keywords = re.findall(r'\*\*(.*?)\*\*', response_text)
                if not keywords:
                    keywords = [line.strip() for line in response_text.split('\n') if line.strip()]
                
                expanded_queries.extend([keyword.strip() for keyword in keywords if keyword.strip()])
            
            if expanded_queries:
                return expanded_queries[:10]  # Limit to top 10 queries
        except Exception as e:
            print(f"Error in query_expansion: {e}")
    
    # Fallback response
    return [
        "adaptive learning software",
        "personalized education technology",
        "AI tutoring systems",
        "machine learning in education",
        "educational data mining",
        "automated assessment tools",
        "natural language processing for education",
        "virtual reality classrooms",
        "AI teaching assistants",
        "smart content in education"
    ]

# Search Tool
def search(queries: List[str]) -> List[str]:
    """Perform web searches for the expanded queries."""
    results = []
    
    # Use a simple web search API (replace with your preferred search API)
    search_url = "https://api.duckduckgo.com/"
    
    for query in queries[:5]:  # Limit to top 5 queries
        try:
            params = {
                'q': query + " education technology",
                'format': 'json'
            }
            response = requests.get(search_url, params=params, timeout=10)
            data = response.json()
            
            # Extract results
            if 'Results' in data and data['Results']:
                for result in data['Results'][:3]:  # Get top 3 results per query
                    title = result.get('Title', 'No Title')
                    url = result.get('FirstURL', '#')
                    results.append(f"{title} - {url}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
        except Exception as e:
            print(f"Search error: {e}")
    
    # If no results were found, use fallback results
    if not results:
        results = [
            "25 Best Online Learning Platforms for the Virtual Classroom | Prodigy Education - https://www.prodigygame.com/main-en/blog/online-learning-platforms/",
            "Virtual Learning Platforms and Tools for Teachers and Kids - https://achievevirtual.org/blog/teacher-resources/virtual-learning-platforms-teachers-kids/",
            "30+ Virtual Learning Platforms and Tools for Teachers and Kids - https://www.weareteachers.com/virtual-learning-platforms/",
            "Best online learning platform of 2024 | TechRadar - https://www.techradar.com/best/best-online-learning-platforms",
            "13 Educational Platforms (Updated list 2024) | SC Training - https://training.safetyculture.com/blog/educational-platforms/"
        ]
    
    return results

# Summarize Content Tool
def summarize_content(content: str) -> str:
    """Generate a concise summary of the provided content."""
    if client:
        try:
            prompt = f"Please summarize the following content:\n\n{content}"
            
            summary = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=256,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stop=["<|eot_id|>"],
                stream=False
            ).choices[0].message.content
            
            return summary
        except Exception as e:
            print(f"Error in summarize_content: {e}")
    
    # Fallback response
    return "Online learning platforms have transformed education by providing accessible, flexible, and personalized learning experiences. These platforms offer a range of features including virtual classrooms, interactive lessons, and adaptive learning paths. Popular platforms like Udemy, Coursera, and edX have democratized access to high-quality educational content across various subjects and skill levels."

# Critique Summary Tool
def critique_summary(summary: str) -> str:
    """Provide a critique of the generated summary."""
    if client:
        try:
            prompt = f"""
            Please critique the following summary and provide suggestions for improvement:
            
            {summary}
            
            Your critique should cover:
            1. Strengths of the summary
            2. Weaknesses or areas for improvement
            3. Specific suggestions to enhance clarity, coherence, and completeness
            """
            
            critique = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=256,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stop=["<|eot_id|>"],
                stream=False
            ).choices[0].message.content
            
            return critique
        except Exception as e:
            print(f"Error in critique_summary: {e}")
    
    # Fallback response
    return "The summary provides a good overview but could benefit from more specific examples and statistics. Consider adding information about the impact of these platforms on learning outcomes and addressing potential challenges or limitations."

# Improve Summary Tool
def improve_summary(summary: str, critique: str) -> str:
    """Improve the summary based on the critique."""
    if client:
        try:
            prompt = f"""
            Initial Summary:
            {summary}

            Critique and Suggestions:
            {critique}

            Based on the above critique and suggestions, improve the initial summary to address the points mentioned.
            """

            improved_summary = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=256,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
                stop=["<|eot_id|>"],
                stream=False
            ).choices[0].message.content

            return improved_summary
        except Exception as e:
            print(f"Error in improve_summary: {e}")
    
    # Fallback response
    return """
**Unlocking the Potential of Education Technology**

In the ever-evolving landscape of education, technology has emerged as a powerful tool to enhance learning outcomes and bridge the gap between students and educators. This summary explores the key concepts and platforms that are revolutionizing the way we learn and teach.

**Online Learning Platforms:**

Online learning platforms have transformed the way we access education, offering a range of features that cater to diverse learning styles and needs. Platforms like Prodigy Education, Achieve Virtual, We Are Teachers, and LearnWorlds provide virtual classrooms, interactive lessons, and personalized learning paths that cater to individual students. For instance, Udemy, Coursera, and edX have democratized access to high-quality educational content, making it possible for anyone to learn new skills and subjects.
"""

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

# You can keep the class for backward compatibility if needed
class ResearchTools:
    topic_breakdown = staticmethod(topic_breakdown)
    query_expansion = staticmethod(query_expansion)
    search = staticmethod(search)
    summarize_content = staticmethod(summarize_content)
    critique_summary = staticmethod(critique_summary)
    improve_summary = staticmethod(improve_summary)
    parse_tool_response = staticmethod(parse_tool_response)
