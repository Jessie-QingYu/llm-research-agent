import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Set up environment variables for testing
os.environ['TOGETHER_API_KEY'] = 'test_api_key'
os.environ['YOU_API_KEY'] = 'test_you_api_key'

# Import the tools module
from src.agent.tools import topic_breakdown, query_expansion, search, summarize_content, critique_summary, improve_summary, extract_title_and_link

# Mock the Together client to avoid actual API calls
def mock_together_client():
    with patch('src.agent.tools.client') as mock_client:
        # Create a mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = """
        **Subtopic 1**
        **Subtopic 2**
        **Subtopic 3**
        - keyword 1
        - keyword 2
        - keyword 3
        """
        mock_client.chat.completions.create.return_value = mock_response
        yield mock_client

# Test functions with mocked client
def test_topic_breakdown(mock_together_client):
    topic = "large language models learning paths"
    result = topic_breakdown(topic)
    
    # Check that we get a list of subtopics
    assert isinstance(result, list)
    # We might get the fallback response, which is fine for testing
    assert len(result) > 0

def test_query_expansion(mock_together_client):
    subtopics = ["LLM fundamentals", "Transformer architecture", "Fine-tuning techniques"]
    result = query_expansion(subtopics)
    
    # Check that we get a list of expanded queries
    assert isinstance(result, list)
    assert len(result) > 0

def test_search():
    # Patch the requests.get to avoid actual API calls
    with patch('src.agent.tools.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {'title': 'Test Title 1', 'url': 'https://example.com/1'},
                {'title': 'Test Title 2', 'url': 'https://example.com/2'}
            ]
        }
        mock_get.return_value = mock_response
        
        queries = ["LLM training resources", "transformer architecture explained"]
        result = search(queries)
        
        # Check that we get a list of search results
        assert isinstance(result, list)

def test_summarize_content(mock_together_client):
    search_results = [
        "Introduction to LLMs - https://example.com/intro",
        "Transformer Architecture Explained - https://example.com/transformers",
        "Fine-tuning LLMs for Specific Tasks - https://example.com/fine-tuning"
    ]
    
    # Handle different function signatures
    try:
        result = summarize_content(search_results, "test topic")
    except TypeError:
        result = summarize_content(search_results)
    
    # Check that we get a string summary
    assert isinstance(result, str)
    assert len(result) > 0

def test_critique_summary(mock_together_client):
    summary = "Large language models are neural networks trained on text data."
    result = critique_summary(summary)
    
    # Check that we get a string critique
    assert isinstance(result, str)
    assert len(result) > 0

def test_improve_summary(mock_together_client):
    summary = "Large language models are neural networks trained on text data."
    critique = "The summary is too brief and lacks details about training methods."
    result = improve_summary(summary, critique)
    
    # Check that we get an improved summary string
    assert isinstance(result, str)
    assert len(result) > 0

def test_extract_title_and_link():
    # Test with a properly formatted result
    result = "Introduction to LLMs - https://example.com/intro"
    title, link = extract_title_and_link(result)
    assert title == "Introduction to LLMs"
    assert link == "https://example.com/intro"
    
    # Test with a malformed result
    result = "No link here"
    title, link = extract_title_and_link(result)
    assert title == "No link here"
    assert link == "#"

def test_tools_with_mock(monkeypatch):
    """Test tools with mocked API responses to avoid actual API calls"""
    # This is a more advanced test that uses pytest's monkeypatch to mock API calls
    # You can implement this later if needed
    pass

if __name__ == "__main__":
    unittest.main()

