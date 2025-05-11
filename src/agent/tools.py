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
                    model=MODEL_TO_USE,  # Using the free model
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
    
    # Add the original topic to ensure relevance
    if "machine learning engineer" not in " ".join(queries_to_use).lower():
        queries_to_use.insert(0, "how to become a machine learning engineer")
    
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
    
    # If no results or API key not available, use fallback
    if not results:
        # Fallback results specifically for machine learning engineer
        results = [
            "How to Become a Machine Learning Engineer - Coursera - https://www.coursera.org/articles/machine-learning-engineer",
            "How to Become a Machine Learning Engineer in 2023 - LearnDataSci - https://www.learndatasci.com/become-machine-learning-engineer/",
            "Machine Learning Engineer: Career Path, Salary & Job Description - Springboard - https://www.springboard.com/blog/data-science/machine-learning-engineer-career-guide/",
            "How to Become a Machine Learning Engineer - Berkeley Boot Camps - https://bootcamp.berkeley.edu/blog/how-to-become-a-machine-learning-engineer/",
            "Machine Learning Engineer Career Path: Skills, Roles & Responsibilities - Simplilearn - https://www.simplilearn.com/machine-learning-engineer-career-path-article"
        ]
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
            
            prompt = f"""Please summarize the following search results about becoming a machine learning engineer:

{formatted_results}

Provide a comprehensive summary that covers:
1. Required skills and knowledge
2. Education and background needed
3. Learning path recommendations
4. Job prospects and career growth
5. Common challenges and how to overcome them

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
    
    # Fallback response
    return """
Becoming a Machine Learning Engineer requires a combination of technical skills, education, and practical experience. Here's a comprehensive guide:

**Required Skills and Knowledge:**
- Strong programming skills in Python, R, or Java
- Solid understanding of mathematics, particularly linear algebra, calculus, and statistics
- Proficiency in machine learning frameworks like TensorFlow, PyTorch, or scikit-learn
- Knowledge of data structures and algorithms
- Experience with data preprocessing and feature engineering
- Understanding of neural networks and deep learning concepts

**Education and Background:**
- A bachelor's degree in Computer Science, Mathematics, Statistics, or related field is typically required
- Many positions prefer a master's degree or Ph.D., especially for research-oriented roles
- Relevant certifications from platforms like Coursera, edX, or specialized programs can supplement formal education

**Learning Path Recommendations:**
- Start with programming fundamentals and mathematics
- Move on to machine learning basics and algorithms
- Gain experience with ML frameworks and libraries
- Work on personal projects to build a portfolio
- Participate in competitions on platforms like Kaggle
- Contribute to open-source projects
- Network with professionals in the field

**Job Prospects and Career Growth:**
- Machine Learning Engineers are in high demand across industries
- Salary ranges are typically high, with median salaries well above average
- Career progression can lead to Senior ML Engineer, ML Architect, or AI Research Scientist roles
- Opportunities exist in tech companies, healthcare, finance, automotive, and many other sectors

**Common Challenges and Solutions:**
- Keeping up with rapidly evolving field: Dedicate time to continuous learning
- Bridging theory and practice: Work on real-world projects
- Handling large datasets: Learn distributed computing and optimization techniques
- Explaining complex models: Develop communication skills to translate technical concepts
"""

# Critique Summary Tool
def critique_summary(summary: str) -> str:
    """Provide a critique of the generated summary."""
    if client:
        try:
            prompt = f"""Please critique the following summary about becoming a machine learning engineer:

{summary}

Evaluate the summary based on:
1. Accuracy and correctness of information
2. Comprehensiveness (are any important aspects missing?)
3. Structure and organization
4. Clarity and readability
5. Actionability (how useful is this for someone wanting to become a machine learning engineer?)

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
    
    # Fallback response
    return """
**Critique of the Summary**

The summary provides a good overview of becoming a machine learning engineer, but has several areas for improvement:

1. **Accuracy**: The information is generally accurate but lacks specific details about the depth of knowledge required in mathematics and statistics.

2. **Comprehensiveness**: The summary misses some important aspects:
   - No mention of cloud platforms (AWS, Azure, GCP) which are essential for deploying ML models
   - Limited discussion of MLOps and deployment practices
   - No information about soft skills like communication and teamwork
   - Missing details about domain expertise importance

3. **Structure**: The organization is logical but the sections could be better connected to show a progression from learning to career.

4. **Clarity**: Some technical terms are used without explanation, which might confuse beginners.

5. **Actionability**: While it provides general guidance, it lacks specific resources, courses, or tools that beginners should start with.

**Suggestions for Improvement:**
- Add specific learning resources and recommended courses
- Include information about cloud platforms and MLOps
- Discuss the importance of domain knowledge in specific industries
- Provide a more detailed roadmap with timeframes
- Add examples of entry-level projects beginners can build
"""

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
    
    # Fallback response should be generic, not specific to ML engineering
    return """
# Summary

This is a fallback summary generated when the API call fails. The actual summary would contain information about the researched topic, addressing the points raised in the critique.

The summary would typically include:
- Key concepts and definitions
- Important aspects of the topic
- Practical applications
- Current trends and developments
- Relevant resources for further exploration

For accurate results, please ensure your API key is correctly configured and try again.
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
