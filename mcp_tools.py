"""
Simple MCP Tools for Weather and Memory

This provides basic weather and memory functionality without requiring
separate MCP servers to keep the demo simple.
"""

import datetime
import json
import requests
from typing import Dict, Any, Optional
from pathlib import Path

class WeatherMCP:
    """Simple weather tool using Open-Meteo API (free)"""
    
    def get_weather(self, city: str, country: str = "") -> Dict[str, Any]:
        """Get current weather for a city"""
        try:
            # Geocoding to get coordinates
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_params = {"name": city, "count": 1}
            geo_response = requests.get(geo_url, params=geo_params, timeout=10)
            geo_data = geo_response.json()
            
            if not geo_data.get("results"):
                return {"error": f"City '{city}' not found"}
            
            location = geo_data["results"][0]
            lat, lon = location["latitude"], location["longitude"]
            
            # Get weather data
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
                "timezone": "auto"
            }
            weather_response = requests.get(weather_url, params=weather_params, timeout=10)
            weather_data = weather_response.json()
            
            current = weather_data.get("current_weather") or {}
            if not current:
                return {"error": "Weather data unavailable"}
            
            return {
                "city": location["name"],
                "country": location.get("country", ""),
                "temperature": f"{current['temperature']}°C",
                "wind_speed": f"{current['windspeed']} km/h",
                "wind_direction": f"{current['winddirection']}°",
                "conditions": self._get_weather_description(current["weathercode"]),
                "coordinates": f"{lat}, {lon}"
            }
            
        except Exception as e:
            return {"error": f"Weather data unavailable: {str(e)}"}
    
    def _get_weather_description(self, code: int) -> str:
        """Convert weather code to description"""
        weather_codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
            55: "Dense drizzle", 61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, "Unknown conditions")

class MemoryMCP:
    """Simple memory tool using local JSON storage"""
    
    def __init__(self):
        self.memory_file = Path("data/memory.json")
        self.memory_file.parent.mkdir(exist_ok=True)
        self._load_memory()
    
    def _load_memory(self):
        """Load memory from file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    self.memory = json.load(f)
            else:
                self.memory = {}
        except Exception:
            self.memory = {}
    
    def _save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Failed to save memory: {e}")
    
    def store_preference(self, category: str, preference: str) -> Dict[str, Any]:
        """Store a user preference"""
        if "preferences" not in self.memory:
            self.memory["preferences"] = {}
        
        if category not in self.memory["preferences"]:
            self.memory["preferences"][category] = []
        
        if preference not in self.memory["preferences"][category]:
            self.memory["preferences"][category].append(preference)
        
        self._save_memory()
        return {"status": "stored", "category": category, "preference": preference}
    
    def get_preferences(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Get user preferences"""
        preferences = self.memory.get("preferences", {})
        
        if category:
            return {category: preferences.get(category, [])}
        
        return preferences
    
    def store_conversation(self, topic: str, summary: str) -> Dict[str, Any]:
        """Store conversation summary"""
        if "conversations" not in self.memory:
            self.memory["conversations"] = []
        
        conversation = {
            "topic": topic,
            "summary": summary,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.memory["conversations"].append(conversation)
        self._save_memory()
        return {"status": "stored", "topic": topic}
    
    def get_conversations(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Get conversation history"""
        conversations = self.memory.get("conversations", [])
        
        if topic:
            filtered = [c for c in conversations if topic.lower() in c["topic"].lower()]
            return {"conversations": filtered}
        
        return {"conversations": conversations[-5:]}  # Last 5 conversations

class SimpleMCP:
    """Simple MCP manager that combines weather and memory tools"""
    
    def __init__(self):
        self.weather = WeatherMCP()
        self.memory = MemoryMCP()
    
    def process_tool_call(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Process a tool call and return results"""
        
        if tool_name == "get_weather":
            city = kwargs.get("city", "")
            country = kwargs.get("country", "")
            return self.weather.get_weather(city, country)
        
        elif tool_name == "store_preference":
            category = kwargs.get("category", "")
            preference = kwargs.get("preference", "")
            return self.memory.store_preference(category, preference)
        
        elif tool_name == "get_preferences":
            category = kwargs.get("category")
            return self.memory.get_preferences(category)
        
        elif tool_name == "store_conversation":
            topic = kwargs.get("topic", "")
            summary = kwargs.get("summary", "")
            return self.memory.store_conversation(topic, summary)
        
        elif tool_name == "get_conversations":
            topic = kwargs.get("topic")
            return self.memory.get_conversations(topic)
        
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def get_available_tools(self) -> Dict[str, str]:
        """Get list of available tools"""
        return {
            "get_weather": "Get current weather for a city",
            "store_preference": "Store a user preference",
            "get_preferences": "Get stored user preferences", 
            "store_conversation": "Store conversation summary",
            "get_conversations": "Get conversation history"
        } 