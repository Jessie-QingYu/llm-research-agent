import unittest
from src.agent.research_agent import ResearchAgent

class TestResearchAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ResearchAgent()
        self.test_topic = "Test Topic"

    def test_research_workflow(self):
        result = self.agent.research(self.test_topic)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_cache_initialization(self):
        expected_keys = [
            'subtopics',
            'expanded_queries',
            'search_results',
            'summary',
            'critique',
            'improved_summary'
        ]
        for key in expected_keys:
            self.assertIn(key, self.agent.cache)

if __name__ == '__main__':
    unittest.main()