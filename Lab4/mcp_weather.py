"""
MCP Weather Data Application

This example demonstrates how to:
1. Create an MCP server that provides comprehensive weather data functionality
2. Connect a Strands agent to the MCP server
3. Use weather tools through natural language for data retrieval and calculations

Weather capabilities include:
- Current weather retrieval
- Weather forecasts
- Temperature conversions
- Weather statistics calculations
- Weather alerts and warnings
"""

import threading
import time
import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from mcp.client.streamable_http import streamablehttp_client
from mcp.server import FastMCP
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.anthropic import AnthropicModel

model = AnthropicModel(
    client_args={
        "api_key": os.getenv("api_key"),  # Get API key from environment variables
    },
    max_tokens=1028,
    model_id="claude-3-7-sonnet-20250219",
    params={
        "temperature": 0.3,
    }
)


def start_weather_server():
    """
    Initialize and start an MCP weather server.

    This function creates a FastMCP server instance that provides weather tools
    for retrieving weather data, performing calculations, and conversions.
    """
    # Create an MCP server with a descriptive name
    mcp = FastMCP("Weather Data Server")

    @mcp.tool(description="Get current weather for a location using coordinates")
    def get_current_weather(latitude: float, longitude: float) -> Dict[str, Any]:
        """Get current weather conditions for specified coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Dictionary containing current weather data
        """
        try:
            # Get grid information from NWS
            points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
            points_response = requests.get(points_url)
            points_response.raise_for_status()
            points_data = points_response.json()
            
            # Get current conditions
            forecast_url = points_data['properties']['forecast']
            forecast_response = requests.get(forecast_url)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            current_period = forecast_data['properties']['periods'][0]
            
            return {
                "location": f"{latitude}, {longitude}",
                "temperature": current_period.get('temperature'),
                "temperature_unit": current_period.get('temperatureUnit'),
                "wind_speed": current_period.get('windSpeed'),
                "wind_direction": current_period.get('windDirection'),
                "short_forecast": current_period.get('shortForecast'),
                "detailed_forecast": current_period.get('detailedForecast'),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to retrieve weather data: {str(e)}"}

    @mcp.tool(description="Convert temperature between Fahrenheit and Celsius")
    def convert_temperature(temperature: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
        """Convert temperature between different units.

        Args:
            temperature: Temperature value to convert
            from_unit: Source unit ('F' for Fahrenheit, 'C' for Celsius)
            to_unit: Target unit ('F' for Fahrenheit, 'C' for Celsius)

        Returns:
            Dictionary containing converted temperature
        """
        try:
            from_unit = from_unit.upper()
            to_unit = to_unit.upper()
            
            if from_unit == to_unit:
                return {
                    "original_temperature": temperature,
                    "original_unit": from_unit,
                    "converted_temperature": temperature,
                    "converted_unit": to_unit
                }
            
            if from_unit == 'F' and to_unit == 'C':
                converted = (temperature - 32) * 5/9
            elif from_unit == 'C' and to_unit == 'F':
                converted = (temperature * 9/5) + 32
            else:
                return {"error": "Invalid units. Use 'F' for Fahrenheit or 'C' for Celsius"}
            
            return {
                "original_temperature": temperature,
                "original_unit": from_unit,
                "converted_temperature": round(converted, 2),
                "converted_unit": to_unit
            }
        except Exception as e:
            return {"error": f"Temperature conversion failed: {str(e)}"}

    @mcp.tool(description="Get weather forecast for a location")
    def get_weather_forecast(latitude: float, longitude: float, days: int = 7) -> Dict[str, Any]:
        """Get weather forecast for specified coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            days: Number of days to forecast (default: 7)

        Returns:
            Dictionary containing forecast data
        """
        try:
            # Get grid information from NWS
            points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
            points_response = requests.get(points_url)
            points_response.raise_for_status()
            points_data = points_response.json()
            
            # Get forecast
            forecast_url = points_data['properties']['forecast']
            forecast_response = requests.get(forecast_url)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            periods = forecast_data['properties']['periods'][:days*2]  # Day and night periods
            
            forecast_list = []
            for period in periods:
                forecast_list.append({
                    "name": period.get('name'),
                    "temperature": period.get('temperature'),
                    "temperature_unit": period.get('temperatureUnit'),
                    "wind_speed": period.get('windSpeed'),
                    "wind_direction": period.get('windDirection'),
                    "short_forecast": period.get('shortForecast'),
                    "detailed_forecast": period.get('detailedForecast')
                })
            
            return {
                "location": f"{latitude}, {longitude}",
                "forecast_periods": forecast_list,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to retrieve forecast: {str(e)}"}

    @mcp.tool(description="Calculate average temperature from a list of temperatures")
    def calculate_average_temperature(temperatures: List[float]) -> Dict[str, Any]:
        """Calculate the average temperature from a list of temperature values.

        Args:
            temperatures: List of temperature values

        Returns:
            Dictionary containing average temperature and statistics
        """
        try:
            if not temperatures:
                return {"error": "No temperatures provided"}
            
            avg_temp = sum(temperatures) / len(temperatures)
            min_temp = min(temperatures)
            max_temp = max(temperatures)
            
            return {
                "average_temperature": round(avg_temp, 2),
                "minimum_temperature": min_temp,
                "maximum_temperature": max_temp,
                "temperature_count": len(temperatures),
                "temperature_range": round(max_temp - min_temp, 2)
            }
        except Exception as e:
            return {"error": f"Temperature calculation failed: {str(e)}"}

    @mcp.tool(description="Calculate heat index based on temperature and humidity")
    def calculate_heat_index(temperature_f: float, humidity_percent: float) -> Dict[str, Any]:
        """Calculate heat index (apparent temperature) based on temperature and humidity.

        Args:
            temperature_f: Temperature in Fahrenheit
            humidity_percent: Relative humidity percentage (0-100)

        Returns:
            Dictionary containing heat index and comfort level
        """
        try:
            if humidity_percent < 0 or humidity_percent > 100:
                return {"error": "Humidity must be between 0 and 100 percent"}
            
            T = temperature_f
            H = humidity_percent
            
            # Simplified heat index calculation
            if T < 80:
                heat_index = T
            else:
                heat_index = (-42.379 + 2.04901523*T + 10.14333127*H - 0.22475541*T*H 
                            - 6.83783e-3*T*T - 5.481717e-2*H*H + 1.22874e-3*T*T*H 
                            + 8.5282e-4*T*H*H - 1.99e-6*T*T*H*H)
            
            # Determine comfort level
            if heat_index < 80:
                comfort = "Comfortable"
            elif heat_index < 90:
                comfort = "Caution - Fatigue possible"
            elif heat_index < 105:
                comfort = "Extreme Caution - Heat exhaustion possible"
            elif heat_index < 130:
                comfort = "Danger - Heat stroke likely"
            else:
                comfort = "Extreme Danger - Heat stroke imminent"
            
            return {
                "temperature_f": temperature_f,
                "humidity_percent": humidity_percent,
                "heat_index_f": round(heat_index, 1),
                "comfort_level": comfort
            }
        except Exception as e:
            return {"error": f"Heat index calculation failed: {str(e)}"}

    @mcp.tool(description="Calculate wind chill based on temperature and wind speed")
    def calculate_wind_chill(temperature_f: float, wind_speed_mph: float) -> Dict[str, Any]:
        """Calculate wind chill temperature based on air temperature and wind speed.

        Args:
            temperature_f: Air temperature in Fahrenheit
            wind_speed_mph: Wind speed in miles per hour

        Returns:
            Dictionary containing wind chill temperature and safety information
        """
        try:
            if wind_speed_mph < 0:
                return {"error": "Wind speed cannot be negative"}
            
            T = temperature_f
            V = wind_speed_mph
            
            # Wind chill calculation (valid for T ≤ 50°F and V ≥ 3 mph)
            if T > 50 or V < 3:
                wind_chill = T
                note = "Wind chill not applicable (temperature > 50°F or wind < 3 mph)"
            else:
                wind_chill = (35.74 + 0.6215*T - 35.75*(V**0.16) + 0.4275*T*(V**0.16))
                note = "Wind chill calculated using NWS formula"
            
            # Determine safety level
            if wind_chill > 32:
                safety = "Safe"
            elif wind_chill > 0:
                safety = "Cold - Dress warmly"
            elif wind_chill > -18:
                safety = "Very Cold - Frostbite possible in 30+ minutes"
            elif wind_chill > -39:
                safety = "Dangerous - Frostbite possible in 10-30 minutes"
            else:
                safety = "Extremely Dangerous - Frostbite possible in under 10 minutes"
            
            return {
                "temperature_f": temperature_f,
                "wind_speed_mph": wind_speed_mph,
                "wind_chill_f": round(wind_chill, 1),
                "safety_level": safety,
                "note": note
            }
        except Exception as e:
            return {"error": f"Wind chill calculation failed: {str(e)}"}

    @mcp.tool(description="Get weather alerts for a location")
    def get_weather_alerts(latitude: float, longitude: float) -> Dict[str, Any]:
        """Get active weather alerts for specified coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Dictionary containing active weather alerts
        """
        try:
            # Get alerts from NWS
            alerts_url = f"https://api.weather.gov/alerts/active?point={latitude},{longitude}"
            alerts_response = requests.get(alerts_url)
            alerts_response.raise_for_status()
            alerts_data = alerts_response.json()
            
            alerts_list = []
            for alert in alerts_data.get('features', []):
                properties = alert.get('properties', {})
                alerts_list.append({
                    "event": properties.get('event'),
                    "severity": properties.get('severity'),
                    "urgency": properties.get('urgency'),
                    "headline": properties.get('headline'),
                    "description": properties.get('description'),
                    "effective": properties.get('effective'),
                    "expires": properties.get('expires')
                })
            
            return {
                "location": f"{latitude}, {longitude}",
                "alert_count": len(alerts_list),
                "alerts": alerts_list,
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to retrieve weather alerts: {str(e)}"}

    # Run the server with Streamable HTTP transport on the default port (8000)
    print("Starting MCP Weather Server on http://localhost:8000")
    mcp.run(transport="streamable-http")


def main():
    """
    Main function that starts the MCP server in a background thread
    and creates a Strands agent that uses the MCP weather tools.
    """
    # Start the MCP server in a background thread
    server_thread = threading.Thread(target=start_weather_server, daemon=True)
    server_thread.start()

    # Wait for the server to start
    print("Waiting for MCP weather server to start...")
    time.sleep(3)

    # Connect to the MCP server using Streamable HTTP transport
    print("Connecting to MCP weather server...")

    def create_streamable_http_transport():
        return streamablehttp_client("http://localhost:8000/mcp/")

    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    # Create a system prompt that explains the weather capabilities
    system_prompt = """
    You are a comprehensive weather assistant with advanced weather data capabilities. You have access to the following weather tools:
    
    - get_current_weather: Get current weather conditions for any location using coordinates
    - get_weather_forecast: Get detailed weather forecasts for up to 7 days
    - convert_temperature: Convert temperatures between Fahrenheit and Celsius
    - calculate_average_temperature: Calculate statistics from temperature data
    - calculate_heat_index: Calculate apparent temperature based on temperature and humidity
    - calculate_wind_chill: Calculate wind chill temperature for cold conditions
    - get_weather_alerts: Get active weather alerts and warnings for a location
    
    When helping users with weather information:
    1. Use the appropriate tools to retrieve real-time weather data
    2. Perform calculations when requested (averages, conversions, comfort indices)
    3. Provide safety information when relevant (heat index, wind chill warnings)
    4. Check for weather alerts when appropriate
    5. Explain weather conditions in clear, understandable terms
    6. Offer practical advice based on weather conditions
    
    For location queries, you may need to ask users for coordinates (latitude, longitude) 
    or help them find coordinates for their desired location.
    
    Always provide comprehensive, accurate, and helpful weather information.
    """

    # Use the MCP client in a context manager
    with streamable_http_mcp_client:
        # Get the tools from the MCP server
        tools = streamable_http_mcp_client.list_tools_sync()

        print(f"Available MCP weather tools: {[tool.tool_name for tool in tools]}")

        # Create an agent with the MCP tools
        agent = Agent(model=model, system_prompt=system_prompt, tools=tools)

        # Interactive loop
        print("\nWeather Data Agent Ready! Type 'exit' to quit.\n")
        print("Example queries:")
        print("- What's the weather like at coordinates 47.6062, -122.3321? (Seattle)")
        print("- Convert 75°F to Celsius")
        print("- Calculate the heat index for 85°F and 60% humidity")
        print("- Get a 5-day forecast for 40.7128, -74.0060 (New York)")
        print("- Are there any weather alerts for 25.7617, -80.1918? (Miami)")
        print()
        
        while True:
            # Get user input
            user_input = input("Weather Query: ")

            # Check if the user wants to exit
            if user_input.lower() in ["exit", "quit"]:
                break

            # Process the user's request
            print("\nAnalyzing weather data...\n")
            response = agent(user_input)

            # Print the agent's response
            print(f"Weather Report: {response}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting weather application...")