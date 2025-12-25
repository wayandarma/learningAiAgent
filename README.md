# 🌤️ Weather AI Agent

A sophisticated AI-powered weather assistant that provides intelligent weather information for US cities using the National Weather Service API and OpenRouter's LLM capabilities.

## 📋 Project Description

The Weather AI Agent is a conversational AI application that combines the power of LangChain, OpenRouter's language models, and the National Weather Service API to deliver accurate, natural-language weather forecasts. The agent can understand various weather-related queries and provide detailed, contextual responses.

### Key Features

- 🤖 **AI-Powered Conversations**: Natural language understanding using OpenRouter's GPT-4 Turbo
- � **Accurate Weather Data**: Real-time weather information from the National Weather Service API
- � **Flexible Location Input**: Support for city names, coordinates, and various location formats
- 🔄 **Robust Error Handling**: Comprehensive error management with retry logic
- 📝 **Detailed Logging**: Complete logging system for debugging and monitoring
- ✅ **Well-Tested**: Comprehensive test suite with pytest
- 🏗️ **Production-Ready**: Industry-standard project structure and best practices

### Technology Stack

- **Python 3.8+**: Core programming language
- **LangChain**: Framework for building LLM applications
- **OpenRouter**: LLM API gateway for accessing GPT-4 Turbo
- **HTTPX**: Modern async HTTP client
- **Pydantic**: Data validation and settings management
- **Tenacity**: Retry logic for API calls
- **Pytest**: Testing framework

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- An OpenRouter API key ([Get one here](https://openrouter.ai/))

### Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd /path/to/wheateragent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   
   On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```
   
   On Windows:
   ```bash
   .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your configuration:
   ```env
   # API Configuration
   API_BASE_URL=https://api.weather.gov
   API_TIMEOUT=30
   LOG_LEVEL=INFO
   
   # OpenRouter Configuration
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   LLM_MODEL=openai/gpt-4-turbo
   LLM_TEMPERATURE=0.0
   LLM_MAX_TOKENS=1000
   ```

## 🎯 How to Run

### Running the Weather Agent

1. **Ensure your virtual environment is activated**:
   ```bash
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate  # Windows
   ```

2. **Run the main application**:
   ```bash
   python -m src.main
   ```

3. **Interact with the agent**:
   
   Once started, you can ask weather-related questions:
   ```
   You: What's the weather in New York?
   🤖 Agent: [Detailed weather information for New York]
   
   You: Will it rain in Seattle tomorrow?
   🤖 Agent: [Forecast information for Seattle]
   
   You: Get forecast for latitude 39.7456, longitude -97.0892
   🤖 Agent: [Weather data for the specified coordinates]
   ```

4. **Exit the application**:
   Type `quit`, `exit`, or `q` to close the agent, or press `Ctrl+C`.

### Running Tests

Run the complete test suite:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests with coverage report:
```bash
pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_weather_tool.py
```

## 📁 Project Structure

```
wheateragent/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── client.py            # HTTP client for API calls
│   ├── config.py            # Configuration management
│   ├── exceptions.py        # Custom exception classes
│   ├── logger.py            # Logging configuration
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── weather_agent.py # Main AI agent implementation
│   │   └── prompts.py       # System prompts for the agent
│   └── tools/
│       ├── __init__.py
│       └── weather_tool.py  # LangChain tool for weather API
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   └── test_weather_tool.py
├── .env                     # Environment variables (not in git)
├── .gitignore
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Configuration

The application uses environment variables for configuration. All settings are defined in `src/config.py` and loaded from the `.env` file.

### Available Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_BASE_URL` | National Weather Service API base URL | `https://api.weather.gov` | Yes |
| `API_TIMEOUT` | API request timeout in seconds | `30` | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` | No |
| `OPENROUTER_API_KEY` | Your OpenRouter API key | - | Yes |
| `OPENROUTER_BASE_URL` | OpenRouter API endpoint | `https://openrouter.ai/api/v1` | No |
| `LLM_MODEL` | Language model to use | `openai/gpt-4-turbo` | No |
| `LLM_TEMPERATURE` | Model temperature (0.0-1.0) | `0.0` | No |
| `LLM_MAX_TOKENS` | Maximum response tokens | `1000` | No |

## 💡 Usage Examples

### Example Queries

The agent understands various types of weather queries:

1. **City-based queries**:
   - "What's the weather in San Francisco?"
   - "Tell me about the weather in Miami"
   - "How's the weather in Chicago today?"

2. **Forecast queries**:
   - "Will it rain in Boston tomorrow?"
   - "What's the forecast for Los Angeles this week?"
   - "Is it going to snow in Denver?"

3. **Coordinate-based queries**:
   - "Get weather for latitude 40.7128, longitude -74.0060"
   - "What's the weather at 37.7749, -122.4194?"

4. **Detailed queries**:
   - "Should I bring an umbrella in Portland today?"
   - "What should I wear in New York tomorrow?"
   - "Is it a good day for a picnic in Austin?"

## 🛠️ Development

### Adding New Features

1. **New Tools**: Add new LangChain tools in `src/tools/`
2. **Agent Modifications**: Update `src/agents/weather_agent.py`
3. **Prompts**: Modify system prompts in `src/agents/prompts.py`
4. **Configuration**: Add new settings in `src/config.py`

### Code Quality

The project follows Python best practices:
- Type hints for better code clarity
- Comprehensive error handling
- Detailed logging
- Unit tests for critical components
- Modular, maintainable code structure

## 🐛 Troubleshooting

### Common Issues

1. **"OPENROUTER_API_KEY not found"**
   - Ensure your `.env` file exists and contains the `OPENROUTER_API_KEY`
   - Verify the API key is valid

2. **"Connection timeout"**
   - Check your internet connection
   - Increase `API_TIMEOUT` in `.env`

3. **"Location not found"**
   - Ensure you're querying US locations (National Weather Service limitation)
   - Try using coordinates instead of city names

4. **Import errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

## 📝 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📧 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Built with ❤️ using LangChain and OpenRouter**
