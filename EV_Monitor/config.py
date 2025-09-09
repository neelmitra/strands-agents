"""
Configuration file for EV Neighborhood Monitor

This file contains configuration settings and API endpoints for the EV monitoring application.
In a production environment, you would configure real API keys and endpoints here.
"""

import os

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Optional for enhanced traffic data

# MCP Server Configuration
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 8001
MCP_SERVER_URL = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/mcp/"

# Data Source URLs (for real implementations)
EV_DATA_SOURCES = {
    "ev_sales_api": "https://api.example.com/ev-sales",  # Replace with real API
    "charging_stations_api": "https://api.plugshare.com/",  # PlugShare API
    "traffic_api": "https://maps.googleapis.com/maps/api/",  # Google Maps API
    "vehicle_registration_api": "https://api.dmv.gov/",  # DMV API (varies by state)
}

# Default Analysis Parameters
DEFAULT_SEARCH_RADIUS_MILES = 5.0
DEFAULT_EV_DENSITY_RADIUS_MILES = 2.0
DEFAULT_ESTIMATION_RADIUS_MILES = 1.0

# EV Model Categories
EV_CATEGORIES = ["sedan", "suv", "truck", "luxury", "budget", "all"]
PRICE_RANGES = ["under_40k", "40k_to_70k", "over_70k", "all"]

# Charging Network Information
CHARGING_NETWORKS = [
    "Tesla Supercharger",
    "Electrify America", 
    "ChargePoint",
    "EVgo",
    "Blink",
    "Volta",
    "Flo",
    "Shell Recharge"
]

# Regional EV Adoption Factors
REGIONAL_FACTORS = {
    "California": {"base_adoption": 0.15, "growth_rate": 0.25},
    "Washington": {"base_adoption": 0.12, "growth_rate": 0.22},
    "Oregon": {"base_adoption": 0.10, "growth_rate": 0.20},
    "New York": {"base_adoption": 0.08, "growth_rate": 0.18},
    "Texas": {"base_adoption": 0.06, "growth_rate": 0.15},
    "Florida": {"base_adoption": 0.05, "growth_rate": 0.12},
    "Colorado": {"base_adoption": 0.09, "growth_rate": 0.19},
    "Nevada": {"base_adoption": 0.08, "growth_rate": 0.17}
}

# Popular Locations for Demo (coordinates)
DEMO_LOCATIONS = {
    "San Francisco": (37.7749, -122.4194),
    "Seattle": (47.6062, -122.3321),
    "Los Angeles": (34.0522, -118.2437),
    "New York": (40.7128, -74.0060),
    "Austin": (30.2672, -97.7431),
    "Denver": (39.7392, -104.9903),
    "Portland": (45.5152, -122.6784),
    "Miami": (25.7617, -80.1918)
}

# Validation Settings
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0
MAX_SEARCH_RADIUS = 50.0  # miles
MIN_SEARCH_RADIUS = 0.1   # miles