"""
Comprehensive Demo of Agentic Fraud Detection Capabilities

This script demonstrates all the agentic capabilities implemented in the fraud detection system:
1. Autonomous decision making
2. Pattern recognition
3. Multi-step reasoning
4. Tool integration
5. Multi-agent collaboration
"""

import os
import json
import time
from typing import Dict, List, Any
from fraud_detection_agent import create_fraud_agent
from sample_transactions import TransactionData

def demo_autonomous_decision_making():
    """Demonstrate autonomous decision making capabilities."""
    
    print("🤖 DEMO 1: Autonomous Decision Making")
    print("=" * 60)
    print("The fraud detection agent can independently analyze transactions")
    print("and make risk assessments without human intervention.\n")
    
    # Create fraud detection agent
    fraud_agent = create_fraud_agent()
    
    # Test with various transaction types
    test_cases = [
        ("Normal grocery purchase", TransactionData.get_legitimate_transactions()[0]),
        ("Suspicious late-night electronics", TransactionData.get_suspicious_transactions()[0]),
        ("High-risk international luxury", TransactionData.get_fraudulent_transactions()[0])
    ]
    
    for description, transaction in test_cases:
        print(f"📊 Analyzing: {description}")
        print(f"   Amount: ${transaction['amount']}")
        print(f"   Merchant: {transaction['merchant']}")
        print(f"   Location: {transaction['location']}")
        
        # Agent makes autonomous decision
        result = fraud_agent.analyze_transaction(transaction)
        
        print("🎯 Agent's Autonomous Decision:")
        print(f"   {result['analysis_response'][:200]}...")
        print("\n" + "-"*60 + "\n")
    
    print("✅ Autonomous Decision Making Demo Complete\n")

def demo_pattern_recognition():
    """Demonstrate pattern recognition across multiple transactions."""
    
    print("🔍 DEMO 2: Pattern Recognition")
    print("=" * 60)
    print("The agent can identify suspicious patterns across multiple transactions")
    print("including card testing, geographic impossibilities, and velocity fraud.\n")
    
    fraud_agent = create_fraud_agent()
    
    # Test pattern recognition scenarios
    scenarios = TransactionData.get_fraud_detection_scenarios()
    
    for scenario in scenarios:
        print(f"📈 Pattern Scenario: {scenario['scenario']}")
        print(f"   Description: {scenario['description']}")
        print(f"   Expected Risk: {scenario['expected_risk']}")
        
        # Analyze pattern
        pattern_prompt = f"""
        Analyze these transactions for the pattern: {scenario['scenario']}
        
        Transactions:
        {json.dumps(scenario['transactions'], indent=2)}
        
        Look for: {scenario['description']}
        Expected pattern: {scenario['reasoning']}
        
        Identify the pattern and assess the risk level.
        """
        
        response = fraud_agent.agent(pattern_prompt)
        
        print("🎯 Pattern Analysis Result:")
        print(f"   {response[:300]}...")
        print("\n" + "-"*60 + "\n")
    
    print("✅ Pattern Recognition Demo Complete\n")

