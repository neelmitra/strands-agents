# EV Neighborhood Monitor

An advanced agentic application for monitoring Electric Vehicles (EVs) in your neighborhood using the Strands Agents framework. This application provides comprehensive EV analytics, traffic analysis, and infrastructure monitoring capabilities.

## 🚗 Features

### Core Monitoring Capabilities
- **EV Sales Data Analysis**: Track EV sales trends and statistics across regions
- **Traffic Pattern Analysis**: Integrate with Google traffic data to understand EV usage patterns
- **Charging Station Locator**: Find and analyze nearby EV charging infrastructure
- **Neighborhood EV Density**: Calculate EV adoption rates and density in specific areas
- **Trend Analysis**: Analyze EV adoption trends over time with forecasting
- **Model Information**: Get detailed information about popular EV models and specifications
- **EV Count Estimation**: Estimate EV population using multiple demographic and infrastructure factors

### Advanced Analytics
- **Multi-factor Analysis**: Consider income, education, infrastructure, and environmental factors
- **Real-time Data Integration**: Support for real Google Maps API integration
- **Comprehensive Reporting**: Detailed analysis with confidence intervals and projections
- **Interactive Querying**: Natural language interface for complex EV analytics

## 📊 Data Sources

1. **EV Sales Data**: Utilizes simulated EV sales databases (extensible to real APIs)
2. **Google Traffic Information**: Integrates with Google Maps APIs for traffic data
3. **Charging Station Data**: Accesses charging station location databases
4. **Demographic Data**: Analyzes factors affecting EV adoption
5. **Vehicle Registration Patterns**: Simulated local vehicle registration analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Anthropic API key (required)
- Google Maps API key (optional, for enhanced traffic data)

### Installation

1. **Navigate to the EV Monitor directory:**
   ```bash
   cd EV_Monitor
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Set your API key:**
   ```bash
   export ANTHROPIC_API_KEY='your_anthropic_api_key_here'
   ```

4. **Optional - Set Google Maps API key for enhanced traffic data:**
   ```bash
   export GOOGLE_MAPS_API_KEY='your_google_maps_api_key_here'
   ```

### Running the Application

**Start the main EV monitoring application:**
```bash
python ev_monitor_app.py
```

**Or run the demo with example queries:**
```bash
python demo_queries.py
```

## 🛠️ Available Tools

The application provides the following MCP tools:

| Tool | Description |
|------|-------------|
| `get_ev_sales_data` | Retrieve EV sales statistics for regions and time periods |
| `get_traffic_data` | Analyze traffic patterns in EV-heavy areas |
| `find_charging_stations` | Locate EV charging stations with detailed information |
| `calculate_ev_density` | Calculate EV adoption density in neighborhoods |
| `analyze_ev_trends` | Analyze EV adoption trends over time |
| `get_ev_models` | Get information about EV models and specifications |
| `estimate_ev_count` | Estimate EV population using multiple factors |

## 💬 Example Queries

### Neighborhood Analysis
```
"How many EVs are in my neighborhood around coordinates 37.7749, -122.4194 within a 1-mile radius?"
```

### Infrastructure Planning
```
"Find charging stations within 5 miles of coordinates 47.6062, -122.3321 and analyze their availability"
```

### Market Analysis
```
"What are the EV sales trends in California for the last year?"
```

### Traffic Analysis
```
"Analyze traffic patterns for EV areas near coordinates 40.7128, -74.0060"
```

### Model Research
```
"What are the most popular EV models in the SUV category under $70k?"
```

### Density Calculation
```
"Calculate EV adoption density in downtown Seattle (47.6062, -122.3321) within 2 miles"
```

## 🏗️ Architecture

The application follows the Strands Agents framework architecture:

```
┌─────────────────────┐
│   User Interface    │
│  (Natural Language) │
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│   Strands Agent     │
│  (Claude 3.5 Sonnet)│
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│    MCP Client       │
│  (Tool Orchestrator)│
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│    MCP Server       │
│   (EV Tools)        │
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│   Data Sources      │
│ (APIs & Databases)  │
└─────────────────────┘
```

## 🔧 Configuration

### Environment Variables
- `ANTHROPIC_API_KEY`: Required for Strands Agents
- `GOOGLE_MAPS_API_KEY`: Optional for enhanced traffic data

### Configuration Files
- `config.py`: Main configuration settings
- `requirements.txt`: Python dependencies
- `.env.template`: Environment variable template

## 🌐 Real Data Integration

The application is designed to easily integrate with real data sources:

### Supported APIs (when configured)
- **Google Maps API**: Real traffic data and charging station locations
- **PlugShare API**: Comprehensive charging station database
- **EV Sales APIs**: Real-time EV sales and registration data
- **Census APIs**: Demographic data for better EV adoption modeling

### Example Integration
```python
# In google_traffic_integration.py
traffic_api = GoogleTrafficIntegration(api_key="your_key")
real_data = traffic_api.get_real_traffic_data(lat, lon, radius)
```

## 📈 Analytics Capabilities

### EV Adoption Factors
- Median household income
- Education levels
- Homeownership rates
- Charging infrastructure density
- Environmental awareness
- Commute patterns

### Trend Analysis
- Historical sales data
- Growth rate calculations
- Market share analysis
- Seasonal patterns
- Regional comparisons

### Forecasting
- Population-based EV estimates
- Infrastructure growth projections
- Adoption rate predictions
- Confidence intervals

## 🧪 Testing

Run the demo to test all functionality:
```bash
python demo_queries.py
```

This will execute example queries for:
- EV count estimation
- Charging station location
- Sales trend analysis
- Traffic pattern analysis
- Density calculations
- Model information

## 🤝 Contributing

To extend the application:

1. **Add new MCP tools** in `ev_monitor_app.py`
2. **Integrate real APIs** using the patterns in `google_traffic_integration.py`
3. **Update configuration** in `config.py`
4. **Add new demo queries** in `demo_queries.py`

## 📝 License

This project follows the same license as the parent repository (MIT-0).

## 🆘 Troubleshooting

### Common Issues

1. **API Key Issues**
   - Ensure `ANTHROPIC_API_KEY` is set correctly
   - Check API key permissions and quotas

2. **Port Conflicts**
   - The application uses port 8001 by default
   - Ensure the port is available or modify in `config.py`

3. **Dependencies**
   - Run `python setup.py` to install all requirements
   - Use a virtual environment for isolation

4. **MCP Server Connection**
   - Allow time for the server to start (3-5 seconds)
   - Check console output for server status

### Getting Help

- Check the console output for detailed error messages
- Verify all environment variables are set correctly
- Ensure all dependencies are installed
- Review the demo queries for proper usage patterns

---

**Ready to monitor EVs in your neighborhood? Start with `python ev_monitor_app.py`!** 🚗⚡