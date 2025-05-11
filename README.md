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
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)

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

For the topic "Climate Change Mitigation Strategies," the agent produces a well-structured summary like this:

### Climate Change Mitigation Strategies

Various approaches are being implemented globally to address climate change:

**Renewable Energy Transition**
- Shifting from fossil fuels to solar, wind, and hydroelectric power
- Implementing grid modernization to support renewable integration
- Examples include Denmark's wind energy program and Morocco's Noor Solar Complex

**Carbon Capture and Sequestration**
- Technologies that capture CO₂ emissions from industrial processes
- Methods for storing carbon in geological formations or utilizing it in products
- Projects like Norway's Sleipner facility and Canada's Quest CCS system

**Sustainable Transportation**
- Electric vehicle adoption and charging infrastructure development
- Public transit expansion and efficiency improvements
- Policies promoting cycling, walking, and reduced car dependency

**Energy Efficiency Measures**
- Building retrofits and improved insulation standards
- Smart grid technologies and demand response systems
- Energy-efficient appliance standards and LED lighting adoption

**Policy and Economic Instruments**
- Carbon pricing through taxes or cap-and-trade systems
- Green financing initiatives and climate bonds
- International agreements like the Paris Climate Accord

*References:*
1. [IPCC Special Report on Climate Change Mitigation](https://example.com/ipcc-mitigation)
2. [Renewable Energy Solutions for Climate Change](https://example.com/renewable-solutions)
3. [Carbon Capture Technologies: Current Status and Future Prospects](https://example.com/carbon-capture)
4. [Sustainable Transportation Systems and Climate Change](https://example.com/sustainable-transport)
5. [Economic Policies for Climate Change Mitigation](https://example.com/climate-economics)

## Setup and Usage

### Prerequisites
- Python 3.8+
- Together API key
- Web search API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-research-agent.git
cd llm-research-agent
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your API keys:
   ```
   TOGETHER_API_KEY=your_together_api_key
   YOU_API_KEY=your_you_api_key
   ```

### Configuration
Set up your API keys as environment variables:
```python
from google.colab import userdata
client = Together(api_key=userdata.get('TOGETHER_API_KEY'))
```

### Running the Agent

#### Basic Usage
```python
from src.agent.research_agent import ResearchAgent
agent = ResearchAgent()
topic = "Your Research Topic"
result = research_agent(topic)
print(result)
```

#### Saving Results to File
```python
import json

# Execute research
result = agent.research("Climate Change Mitigation Strategies")

# Save to markdown file
with open("research_results.md", "w") as f:
    f.write(result)

# Save cache for later analysis
with open("research_cache.json", "w") as f:
    json.dump(agent.cache, f, indent=2)
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
├── config/               # Configuration files
│   └── config.yaml       # Main configuration
├── examples/             # Example usage scripts
├── notebooks/            # Jupyter notebooks for development and demonstration
├── src/                  # Source code
│   ├── agent/            # Research agent implementation
│   │   ├── research_agent.py  # Main agent class
│   │   └── tools.py      # Research tools implementation
│   └── utils/            # Utility functions
│       └── helpers.py    # Helper functions including config loading
├── tests/                # Test files
├── .env                  # Environment variables (not tracked by git)
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
├── requirements.txt      # Project dependencies
└── LICENSE               # License information
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

## Performance Considerations

- **API Costs**: Using LLMs via API calls incurs costs. Monitor your usage.
- **Rate Limits**: Together AI and search APIs have rate limits. Implement retry logic.
- **Memory Usage**: Processing large research topics may require significant memory.
- **Execution Time**: A complete research cycle typically takes 2-5 minutes depending on the topic complexity.

## Troubleshooting

### API Key Issues
- Ensure your API keys are correctly set in the `.env` file
- Verify that you have sufficient credits/quota on your Together AI account
- Check that your API key has the necessary permissions

### Search Results Problems
- If search results are empty, try using more general queries
- Ensure your YOU_API_KEY is valid and has search permissions
- Check your internet connection

### Model Errors
- If you encounter model errors, try reducing the max_tokens parameter
- Some models may have rate limits - implement exponential backoff
- Check the Together AI status page for service disruptions

---

Feel free to contribute to this project by submitting issues or pull requests!