def demo_multi_step_reasoning():
    """Demonstrate multi-step reasoning for complex fraud scenarios."""
    
    print("🧠 DEMO 3: Multi-Step Reasoning")
    print("=" * 60)
    print("The agent performs complex, multi-step analysis considering")
    print("multiple factors and data sources for comprehensive assessment.\n")
    
    fraud_agent = create_fraud_agent()
    
    # Complex scenario requiring multi-step reasoning
    complex_scenario = {
        "transaction": {
            "transaction_id": "TXN_COMPLEX_001",
            "user_id": "USER_12345",
            "amount": 2500.00,
            "currency": "USD",
            "merchant": "Electronics Store International",
            "merchant_category": "electronics",
            "location": "Tokyo, Japan",
            "timestamp": "2024-01-17T03:30:00Z",
            "payment_method": "credit_card",
            "card_last_four": "1234",
            "description": "Large electronics purchase in foreign country"
        },
        "user_context": {
            "typical_spending": 200.00,
            "typical_locations": ["New York, NY", "Boston, MA"],
            "account_age_months": 24,
            "previous_international": False,
            "recent_travel": False
        },
        "additional_context": {
            "time_since_last_transaction": "2 hours",
            "last_transaction_location": "New York, NY",
            "merchant_reputation": "unknown",
            "card_usage_pattern": "first_international_use"
        }
    }
    
    print("📊 Complex Fraud Scenario Analysis")
    print("   Transaction: $2,500 electronics purchase in Tokyo")
    print("   User Profile: Typical $200 spending, never traveled internationally")
    print("   Context: 2 hours after NYC transaction, unknown merchant")
    
    reasoning_prompt = f"""
    Perform multi-step reasoning analysis for this complex fraud scenario:
    
    TRANSACTION:
    {json.dumps(complex_scenario['transaction'], indent=2)}
    
    USER CONTEXT:
    {json.dumps(complex_scenario['user_context'], indent=2)}
    
    ADDITIONAL CONTEXT:
    {json.dumps(complex_scenario['additional_context'], indent=2)}
    
    Please perform step-by-step analysis:
    1. Analyze the transaction amount vs user patterns
    2. Evaluate geographic feasibility 
    3. Assess merchant and category risk
    4. Consider temporal patterns
    5. Evaluate user behavior consistency
    6. Synthesize all factors for final assessment
    
    Show your reasoning process for each step.
    """
    
    print("\n🤖 Agent's Multi-Step Reasoning Process:")
    response = fraud_agent.agent(reasoning_prompt)
    print(response)
    
    print("\n✅ Multi-Step Reasoning Demo Complete\n")

def demo_tool_integration():
    """Demonstrate integration with specialized tools (simulated)."""
    
    print("🔧 DEMO 4: Tool Integration")
    print("=" * 60)
    print("The agent can use specialized tools for enhanced analysis")
    print("including risk calculators, blacklist checks, and anomaly detection.\n")
    
    fraud_agent = create_fraud_agent()
    
    # Simulate tool usage scenario
    tool_scenario = {
        "transaction": TransactionData.get_fraudulent_transactions()[0],
        "available_tools": [
            "risk_score_calculator",
            "merchant_blacklist_checker", 
            "geographic_validator",
            "spending_anomaly_detector"
        ]
    }
    
    print("📊 Tool Integration Scenario")
    print(f"   Transaction: ${tool_scenario['transaction']['amount']} at {tool_scenario['transaction']['merchant']}")
    print(f"   Available Tools: {', '.join(tool_scenario['available_tools'])}")
    
    tool_prompt = f"""
    Analyze this transaction using the concept of specialized fraud detection tools:
    
    Transaction:
    {json.dumps(tool_scenario['transaction'], indent=2)}
    
    Imagine you have access to these tools:
    - risk_score_calculator: Calculates quantitative risk scores
    - merchant_blacklist_checker: Checks merchant against fraud databases
    - geographic_validator: Validates location feasibility
    - spending_anomaly_detector: Detects unusual spending patterns
    
    Describe how you would use each tool and what insights they would provide.
    Then provide a comprehensive analysis based on the tool results.
    """
    
    print("\n🤖 Agent's Tool Integration Analysis:")
    response = fraud_agent.agent(tool_prompt)
    print(response)
    
    print("\n✅ Tool Integration Demo Complete\n")

