"""
MCP + DeepSeek AI Demo

This demonstrates AI interaction with external tools (Weather and Memory)
using the Model Context Protocol approach.

Run: python mcp_demo.py
"""

import json
from openai import OpenAI
from config import Config
from mcp_tools import SimpleMCP

class SmartAI:
    """AI with MCP tool access"""
    
    def __init__(self):
        config = Config()
        self.client = OpenAI(
            api_key=config.deepseek_api_key,
            base_url=config.deepseek_base_url
        )
        self.mcp = SimpleMCP()
        self.conversation_history = []
    
    def chat(self, message: str) -> str:
        """Chat with AI that can use external tools"""
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Define available functions for the AI
        functions = [
            {
                "name": "get_weather",
                "description": "Get current weather information for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "The city name"},
                        "country": {"type": "string", "description": "The country (optional)"}
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "store_preference",
                "description": "Store a user preference",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Category like 'travel', 'food', etc."},
                        "preference": {"type": "string", "description": "The preference to store"}
                    },
                    "required": ["category", "preference"]
                }
            },
            {
                "name": "get_preferences",
                "description": "Get stored user preferences",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Specific category or all if not specified"}
                    }
                }
            }
        ]
        
        try:
            # First API call with function definitions
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.conversation_history,
                functions=functions,
                function_call="auto",
                temperature=0.7
            )
            
            message = response.choices[0].message
            
            # Check if AI wants to call a function
            if hasattr(message, 'function_call') and message.function_call:
                return self._handle_function_call(message)
            else:
                # Regular response
                content = message.content if isinstance(message, dict) else str(message)
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _handle_function_call(self, message) -> str:
        """Handle AI function call and return final response"""
        
        function_name = message.function_call.name
        function_args = json.loads(message.function_call.arguments)
        
        print(f"AI is calling: {function_name}({function_args})")
        
        # Call the MCP tool
        tool_result = self.mcp.process_tool_call(function_name, **function_args)
        
        # Add function call and result to conversation
        self.conversation_history.append({
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": function_name,
                "arguments": message.function_call.arguments
            }
        })
        
        self.conversation_history.append({
            "role": "function",
            "name": function_name,
            "content": json.dumps(tool_result)
        })
        
        # Get final response with tool results
        try:
            final_response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.conversation_history,
                temperature=0.7
            )
            
            content = final_response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": content})
            return content
            
        except Exception as e:
            return f"Error processing tool result: {str(e)}"

def demo_mcp_tools():
    """Demonstrate MCP tools independently"""
    print("\n=== MCP Tools Demo ===")
    mcp = SimpleMCP()
    
    # Test weather
    print("\nTesting Weather MCP:")
    weather = mcp.process_tool_call("get_weather", city="Tokyo")
    print(f"Tokyo weather: {weather}")
    
    # Test memory
    print("\nTesting Memory MCP:")
    mcp.process_tool_call("store_preference", category="travel", preference="museums")
    mcp.process_tool_call("store_preference", category="travel", preference="local food")
    prefs = mcp.process_tool_call("get_preferences", category="travel")
    print(f"Travel preferences: {prefs}")
    
    print("\nMCP tools working!")

def main():
    print("MCP + DeepSeek AI Demo")
    print("AI can now use weather and memory tools!")
    print("Try asking about weather or telling it your preferences")
    print("Type 'demo' to test MCP tools, 'quit' to exit")
    print("-" * 50)
    
    # Test MCP tools first
    try:
        demo_mcp_tools()
    except Exception as e:
        print(f"MCP tools test failed: {e}")
        print("You may not have internet connection for weather data")
    
    # Initialize AI
    try:
        ai = SmartAI()
        print("\nAI initialized with MCP tools!")
    except Exception as e:
        print(f"AI setup failed: {e}")
        print("Make sure you have:")
        print("1. Created .env file with DEEPSEEK_API_KEY")
        print("2. Installed requirements: pip install -r requirements.txt")
        return
    
    # Chat loop
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if user_input.lower() == 'demo':
            demo_mcp_tools()
            continue
            
        if not user_input:
            continue
            
        print("AI: ", end="")
        response = ai.chat(user_input)
        print(response)

if __name__ == "__main__":
    main() 