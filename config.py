"""
Configuration module for AutoGen + MCP + DeepSeek demo.
Loads environment variables and MCP server configurations.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Simple configuration class"""
    
    def __init__(self):
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.deepseek_base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
        
        if not self.deepseek_api_key:
            print("Warning: DEEPSEEK_API_KEY not found in environment") 