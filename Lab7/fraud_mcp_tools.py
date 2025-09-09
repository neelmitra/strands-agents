"""
Fraud Detection MCP Tools Server

This module provides specialized MCP tools for fraud detection including:
- Risk scoring algorithms
- Pattern analysis tools
- Geographic validation
- Merchant verification
- Anomaly detection
"""

import threading
import time
import os
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from mcp.client.streamable_http import streamablehttp_client
from mcp.server import FastMCP
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.anthropic import AnthropicModel
from sample_transactions import TransactionData

# Global data stores for fraud detection
BLACKLISTED_MERCHANTS = {
    "Suspicious Online Store",
    "Fake Electronics Ltd",
    "Scam Services Inc",
    "Fraudulent Marketplace"
}

HIGH_RISK_LOCATIONS = {
    "Unknown",
    "Tor Network",
    "VPN Location"
}

MERCHANT_RISK_SCORES = {
    "grocery": 0.1,
    "restaurant": 0.2,
    "gas_station": 0.3,
    "online_retail": 0.4,
    "electronics": 0.6,
    "cash_advance": 0.9,
    "cryptocurrency": 0.8,
    "luxury_goods": 0.7,
    "online_services": 0.5
}

def start_fraud_mcp_server():
    """Initialize and start the fraud detection MCP server."""
    
    mcp = FastMCP("Fraud Detection Tools Server")
    
    @mcp.tool(description="Calculate risk score for a transaction based on multiple factors")
    def calculate_risk_score(
        amount: float,
        merchant_category: str,
        location: str,
        time_hour: int,
        user_avg_spending: float = 500.0,
        is_international: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive risk score for a transaction.
        
        Args:
            amount: Transaction amount
            merchant_category: Category of merchant
            location: Transaction location
            time_hour: Hour of transaction (0-23)
            user_avg_spending: User's average spending
            is_international: Whether transaction is international
            
        Returns:
            Dictionary with risk score and breakdown
        """
        risk_factors = {}
        total_risk = 0.0
        
        # Amount risk (0-30 points)
        amount_ratio = amount / user_avg_spending if user_avg_spending > 0 else 1
        if amount_ratio > 10:
            amount_risk = 30
        elif amount_ratio > 5:
            amount_risk = 20
        elif amount_ratio > 2:
            amount_risk = 10
        else:
            amount_risk = 0
        
        risk_factors["amount_risk"] = amount_risk
        total_risk += amount_risk
        
        # Merchant category risk (0-25 points)
        merchant_risk = MERCHANT_RISK_SCORES.get(merchant_category, 0.5) * 25
        risk_factors["merchant_risk"] = merchant_risk
        total_risk += merchant_risk
        
        # Location risk (0-20 points)
        location_risk = 20 if location in HIGH_RISK_LOCATIONS else 0
        if is_international:
            location_risk += 10
        risk_factors["location_risk"] = min(location_risk, 20)
        total_risk += risk_factors["location_risk"]
        
        # Time risk (0-15 points)
        if time_hour < 6 or time_hour > 23:
            time_risk = 15
        elif time_hour < 8 or time_hour > 22:
            time_risk = 8
        else:
            time_risk = 0
        risk_factors["time_risk"] = time_risk
        total_risk += time_risk
        
        # International transaction risk (0-10 points)
        international_risk = 10 if is_international else 0
        risk_factors["international_risk"] = international_risk
        total_risk += international_risk
        
        # Normalize to 0-100 scale
        total_risk = min(total_risk, 100)
        
        # Determine risk level
        if total_risk >= 70:
            risk_level = "HIGH"
        elif total_risk >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "risk_score": round(total_risk, 2),
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "max_possible_score": 100
        }
    
    @mcp.tool(description="Check if merchant is blacklisted or high-risk")
    def check_merchant_status(merchant_name: str, merchant_category: str) -> Dict[str, Any]:
        """
        Check merchant against blacklists and risk databases.
        
        Args:
            merchant_name: Name of the merchant
            merchant_category: Category of the merchant
            
        Returns:
            Dictionary with merchant status information
        """
        is_blacklisted = merchant_name in BLACKLISTED_MERCHANTS
        category_risk = MERCHANT_RISK_SCORES.get(merchant_category, 0.5)
        
        # Simulate merchant verification
        verification_status = "verified" if not is_blacklisted and category_risk < 0.7 else "unverified"
        
        return {
            "merchant_name": merchant_name,
            "is_blacklisted": is_blacklisted,
            "category_risk_score": category_risk,
            "verification_status": verification_status,
            "risk_level": "HIGH" if is_blacklisted or category_risk > 0.7 else "LOW"
        }
    
    @mcp.tool(description="Analyze geographic feasibility of transactions")
    def analyze_geographic_pattern(
        transactions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze geographic patterns in transactions for impossibilities.
        
        Args:
            transactions: List of transaction dictionaries with location and timestamp
            
        Returns:
            Dictionary with geographic analysis results
        """
        if len(transactions) < 2:
            return {"analysis": "Insufficient data for geographic analysis"}
        
        # Sort transactions by timestamp
        sorted_txns = sorted(transactions, key=lambda x: x.get('timestamp', ''))
        
        geographic_issues = []
        
        for i in range(1, len(sorted_txns)):
            prev_txn = sorted_txns[i-1]
            curr_txn = sorted_txns[i]
            
            prev_location = prev_txn.get('location', '')
            curr_location = curr_txn.get('location', '')
            
            # Simple geographic impossibility check
            if prev_location != curr_location:
                # Simulate time difference calculation
                time_diff_minutes = 30  # Simplified for demo
                
                # Check for impossible travel times
                if "NY" in prev_location and "CA" in curr_location and time_diff_minutes < 300:
                    geographic_issues.append({
                        "issue": "impossible_travel",
                        "from_location": prev_location,
                        "to_location": curr_location,
                        "time_difference_minutes": time_diff_minutes,
                        "minimum_travel_time_minutes": 300
                    })
        
        return {
            "geographic_issues": geographic_issues,
            "risk_level": "HIGH" if geographic_issues else "LOW",
            "analysis_summary": f"Found {len(geographic_issues)} geographic impossibilities"
        }
    
    @mcp.tool(description="Detect anomalies in spending patterns")
    def detect_spending_anomalies(
        current_amount: float,
        historical_amounts: List[float],
        merchant_category: str
    ) -> Dict[str, Any]:
        """
        Detect anomalies in spending patterns using statistical analysis.
        
        Args:
            current_amount: Current transaction amount
            historical_amounts: List of historical transaction amounts
            merchant_category: Category of current transaction
            
        Returns:
            Dictionary with anomaly detection results
        """
        if not historical_amounts:
            return {
                "is_anomaly": True,
                "reason": "No historical data available",
                "anomaly_score": 0.8
            }
        
        # Calculate statistical measures
        mean_amount = sum(historical_amounts) / len(historical_amounts)
        variance = sum((x - mean_amount) ** 2 for x in historical_amounts) / len(historical_amounts)
        std_dev = math.sqrt(variance) if variance > 0 else 0
        
        # Calculate z-score
        z_score = (current_amount - mean_amount) / std_dev if std_dev > 0 else 0
        
        # Determine if anomaly
        is_anomaly = abs(z_score) > 2.5  # More than 2.5 standard deviations
        
        # Calculate anomaly score (0-1)
        anomaly_score = min(abs(z_score) / 3.0, 1.0)
        
        return {
            "is_anomaly": is_anomaly,
            "z_score": round(z_score, 2),
            "anomaly_score": round(anomaly_score, 2),
            "mean_historical": round(mean_amount, 2),
            "std_deviation": round(std_dev, 2),
            "current_amount": current_amount,
            "analysis": f"Current amount is {abs(z_score):.1f} standard deviations from mean"
        }
    
    print("Starting Fraud Detection MCP Server on http://localhost:8000")
    mcp.run(transport="streamable-http")


def create_fraud_agent_with_tools():
    """Create a fraud detection agent with MCP tools."""
    
    model = AnthropicModel(
        client_args={
            "api_key": os.getenv("api_key", os.getenv("ANTHROPIC_API_KEY")),
        },
        max_tokens=2048,
        model_id="claude-3-7-sonnet-20250219",
        params={
            "temperature": 0.1,
        }
    )
    
    system_prompt = """You are an advanced fraud detection agent with access to specialized tools.
    
    You have access to the following fraud detection tools:
    - calculate_risk_score: Calculate comprehensive risk scores for transactions
    - check_merchant_status: Verify merchant reputation and blacklist status
    - analyze_geographic_pattern: Check for geographic impossibilities
    - detect_spending_anomalies: Identify unusual spending patterns
    
    When analyzing transactions:
    1. Use the appropriate tools to gather quantitative risk assessments
    2. Combine tool results with your analytical expertise
    3. Provide clear, actionable recommendations
    4. Explain your reasoning and tool usage
    
    Always use tools when available data supports their use, and explain how tool results inform your final assessment."""
    
    return model, system_prompt


def main():
    """Main function that starts the MCP server and creates an agent with fraud detection tools."""
    
    # Start the MCP server in a background thread
    server_thread = threading.Thread(target=start_fraud_mcp_server, daemon=True)
    server_thread.start()
    
    # Wait for the server to start
    print("Waiting for Fraud Detection MCP server to start...")
    time.sleep(3)
    
    # Connect to the MCP server
    print("Connecting to Fraud Detection MCP server...")
    
    def create_streamable_http_transport():
        return streamablehttp_client("http://localhost:8000/mcp/")
    
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
    
    # Get model and system prompt
    model, system_prompt = create_fraud_agent_with_tools()
    
    # Use the MCP client in a context manager
    with streamable_http_mcp_client:
        # Get the tools from the MCP server
        tools = streamable_http_mcp_client.list_tools_sync()
        
        print(f"Available Fraud Detection Tools: {[tool.tool_name for tool in tools]}")
        
        # Create an agent with the fraud detection tools
        agent = Agent(model=model, system_prompt=system_prompt, tools=tools)
        
        # Demo the fraud detection system
        demo_fraud_detection_with_tools(agent)


def demo_fraud_detection_with_tools(agent: Agent):
    """Demonstrate fraud detection with MCP tools."""
    
    print("\n🔍 Fraud Detection System with MCP Tools")
    print("=" * 60)
    
    # Test cases with different risk levels
    test_cases = [
        {
            "name": "Normal Transaction",
            "transaction": TransactionData.get_legitimate_transactions()[0],
            "description": "Regular grocery purchase"
        },
        {
            "name": "High-Risk Transaction", 
            "transaction": TransactionData.get_fraudulent_transactions()[0],
            "description": "Large international luxury purchase"
        },
        {
            "name": "Suspicious Pattern",
            "transaction": TransactionData.get_suspicious_transactions()[0],
            "description": "Late night electronics purchase"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print("-" * 40)
        
        transaction = test_case['transaction']
        
        # Format transaction for analysis
        analysis_prompt = f"""
        Analyze this transaction for fraud risk using your available tools:
        
        Transaction Details:
        - Amount: ${transaction['amount']}
        - Merchant: {transaction['merchant']} ({transaction['merchant_category']})
        - Location: {transaction['location']}
        - Time: {transaction['timestamp']}
        - User ID: {transaction['user_id']}
        
        Please use the appropriate fraud detection tools to:
        1. Calculate a risk score
        2. Check merchant status
        3. Detect any spending anomalies
        4. Provide a comprehensive fraud assessment
        """
        
        print("🤖 Agent Analysis:")
        response = agent(analysis_prompt)
        print(response)
        print("\n" + "="*60)


def interactive_fraud_detection_with_tools():
    """Interactive fraud detection session with MCP tools."""
    
    print("🤖 Interactive Fraud Detection with Advanced Tools")
    print("Type 'exit' to quit, 'demo' for sample analysis")
    print("=" * 60)
    
    # Start the MCP server in a background thread
    server_thread = threading.Thread(target=start_fraud_mcp_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    def create_streamable_http_transport():
        return streamablehttp_client("http://localhost:8000/mcp/")
    
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
    model, system_prompt = create_fraud_agent_with_tools()
    
    with streamable_http_mcp_client:
        tools = streamable_http_mcp_client.list_tools_sync()
        agent = Agent(model=model, system_prompt=system_prompt, tools=tools)
        
        print(f"🔧 Available Tools: {[tool.tool_name for tool in tools]}")
        
        while True:
            user_input = input("\n💬 Describe a transaction or ask about fraud detection: ")
            
            if user_input.lower() in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'demo':
                demo_fraud_detection_with_tools(agent)
                continue
            
            # Process the user's input
            print("\n🔍 Analyzing with fraud detection tools...")
            response = agent(user_input)
            print(f"\n🤖 Fraud Detection Agent: {response}")


def test_individual_tools():
    """Test individual MCP tools directly."""
    
    print("🧪 Testing Individual Fraud Detection Tools")
    print("=" * 50)
    
    # Start server
    server_thread = threading.Thread(target=start_fraud_mcp_server, daemon=True)
    server_thread.start()
    time.sleep(3)
    
    def create_streamable_http_transport():
        return streamablehttp_client("http://localhost:8000/mcp/")
    
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
    
    with streamable_http_mcp_client:
        tools = streamable_http_mcp_client.list_tools_sync()
        
        print(f"Available tools: {[tool.tool_name for tool in tools]}")
        
        # Test risk score calculation
        print("\n🔢 Testing Risk Score Calculation:")
        risk_result = streamable_http_mcp_client.call_tool_sync(
            "calculate_risk_score",
            {
                "amount": 5000.0,
                "merchant_category": "luxury_goods",
                "location": "London, UK",
                "time_hour": 3,
                "user_avg_spending": 500.0,
                "is_international": True
            }
        )
        print(json.dumps(risk_result, indent=2))
        
        # Test merchant status check
        print("\n🏪 Testing Merchant Status Check:")
        merchant_result = streamable_http_mcp_client.call_tool_sync(
            "check_merchant_status",
            {
                "merchant_name": "Suspicious Online Store",
                "merchant_category": "online_retail"
            }
        )
        print(json.dumps(merchant_result, indent=2))


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'interactive':
            interactive_fraud_detection_with_tools()
        elif sys.argv[1] == 'test':
            test_individual_tools()
        else:
            main()
    else:
        main()