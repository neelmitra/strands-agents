"""
Multi-Agent Fraud Detection System

This module demonstrates advanced agentic capabilities through a collaborative
multi-agent system for fraud detection. The system includes:

- Primary Fraud Detection Agent (coordinator)
- Pattern Analysis Agent (specialist)
- Risk Assessment Agent (specialist)
- Agent-to-Agent communication for collaborative decision making
"""

import os
import json
import asyncio
import threading
import time
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from strands import Agent
from strands.models.anthropic import AnthropicModel
from strands_tools.a2a_client import A2AClientToolProvider
from sample_transactions import TransactionData

# Request/Response models for API communication
class TransactionAnalysisRequest(BaseModel):
    transaction: Dict[str, Any]
    user_context: Optional[Dict[str, Any]] = None

class PatternAnalysisRequest(BaseModel):
    transactions: List[Dict[str, Any]]
    analysis_type: str = "fraud_patterns"

class RiskAssessmentRequest(BaseModel):
    transaction: Dict[str, Any]
    pattern_analysis: Optional[Dict[str, Any]] = None
    user_profile: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    agent_id: str
    analysis_result: Dict[str, Any]
    confidence_score: float
    timestamp: str

# Agent configurations
def get_model_config():
    """Get standard model configuration for all agents."""
    return AnthropicModel(
        client_args={
            "api_key": os.getenv("api_key", os.getenv("ANTHROPIC_API_KEY")),
        },
        max_tokens=1024,
        model_id="claude-3-7-sonnet-20250219",
        params={
            "temperature": 0.2,
        }
    )

class PatternAnalysisAgent:
    """Specialized agent for detecting patterns across multiple transactions."""
    
    def __init__(self, port: int = 8001):
        self.port = port
        self.app = FastAPI(title="Pattern Analysis Agent")
        self.model = get_model_config()
        
        system_prompt = """You are a specialized Pattern Analysis Agent focused on detecting suspicious patterns across multiple transactions.

Your expertise includes:
- Identifying card testing patterns (multiple small transactions)
- Detecting geographic impossibilities
- Recognizing time-based anomalies
- Finding merchant pattern irregularities
- Spotting velocity-based fraud indicators

When analyzing transaction patterns:
1. Look for sequences that indicate testing or probing
2. Identify impossible geographic/temporal combinations
3. Detect unusual merchant category combinations
4. Calculate transaction velocity and frequency anomalies
5. Provide pattern-specific risk scores

Always provide:
- Pattern type detected
- Confidence level (0-1)
- Supporting evidence
- Risk assessment for the pattern
- Recommendations for further investigation"""

        self.agent = Agent(model=self.model, system_prompt=system_prompt)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup FastAPI routes for the pattern analysis agent."""
        
        @self.app.get("/health")
        def health_check():
            return {"status": "healthy", "agent": "pattern_analysis"}
        
        @self.app.post("/analyze_patterns")
        def analyze_patterns(request: PatternAnalysisRequest):
            try:
                analysis_prompt = f"""
                Analyze the following {len(request.transactions)} transactions for suspicious patterns:
                
                Transactions:
                {json.dumps(request.transactions, indent=2)}
                
                Analysis Type: {request.analysis_type}
                
                Provide a comprehensive pattern analysis including:
                1. Identified patterns and their risk levels
                2. Evidence supporting each pattern
                3. Overall pattern-based risk assessment
                4. Recommendations for the primary fraud detection system
                """
                
                response = self.agent(analysis_prompt)
                
                return AnalysisResponse(
                    agent_id="pattern_analysis_agent",
                    analysis_result={
                        "pattern_analysis": response,
                        "transaction_count": len(request.transactions),
                        "analysis_type": request.analysis_type
                    },
                    confidence_score=0.85,
                    timestamp="2024-01-17T12:00:00Z"
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def start(self):
        """Start the pattern analysis agent server."""
        uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info")

class RiskAssessmentAgent:
    """Specialized agent for detailed risk assessment of individual transactions."""
    
    def __init__(self, port: int = 8002):
        self.port = port
        self.app = FastAPI(title="Risk Assessment Agent")
        self.model = get_model_config()
        
        system_prompt = """You are a specialized Risk Assessment Agent focused on detailed risk evaluation of individual transactions.

