# DeepSeek + MCP Integration Demo

This demonstrates using DeepSeek API with MCP (Model Context Protocol) integration for external tools - a cost-effective AI solution with real-world capabilities.

## What is DeepSeek?

DeepSeek is a high-quality AI model that:
- Costs about 95% less than GPT-4
- Uses OpenAI-compatible API
- Provides similar reasoning capabilities
- Works as a drop-in replacement

## What is MCP?

Model Context Protocol (MCP) allows AI models to connect to external tools and data sources:
- Real-time data access (weather, databases)
- Persistent memory across conversations
- File operations and web search
- Standardized tool integration

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup environment:**
   ```bash
   copy config.env.example .env
   ```
   Edit `.env` and add your DeepSeek API key

3. **Run the MCP demo:**
   ```bash
   python mcp_demo.py
   ```

## Getting DeepSeek API Key

1. Go to [DeepSeek Platform](https://platform.deepseek.com)
2. Sign up and get your API key
3. Add it to your `.env` file:
   ```
   DEEPSEEK_API_KEY=your-api-key-here
   ```

## MCP Tools Included

### 1. Weather MCP
- **Purpose**: Real-time weather data
- **Data Source**: Open-Meteo API (free, no key required)
- **Usage**: "What's the weather in Tokyo?"

### 2. Memory MCP  
- **Purpose**: Store and recall user preferences
- **Data Source**: Local JSON file (data/memory.json)
- **Usage**: "Remember I like museums" → "What do I like?"

## Architecture

```
User → DeepSeek → Function Call → MCP Tools → External APIs/Storage → Enhanced Response
```

## Example Interactions

### Weather Tool:
```
You: "What's the weather in Paris?"
AI is calling: get_weather({'city': 'Paris'})
AI: "Currently in Paris, it's 12°C with partly cloudy skies. 
     The humidity is 68% with wind speeds of 15 km/h."
```

### Memory Tool:
```
You: "I love Italian food and jazz music"
AI is calling: store_preference({'category': 'food', 'preference': 'Italian'})
AI is calling: store_preference({'category': 'music', 'preference': 'jazz'})
AI: "I've noted your preferences for Italian food and jazz music!"

You: "What do I like?"
AI is calling: get_preferences({})
AI: "Based on what you've told me, you enjoy Italian food and jazz music."
```

### Travel Planning Example:
```
You: "Plan a trip to Tokyo, remember I like museums"
AI will:
1. Get Tokyo weather forecast
2. Store your museum preference 
3. Create weather-aware recommendations including museums
```

## Files

- `mcp_demo.py` - Main demo with MCP integration
- `mcp_tools.py` - Weather and Memory MCP implementations
- `config.py` - Configuration management
- `requirements.txt` - Dependencies
- `config.env.example` - Environment template

## Cost Comparison

| Service | Input (per 1M tokens) | Output (per 1M tokens) |
|---------|---------------------|----------------------|
| GPT-4   | $10.00             | $30.00              |
| DeepSeek | $0.14              | $0.28               |

**Savings: ~95% cost reduction**

## Demo Features

- **Function Calling**: AI decides when to use external tools
- **Real Weather Data**: Live weather from Open-Meteo API
- **Persistent Memory**: Preferences stored across sessions
- **Conversation History**: Maintains context throughout chat
- **Error Handling**: Graceful handling of API failures
- **No API Keys**: Weather service is completely free

## Use Cases

- Travel planning assistants
- Personal AI assistants  
- Data-driven applications
- Multi-step workflows
- Customer support systems

## Extending the Demo

You can easily add new MCP tools:
- Database connections
- File system access
- Web search capabilities
- Calendar integration
- Email automation

## Support

If you have issues:
1. Check your DeepSeek API key is correct
2. Ensure internet connection for weather data
3. Verify Python 3.8+ is installed
4. Check error messages for specific issues

## Architecture Benefits

- **Cost Effective**: 95% savings vs GPT-4
- **Real-time Data**: Live external information
- **Extensible**: Easy to add new MCP tools
- **Production Ready**: Handles real-world data sources
- **Simple Integration**: Uses standard OpenAI API 