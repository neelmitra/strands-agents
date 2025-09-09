"""
EV Monitor Demo Queries

This script demonstrates various queries you can make to the EV Neighborhood Monitor.
Run this after starting the main ev_monitor_app.py to see example interactions.
"""

import time
import os
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client
from strands.models.anthropic import AnthropicModel

# Configure the model
model = AnthropicModel(
    client_args={
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
    max_tokens=2048,
    model_id="claude-3-5-sonnet-20241022",
    params={
        "temperature": 0.3,
    }
)

def run_demo_queries():
    """Run a series of demo queries to showcase EV monitoring capabilities."""
    
    print("🚗 EV Neighborhood Monitor Demo")
    print("=" * 50)
    
    # Connect to the MCP server
    def create_streamable_http_transport():
        return streamablehttp_client("http://localhost:8001/mcp/")

    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
    
    system_prompt = """
    You are an EV monitoring assistant. Provide clear, concise responses to EV-related queries.
    Focus on the most important information and present it in an easy-to-read format.
    """

    with streamable_http_mcp_client:
        tools = streamable_http_mcp_client.list_tools_sync()
        agent = Agent(model=model, system_prompt=system_prompt, tools=tools)

        # Demo queries with realistic coordinates
        demo_queries = [
            {
                "title": "EV Count Estimation - San Francisco",
                "query": "Estimate how many EVs are in the neighborhood around coordinates 37.7749, -122.4194 within a 1-mile radius",
                "description": "Estimating EV population in downtown San Francisco"
            },
            {
                "title": "Charging Stations - Seattle",
                "query": "Find EV charging stations within 5 miles of coordinates 47.6062, -122.3321",
                "description": "Locating charging infrastructure in Seattle"
            },
            {
                "title": "EV Sales Trends - California",
                "query": "What are the EV sales trends in California for 2024?",
                "description": "Analyzing state-level EV adoption"
            },
            {
                "title": "Traffic Analysis - New York",
                "query": "Analyze traffic patterns for EV areas near coordinates 40.7128, -74.0060",
                "description": "Understanding EV traffic in Manhattan"
            },
            {
                "title": "EV Density - Austin",
                "query": "Calculate EV adoption density in the area around coordinates 30.2672, -97.7431 within 2 miles",
                "description": "Measuring EV concentration in Austin, TX"
            },
            {
                "title": "Popular EV Models",
                "query": "What are the most popular EV models in the SUV category?",
                "description": "Exploring EV model preferences"
            }
        ]

        for i, demo in enumerate(demo_queries, 1):
            print(f"\n📍 Demo Query {i}: {demo['title']}")
            print(f"Description: {demo['description']}")
            print(f"Query: {demo['query']}")
            print("-" * 50)
            
            try:
                response = agent(demo['query'])
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error: {str(e)}")
            
            print("\n" + "=" * 50)
            
            # Add a small delay between queries
            time.sleep(2)

        print("\n✅ Demo completed! You can now run your own queries using ev_monitor_app.py")

if __name__ == "__main__":
    try:
        print("Connecting to EV Monitor server...")
        time.sleep(1)  # Give server time to start if needed
        run_demo_queries()
    except Exception as e:
        print(f"❌ Error running demo: {str(e)}")
        print("Make sure ev_monitor_app.py is running first!")