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
        """
        Execute the research workflow on the given topic.
        
        Args:
            topic: The research topic to explore
            
        Returns:
            str: The improved summary of the research
        """
        result = topic  # Initialize result
        
        for step in self.steps:
            print(f"Step: {step}")
            
            # Execute the appropriate function for each step
            if "Break down the research topic" in step:
                subtopics = topic_breakdown(topic)
                self.cache['subtopics'] = subtopics
                result = json.dumps(subtopics)
                
            elif "Generate related keywords" in step:
                expanded_queries = query_expansion(self.cache['subtopics'])
                self.cache['expanded_queries'] = expanded_queries
                result = json.dumps(expanded_queries)
                
            elif "Perform a search query" in step:
                search_results = search(self.cache['expanded_queries'])
                self.cache['search_results'].extend(search_results)
                result = "\n".join(search_results)
                
            elif "summarize" in step.lower():
                summary = summarize_content(result)
                self.cache['summary'] = summary
                result = summary
                
            elif "critique" in step.lower():
                critique = critique_summary(self.cache['summary'])
                self.cache['critique'] = critique
                result = critique
                
            elif "improve" in step.lower():
                improved_summary = improve_summary(self.cache['summary'], self.cache['critique'])
                self.cache['improved_summary'] = improved_summary
                result = improved_summary
            
            print(f"Result: {result[:100]}...\n")
            
        # Format the final result with references
        references = []
        for i, result in enumerate(self.cache['search_results'][:5]):
            # Extract title and link if available
            match = re.match(r'(.*?) - (https?://\S+)', result)
            if match:
                title, link = match.groups()
                references.append(f"{i+1}. [{title}]({link})")
            else:
                references.append(f"{i+1}. {result}")
                
        formatted_references = "\n".join(references)
        
        final_result = f"{self.cache['improved_summary']}\n\nReferences:\n{formatted_references}"
        return final_result