"""
Weather MCP Application Demo

This script demonstrates the weather agent capabilities with predefined queries.
It shows how the agent can handle various weather-related requests using MCP tools.
"""

import threading
import time
import os
from mcp.client.streamable_http import streamablehttp_client
from mcp_weather import start_weather_server
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.anthropic import AnthropicModel

# Configure the model (you'll need to set your API key)
model = AnthropicModel(
    client_args={
        "api_key": os.getenv("api_key", "your-api-key-here"),
    },
    max_tokens=1028,
    model_id="claude-3-7-sonnet-20250219",
    params={
        "temperature": 0.3,
    }
)

def run_weather_demo():
    """Run a demonstration of the weather MCP application."""
    
    # Start the MCP server in a background thread
    print("🌤️  Starting Weather MCP Demo...")
    print("=" * 50)
    server_thread = threading.Thread(target=start_weather_server, daemon=True)
    server_thread.start()
    
    # Wait for the server to start
    print("Initializing weather server...")
    time.sleep(3)
    
    # Connect to the MCP server
    def create_streamable_http_transport():
        return streamablehttp_client("http://localhost:8000/mcp/")
    
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
    
    # System prompt for the weather agent
    system_prompt = """
    You are a comprehensive weather assistant with advanced weather data capabilities. 
    Provide clear, helpful weather information and calculations. Always use the appropriate 
    tools to get accurate data and perform calculations. Format your responses in a 
    user-friendly way with relevant safety information when applicable.
    """
    
    # Demo queries to test various capabilities
    demo_queries = [
        {
            "title": "Temperature Conversion",
            "query": "Convert 32°F to Celsius and explain what this temperature means."
        },
        {
            "title": "Heat Index Calculation", 
            "query": "Calculate the heat index for a temperature of 90°F with 70% humidity. What does this mean for outdoor activities?"
        },
        {
            "title": "Wind Chill Assessment",
            "query": "What's the wind chill for 15°F with 25 mph winds? Is it safe to be outside?"
        },
        {
            "title": "Temperature Statistics",
            "query": "I recorded these temperatures this week: 68, 72, 75, 71, 69, 73, 70. Calculate the average and tell me about the temperature variation."
        },
        {
            "title": "Current Weather - Seattle",
            "query": "What's the current weather like in Seattle? Use coordinates 47.6062, -122.3321."
        },
        {
            "title": "Weather Forecast - New York",
            "query": "Get me a 3-day weather forecast for New York City using coordinates 40.7128, -74.0060."
        },
        {
            "title": "Weather Alerts Check",
            "query": "Are there any weather alerts or warnings for Miami, Florida? Use coordinates 25.7617, -80.1918."
        }
    ]
    
    with streamable_http_mcp_client:
        # Get the tools from the MCP server
        tools = streamable_http_mcp_client.list_tools_sync()
        print(f"✅ Connected to MCP server with {len(tools)} weather tools")
        print(f"Available tools: {[tool.tool_name for tool in tools]}")
        print()
        
        # Create the weather agent
        agent = Agent(model=model, system_prompt=system_prompt, tools=tools)
        
        # Run through demo queries
        for i, demo in enumerate(demo_queries, 1):
            print(f"🔍 Demo {i}: {demo['title']}")
            print("-" * 40)
            print(f"Query: {demo['query']}")
            print()
            
            try:
                print("🤖 Agent Response:")
                response = agent(demo['query'])
                print(response)
                print()
                
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
            
            # Add a small delay between queries
            time.sleep(1)
            print("=" * 50)
            print()
        
        print("🎉 Weather MCP Demo completed!")
        print("\nTo run the interactive version, use: python3 mcp_weather.py")

if __name__ == "__main__":
    try:
        run_weather_demo()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\nMake sure to:")
        print("1. Set your API key: export api_key='your-anthropic-api-key'")
        print("2. Install requirements: pip install -r requirements.txt")