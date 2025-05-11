import os
import json
import re
from typing import List, Dict, Any
from dotenv import load_dotenv # type: ignore
from ..utils.helpers import load_config
from .tools import (
    topic_breakdown,
    query_expansion,
    search,
    summarize_content,
    critique_summary,
    improve_summary,
    parse_tool_response
)

class ResearchAgent:
    def __init__(self):
        """Initialize the research agent."""

        # Load environment variables
        load_dotenv()
        
        # Print API key status (for debugging)
        api_key = os.getenv('TOGETHER_API_KEY')
        if api_key:
            print("API key loaded successfully")
        else:
            print("WARNING: TOGETHER_API_KEY not found in environment variables")
            
        self.cache = {
            'subtopics': [],
            'expanded_queries': [],
            'search_results': [],
            'summary': "",
            'critique': "",
            'improved_summary': ""
        }
        
        # Define the research steps
        self.steps = [
            "Break down the research topic",
            "Generate related keywords, synonyms, and phrases for subtopics",
            "Perform a search query",
            "Please summarize the following content",
            "Provide a critique of the generated summary",
            "Improve the generated summary based on critique"
        ]
        
        # Map step names to functions
        self.available_functions = {
            "topic_breakdown": topic_breakdown,
            "query_expansion": query_expansion,
            "search": search,
            "summarize_content": summarize_content,
            "critique_summary": critique_summary,
            "improve_summary": improve_summary
        }

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
        references = []
        seen_urls = set()  # To prevent duplicate references
        
        for i, result in enumerate(self.cache['search_results'][:5]):
            # Extract title and link if available
            match = re.match(r'(.*?) - (https?://\S+)', result)
            if match:
                title, link = match.groups()
                # Check if we've already seen this URL
                if link not in seen_urls:
                    seen_urls.add(link)
                    references.append(f"{len(references)+1}. [{title}]({link})")
            else:
                # If no URL pattern found, just use the result as is
                references.append(f"{len(references)+1}. {result}")
        
        formatted_references = "\n".join(references)
        
        final_result = f"{self.cache['improved_summary']}\n\nReferences:\n{formatted_references}"
        return final_result