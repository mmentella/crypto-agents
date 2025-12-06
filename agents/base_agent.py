from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the trading system.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.info(f"Agent {name} created.")

    def initialize(self):
        """
        Setup any resources, connections or state.
        """
        self.logger.info(f"Agent {self.name} initialized.")

    @abstractmethod
    def process(self, data):
        """
        Process incoming data and return a result.
        """
        pass

    def shutdown(self):
        """
        Clean up resources.
        """
        self.logger.info(f"Agent {self.name} shutting down.")
