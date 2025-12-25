import sys
import argparse
import warnings
import threading
import itertools
import time
from src.agents.weather_agent import WeatherAgent
from src.logger import setup_logger
from src.exceptions import AppError
from src.config import settings

# Suppress urllib3 warnings only if not in debug mode
def suppress_warnings():
    if not settings.DEBUG:
        warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
        warnings.filterwarnings("ignore", message=".*ssl.*")

class Spinner:
    """A simple spinner for console feedback during long operations"""
    def __init__(self, message="Thinking..."):
        self.message = message
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()

    def _animate(self):
        while self.running:
            sys.stdout.write(f'\r{next(self.spinner)} {self.message}')
            sys.stdout.flush()
            time.sleep(0.1)

def parse_args():
    parser = argparse.ArgumentParser(description="Weather AI Agent")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Update global settings based on args
    if args.debug:
        settings.DEBUG = True
        print("🔧 Debug mode enabled")

def main():
    parse_args()
    suppress_warnings()
    
    # Setup logger after configuring settings
    logger = setup_logger("main")
    logger.info("Starting Weather AI Agent")
    
    try:
        # Initialize agent
        if not settings.DEBUG:
            print("\n🌤️  Initializing Weather AI Agent...")
            spinner = Spinner("Connecting to weather services...")
            spinner.start()
            try:
                agent = WeatherAgent()
            finally:
                spinner.stop()
        else:
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
                query = input("\033[1;36mYou:\033[0m ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Stay safe in any weather!")
                    break
                
                if not query:
                    continue
                
                # Get response from agent
                if not settings.DEBUG:
                    spinner = Spinner("Checking weather data...")
                    spinner.start()
                    try:
                        response = agent.run(query)
                    finally:
                        spinner.stop()
                else:
                    response = agent.run(query)
                
                print(f"\n\033[1;32m🤖 Agent:\033[0m {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Stay safe in any weather!")
                break
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                print(f"\n\033[1;31m❌ Error:\033[0m {str(e)}\n")
        
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
