"""
Google Traffic Integration for EV Monitor

This module shows how to integrate real Google Maps Traffic API data
into the EV monitoring application. This is an enhanced version that
could replace the simulated traffic data in the main application.

Note: Requires a valid Google Maps API key to function.
"""

import os
import requests
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class GoogleTrafficIntegration:
    """Integration class for Google Maps Traffic API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Google Maps API key."""
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api"
        
    def get_real_traffic_data(self, latitude: float, longitude: float, 
                             radius_miles: float = 5.0) -> Dict[str, Any]:
        """
        Get real traffic data from Google Maps API.
        
        Args:
            latitude: Center latitude
            longitude: Center longitude  
            radius_miles: Search radius in miles
            
        Returns:
            Dictionary with traffic information
        """
        if not self.api_key:
            return self._get_simulated_traffic_data(latitude, longitude, radius_miles)
            
        try:
            # Convert miles to meters for Google API
            radius_meters = int(radius_miles * 1609.34)
            
            # Get nearby places (charging stations, shopping centers, etc.)
            places_url = f"{self.base_url}/place/nearbysearch/json"
            places_params = {
                "location": f"{latitude},{longitude}",
                "radius": radius_meters,
                "type": "gas_station|shopping_mall|restaurant",  # EV-relevant locations
                "key": self.api_key
            }
            
            places_response = requests.get(places_url, params=places_params)
            places_data = places_response.json() if places_response.status_code == 200 else {}
            
            # Get traffic conditions using Distance Matrix API
            # This gives us travel times with current traffic
            destinations = []
            if places_data.get("results"):
                # Use first few places as destinations to check traffic
                for place in places_data["results"][:5]:
                    place_lat = place["geometry"]["location"]["lat"]
                    place_lng = place["geometry"]["location"]["lng"]
                    destinations.append(f"{place_lat},{place_lng}")
            
            traffic_data = {}
            if destinations:
                matrix_url = f"{self.base_url}/distancematrix/json"
                matrix_params = {
                    "origins": f"{latitude},{longitude}",
                    "destinations": "|".join(destinations),
                    "departure_time": "now",
                    "traffic_model": "best_guess",
                    "key": self.api_key
                }
                
                matrix_response = requests.get(matrix_url, params=matrix_params)
                matrix_data = matrix_response.json() if matrix_response.status_code == 200 else {}
                
                if matrix_data.get("rows"):
                    elements = matrix_data["rows"][0]["elements"]
                    traffic_delays = []
                    
                    for element in elements:
                        if element["status"] == "OK":
                            duration = element.get("duration", {}).get("value", 0)
                            duration_in_traffic = element.get("duration_in_traffic", {}).get("value", 0)
                            
                            if duration_in_traffic > duration:
                                delay_ratio = duration_in_traffic / duration
                                traffic_delays.append(delay_ratio)
                    
                    avg_delay_ratio = sum(traffic_delays) / len(traffic_delays) if traffic_delays else 1.0
                    
                    # Determine traffic condition based on delay ratio
                    if avg_delay_ratio < 1.1:
                        traffic_condition = "Light"
                    elif avg_delay_ratio < 1.3:
                        traffic_condition = "Moderate"
                    elif avg_delay_ratio < 1.6:
                        traffic_condition = "Heavy"
                    else:
                        traffic_condition = "Very Heavy"
                        
                    traffic_data = {
                        "current_traffic_condition": traffic_condition,
                        "average_delay_ratio": round(avg_delay_ratio, 2),
                        "traffic_score": max(1, min(10, int(11 - avg_delay_ratio * 5)))
                    }
            
            # Process nearby places for EV-relevant information
            nearby_locations = []
            if places_data.get("results"):
                for place in places_data["results"][:10]:
                    place_info = {
                        "name": place.get("name", "Unknown"),
                        "type": place.get("types", []),
                        "rating": place.get("rating", 0),
                        "ev_friendly": self._is_ev_friendly(place),
                        "distance": self._calculate_distance(
                            latitude, longitude,
                            place["geometry"]["location"]["lat"],
                            place["geometry"]["location"]["lng"]
                        )
                    }
                    nearby_locations.append(place_info)
            
            return {
                "location": f"{latitude}, {longitude}",
                "search_radius_miles": radius_miles,
                "data_source": "Google Maps API",
                "nearby_locations": nearby_locations,
                "retrieved_at": datetime.now().isoformat(),
                **traffic_data
            }
            
        except Exception as e:
            # Fallback to simulated data if API fails
            return self._get_simulated_traffic_data(latitude, longitude, radius_miles)
    
    def find_real_charging_stations(self, latitude: float, longitude: float, 
                                   radius_miles: float = 10.0) -> Dict[str, Any]:
        """
        Find real charging stations using Google Places API.
        
        Args:
            latitude: Search center latitude
            longitude: Search center longitude
            radius_miles: Search radius in miles
            
        Returns:
            Dictionary with charging station information
        """
        if not self.api_key:
            return {"error": "Google Maps API key not configured"}
            
        try:
            radius_meters = int(radius_miles * 1609.34)
            
            # Search for EV charging stations
            places_url = f"{self.base_url}/place/nearbysearch/json"
            params = {
                "location": f"{latitude},{longitude}",
                "radius": radius_meters,
                "keyword": "electric vehicle charging station",
                "key": self.api_key
            }
            
            response = requests.get(places_url, params=params)
            data = response.json()
            
            if response.status_code != 200 or data.get("status") != "OK":
                return {"error": f"API error: {data.get('status', 'Unknown error')}"}
            
            stations = []
            for place in data.get("results", []):
                # Get detailed information for each station
                place_id = place.get("place_id")
                details = self._get_place_details(place_id) if place_id else {}
                
                station = {
                    "name": place.get("name", "Unknown Station"),
                    "latitude": place["geometry"]["location"]["lat"],
                    "longitude": place["geometry"]["location"]["lng"],
                    "distance_miles": round(self._calculate_distance(
                        latitude, longitude,
                        place["geometry"]["location"]["lat"],
                        place["geometry"]["location"]["lng"]
                    ), 1),
                    "rating": place.get("rating", 0),
                    "user_ratings_total": place.get("user_ratings_total", 0),
                    "price_level": place.get("price_level", "Unknown"),
                    "status": "Available" if place.get("business_status") == "OPERATIONAL" else "Unknown",
                    "address": details.get("formatted_address", "Address not available"),
                    "phone": details.get("formatted_phone_number", "Phone not available"),
                    "website": details.get("website", "Website not available"),
                    "opening_hours": details.get("opening_hours", {}).get("weekday_text", [])
                }
                stations.append(station)
            
            # Sort by distance
            stations.sort(key=lambda x: x["distance_miles"])
            
            return {
                "search_location": f"{latitude}, {longitude}",
                "search_radius_miles": radius_miles,
                "total_stations_found": len(stations),
                "stations": stations,
                "data_source": "Google Places API",
                "retrieved_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Failed to find charging stations: {str(e)}"}
    
    def _get_place_details(self, place_id: str) -> Dict[str, Any]:
        """Get detailed information about a place."""
        try:
            details_url = f"{self.base_url}/place/details/json"
            params = {
                "place_id": place_id,
                "fields": "formatted_address,formatted_phone_number,website,opening_hours",
                "key": self.api_key
            }
            
            response = requests.get(details_url, params=params)
            data = response.json()
            
            if response.status_code == 200 and data.get("status") == "OK":
                return data.get("result", {})
            return {}
            
        except Exception:
            return {}
    
    def _is_ev_friendly(self, place: Dict[str, Any]) -> bool:
        """Determine if a place is EV-friendly based on its type and name."""
        ev_friendly_types = ["shopping_mall", "restaurant", "lodging", "hospital"]
        ev_keywords = ["tesla", "electric", "charging", "green", "eco"]
        
        place_types = place.get("types", [])
        place_name = place.get("name", "").lower()
        
        # Check if it's an EV-friendly type
        if any(ptype in ev_friendly_types for ptype in place_types):
            return True
            
        # Check if name contains EV-related keywords
        if any(keyword in place_name for keyword in ev_keywords):
            return True
            
        return False
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in miles."""
        import math
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in miles
        r = 3956
        return r * c
    
    def _get_simulated_traffic_data(self, latitude: float, longitude: float, 
                                   radius_miles: float) -> Dict[str, Any]:
        """Fallback simulated traffic data when API is not available."""
        import random
        
        traffic_conditions = ["Light", "Moderate", "Heavy", "Very Heavy"]
        current_traffic = random.choice(traffic_conditions)
        
        return {
            "location": f"{latitude}, {longitude}",
            "search_radius_miles": radius_miles,
            "current_traffic_condition": current_traffic,
            "average_speed_mph": random.randint(25, 55),
            "traffic_score": random.randint(1, 10),
            "data_source": "Simulated (Google API not configured)",
            "retrieved_at": datetime.now().isoformat(),
            "note": "Set GOOGLE_MAPS_API_KEY environment variable for real traffic data"
        }


# Example usage
if __name__ == "__main__":
    # Test the Google Traffic Integration
    traffic_api = GoogleTrafficIntegration()
    
    # Test San Francisco coordinates
    sf_lat, sf_lon = 37.7749, -122.4194
    
    print("Testing Google Traffic Integration...")
    print("=" * 50)
    
    # Test traffic data
    traffic_data = traffic_api.get_real_traffic_data(sf_lat, sf_lon, 5.0)
    print("Traffic Data:")
    print(json.dumps(traffic_data, indent=2))
    
    print("\n" + "=" * 50)
    
    # Test charging stations
    charging_data = traffic_api.find_real_charging_stations(sf_lat, sf_lon, 10.0)
    print("Charging Stations:")
    print(json.dumps(charging_data, indent=2))