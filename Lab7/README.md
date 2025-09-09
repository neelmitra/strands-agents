# Lab7 - Fraud Detection with Agentic Capabilities

This lab demonstrates how to build an intelligent fraud detection system using Strands Agents with advanced agentic capabilities including:

- Autonomous transaction analysis and risk assessment
- Pattern recognition across multiple transactions
- Multi-step reasoning for complex fraud scenarios
- MCP tools for specialized fraud detection functions
- Multi-agent architecture for collaborative fraud detection

## Files

- `fraud_detection_agent.py` - Main fraud detection agent implementation
- `fraud_mcp_tools.py` - MCP server with fraud detection tools
- `multi_agent_fraud_system.py` - Advanced multi-agent fraud detection system
- `sample_transactions.py` - Sample transaction data for testing
- `requirements.txt` - Additional dependencies for fraud detection
- `README.md` - This file

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the basic fraud detection agent:
   ```bash
   python fraud_detection_agent.py
   ```

3. Run the advanced MCP-enabled system:
   ```bash
   python fraud_mcp_tools.py
   ```

4. Run the multi-agent system:
   ```bash
   python multi_agent_fraud_system.py
   ```

5. Run comprehensive agentic capabilities demo:
   ```bash
   python demo_agentic_fraud_detection.py
   
   # Or interactive demo
   python demo_agentic_fraud_detection.py interactive
   ```

## Features

### Agentic Capabilities

1. **Autonomous Decision Making**: The fraud detection agent can independently analyze transactions and make risk assessments without human intervention.

2. **Pattern Recognition**: The system identifies suspicious patterns across multiple transactions, including:
   - Unusual spending patterns
   - Geographic anomalies
   - Time-based irregularities
   - Merchant category inconsistencies

3. **Multi-Step Reasoning**: The agent performs complex analysis involving:
   - Historical transaction analysis
   - Risk factor correlation
   - Contextual decision making
   - Evidence-based conclusions

4. **Adaptive Learning**: The system adjusts its detection criteria based on:
   - Transaction history
   - User behavior patterns
   - Risk threshold configurations

5. **Tool Integration**: Enhanced capabilities through MCP tools:
   - Risk scoring algorithms
   - Merchant verification
   - Geographic validation
   - Anomaly detection

6. **Multi-Agent Collaboration**: Specialized agents working together:
   - Primary coordination agent
   - Pattern analysis specialist
   - Risk assessment specialist
   - Agent-to-agent communication

### Technical Architecture

- **Primary Agent**: Main fraud detection agent with specialized system prompt
- **MCP Tools**: Custom tools for risk scoring, pattern analysis, and data processing
- **Multi-Agent System**: Collaborative agents for specialized fraud detection tasks
- **Data Integration**: Support for various transaction data formats and sources

## Usage Examples

### Basic Fraud Detection
```python
from fraud_detection_agent import create_fraud_agent

agent = create_fraud_agent()
result = agent("Analyze this transaction: $5000 purchase at electronics store in foreign country")
```

### Advanced Pattern Analysis
```python
from fraud_mcp_tools import start_fraud_detection_system

# Starts MCP server and creates agent with fraud detection tools
start_fraud_detection_system()
```

### Multi-Agent Collaboration
```python
from multi_agent_fraud_system import FraudDetectionSystem

system = FraudDetectionSystem()
system.start_all_agents()
result = system.analyze_transaction_batch(transactions)
```

### Comprehensive Demo
```python
from demo_agentic_fraud_detection import demo_comprehensive_agentic_capabilities

# Demonstrates all agentic capabilities
demo_comprehensive_agentic_capabilities()
```

## Agentic Capabilities Demonstrated

### 1. Autonomous Decision Making
- Independent transaction analysis
- Risk assessment without human intervention
- Automated fraud/legitimate classification
- Confidence scoring and recommendations

### 2. Pattern Recognition
- Card testing detection (multiple small transactions)
- Geographic impossibility identification
- Velocity fraud pattern recognition
- Merchant category anomaly detection
- Time-based pattern analysis

### 3. Multi-Step Reasoning
- Complex scenario analysis
- Multiple factor consideration
- Evidence correlation and synthesis
- Step-by-step logical progression
- Contextual decision making

### 4. Tool Integration
- MCP tool utilization for enhanced analysis
- Risk scoring algorithm integration
- External data source consultation
- Specialized function execution
- Tool result synthesis

### 5. Adaptive Learning
- Historical pattern learning
- Context-aware adjustments
- Feedback incorporation
- Dynamic threshold adaptation
- Continuous improvement

### 6. Multi-Agent Collaboration
- Specialized agent coordination
- Agent-to-agent communication
- Collaborative decision making
- Expertise distribution
- Consensus building

## System Components

### Core Files
- `fraud_detection_agent.py` - Main fraud detection agent with agentic capabilities
- `fraud_mcp_tools.py` - MCP server with specialized fraud detection tools
- `multi_agent_fraud_system.py` - Multi-agent collaborative fraud detection
- `sample_transactions.py` - Comprehensive test data and scenarios
- `demo_agentic_fraud_detection.py` - Comprehensive demonstration of all capabilities

### Key Features
- **Strands Agents Integration**: Built on the Strands Agents framework
- **MCP Tool Support**: Custom tools for enhanced fraud detection
- **A2A Communication**: Agent-to-agent collaboration capabilities
- **Comprehensive Testing**: Extensive sample data and test scenarios
- **Interactive Demos**: Multiple ways to explore and test the system

## Advanced Scenarios

The system handles complex fraud detection scenarios including:

1. **Card Testing Attacks**: Detection of multiple small transactions used to validate stolen cards
2. **Geographic Impossibilities**: Identification of transactions in locations too far apart in short time
3. **Spending Pattern Anomalies**: Detection of purchases inconsistent with user history
4. **Merchant Risk Assessment**: Evaluation of merchant reputation and category risk
5. **Temporal Pattern Analysis**: Identification of unusual transaction timing
6. **Multi-Factor Risk Scoring**: Comprehensive risk assessment using multiple data points

## Getting Started

1. **Basic Usage**: Start with `fraud_detection_agent.py` to understand core capabilities
2. **Enhanced Tools**: Explore `fraud_mcp_tools.py` for tool-enhanced analysis
3. **Multi-Agent**: Try `multi_agent_fraud_system.py` for collaborative detection
4. **Comprehensive Demo**: Run `demo_agentic_fraud_detection.py` to see all capabilities
5. **Interactive Exploration**: Use interactive modes to test custom scenarios

This fraud detection system demonstrates the full potential of agentic AI in financial security applications, showcasing autonomous decision making, pattern recognition, multi-step reasoning, and collaborative intelligence.