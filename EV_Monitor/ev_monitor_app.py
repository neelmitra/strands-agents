"""
EV Neighborhood Monitor Application

This application demonstrates how to:
1. Create an MCP server that provides comprehensive EV monitoring functionality
2. Connect a Strands agent to the MCP server
3. Use EV monitoring tools through natural language for data analysis

EV monitoring capabilities include:
- EV sales data retrieval and analysis
- Traffic pattern analysis for EV-heavy areas
- Charging station location services
- EV density calculations for neighborhoods
- EV adoption trend analysis
- Popular EV model information
"""

import threading
import time
import os
import requests
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from mcp.client.streamable_http import streamablehttp_client
from mcp.server import FastMCP
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.anthropic import AnthropicModel

# Configure the Anthropic model
model = AnthropicModel(
    client_args={
        "api_key": os.getenv("ANTHROPIC_API_KEY"),  # Get API key from environment variables
    },
    max_tokens=2048,
    model_id="claude-3-5-sonnet-20241022",
    params={
        "temperature": 0.3,
    }
)


def start_ev_monitor_server():
    """
    Initialize and start an MCP EV monitoring server.

    This function creates a FastMCP server instance that provides EV monitoring tools
    for retrieving EV data, analyzing trends, and monitoring neighborhood adoption.
    """
    # Create an MCP server with a descriptive name
    mcp = FastMCP("EV Neighborhood Monitor Server")

    @mcp.tool(description="Get EV sales data for a specific region and time period")
    def get_ev_sales_data(region: str, year: int = 2024, quarter: Optional[int] = None) -> Dict[str, Any]:
        """Get EV sales statistics for a specified region and time period.

        Args:
            region: Region name (e.g., "California", "Washington", "Texas")
            year: Year for sales data (default: 2024)
            quarter: Optional quarter (1-4) for more specific data

        Returns:
            Dictionary containing EV sales data and statistics
        """
        try:
            # Simulate EV sales data (in a real implementation, this would call actual APIs)
            # This could integrate with APIs like:
            # - EV Sales API
            # - Department of Motor Vehicles APIs
            # - Automotive industry databases
            
            base_sales = {
                "California": 150000,
                "Washington": 45000,
                "Texas": 85000,
                "New York": 65000,
                "Florida": 55000,
                "Oregon": 25000,
                "Colorado": 30000,
                "Nevada": 20000
            }
            
            region_sales = base_sales.get(region, 15000)
            
            # Add some realistic variation
            if quarter:
                quarterly_multiplier = [0.8, 1.1, 1.2, 0.9][quarter - 1]
                region_sales = int(region_sales * quarterly_multiplier / 4)
                period = f"Q{quarter} {year}"
            else:
                period = str(year)
            
            # Calculate growth rate (simulated)
            growth_rate = random.uniform(15.0, 45.0)
            
            # Popular models in the region
            popular_models = [
                {"model": "Tesla Model Y", "percentage": 28.5},
                {"model": "Tesla Model 3", "percentage": 22.1},
                {"model": "Ford Mustang Mach-E", "percentage": 8.7},
                {"model": "Chevrolet Bolt EV", "percentage": 7.3},
                {"model": "BMW iX", "percentage": 5.9},
                {"model": "Hyundai IONIQ 5", "percentage": 5.2},
                {"model": "Volkswagen ID.4", "percentage": 4.8},
                {"model": "Others", "percentage": 17.5}
            ]
            
            return {
                "region": region,
                "period": period,
                "total_ev_sales": region_sales,
                "year_over_year_growth": f"{growth_rate:.1f}%",
                "market_share": f"{random.uniform(8.0, 15.0):.1f}%",
                "popular_models": popular_models,
                "data_source": "Simulated EV Sales Database",
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to retrieve EV sales data: {str(e)}"}

    @mcp.tool(description="Get traffic data and patterns for EV-heavy areas")
    def get_traffic_data(latitude: float, longitude: float, radius_miles: float = 5.0) -> Dict[str, Any]:
        """Get traffic information and patterns for areas with high EV adoption.

        Args:
            latitude: Latitude coordinate of the center point
            longitude: Longitude coordinate of the center point
            radius_miles: Radius in miles to analyze (default: 5.0)

        Returns:
            Dictionary containing traffic data and EV-related patterns
        """
        try:
            # In a real implementation, this would integrate with:
            # - Google Maps Traffic API
            # - Google Roads API
            # - Real-time traffic data services
            
            # Simulate traffic data
            traffic_conditions = ["Light", "Moderate", "Heavy", "Very Heavy"]
            current_traffic = random.choice(traffic_conditions)
            
            # Simulate EV-specific traffic patterns
            ev_charging_traffic = {
                "peak_charging_hours": ["7:00-9:00 AM", "5:00-7:00 PM", "10:00 PM-12:00 AM"],
                "charging_station_congestion": f"{random.uniform(15, 85):.1f}%",
                "average_charging_wait_time": f"{random.randint(5, 25)} minutes"
            }
            
            # Simulate nearby points of interest
            nearby_locations = [
                {"name": "Shopping Center", "ev_friendly": True, "distance": 1.2},
                {"name": "Office Complex", "ev_friendly": True, "distance": 0.8},
                {"name": "Residential Area", "ev_friendly": False, "distance": 0.5},
                {"name": "Highway Access", "ev_friendly": True, "distance": 2.1}
            ]
            
            return {
                "location": f"{latitude}, {longitude}",
                "search_radius_miles": radius_miles,
                "current_traffic_condition": current_traffic,
                "average_speed_mph": random.randint(25, 55),
                "ev_charging_patterns": ev_charging_traffic,
                "nearby_locations": nearby_locations,
                "traffic_score": random.randint(1, 10),
                "ev_traffic_percentage": f"{random.uniform(8, 25):.1f}%",
                "data_source": "Simulated Traffic API",
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to retrieve traffic data: {str(e)}"}

    @mcp.tool(description="Find EV charging stations near a location")
    def find_charging_stations(latitude: float, longitude: float, radius_miles: float = 10.0, 
                             charging_type: str = "all") -> Dict[str, Any]:
        """Find EV charging stations within a specified radius of a location.

        Args:
            latitude: Latitude coordinate of the search center
            longitude: Longitude coordinate of the search center
            radius_miles: Search radius in miles (default: 10.0)
            charging_type: Type of charging ("fast", "level2", "level1", "all")

        Returns:
            Dictionary containing nearby charging stations and their details
        """
        try:
            # In a real implementation, this would use:
            # - PlugShare API
            # - ChargePoint API
            # - Electrify America API
            # - Tesla Supercharger API
            
            # Simulate charging stations
            charging_networks = ["Tesla Supercharger", "Electrify America", "ChargePoint", 
                               "EVgo", "Blink", "Volta", "Flo"]
            
            stations = []
            num_stations = random.randint(5, 15)
            
            for i in range(num_stations):
                # Generate random nearby coordinates
                lat_offset = random.uniform(-0.1, 0.1)
                lon_offset = random.uniform(-0.1, 0.1)
                
                station = {
                    "name": f"{random.choice(charging_networks)} Station {i+1}",
                    "network": random.choice(charging_networks),
                    "latitude": latitude + lat_offset,
                    "longitude": longitude + lon_offset,
                    "distance_miles": round(random.uniform(0.5, radius_miles), 1),
                    "charging_speed": random.choice(["Fast DC", "Level 2", "Level 1"]),
                    "power_kw": random.choice([50, 150, 250, 350]) if random.random() > 0.3 else random.choice([7, 11, 22]),
                    "available_ports": random.randint(1, 8),
                    "total_ports": random.randint(2, 12),
                    "price_per_kwh": f"${random.uniform(0.15, 0.45):.2f}",
                    "amenities": random.sample(["Restaurant", "Shopping", "Restroom", "WiFi", "Covered"], 
                                             random.randint(1, 3)),
                    "status": random.choice(["Available", "Busy", "Maintenance"])
                }
                stations.append(station)
            
            # Sort by distance
            stations.sort(key=lambda x: x["distance_miles"])
            
            return {
                "search_location": f"{latitude}, {longitude}",
                "search_radius_miles": radius_miles,
                "charging_type_filter": charging_type,
                "total_stations_found": len(stations),
                "stations": stations,
                "data_source": "Simulated Charging Station Database",
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to find charging stations: {str(e)}"}

    @mcp.tool(description="Calculate EV adoption density in a neighborhood area")
    def calculate_ev_density(latitude: float, longitude: float, radius_miles: float = 2.0) -> Dict[str, Any]:
        """Calculate the density of EV adoption in a specific neighborhood area.

        Args:
            latitude: Latitude coordinate of the neighborhood center
            longitude: Longitude coordinate of the neighborhood center
            radius_miles: Radius in miles to analyze (default: 2.0)

        Returns:
            Dictionary containing EV density statistics and analysis
        """
        try:
            # In a real implementation, this would use:
            # - Vehicle registration databases
            # - Census data
            # - Local DMV records
            # - Charging station usage data
            
            # Simulate neighborhood data
            total_households = random.randint(500, 5000)
            total_vehicles = int(total_households * random.uniform(1.2, 2.8))
            ev_count = int(total_vehicles * random.uniform(0.08, 0.35))
            
            # Calculate density metrics
            area_sq_miles = 3.14159 * (radius_miles ** 2)
            ev_density_per_sq_mile = ev_count / area_sq_miles
            ev_adoption_rate = (ev_count / total_vehicles) * 100
            
            # Demographic factors affecting EV adoption
            demographic_factors = {
                "median_income": f"${random.randint(45000, 150000):,}",
                "college_educated_percentage": f"{random.uniform(35, 85):.1f}%",
                "homeownership_rate": f"{random.uniform(45, 85):.1f}%",
                "average_commute_miles": random.randint(8, 35)
            }
            
            # EV adoption trends
            monthly_growth = random.uniform(2.5, 8.5)
            projected_ev_count_next_year = int(ev_count * (1 + monthly_growth/100) ** 12)
            
            return {
                "location": f"{latitude}, {longitude}",
                "analysis_radius_miles": radius_miles,
                "area_square_miles": round(area_sq_miles, 2),
                "total_households": total_households,
                "total_vehicles": total_vehicles,
                "current_ev_count": ev_count,
                "ev_density_per_square_mile": round(ev_density_per_sq_mile, 1),
                "ev_adoption_rate_percentage": round(ev_adoption_rate, 2),
                "demographic_factors": demographic_factors,
                "monthly_growth_rate": f"{monthly_growth:.1f}%",
                "projected_ev_count_next_year": projected_ev_count_next_year,
                "neighborhood_ev_score": random.randint(1, 10),
                "data_source": "Simulated Neighborhood Analysis",
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to calculate EV density: {str(e)}"}

    @mcp.tool(description="Analyze EV adoption trends over time")
    def analyze_ev_trends(region: str, time_period: str = "12_months") -> Dict[str, Any]:
        """Analyze EV adoption trends and patterns over a specified time period.

        Args:
            region: Region name for analysis
            time_period: Time period for analysis ("6_months", "12_months", "24_months")

        Returns:
            Dictionary containing trend analysis and projections
        """
        try:
            # Generate historical trend data
            months = {"6_months": 6, "12_months": 12, "24_months": 24}[time_period]
            
            trend_data = []
            base_sales = random.randint(1000, 10000)
            
            for i in range(months):
                month_date = datetime.now() - timedelta(days=30 * (months - i - 1))
                # Simulate growth trend with some variation
                growth_factor = 1 + (i * 0.05) + random.uniform(-0.02, 0.02)
                monthly_sales = int(base_sales * growth_factor)
                
                trend_data.append({
                    "month": month_date.strftime("%Y-%m"),
                    "ev_sales": monthly_sales,
                    "market_share": round(random.uniform(8, 20), 1),
                    "charging_stations_added": random.randint(5, 25)
                })
            
            # Calculate trend metrics
            first_month_sales = trend_data[0]["ev_sales"]
            last_month_sales = trend_data[-1]["ev_sales"]
            total_growth = ((last_month_sales - first_month_sales) / first_month_sales) * 100
            
            # Popular trends
            market_trends = [
                "Increased adoption of long-range EVs",
                "Growing interest in EV trucks and SUVs",
                "Expansion of fast-charging networks",
                "Government incentives driving adoption",
                "Corporate fleet electrification"
            ]
            
            return {
                "region": region,
                "analysis_period": time_period,
                "total_growth_percentage": round(total_growth, 1),
                "average_monthly_growth": round(total_growth / months, 2),
                "trend_data": trend_data,
                "key_market_trends": random.sample(market_trends, 3),
                "forecast_confidence": f"{random.uniform(75, 95):.1f}%",
                "data_source": "Simulated Trend Analysis",
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to analyze EV trends: {str(e)}"}

    @mcp.tool(description="Get detailed information about popular EV models")
    def get_ev_models(category: str = "all", price_range: str = "all") -> Dict[str, Any]:
        """Get information about popular EV models, specifications, and availability.

        Args:
            category: EV category ("sedan", "suv", "truck", "luxury", "budget", "all")
            price_range: Price range filter ("under_40k", "40k_to_70k", "over_70k", "all")

        Returns:
            Dictionary containing EV model information and specifications
        """
        try:
            # Comprehensive EV model database
            ev_models = [
                {
                    "model": "Tesla Model 3",
                    "manufacturer": "Tesla",
                    "category": "sedan",
                    "price_range": "40k_to_70k",
                    "starting_price": 38990,
                    "range_miles": 272,
                    "charging_speed": "250 kW",
                    "acceleration_0_60": "5.8 seconds",
                    "efficiency_mpge": 132,
                    "availability": "Available",
                    "popularity_score": 9.2
                },
                {
                    "model": "Tesla Model Y",
                    "manufacturer": "Tesla",
                    "category": "suv",
                    "price_range": "40k_to_70k",
                    "starting_price": 47740,
                    "range_miles": 330,
                    "charging_speed": "250 kW",
                    "acceleration_0_60": "6.6 seconds",
                    "efficiency_mpge": 122,
                    "availability": "Available",
                    "popularity_score": 9.5
                },
                {
                    "model": "Ford Mustang Mach-E",
                    "manufacturer": "Ford",
                    "category": "suv",
                    "price_range": "40k_to_70k",
                    "starting_price": 42995,
                    "range_miles": 312,
                    "charging_speed": "150 kW",
                    "acceleration_0_60": "6.1 seconds",
                    "efficiency_mpge": 105,
                    "availability": "Available",
                    "popularity_score": 8.1
                },
                {
                    "model": "Chevrolet Bolt EV",
                    "manufacturer": "Chevrolet",
                    "category": "sedan",
                    "price_range": "under_40k",
                    "starting_price": 31995,
                    "range_miles": 259,
                    "charging_speed": "55 kW",
                    "acceleration_0_60": "6.5 seconds",
                    "efficiency_mpge": 120,
                    "availability": "Available",
                    "popularity_score": 7.8
                },
                {
                    "model": "BMW iX",
                    "manufacturer": "BMW",
                    "category": "luxury",
                    "price_range": "over_70k",
                    "starting_price": 87100,
                    "range_miles": 324,
                    "charging_speed": "200 kW",
                    "acceleration_0_60": "4.6 seconds",
                    "efficiency_mpge": 86,
                    "availability": "Available",
                    "popularity_score": 8.7
                },
                {
                    "model": "Ford F-150 Lightning",
                    "manufacturer": "Ford",
                    "category": "truck",
                    "price_range": "40k_to_70k",
                    "starting_price": 59974,
                    "range_miles": 320,
                    "charging_speed": "150 kW",
                    "acceleration_0_60": "4.5 seconds",
                    "efficiency_mpge": 78,
                    "availability": "Limited",
                    "popularity_score": 8.9
                }
            ]
            
            # Filter by category
            if category != "all":
                ev_models = [model for model in ev_models if model["category"] == category]
            
            # Filter by price range
            if price_range != "all":
                ev_models = [model for model in ev_models if model["price_range"] == price_range]
            
            # Sort by popularity
            ev_models.sort(key=lambda x: x["popularity_score"], reverse=True)
            
            return {
                "category_filter": category,
                "price_range_filter": price_range,
                "total_models_found": len(ev_models),
                "ev_models": ev_models,
                "market_summary": {
                    "average_range": round(sum(model["range_miles"] for model in ev_models) / len(ev_models), 1) if ev_models else 0,
                    "average_price": round(sum(model["starting_price"] for model in ev_models) / len(ev_models), 0) if ev_models else 0,
                    "most_popular": ev_models[0]["model"] if ev_models else "None"
                },
                "data_source": "EV Model Database",
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to retrieve EV model information: {str(e)}"}

    @mcp.tool(description="Estimate EV count in a neighborhood based on multiple factors")
    def estimate_ev_count(latitude: float, longitude: float, radius_miles: float = 1.0) -> Dict[str, Any]:
        """Estimate the number of EVs in a neighborhood using multiple data sources and factors.

        Args:
            latitude: Latitude coordinate of the neighborhood center
            longitude: Longitude coordinate of the neighborhood center
            radius_miles: Radius in miles for the estimation area (default: 1.0)

        Returns:
            Dictionary containing EV count estimation and contributing factors
        """
        try:
            # Simulate estimation factors
            area_sq_miles = 3.14159 * (radius_miles ** 2)
            population_density = random.randint(1000, 8000)  # people per sq mile
            estimated_population = int(area_sq_miles * population_density)
            
            # Factors affecting EV adoption
            income_factor = random.uniform(0.8, 1.5)  # Higher income = more EVs
            education_factor = random.uniform(0.9, 1.3)  # Higher education = more EVs
            charging_infrastructure_factor = random.uniform(0.7, 1.4)  # More stations = more EVs
            environmental_awareness_factor = random.uniform(0.8, 1.2)
            
            # Base EV adoption rate (national average ~3-5%)
            base_adoption_rate = 0.04
            
            # Calculate adjusted adoption rate
            adjusted_rate = (base_adoption_rate * income_factor * education_factor * 
                           charging_infrastructure_factor * environmental_awareness_factor)
            
            # Estimate vehicles and EVs
            vehicles_per_household = random.uniform(1.5, 2.2)
            households = estimated_population / random.uniform(2.2, 2.8)
            total_vehicles = int(households * vehicles_per_household)
            estimated_evs = int(total_vehicles * adjusted_rate)
            
            # Confidence intervals
            confidence_low = int(estimated_evs * 0.7)
            confidence_high = int(estimated_evs * 1.3)
            
            return {
                "location": f"{latitude}, {longitude}",
                "estimation_radius_miles": radius_miles,
                "area_square_miles": round(area_sq_miles, 2),
                "estimated_population": estimated_population,
                "estimated_households": int(households),
                "estimated_total_vehicles": total_vehicles,
                "estimated_ev_count": estimated_evs,
                "confidence_interval": f"{confidence_low} - {confidence_high} EVs",
                "adoption_factors": {
                    "income_multiplier": round(income_factor, 2),
                    "education_multiplier": round(education_factor, 2),
                    "charging_infrastructure_multiplier": round(charging_infrastructure_factor, 2),
                    "environmental_awareness_multiplier": round(environmental_awareness_factor, 2)
                },
                "base_adoption_rate": f"{base_adoption_rate * 100:.1f}%",
                "adjusted_adoption_rate": f"{adjusted_rate * 100:.1f}%",
                "estimation_confidence": f"{random.uniform(70, 90):.1f}%",
                "data_source": "Multi-factor EV Estimation Model",
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to estimate EV count: {str(e)}"}

    # Run the server with Streamable HTTP transport on port 8001
    print("Starting MCP EV Monitor Server on http://localhost:8001")
    mcp.run(transport="streamable-http", port=8001)


def main():
    """
    Main function that starts the MCP server in a background thread
    and creates a Strands agent that uses the EV monitoring tools.
    """
    # Start the MCP server in a background thread
    server_thread = threading.Thread(target=start_ev_monitor_server, daemon=True)
    server_thread.start()

    # Wait for the server to start
    print("Waiting for MCP EV Monitor server to start...")
    time.sleep(3)

    # Connect to the MCP server using Streamable HTTP transport
    print("Connecting to MCP EV Monitor server...")

    def create_streamable_http_transport():
        return streamablehttp_client("http://localhost:8001/mcp/")

    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

    # Create a comprehensive system prompt for EV monitoring
    system_prompt = """
    You are an advanced EV (Electric Vehicle) neighborhood monitoring assistant with comprehensive capabilities for analyzing EV adoption, traffic patterns, and infrastructure. You have access to the following specialized tools:
    
    **EV Data Analysis Tools:**
    - get_ev_sales_data: Retrieve EV sales statistics and trends for regions
    - analyze_ev_trends: Analyze EV adoption patterns over time periods
    - get_ev_models: Get detailed information about EV models and specifications
    
    **Location & Infrastructure Tools:**
    - find_charging_stations: Locate EV charging stations with detailed information
    - get_traffic_data: Analyze traffic patterns in EV-heavy areas
    - calculate_ev_density: Calculate EV adoption density in neighborhoods
    - estimate_ev_count: Estimate EV population using multiple factors
    
    **Your Expertise:**
    1. **EV Market Analysis**: Provide insights on EV sales trends, popular models, and market growth
    2. **Neighborhood Assessment**: Analyze EV adoption rates and density in specific areas
    3. **Infrastructure Planning**: Help locate charging stations and assess charging infrastructure
    4. **Traffic Analysis**: Understand traffic patterns related to EV usage and charging behavior
    5. **Trend Forecasting**: Predict EV adoption trends and future neighborhood changes
    
    **When helping users:**
    - Use multiple tools to provide comprehensive analysis
    - Explain EV adoption factors (income, education, infrastructure, environmental awareness)
    - Provide practical recommendations for EV owners and potential buyers
    - Highlight charging infrastructure availability and accessibility
    - Discuss traffic implications of EV adoption
    - Offer insights on neighborhood EV trends and future projections
    
    **For location-based queries:**
    - Ask for coordinates (latitude, longitude) when needed
    - Suggest popular locations if users need examples
    - Provide radius options for different analysis scopes
    
    Always provide detailed, accurate, and actionable EV monitoring information to help users understand their neighborhood's EV ecosystem.
    """

    # Use the MCP client in a context manager
    with streamable_http_mcp_client:
        # Get the tools from the MCP server
        tools = streamable_http_mcp_client.list_tools_sync()

        print(f"Available MCP EV monitoring tools: {[tool.tool_name for tool in tools]}")

        # Create an agent with the MCP tools
        agent = Agent(model=model, system_prompt=system_prompt, tools=tools)

        # Interactive loop
        print("\n🚗 EV Neighborhood Monitor Agent Ready! Type 'exit' to quit.\n")
        print("Example queries:")
        print("- How many EVs are in my neighborhood around coordinates 37.7749, -122.4194?")
        print("- What are the EV sales trends in California for the last year?")
        print("- Find charging stations within 5 miles of coordinates 47.6062, -122.3321")
        print("- Analyze traffic patterns for EV areas near 40.7128, -74.0060")
        print("- What are the most popular EV models under $50k?")
        print("- Calculate EV density in downtown Seattle (47.6062, -122.3321)")
        print("- Show me EV adoption trends in Texas over 24 months")
        print()
        
        while True:
            # Get user input
            user_input = input("EV Monitor Query: ")

            # Check if the user wants to exit
            if user_input.lower() in ["exit", "quit"]:
                break

            # Process the user's request
            print("\n🔍 Analyzing EV data...\n")
            response = agent(user_input)

            # Print the agent's response
            print(f"📊 EV Analysis Report: {response}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Exiting EV Neighborhood Monitor...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure you have set the ANTHROPIC_API_KEY environment variable.")