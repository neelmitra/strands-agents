"""
Fraud Detection Agent with Agentic Capabilities

This module demonstrates how to create an intelligent fraud detection agent using
Strands Agents framework. The agent exhibits agentic capabilities including:
- Autonomous decision making
- Pattern recognition
- Multi-step reasoning
- Risk assessment and scoring
"""

import os
import json
from typing import Dict, List, Any, Optional
from strands import Agent
from strands.models.anthropic import AnthropicModel
from sample_transactions import TransactionData

class FraudDetectionAgent:
    """
    An intelligent fraud detection agent with advanced agentic capabilities.
    
    This agent can autonomously analyze transactions, detect patterns,
    assess risk levels, and make decisions about potential fraud.
    """
    
    def __init__(self, model_config: Optional[Dict] = None):
        """Initialize the fraud detection agent with specialized configuration."""
        
        # Default model configuration
        default_config = {
            "client_args": {
                "api_key": os.getenv("api_key", os.getenv("ANTHROPIC_API_KEY")),
            },
            "max_tokens": 2048,
            "model_id": "claude-3-7-sonnet-20250219",
            "params": {
                "temperature": 0.1,  # Low temperature for consistent fraud detection
            }
        }
        
        # Merge with provided config
        if model_config:
            default_config.update(model_config)
            
        self.model = AnthropicModel(**default_config)
        
        # Specialized system prompt for fraud detection
        self.system_prompt = self._create_fraud_detection_system_prompt()
        
        # Create the agent with fraud detection expertise
        self.agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt
        )
        
        # Load user profiles for context
        self.user_profiles = TransactionData.get_user_profiles()
    
    def _create_fraud_detection_system_prompt(self) -> str:
        """Creates a comprehensive system prompt for fraud detection expertise."""
        return """You are an expert fraud detection agent with advanced analytical capabilities. 
Your primary responsibility is to analyze financial transactions and assess fraud risk with high accuracy.

CORE EXPERTISE:
- Financial fraud patterns and indicators
- Risk assessment and scoring methodologies  
- Behavioral analysis and anomaly detection
- Geographic and temporal pattern recognition
- Payment method and merchant category analysis

ANALYTICAL FRAMEWORK:
When analyzing transactions, systematically evaluate these risk factors:

1. AMOUNT ANALYSIS:
   - Compare to user's typical spending patterns
   - Identify unusually high or low amounts for the merchant category
   - Flag round numbers that might indicate testing

2. TEMPORAL PATTERNS:
   - Unusual transaction times (very late night, early morning)
   - Rapid succession of transactions
   - Transactions during user's typical inactive hours

3. GEOGRAPHIC ANALYSIS:
   - Location consistency with user's typical patterns
   - Geographic impossibility (too far, too fast)
   - High-risk locations or countries

4. MERCHANT AND CATEGORY ANALYSIS:
   - Merchant reputation and risk level
   - Category consistency with user behavior
   - High-risk categories (cash advances, cryptocurrency, etc.)

5. PAYMENT METHOD ANALYSIS:
   - Consistency with user's preferred methods
   - Card testing patterns
   - Unusual payment method for merchant type

6. BEHAVIORAL PATTERNS:
   - Deviation from established spending habits
   - Account age and transaction history
   - Previous fraud reports or suspicious activity

DECISION MAKING PROCESS:
1. Gather all available transaction and user context
2. Systematically analyze each risk factor
3. Identify patterns and correlations
4. Calculate overall risk score (LOW/MEDIUM/HIGH)
5. Provide clear reasoning for the assessment
6. Recommend specific actions

RISK SCORING:
- LOW RISK (0-30): Normal transaction, consistent with user patterns
- MEDIUM RISK (31-70): Some suspicious indicators, requires monitoring
- HIGH RISK (71-100): Strong fraud indicators, immediate action required

OUTPUT FORMAT:
Always provide structured analysis including:
- Risk Score (0-100)
- Risk Level (LOW/MEDIUM/HIGH)  
- Key Risk Factors identified
- Detailed reasoning
- Recommended actions
- Confidence level in assessment

IMPORTANT GUIDELINES:
- Be thorough but decisive in your analysis
- Consider multiple data points before making conclusions
- Explain your reasoning clearly for audit purposes
- Balance fraud prevention with customer experience
- Flag edge cases that need human review
- Continuously learn from patterns across transactions

You have the ability to analyze individual transactions or patterns across multiple transactions.
Always provide actionable insights and clear recommendations."""

    def analyze_transaction(self, transaction: Dict[str, Any], 
                          user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze a single transaction for fraud risk.
        
        Args:
            transaction: Transaction data dictionary
            user_context: Optional user profile information
            
        Returns:
            Dictionary containing fraud analysis results
        """
        
        # Get user context if not provided
        if not user_context and transaction.get('user_id'):
            user_context = self.user_profiles.get(transaction['user_id'], {})
        
        # Format transaction for analysis
        analysis_prompt = self._format_transaction_analysis_prompt(transaction, user_context)
        
        # Get agent analysis
        response = self.agent(analysis_prompt)
        
        # Parse and structure the response
        return self._parse_fraud_analysis_response(response, transaction['transaction_id'])
    
    def analyze_transaction_batch(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze multiple transactions for patterns and individual risk.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            List of analysis results for each transaction
        """
        results = []
        
        # First, analyze for cross-transaction patterns
        pattern_analysis = self._analyze_transaction_patterns(transactions)
        
        # Then analyze each transaction individually with pattern context
        for transaction in transactions:
            user_context = self.user_profiles.get(transaction.get('user_id'), {})
            
            # Include pattern analysis in the context
            enhanced_context = {
                **user_context,
                'pattern_analysis': pattern_analysis
            }
            
            result = self.analyze_transaction(transaction, enhanced_context)
            results.append(result)
        
        return results
    
    def _analyze_transaction_patterns(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns across multiple transactions."""
        
        pattern_prompt = f"""
        Analyze the following batch of {len(transactions)} transactions for suspicious patterns:
        
        {json.dumps(transactions, indent=2)}
        
        Look for patterns such as:
        - Card testing (multiple small amounts)
        - Geographic impossibilities
        - Rapid succession of transactions
        - Unusual merchant combinations
        - Time-based patterns
        
        Provide a summary of any suspicious patterns detected.
        """
        
        response = self.agent(pattern_prompt)
        
        return {
            'pattern_analysis': response,
            'transaction_count': len(transactions),
            'analysis_timestamp': '2024-01-17T12:00:00Z'
        }
    
    def _format_transaction_analysis_prompt(self, transaction: Dict[str, Any], 
                                          user_context: Optional[Dict[str, Any]] = None) -> str:
        """Format transaction data into analysis prompt."""
        
        prompt = f"""
        FRAUD DETECTION ANALYSIS REQUEST
        
        TRANSACTION DETAILS:
        {json.dumps(transaction, indent=2)}
        """
        
        if user_context:
            prompt += f"""
        
        USER CONTEXT:
        {json.dumps(user_context, indent=2)}
        """
        
        prompt += """
        
        Please provide a comprehensive fraud risk analysis for this transaction.
        Include your risk score, reasoning, and recommended actions.
        """
        
        return prompt
    
    def _parse_fraud_analysis_response(self, response: str, transaction_id: str) -> Dict[str, Any]:
        """Parse the agent's response into structured format."""
        
        # This is a simplified parser - in production, you might use more sophisticated parsing
        return {
            'transaction_id': transaction_id,
            'analysis_response': response,
            'timestamp': '2024-01-17T12:00:00Z',
            'agent_version': '1.0'
        }


def create_fraud_agent(model_config: Optional[Dict] = None) -> FraudDetectionAgent:
    """Factory function to create a fraud detection agent."""
    return FraudDetectionAgent(model_config)


def demo_fraud_detection():
    """Demonstrate the fraud detection agent capabilities."""
    
    print("🔍 Fraud Detection Agent Demo")
    print("=" * 50)
    
    # Create the fraud detection agent
    fraud_agent = create_fraud_agent()
    
    # Test with different transaction types
    test_cases = [
        ("Legitimate Transaction", TransactionData.get_legitimate_transactions()[0]),
        ("Suspicious Transaction", TransactionData.get_suspicious_transactions()[0]),
        ("Fraudulent Transaction", TransactionData.get_fraudulent_transactions()[0])
    ]
    
    for case_name, transaction in test_cases:
        print(f"\n📊 Analyzing: {case_name}")
        print("-" * 30)
        
        # Analyze the transaction
        result = fraud_agent.analyze_transaction(transaction)
        
        print(f"Transaction ID: {transaction['transaction_id']}")
        print(f"Amount: ${transaction['amount']}")
        print(f"Merchant: {transaction['merchant']}")
        print(f"\nAnalysis Result:")
        print(result['analysis_response'])
        print("\n" + "="*50)


def interactive_fraud_detection():
    """Interactive fraud detection session."""
    
    print("🤖 Interactive Fraud Detection Agent")
    print("Type 'exit' to quit, 'demo' for sample analysis, or describe a transaction")
    print("=" * 60)
    
    fraud_agent = create_fraud_agent()
    
    while True:
        user_input = input("\n💬 Describe a transaction or ask about fraud detection: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break
        elif user_input.lower() == 'demo':
            demo_fraud_detection()
            continue
        
        # Process the user's input
        print("\n🔍 Analyzing...")
        response = fraud_agent.agent(user_input)
        print(f"\n🤖 Fraud Detection Agent: {response}")


if __name__ == "__main__":
    # Check if we should run interactive mode or demo
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_fraud_detection()
    else:
        demo_fraud_detection()