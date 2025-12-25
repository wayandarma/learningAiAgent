import sys
from src.agents.weather_agent import WeatherAgent
from src.logger import setup_logger
from src.exceptions import AppError

logger = setup_logger("main")


def main():
    logger.info("Starting Weather AI Agent")
    
    try:
        # Initialize agent
        print("\n🌤️  Initializing Weather AI Agent...")
        agent = WeatherAgent()
        
        # Interactive mode
        print("\n" + "="*60)
        print("🌤️  Weather AI Agent - Powered by OpenRouter")
        print("="*60)
        print("\nAsk me about weather in US cities!")
        print("Examples:")
        print("  - What's the weather in New York?")
        print("  - Will it rain in Seattle tomorrow?")
        print("  - Get forecast for latitude 39.7456, longitude -97.0892")
        print("\nType 'quit' or 'exit' to leave\n")
        
        while True:
            try:
                query = input("You: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Stay safe in any weather!")
                    break
                
                if not query:
                    continue
                
                # Get response from agent
                print("\n🤖 Agent: ", end="", flush=True)
                response = agent.run(query)
                print(response + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Stay safe in any weather!")
                break
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                print(f"\n❌ Error: {str(e)}\n")
        
    except AppError as e:
        logger.error(f"Application error: {e}")
        print(f"\n❌ Application Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
