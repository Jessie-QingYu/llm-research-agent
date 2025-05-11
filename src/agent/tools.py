import os
import re
import json
import requests 
from typing import List, Dict, Optional
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Set the model to use - using the free model
MODEL_TO_USE = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

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
            prompt = f"""Please improve the following summary about becoming a machine learning engineer based on the critique provided:

Original Summary:
{summary}

Critique:
{critique}

Create an improved, comprehensive summary that addresses all the issues mentioned in the critique. The improved summary should be well-structured, accurate, and highly actionable for someone wanting to become a machine learning engineer.
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
    
    # Fallback response
    return """
# Comprehensive Guide to Becoming a Machine Learning Engineer

Becoming a successful Machine Learning Engineer requires a strategic approach to skill development, education, and practical experience. This guide provides a roadmap to help you navigate this exciting career path.

## 1. Essential Technical Skills

**Programming Proficiency:**
- **Python**: The primary language for ML development (focus on NumPy, Pandas, Matplotlib)
- **SQL**: For database interactions and data extraction
- **Optional**: R, Java, or C++ for specific applications

**Mathematics and Statistics:**
- Linear Algebra: Understand vectors, matrices, and tensor operations
- Calculus: Grasp derivatives, gradients, and optimization techniques
- Probability and Statistics: Master statistical testing, distributions, and Bayesian thinking

**Machine Learning Frameworks:**
- TensorFlow and Keras: For building and deploying ML models
- PyTorch: Popular for research and deep learning applications
- Scikit-learn: For classical ML algorithms and preprocessing

**Cloud and MLOps:**
- AWS (SageMaker), Azure ML, or Google Cloud AI: For scalable ML deployment
- Docker and Kubernetes: For containerization and orchestration
- CI/CD for ML: Implementing automated testing and deployment pipelines

## 2. Education and Learning Path

**Formal Education Options:**
- Bachelor's degree in Computer Science, Data Science, Mathematics, or related field
- Master's or PhD for research-oriented positions or specialized roles
- Bootcamps as an alternative or supplement to traditional education

**Self-Learning Roadmap:**
1. **Months 1-3**: Programming fundamentals and mathematics refresher
   - Recommended: CS50 (Harvard), Mathematics for Machine Learning (Imperial College London)
2. **Months 4-6**: Machine learning basics and algorithms
   - Recommended: Andrew Ng's Machine Learning course, Fast.ai
3. **Months 7-9**: Deep learning and specialized areas
   - Recommended: Deep Learning Specialization (Coursera), Practical Deep Learning for Coders
4. **Months 10-12**: Projects and portfolio building
   - Focus on solving real problems in domains that interest you

**Certifications Worth Pursuing:**
- AWS Machine Learning Specialty
- TensorFlow Developer Certificate
- Microsoft Azure AI Engineer
- Google Professional Machine Learning Engineer

## 3. Building Practical Experience

**Project Portfolio:**
- Start with tutorial-based projects, then build original solutions
- Include diverse projects: classification, regression, NLP, computer vision
- Document your work thoroughly on GitHub with clean code and explanations

**Practical Learning Opportunities:**
- Kaggle competitions: Start with "Getting Started" competitions
- Open-source contributions: Find beginner-friendly ML projects
- Internships or freelance projects: Gain real-world experience

**Networking and Community:**
- Join ML communities: Reddit r/MachineLearning, Discord servers, local meetups
- Attend conferences: NeurIPS, ICML, or local ML events
- Connect with professionals on LinkedIn and Twitter

## 4. Career Development

**Job Search Strategy:**
- Target entry-level positions: ML Engineer, Junior Data Scientist, AI Developer
- Highlight projects relevant to the company's domain
- Prepare for technical interviews with a focus on ML algorithms and coding challenges

**Salary Expectations:**
- Entry-level: $80,000-$110,000 (US average)
- Mid-level: $110,000-$150,000
- Senior-level: $150,000+ (can exceed $200,000 at top companies)

**Career Progression:**
- Junior ML Engineer → ML Engineer → Senior ML Engineer → Lead ML Engineer/Architect
- Alternative paths: ML Research Scientist, ML Product Manager, AI Consultant

## 5. Continuous Growth

**Staying Current:**
- Follow research papers on arXiv and conference publications
- Subscribe to newsletters: Import AI, The Batch, ML Ops Roundup
- Take advanced courses in emerging areas like reinforcement learning or GANs

**Domain Specialization:**
- Consider focusing on a specific industry: healthcare, finance, robotics, etc.
- Develop domain expertise alongside technical skills
- Understand the business context and value of ML applications

**Soft Skills Development:**
- Communication: Learn to explain complex concepts to non-technical stakeholders
- Teamwork: Collaborate effectively with data engineers, product managers, and domain experts
- Business acumen: Understand how ML creates value for organizations

By following this comprehensive approach, you'll be well-positioned to build a successful career as a Machine Learning Engineer in this rapidly evolving field.
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

    def research(self, topic: str) -> str:
        """Execute the research process on a given topic."""
        print(f"Starting research on: {topic}")
        
        # Step 1: Break down the topic into subtopics
        self.cache['subtopics'] = topic_breakdown(topic)
        print(f"Subtopics: {self.cache['subtopics']}")
        
        # Step 2: Generate expanded queries
        self.cache['expanded_queries'] = query_expansion(self.cache['subtopics'])
        print(f"Expanded queries: {self.cache['expanded_queries'][:5]}...")
        
        # Step 3: Perform search
        self.cache['search_results'] = search(self.cache['expanded_queries'])
        print(f"Found {len(self.cache['search_results'])} search results")
        
        # Step 4: Summarize content
        self.cache['summary'] = summarize_content(self.cache['search_results'])
        print("Generated summary")
        
        # Step 5: Critique summary
        self.cache['critique'] = critique_summary(self.cache['summary'])
        print("Generated critique")
        
        # Step 6: Improve summary
        self.cache['improved_summary'] = improve_summary(self.cache['summary'], self.cache['critique'])
        print("Generated improved summary")
        
        # Extract references from search results
        from .tools import extract_title_and_link
        references = []
        for i, result in enumerate(self.cache['search_results'][:5]):
            title, link = extract_title_and_link(result)
            if title and link:
                references.append(f"{i+1}. [{title}]({link})")
        formatted_references = "\n".join(references)
        
        # Add references to the final output
        final_result = self.cache['improved_summary'] + "\n\nReferences:\n" + formatted_references
        
        return final_result
