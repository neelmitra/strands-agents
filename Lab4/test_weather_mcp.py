"""
Test script for the Weather MCP Application

This script demonstrates the weather MCP tools without requiring user interaction.
It tests various weather calculation functions and API calls.
"""

import threading
import time
import os
from mcp_weather import start_weather_server
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient

def test_weather_tools():
    """Test the weather MCP tools programmatically."""
    
    # Start the MCP server in a background thread
    print("Starting MCP Weather Server for testing...")
    server_thread = threading.Thread(target=start_weather_server, daemon=True)
    server_thread.start()
    
    # Wait for the server to start
    time.sleep(3)
    
    # Connect to the MCP server
    def create_streamable_http_transport():
        return streamablehttp_client("http://localhost:8000/mcp/")
    
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
    
    print("Testing Weather MCP Tools...\n")
    
    with streamable_http_mcp_client:
        # Get available tools
        tools = streamable_http_mcp_client.list_tools_sync()
        print(f"Available tools: {[tool.tool_name for tool in tools]}\n")
        
        # Test temperature conversion
        print("=== Testing Temperature Conversion ===")
        try:
            result = streamable_http_mcp_client.call_tool_sync(
                "convert_temperature",
                {"temperature": 75.0, "from_unit": "F", "to_unit": "C"}
            )
            print(f"75°F to Celsius: {result}")
        except Exception as e:
            print(f"Temperature conversion test failed: {e}")
        
        print()
        
        # Test heat index calculation
        print("=== Testing Heat Index Calculation ===")
        try:
            result = streamable_http_mcp_client.call_tool_sync(
                "calculate_heat_index",
                {"temperature_f": 85.0, "humidity_percent": 60.0}
            )
            print(f"Heat index for 85°F and 60% humidity: {result}")
        except Exception as e:
            print(f"Heat index test failed: {e}")
        
        print()
        
        # Test wind chill calculation
        print("=== Testing Wind Chill Calculation ===")
        try:
            result = streamable_http_mcp_client.call_tool_sync(
                "calculate_wind_chill",
                {"temperature_f": 20.0, "wind_speed_mph": 15.0}
            )
            print(f"Wind chill for 20°F and 15 mph wind: {result}")
        except Exception as e:
            print(f"Wind chill test failed: {e}")
        
        print()
        
        # Test temperature statistics
        print("=== Testing Temperature Statistics ===")
        try:
            result = streamable_http_mcp_client.call_tool_sync(
                "calculate_average_temperature",
                {"temperatures": [72.0, 75.0, 68.0, 80.0, 77.0]}
            )
            print(f"Temperature statistics for [72, 75, 68, 80, 77]: {result}")
        except Exception as e:
            print(f"Temperature statistics test failed: {e}")
        
        print()
        
        # Test current weather (Seattle coordinates)
        print("=== Testing Current Weather (Seattle) ===")
        try:
            result = streamable_http_mcp_client.call_tool_sync(
                "get_current_weather",
                {"latitude": 47.6062, "longitude": -122.3321}
            )
            print(f"Current weather in Seattle: {result}")
        except Exception as e:
            print(f"Current weather test failed: {e}")
        
        print()
        
        # Test weather forecast (New York coordinates)
        print("=== Testing Weather Forecast (New York) ===")
        try:
            result = streamable_http_mcp_client.call_tool_sync(
                "get_weather_forecast",
                {"latitude": 40.7128, "longitude": -74.0060, "days": 3}
            )
            print(f"3-day forecast for New York: {result}")
        except Exception as e:
            print(f"Weather forecast test failed: {e}")
        
        print()
        
        # Test weather alerts (Miami coordinates)
        print("=== Testing Weather Alerts (Miami) ===")
        try:
            result = streamable_http_mcp_client.call_tool_sync(
                "get_weather_alerts",
                {"latitude": 25.7617, "longitude": -80.1918}
            )
            print(f"Weather alerts for Miami: {result}")
        except Exception as e:
            print(f"Weather alerts test failed: {e}")
        
        print("\n=== All Tests Completed ===")

if __name__ == "__main__":
    try:
        test_weather_tools()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test failed with error: {e}")