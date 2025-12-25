from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.config import settings
from src.tools.weather_tool import WeatherTool
from src.agents.prompts import WEATHER_AGENT_SYSTEM_PROMPT
from src.logger import setup_logger

logger = setup_logger(__name__)


class WeatherAgent:
    """AI Agent for weather-related queries using OpenRouter"""
    
    def __init__(self):
        logger.info("Initializing Weather Agent with OpenRouter")
        
        # Validate API key
        if not settings.OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY is not set. Please add it to your .env file.\n"
                "Get your API key from: https://openrouter.ai/"
            )
        
        # Initialize LLM with OpenRouter
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": "https://github.com/wayandarma/learningAiAgent",
                "X-Title": "Weather AI Agent"
            }
        )
        
        logger.info(f"LLM initialized with model: {settings.LLM_MODEL}")
        
        # Initialize tools
        self.tools = [WeatherTool()]
        logger.info(f"Registered {len(self.tools)} tool(s)")
        
        # Create prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", WEATHER_AGENT_SYSTEM_PROMPT),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent using tool calling (not deprecated functions)
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=settings.DEBUG,
            max_iterations=3,
            handle_parsing_errors=True
        )
        
        logger.info("Weather Agent initialized successfully")
    
    def run(self, query: str) -> str:
        """
        Run the agent with a user query
        
        Args:
            query: User's weather-related question
            
        Returns:
            Agent's response as a string
        """
        logger.info(f"Processing query: {query}")
        
        try:
            result = self.agent_executor.invoke({"input": query})
            response = result.get("output", "I couldn't generate a response.")
            logger.info("Query processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Agent error: {e}", exc_info=True)
            return f"Sorry, I encountered an error: {str(e)}"
