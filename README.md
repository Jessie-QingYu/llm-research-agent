# LLM-Based Research Agent for Automated Topic Exploration

An autonomous research agent that leverages large language models to explore academic topics comprehensively with minimal human intervention.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1fcu2hZVh2U-EuSYRZ7VmLbrDOrIoD6eb?usp=sharing)

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Technical Implementation](#technical-implementation)
- [Sample Output](#sample-output)
- [Setup and Usage](#setup-and-usage)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Agent](#running-the-agent)
  - [Google Colab](#google-colab)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

This project demonstrates how AI can transform the research process by automating the collection, analysis, and synthesis of information on any given topic. The agent follows a structured workflow that breaks down research questions, expands queries, searches for relevant information, and generates polished summaries—all with minimal human guidance.

## Key Features

- **Autonomous Function Selection**: Utilizes Meta-Llama-3.1 models to automatically choose appropriate tools based on the current research step
- **Modular Tool Architecture**: Implements specialized components for topic breakdown, query expansion, web search, content summarization, and critique-based refinement
- **Self-Improving Mechanism**: Incorporates feedback loops where the system critiques and improves its own outputs
- **Efficient Resource Management**: Uses a caching system to track and reuse intermediate research artifacts
- **External API Integration**: Connects with Together AI API for LLM capabilities and web search services for knowledge retrieval

## How It Works

The research agent follows a six-step process:

1. **Topic Breakdown**: Divides the main research topic into manageable subtopics
2. **Query Expansion**: Generates related keywords, synonyms, and phrases for each subtopic
3. **Web Search**: Performs targeted searches based on expanded queries
4. **Content Summarization**: Synthesizes search results into a coherent summary
5. **Self-Critique**: Evaluates the quality of the generated summary and identifies areas for improvement
6. **Summary Refinement**: Improves the summary based on the critique

## Technical Implementation

The system is built in Python and uses:
- Together AI API for accessing Meta-Llama-3.1 models
- Web search APIs for information retrieval
- Regular expressions for parsing and extracting relevant information
- BeautifulSoup for HTML parsing
- Tenacity for robust API calls with retry logic
- Markdown formatting for presentable outputs

## Sample Output

For the topic "Applications of Artificial Intelligence in Education," the agent produces a well-structured summary like this:


## Setup and Usage

### Prerequisites
- Python 3.8+
- Together API key
- Web search API key

### Installation
```bash
pip install Together
```

### Configuration
Set up your API keys as environment variables:
```python
from google.colab import userdata
client = Together(api_key=userdata.get('TOGETHER_API_KEY'))
```

### Running the Agent
```python
topic = "Your Research Topic"
result = research_agent(topic)
print(result)
```

### Google Colab
You can run this project directly in Google Colab using the badge at the top of this README or by clicking [here](https://colab.research.google.com/drive/1fcu2hZVh2U-EuSYRZ7VmLbrDOrIoD6eb?usp=sharing).

When using Colab:
1. You'll need to add your API keys to the Colab secrets
2. Follow the notebook instructions for executing each cell
3. You can modify the research topic and explore different subject areas

## Project Structure
```
llm-research-agent/
├── examples/              # Example usage scripts
├── notebooks/             # Jupyter notebooks for development and demonstration
├── src/                   # Source code
│   ├── agent/             # Research agent implementation
│   │   ├── research_agent.py  # Main agent class
│   │   └── tools.py       # Research tools implementation
│   └── utils/             # Utility functions
├── .env                   # Environment variables (not tracked by git)
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
└── LICENSE                # License information
```

## Future Improvements

- Integration with additional knowledge sources (academic databases, books)
- Enhanced critique capabilities through specialized evaluation metrics
- Improved search result filtering and source credibility assessment
- Support for multimedia content in research outputs
- User interface for easier interaction with the research agent

## Contributing

Contributions are welcome! Here's how you can contribute:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add some amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a pull request**

Please make sure to update tests as appropriate and adhere to the existing coding style.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Together AI for providing access to state-of-the-art language models
- You.com for search API capabilities
- The open-source NLP community for inspiration and resources

---

Feel free to contribute to this project by submitting issues or pull requests!