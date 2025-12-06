import pandas as pd
from agents.base_agent import BaseAgent

class StrategyAgent(BaseAgent):
    def __init__(self, name: str = "Strategy"):
        super().__init__(name)

    def process(self, df: pd.DataFrame):
        """
        Analyzes the latest data point and returns a signal.
        Signal format: {'action': 'BUY', 'reason': 'RSI < 30', 'price': 100.0}
        """
        if df is None or df.empty:
            return {'action': 'HOLD', 'reason': 'No Data'}

        # Analyze the last row
        last_row = df.iloc[-1]
        rsi = last_row.get('rsi')
        
        if pd.isna(rsi):
            return {'action': 'HOLD', 'reason': 'Not enough data for indicators'}

        self.logger.info(f"Analyzing market state: RSI={rsi:.2f}")

        if rsi < 30:
            return {
                'action': 'BUY',
                'reason': f'Oversold (RSI {rsi:.2f} < 30)',
                'price': last_row['close'],
                'timestamp': last_row['timestamp']
            }
        elif rsi > 70:
             return {
                'action': 'SELL',
                'reason': f'Overbought (RSI {rsi:.2f} > 70)',
                'price': last_row['close'],
                'timestamp': last_row['timestamp']
            }
        
        return {'action': 'HOLD', 'reason': 'Neutral', 'price': last_row['close']}