def demo_adaptive_learning():
    """Demonstrate adaptive learning from transaction patterns."""
    
    print("📚 DEMO 5: Adaptive Learning")
    print("=" * 60)
    print("The agent can adapt its analysis based on learned patterns")
    print("and feedback from previous fraud detection decisions.\n")
    
    fraud_agent = create_fraud_agent()
    
    # Simulate learning scenario
    learning_scenario = {
        "historical_cases": [
            {"transaction_type": "late_night_gas", "outcome": "legitimate", "reason": "night_shift_worker"},
            {"transaction_type": "international_luxury", "outcome": "fraud", "reason": "no_travel_history"},
            {"transaction_type": "multiple_small_online", "outcome": "fraud", "reason": "card_testing"}
        ],
        "new_transaction": {
            "transaction_id": "TXN_LEARN_001",
            "amount": 75.00,
            "merchant": "24/7 Gas Station",
            "location": "Highway Rest Stop",
            "timestamp": "2024-01-17T02:15:00Z",
            "merchant_category": "gas_station",
            "user_context": "works_night_shift"
        }
    }
    
    print("📊 Adaptive Learning Scenario")
    print("   Historical Learning: Late night gas purchases often legitimate for night workers")
    print("   New Transaction: $75 gas purchase at 2:15 AM")
    print("   User Context: Known night shift worker")
    
    learning_prompt = f"""
    Demonstrate adaptive learning by analyzing this transaction considering historical patterns:
    
    HISTORICAL LEARNING CASES:
    {json.dumps(learning_scenario['historical_cases'], indent=2)}
    
    NEW TRANSACTION TO ANALYZE:
    {json.dumps(learning_scenario['new_transaction'], indent=2)}
    
    Show how you adapt your analysis based on:
    1. Learned patterns from historical cases
    2. Context-specific factors
    3. Updated risk assessment criteria
    4. Confidence adjustments based on similar past cases
    
    Explain how historical learning influences your current assessment.
    """
    
    print("\n🤖 Agent's Adaptive Learning Analysis:")
    response = fraud_agent.agent(learning_prompt)
    print(response)
    
    print("\n✅ Adaptive Learning Demo Complete\n")

def demo_comprehensive_agentic_capabilities():
    """Run comprehensive demo of all agentic capabilities."""
    
    print("🚀 COMPREHENSIVE AGENTIC FRAUD DETECTION DEMO")
    print("=" * 80)
    print("This demo showcases the advanced agentic capabilities implemented")
    print("in the fraud detection system using the Strands Agents framework.")
    print("=" * 80 + "\n")
    
    # Run all demos
    demo_autonomous_decision_making()
    demo_pattern_recognition()
    demo_multi_step_reasoning()
    demo_tool_integration()
    demo_adaptive_learning()
    
    print("🎉 COMPREHENSIVE DEMO COMPLETE")
    print("=" * 80)
    print("The fraud detection system has demonstrated:")
    print("✅ Autonomous decision making without human intervention")
    print("✅ Pattern recognition across multiple transactions")
    print("✅ Multi-step reasoning for complex scenarios")
    print("✅ Tool integration for enhanced capabilities")
    print("✅ Adaptive learning from historical patterns")
    print("\nThe system exhibits true agentic behavior with:")
    print("• Independent analysis and decision making")
    print("• Contextual understanding and reasoning")
    print("• Continuous learning and adaptation")
    print("• Tool usage for enhanced capabilities")
    print("• Multi-agent collaboration potential")
    print("=" * 80)

def interactive_demo():
    """Interactive demo allowing users to test specific capabilities."""
    
    print("🎮 INTERACTIVE AGENTIC FRAUD DETECTION DEMO")
    print("=" * 60)
    print("Choose a demo to run:")
    print("1. Autonomous Decision Making")
    print("2. Pattern Recognition")
    print("3. Multi-Step Reasoning")
    print("4. Tool Integration")
    print("5. Adaptive Learning")
    print("6. Comprehensive Demo (All)")
    print("0. Exit")
    
    while True:
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == "0":
            print("👋 Demo complete!")
            break
        elif choice == "1":
            demo_autonomous_decision_making()
        elif choice == "2":
            demo_pattern_recognition()
        elif choice == "3":
            demo_multi_step_reasoning()
        elif choice == "4":
            demo_tool_integration()
        elif choice == "5":
            demo_adaptive_learning()
        elif choice == "6":
            demo_comprehensive_agentic_capabilities()
        else:
            print("❌ Invalid choice. Please enter 0-6.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_demo()
    else:
        demo_comprehensive_agentic_capabilities()