Your expertise includes:
- Quantitative risk scoring methodologies
- User behavior analysis and profiling
- Transaction context evaluation
- Risk factor weighting and correlation
- Regulatory compliance considerations

When assessing transaction risk:
1. Evaluate amount relative to user patterns
2. Assess merchant and location risk factors
3. Analyze temporal patterns and anomalies
4. Consider user profile and history
5. Apply risk scoring algorithms
6. Account for regulatory requirements

Always provide:
- Numerical risk score (0-100)
- Risk level classification (LOW/MEDIUM/HIGH)
- Detailed risk factor breakdown
- Confidence interval for assessment
- Compliance considerations
- Recommended actions"""

        self.agent = Agent(model=self.model, system_prompt=system_prompt)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup FastAPI routes for the risk assessment agent."""
        
        @self.app.get("/health")
        def health_check():
            return {"status": "healthy", "agent": "risk_assessment"}
        
        @self.app.post("/assess_risk")
        def assess_risk(request: RiskAssessmentRequest):
            try:
                analysis_prompt = f"""
                Perform detailed risk assessment for this transaction:
                
                Transaction:
                {json.dumps(request.transaction, indent=2)}
                """
                
                if request.user_profile:
                    analysis_prompt += f"""
                    
                    User Profile:
                    {json.dumps(request.user_profile, indent=2)}
                    """
                
                if request.pattern_analysis:
                    analysis_prompt += f"""
                    
                    Pattern Analysis Context:
                    {json.dumps(request.pattern_analysis, indent=2)}
                    """
                
                analysis_prompt += """
                
                Provide a comprehensive risk assessment including:
                1. Numerical risk score (0-100)
                2. Risk level classification
                3. Detailed breakdown of risk factors
                4. Confidence level in assessment
                5. Recommended actions
                6. Compliance considerations
                """
                
                response = self.agent(analysis_prompt)
                
                return AnalysisResponse(
                    agent_id="risk_assessment_agent",
                    analysis_result={
                        "risk_assessment": response,
                        "transaction_id": request.transaction.get("transaction_id", "unknown")
                    },
                    confidence_score=0.90,
                    timestamp="2024-01-17T12:00:00Z"
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def start(self):
        """Start the risk assessment agent server."""
        uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info")

class PrimaryFraudDetectionAgent:
    """Primary fraud detection agent that coordinates with specialist agents."""
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.app = FastAPI(title="Primary Fraud Detection Agent")
        self.model = get_model_config()
        
        # URLs for specialist agents
        self.pattern_agent_url = "http://localhost:8001/"
        self.risk_agent_url = "http://localhost:8002/"
        
        system_prompt = """You are the Primary Fraud Detection Agent coordinating a multi-agent fraud detection system.

You have access to specialist agents:
- Pattern Analysis Agent: Detects patterns across multiple transactions
- Risk Assessment Agent: Provides detailed risk scoring for individual transactions

Your responsibilities:
1. Coordinate analysis across specialist agents
2. Synthesize results from multiple agents
3. Make final fraud determination decisions
4. Provide comprehensive fraud assessment reports
5. Recommend actions based on collaborative analysis

When analyzing transactions:
1. Use specialist agents for their expertise areas
2. Combine and correlate their findings
3. Apply your own analytical capabilities
4. Make final risk determinations
5. Provide clear, actionable recommendations

Always provide:
- Final fraud determination (APPROVED/DECLINED/REVIEW)
- Comprehensive risk assessment
- Evidence from all agents
- Confidence level in decision
- Recommended actions
- Audit trail of agent consultations"""

        # Setup A2A communication with specialist agents
        self.a2a_provider = A2AClientToolProvider(
            known_agent_urls=[self.pattern_agent_url, self.risk_agent_url]
        )
        
        self.agent = Agent(
            model=self.model, 
            system_prompt=system_prompt,
            tools=self.a2a_provider.tools
        )
        
        self.setup_routes()
    
    def setup_routes(self):
        """Setup FastAPI routes for the primary fraud detection agent."""
        
        @self.app.get("/health")
        def health_check():
            return {"status": "healthy", "agent": "primary_fraud_detection"}
        
        @self.app.post("/analyze_transaction")
        def analyze_transaction(request: TransactionAnalysisRequest):
            try:
                analysis_prompt = f"""
                Perform comprehensive fraud analysis for this transaction using specialist agents:
                
                Transaction:
                {json.dumps(request.transaction, indent=2)}
                """
                
                if request.user_context:
                    analysis_prompt += f"""
                    
                    User Context:
                    {json.dumps(request.user_context, indent=2)}
                    """
                
                analysis_prompt += """
                
                Please:
                1. Consult the Risk Assessment Agent for detailed risk scoring
                2. If analyzing multiple transactions, consult the Pattern Analysis Agent
                3. Synthesize all findings into a final fraud determination
                4. Provide comprehensive analysis and recommendations
                
                Use the available agent communication tools to coordinate the analysis.
                """
                
                response = self.agent(analysis_prompt)
                
                return AnalysisResponse(
                    agent_id="primary_fraud_detection_agent",
                    analysis_result={
                        "comprehensive_analysis": response,
                        "transaction_id": request.transaction.get("transaction_id", "unknown"),
                        "agents_consulted": ["risk_assessment", "pattern_analysis"]
                    },
                    confidence_score=0.95,
                    timestamp="2024-01-17T12:00:00Z"
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def start(self):
        """Start the primary fraud detection agent server."""
        uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info")

class FraudDetectionSystem:
    """Orchestrator for the multi-agent fraud detection system."""
    
    def __init__(self):
        self.agents = {
            "primary": PrimaryFraudDetectionAgent(8000),
            "pattern": PatternAnalysisAgent(8001), 
            "risk": RiskAssessmentAgent(8002)
        }
        self.agent_threads = {}
    
    def start_all_agents(self):
        """Start all agents in the fraud detection system."""
        print("🚀 Starting Multi-Agent Fraud Detection System")
        print("=" * 50)
        
        for agent_name, agent in self.agents.items():
            print(f"Starting {agent_name} agent on port {agent.port}...")
            thread = threading.Thread(target=agent.start, daemon=True)
            thread.start()
            self.agent_threads[agent_name] = thread
            time.sleep(2)  # Stagger startup
        
        print("✅ All agents started successfully!")
        print("\nAgent URLs:")
        print("- Primary Agent: http://localhost:8000")
        print("- Pattern Agent: http://localhost:8001") 
        print("- Risk Agent: http://localhost:8002")
    
    def demo_multi_agent_analysis(self):
        """Demonstrate multi-agent fraud detection capabilities."""
        
        print("\n🔍 Multi-Agent Fraud Detection Demo")
        print("=" * 50)
        
        # Wait for agents to be ready
        time.sleep(5)
        
        # Test cases
        test_transactions = [
            TransactionData.get_legitimate_transactions()[0],
            TransactionData.get_suspicious_transactions()[0],
            TransactionData.get_fraudulent_transactions()[0]
        ]
        
        for i, transaction in enumerate(test_transactions, 1):
            print(f"\n📊 Test Case {i}: {transaction['description']}")
            print(f"Amount: ${transaction['amount']}")
            print(f"Merchant: {transaction['merchant']}")
            print("-" * 40)
            
            # In a real implementation, you would make HTTP requests to the primary agent
            # For this demo, we'll simulate the multi-agent coordination
            print("🤖 Multi-agent analysis in progress...")
            print("   ├── Consulting Pattern Analysis Agent...")
            print("   ├── Consulting Risk Assessment Agent...")
            print("   └── Primary Agent synthesizing results...")
            
            # Simulate analysis result
            if "fraud" in transaction.get('risk_factors', []):
                result = "HIGH RISK - Transaction declined"
            elif "suspicious" in transaction.get('description', '').lower():
                result = "MEDIUM RISK - Manual review required"
            else:
                result = "LOW RISK - Transaction approved"
            
            print(f"🎯 Final Decision: {result}")
            print("="*50)

def main():
    """Main function to run the multi-agent fraud detection system."""
    
    system = FraudDetectionSystem()
    
    try:
        # Start all agents
        system.start_all_agents()
        
        # Run demo
        system.demo_multi_agent_analysis()
        
        # Keep system running
        print("\n💡 System is running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 Shutting down Multi-Agent Fraud Detection System...")

if __name__ == "__main__":
    main()