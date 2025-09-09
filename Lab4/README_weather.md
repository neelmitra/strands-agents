# Weather Data MCP Application

This is a comprehensive agentic application for calculating and retrieving weather data using the Model Context Protocol (MCP). The application demonstrates how to create a sophisticated weather assistant that can perform real-time weather data retrieval, calculations, and analysis.

## Features

### Weather Data Retrieval
- **Current Weather**: Get real-time weather conditions for any location using coordinates
- **Weather Forecasts**: Retrieve detailed weather forecasts for up to 7 days
- **Weather Alerts**: Check for active weather alerts and warnings

### Weather Calculations
- **Temperature Conversion**: Convert between Fahrenheit and Celsius
- **Heat Index**: Calculate apparent temperature based on temperature and humidity
- **Wind Chill**: Calculate wind chill temperature for cold conditions
- **Temperature Statistics**: Calculate averages, minimums, maximums, and ranges from temperature data

### Safety Information
- Comfort level assessments based on heat index
- Safety warnings for wind chill conditions
- Weather alert notifications

## Architecture

The application follows the MCP (Model Context Protocol) pattern with:

1. **MCP Server**: Hosts weather-related tools and calculations
2. **MCP Client**: Integrated with Strands Agent Framework
3. **Weather Tools**: Specific functionalities for weather data operations
4. **Agent Interface**: Natural language interaction with weather capabilities

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Anthropic API key as an environment variable:
```bash
export api_key="your-anthropic-api-key"
```

## Usage

### Running the Application

Execute the weather MCP application:
```bash
python3 mcp_weather.py
```

The application will:
1. Start the MCP weather server on `http://localhost:8000`
2. Connect the Strands agent to the MCP server
3. Provide an interactive interface for weather queries

### Example Queries

The weather agent can handle various types of natural language queries:

#### Current Weather
```
What's the weather like at coordinates 47.6062, -122.3321?
```
(Seattle coordinates)

#### Temperature Conversion
```
Convert 75°F to Celsius
```

#### Weather Calculations
```
Calculate the heat index for 85°F and 60% humidity
What's the wind chill for 20°F with 15 mph winds?
```

#### Weather Forecasts
```
Get a 5-day forecast for 40.7128, -74.0060
```
(New York coordinates)

#### Weather Alerts
```
Are there any weather alerts for 25.7617, -80.1918?
```
(Miami coordinates)

#### Temperature Statistics
```
Calculate the average temperature from these values: 72, 75, 68, 80, 77
```

## Available MCP Tools

### 1. get_current_weather
- **Purpose**: Retrieve current weather conditions
- **Parameters**: latitude, longitude
- **Returns**: Temperature, wind conditions, forecast summary

### 2. get_weather_forecast
- **Purpose**: Get weather forecast data
- **Parameters**: latitude, longitude, days (optional, default: 7)
- **Returns**: Detailed forecast periods with temperature and conditions

### 3. convert_temperature
- **Purpose**: Convert temperature between units
- **Parameters**: temperature, from_unit, to_unit
- **Returns**: Converted temperature with original and target units

### 4. calculate_average_temperature
- **Purpose**: Calculate temperature statistics
- **Parameters**: temperatures (list of values)
- **Returns**: Average, minimum, maximum, count, and range

### 5. calculate_heat_index
- **Purpose**: Calculate apparent temperature
- **Parameters**: temperature_f, humidity_percent
- **Returns**: Heat index and comfort level assessment

### 6. calculate_wind_chill
- **Purpose**: Calculate wind chill temperature
- **Parameters**: temperature_f, wind_speed_mph
- **Returns**: Wind chill temperature and safety information

### 7. get_weather_alerts
- **Purpose**: Retrieve active weather alerts
- **Parameters**: latitude, longitude
- **Returns**: List of active alerts with severity and details

## Data Sources

The application uses the **National Weather Service (NWS) API** for weather data:
- Current conditions and forecasts
- Weather alerts and warnings
- No API key required for NWS data

## Technical Details

### MCP Server Configuration
- **Transport**: Streamable HTTP
- **Port**: 8000
- **Endpoint**: `http://localhost:8000/mcp/`

### Model Configuration
- **Provider**: Anthropic Claude
- **Model**: claude-3-7-sonnet-20250219
- **Temperature**: 0.3 (for consistent weather reporting)
- **Max Tokens**: 1028

### Error Handling
- Comprehensive error handling for API failures
- Input validation for all calculations
- Graceful degradation when services are unavailable

## Coordinate Reference

For testing, here are some major city coordinates:

| City | Latitude | Longitude |
|------|----------|-----------|
| Seattle, WA | 47.6062 | -122.3321 |
| New York, NY | 40.7128 | -74.0060 |
| Miami, FL | 25.7617 | -80.1918 |
| Chicago, IL | 41.8781 | -87.6298 |
| Los Angeles, CA | 34.0522 | -118.2437 |
| Denver, CO | 39.7392 | -104.9903 |

## Extending the Application

The MCP architecture makes it easy to add new weather-related tools:

1. Add new `@mcp.tool` decorated functions to the server
2. Implement the desired weather calculation or data retrieval
3. Update the system prompt to include the new capabilities
4. The agent will automatically have access to the new tools

## Troubleshooting

### Common Issues

1. **Server Connection Failed**
   - Ensure the MCP server has time to start (wait 3+ seconds)
   - Check that port 8000 is available

2. **API Key Error**
   - Verify the `api_key` environment variable is set
   - Ensure the API key is valid and has sufficient credits

3. **Weather Data Unavailable**
   - NWS API only covers US locations
   - Check that coordinates are valid and within the US

4. **Import Errors**
   - Install all requirements: `pip install -r requirements.txt`
   - Ensure you have the latest versions of strands-agents and mcp

## License

This application is part of the Strands Agent Framework examples and follows the same licensing terms.