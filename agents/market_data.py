import ccxt
import pandas as pd
from agents.base_agent import BaseAgent

class MarketDataAgent(BaseAgent):
    def __init__(self, name: str = "MarketData", exchange_id: str = 'binance'):
        super().__init__(name)
        self.exchange_id = exchange_id
        self.exchange = None

    def initialize(self):
        super().initialize()
        try:
            exchange_class = getattr(ccxt, self.exchange_id)
            self.exchange = exchange_class({
                'enableRateLimit': True,
            })
            self.logger.info(f"Connected to {self.exchange_id}")
        except AttributeError:
            self.logger.error(f"Exchange {self.exchange_id} not found in ccxt")
            raise

    def process(self, request: dict):
        """
        Expects request format:
        {
            'symbol': 'BTC/USDT',
            'timeframe': '1h',
            'limit': 100
        }
        """
        symbol = request.get('symbol', 'BTC/USDT')
        timeframe = request.get('timeframe', '1h')
        limit = request.get('limit', 100)

        self.logger.info(f"Fetching {limit} candles for {symbol} {timeframe}")
        
        if not self.exchange:
            self.logger.error("Exchange not initialized")
            return None

        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            self.logger.error(f"Error fetching data: {e}")
            return None
