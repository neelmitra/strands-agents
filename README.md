# Getting Started with Strands Agents

A comprehensive hands-on course for learning AI agent development using the [Strands Agents framework](https://strandsagents.com/). This repository contains 6 progressive labs that teach you how to build, deploy, and monitor AI agents with advanced capabilities.

## 🎯 Course Overview

This course covers the complete journey of AI agent development, from basic usage to advanced topics like [agent-to-agent (A2A)](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agent-to-agent/) communication and [observability](https://strandsagents.com/latest/documentation/docs/user-guide/observability-evaluation/observability/). You'll learn to work with:

- **Strands Agents Framework** - Build intelligent AI agents
- **Model Context Protocol (MCP)** - Enable tool integration
- **Agent-to-Agent Communication** - Create multi-agent systems
- **Observability & Evaluation** - Monitor and improve agent performance

## 📚 Lab Structure

### Lab 1: Basic Agent Usage
**Files:** `basic-use.py`, `http-tool-use.py`, `system-prompt-use.py`

Learn the fundamentals of creating and using Strands agents:
- Basic agent initialization and usage
- System prompt customization
- HTTP tool integration

### Lab 2: Model Providers & Configuration
**Files:** `anthropic-model-provider.py`, `anthropic-pet-breed-agent.py`, `bedrock-default-config.py`, `bedrock-detailed-config.py`

_(Certain portions of code in this lab require a pre-existing AWS account to make use of the 'generate_image' tool.)_

Explore different model providers and configuration options:
- Anthropic model integration
- Amazon Bedrock model configuration

### Lab 3: ['use_aws'](https://github.com/strands-agents/tools/blob/main/src/strands_tools/use_aws.py) Tool Integration
**Files:** `aws-tool-use.py`

_(The code in this lab requires a pre-existing AWS account to properly utilize the 'use_aws' tool. An example Amazon DynamoDB Table is used to generate results when querying a table.)_

Learn to integrate AWS services with your Strands agents:
- AWS service tool usage
- Examples using Amazon S3 and Amazon DynamoDB

### Lab 4: Model Context Protocol (MCP) as Tools
**Files:** `mcp-and-tools.ipynb`, `mcp_calulator.py`

Deep dive into the Model Context Protocol:
- MCP server creation
- Tool definition and usage
- Calculator and Weather agents examples
- Interactive Jupyter notebook tutorial

### Lab 5: Agent-to-Agent Communication
**Files:** `a2a-communication.ipynb`, `run_a2a_system.py`, `employee_data.py`, `employee-agent.py`,  `hr-agent.py`

Build multi-agent systems with inter-agent communication:
- A2A communication patterns
- Employee/HR agent system example
- MCP server for data sharing
- REST API integration

### Lab 6: Observability and Evaluation
**Files:** `observability-with-langfuse-and-evaluation-with-ragas.ipynb`, `restaurant-data/`

Monitor and evaluate agent performance:
- Restaurant recommendation agent example
- LangFuse integration for observability
- RAGAS evaluation framework
- Performance metrics and tracing

### EV Monitor: Electric Vehicle Neighborhood Monitoring
**Files:** `EV_Monitor/` directory with complete application

**NEW!** Comprehensive agentic application for monitoring EVs in your neighborhood:
- EV sales data analysis and trend monitoring
- Google Traffic API integration for EV usage patterns
- Charging station location and availability tracking
- Neighborhood EV density calculations
- Multi-factor EV adoption analysis
- Real-time traffic pattern analysis for EV-heavy areas
- Popular EV model information and specifications

**Key Features:**
- 7 specialized MCP tools for EV monitoring
- Natural language interface for complex analytics
- Support for real Google Maps API integration
- Comprehensive demographic and infrastructure analysis
- Interactive demo with example queries
- Extensible architecture for additional data sources

## 📖 Learning Path

1. **Start with Lab 1** - Get familiar with basic agent creation
2. **Progress through Labs 2-3** - Learn model providers and AWS integration
3. **Master Lab 4** - Understand MCP and tool integration
4. **Build with Lab 5** - Create multi-agent systems
5. **Monitor with Lab 6** - Implement observability and evaluation
6. **Explore EV Monitor** - See a complete real-world application example

## 🔧 Configuration

The course uses several configuration approaches:

- **Environment variables** - API keys and sensitive data
- **Inline configuration** - Within individual lab files


## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- API keys for:
  - Anthropic Claude (recommended)
  - Amazon Bedrock (for Lab 1-3)
  - LangFuse (for Lab 6)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aws-samples/sample-getting-started-with-strands-agents-course.git
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Labs

Each lab can be run independently. Start with Lab 1 for the basics:


**Lab 1-3 - Basic Usage**
```bash
cd Lab1
python basic-use.py
```

**Lab 4 - MCP Calculator (interactive)**
```bash
cd Lab4
```
Follow the steps in `mcp-and-tools.ipynb`

**Lab 5 - A2A System**
```bash
cd Lab5
```
Follow the steps in `a2a-communication.ipynb`

**Lab 6 - Observability and Evaluation**
```bash
cd Lab6
```
Follow the steps in `observability-with-langfuse-and-evaluation-with-ragas.ipynb`

**EV Monitor - Complete Application**
```bash
cd EV_Monitor
python setup.py  # Install dependencies and configure
python ev_monitor_app.py  # Run the main application
```




## 📝 Additional Resources

- [Strands Documentation](https://strandsagents.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [LangFuse Documentation](https://langfuse.com/docs)
- [RAGAS Documentation](https://docs.ragas.io/)
- [Setting up AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)

## 🐛 Troubleshooting

Common issues and solutions:

1. **API Key Issues** - Ensure all required API keys are set in your environment
2. **Port Conflicts** - Labs use ports 8000-8002, ensure they're available
3. **Dependencies** - Run `pip install -r requirements.txt` if you encounter import errors
4. **MCP Server** - Allow time for servers to start before connecting clients

---

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.